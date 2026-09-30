"""Regressões de período, dados, cache, entrega e fila, sem rede ou destinatários reais."""
import copy
import sys
import time
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.core.clients.powerbi_client import DaxQueryError, PowerBIClient, _dax_cache
from src.core.services.powerbi_data import METAS_DATASET_ID, PowerBIDataFetcher, format_currency
from src.core.services.notification_service import NotificationService
from src.core.utils.metas_period import MetasPeriod, TIMEZONE


def model_row():
    row = {"GS_Realizado": 92, "Total_Geral": 165, "Administracao": 1,
           "Comercial_Realizado": 28, "Operacional_Realizado": 64,
           "Intercompany": 40, "Outras_Receitas": 5, "Sem_Categoria": 9, "Repasse_Total": 18}
    for n, target in enumerate((200, 250, 300), 1):
        row[f"GS_Meta{n}"] = target
        row[f"GS_Pct{n}"] = 92 / target
    for group, value in (("Comercial", 28), ("Operacional", 64)):
        for n in range(1, 4):
            row[f"{group}_Meta{n}"] = 100
            row[f"{group}_Pct{n}"] = value / 100
    for prefix, gross, repasse in (("TAX", 60, 12), ("CORPORATE", 20, 4), ("EXPANSAO", 10, 2),
                                   ("EDUCACAO", 10, 0), ("FRANCHISING", 10, 0), ("PJ", 0, 0)):
        row.update({f"{prefix}_Bruto": gross, f"{prefix}_Repasse": repasse,
                    f"{prefix}_Liquido_Card": gross - repasse, f"{prefix}_Liquido_Meta": gross - repasse})
        for n in range(1, 4):
            row[f"{prefix}_Meta{n}"] = 100
            row[f"{prefix}_Pct{n}"] = None if prefix == "PJ" else (gross - repasse) / 100
    return {f"[{key}]": value for key, value in row.items()}


class FakeModel:
    dataset_id = METAS_DATASET_ID
    workspace_id = "fake-workspace"

    def __init__(self, row=None, status="Completed"):
        self.row = model_row() if row is None else row
        self.status = status
        self.calls = []

    def get_dataset_info(self):
        return {"id": METAS_DATASET_ID, "name": "Ranking_Metas_V2"}

    def get_latest_refresh(self):
        return {"status": self.status, "endTime": "2026-09-30T12:00:00Z"}

    def execute_dax(self, query, **kwargs):
        self.calls.append((query, kwargs))
        return [self.row]


def current_period():
    return MetasPeriod.current_snapshot(now=datetime(2026, 9, 30, 14, tzinfo=TIMEZONE))


@pytest.mark.parametrize("instant,expected_start,expected_end", [
    (datetime(2026, 9, 30, 14, tzinfo=TIMEZONE), "2026-09-01", "2026-09-29"),
    (datetime(2026, 10, 1, 14, tzinfo=TIMEZONE), "2026-09-01", "2026-09-30"),
    (datetime(2027, 1, 1, 14, tzinfo=TIMEZONE), "2026-12-01", "2026-12-31"),
])
def test_daily_period_matches_caption_and_query(instant, expected_start, expected_end):
    period = MetasPeriod.daily(now=instant)
    assert period.start.isoformat() == expected_start
    assert period.end.isoformat() == expected_end
    assert period.end.strftime("%d/%m/%Y") in period.header


def test_snapshot_is_one_query_and_preserves_the_bi_metric_meanings():
    client = FakeModel(status="Failed")
    fetcher = PowerBIDataFetcher(current_period(), client=client)
    snapshot = fetcher.fetch_snapshot()
    total, departments, revenues = fetcher.snapshot_to_report(snapshot)
    assert len(client.calls) == 1 and len(snapshot["values"]) == 87
    assert client.calls[0][1] == {"use_cache": False, "strict": True}
    assert "DATE(2026, 9, 30)" in client.calls[0][0]
    assert total["realizado"] == "R$ 92,00"
    assert total["total_geral"] == "R$ 165,00"
    assert revenues["administracao"] == "R$ 1,00"
    tax = next(d for d in departments if d["nome"] == "Tax")
    assert tax["realizado"] == "R$ 60,00" and tax["liquido"] == "R$ 48,00"
    assert tax["pct_meta1"] == 48
    tech = next(d for d in departments if d["nome"] == "Tecnologia")
    assert tech["realizado"] == "R$ 0,00" and tech["pct_meta1"] == 0
    assert format_currency(None) != format_currency(0)


def test_daily_rejects_failed_refresh_while_explicit_bi_snapshot_is_allowed():
    client = FakeModel(status="Failed")
    with pytest.raises(DaxQueryError, match="atualização"):
        PowerBIDataFetcher(MetasPeriod.daily(now=datetime(2026, 9, 30, 14, tzinfo=TIMEZONE)), client=client).fetch_snapshot()
    assert not client.calls


@pytest.mark.parametrize("invalid", ["missing", "nan", "missing_goal", "ratio"])
def test_invalid_collection_cannot_become_a_report(invalid):
    row = model_row()
    if invalid == "missing": del row["[TAX_Repasse]"]
    if invalid == "nan": row["[GS_Realizado]"] = float("nan")
    if invalid == "missing_goal": row["[GS_Meta1]"] = None
    if invalid == "ratio": row["[GS_Pct1]"] = 0.9
    with pytest.raises(DaxQueryError):
        PowerBIDataFetcher(current_period(), client=FakeModel(row)).fetch_snapshot()


class FakeResponse:
    def __init__(self, body): self.body = body
    def raise_for_status(self): return None
    def json(self): return self.body


def dax_client(model, value):
    client = PowerBIClient.__new__(PowerBIClient)
    client.dataset_id, client.workspace_id = model, "fake-workspace"
    client.token, client.token_expiry = "fake", time.time() + 600
    client.session = SimpleNamespace(post=Mock(return_value=FakeResponse({"results": [{"tables": [{"rows": [{"[value]": value}]}]}]})))
    return client


def test_cache_cannot_cross_models_and_explicit_snapshot_bypasses_it():
    _dax_cache.clear()
    a, b = dax_client("model-A", 10), dax_client("model-B", 20)
    query = 'EVALUATE ROW("value", 1)'
    assert a.execute_dax(query)[0]["[value]"] == 10
    assert b.execute_dax(query)[0]["[value]"] == 20
    a.execute_dax(query, use_cache=False)
    assert a.session.post.call_count == 2


@pytest.mark.parametrize("body", [
    {"error": {"message": "fake"}}, {"results": [{"error": {"message": "fake"}}]},
    {"results": [{"tables": [{"error": {"message": "fake"}}]}]}, {"results": [{"tables": [{}]}]},
])
def test_http200_with_dax_error_is_not_a_success(body):
    client = dax_client("fake-error-model", 0)
    client.session.post.return_value = FakeResponse(body)
    with pytest.raises(DaxQueryError):
        client.execute_dax("fake error query", use_cache=False, strict=True)


def test_delivery_false_never_logs_message_sent(monkeypatch):
    import src.core.services.notification_service as notification
    monkeypatch.setattr(notification.time, "sleep", lambda seconds: None)
    service = NotificationService.__new__(NotificationService)
    service.whatsapp = SimpleNamespace(set_presence=Mock(), send_file=Mock(return_value=False))
    service.supabase = SimpleNamespace(log_event=Mock())
    assert not service.send_whatsapp_report({"phone": "fake", "id": "fake"}, "fake.png", "fake")
    assert service.supabase.log_event.call_args[0][0] == "message_error"


def test_generate_only_does_not_send_and_collection_failure_does_not_generate(tmp_path):
    from src.modules.metas.runner import MetasAutomation
    automation = MetasAutomation.__new__(MetasAutomation)
    automation.period, automation.run_id, automation.output_dir = current_period(), "fake", tmp_path
    automation.generate_images, automation.send_whatsapp = Mock(return_value={}), Mock()
    automation.fetch_data = Mock(side_effect=DaxQueryError("fake"))
    with pytest.raises(DaxQueryError): automation.run(generate_only=True)
    automation.generate_images.assert_not_called()
    automation.send_whatsapp.assert_not_called()
    automation.fetch_data = Mock(return_value=PowerBIDataFetcher.snapshot_to_report(PowerBIDataFetcher(current_period(), client=FakeModel()).fetch_snapshot()))
    automation.run(generate_only=True)
    automation.send_whatsapp.assert_not_called()


def test_queue_records_failed_instead_of_completed(monkeypatch):
    from src.core.services.job_service import JobService
    import src.core.services.job_service as queue
    import src.core.jobs as jobs
    db = SimpleNamespace(claim_job=Mock(return_value=True), log_event=Mock(), update_job_status=Mock(),
                         get_schedule_by_id=lambda sid: {"definition": {"key": "fake"}})
    monkeypatch.setattr(jobs, "SupabaseService", lambda: db)
    def fails(**kwargs): raise RuntimeError("fake failure")
    monkeypatch.setattr(queue, "JOB_MAPPING", {"fake": fails})
    worker = JobService.__new__(JobService)
    worker.supabase = db
    worker._process_single_job({"id": "fake", "schedule_id": "fake", "payload": {"recipients": [{}]}})
    assert db.update_job_status.call_args[0][1] == "failed"
    assert all(call.args[0] != "job_success" for call in db.log_event.call_args_list)


def test_queue_only_runs_after_atomic_claim(monkeypatch):
    from src.core.services.job_service import JobService
    worker = JobService.__new__(JobService)
    worker.supabase = SimpleNamespace(claim_job=Mock(return_value=False), log_event=Mock())
    worker._process_single_job({"id": "fake"})
    worker.supabase.log_event.assert_not_called()


def test_collective_is_blocked_today_and_first_daily_reference_tomorrow_is_september():
    from src.modules.metas.runner import MetasAutomation
    automation = MetasAutomation.__new__(MetasAutomation)
    automation.period = current_period()
    automation.supabase = SimpleNamespace(get_setting=lambda key, default=None: "2026-10-01" if key == "metas_delivery_start_date" else False)
    with pytest.raises(RuntimeError, match="retoma"):
        automation.send_whatsapp({}, custom_recipients=[{"phone": "fake1"}, {"phone": "fake2"}])
    tomorrow = MetasPeriod.daily(now=datetime(2026, 10, 1, 14, tzinfo=TIMEZONE))
    assert tomorrow.label == "Setembro/2026" and tomorrow.end.isoformat() == "2026-09-30"


def test_legacy_dataset_migration_is_explicit_and_unknown_model_is_rejected():
    client = FakeModel()
    client.dataset_id = "unknown-model"
    with pytest.raises(ValueError, match="Ranking_Metas_V2"):
        PowerBIDataFetcher(current_period(), client=client)
