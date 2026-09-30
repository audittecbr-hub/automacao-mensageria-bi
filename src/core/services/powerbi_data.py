"""Snapshot de Metas: uma consulta, mesmo modelo e contexto dos cartões do BI."""
import hashlib
import json
import math
import re
from datetime import datetime

from src.config import METAS_DATASET_MIGRATED, POWERBI_CONFIG
from src.core.clients.powerbi_client import DaxQueryError, PowerBIClient
from src.core.services.dax_queries import METAS_DEPARTMENTS, get_metas_snapshot_query
from src.core.utils.metas_period import MetasPeriod, TIMEZONE
from src.core.utils.logger import get_logger

logger = get_logger("powerbi_data")
METAS_DATASET_ID = "72edf515-6d51-4fb9-ad43-be8b77c85604"
DEPARTMENT_NAMES = {"TAX": "Tax", "CORPORATE": "Corporate", "EXPANSAO": "Expansão",
                    "EDUCACAO": "Educação", "FRANCHISING": "Franchising", "PJ": "Tecnologia"}


def format_currency(value) -> str:
    if value is None:
        return "Sem dados"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value) -> str:
    return "Sem dados" if value is None else f"{value:.2f}%".replace(".", ",")


class PowerBIDataFetcher:
    def __init__(self, period: MetasPeriod | None = None, *, client=None):
        self.period = period or MetasPeriod.daily()
        self.client = client or PowerBIClient(
            workspace_id=POWERBI_CONFIG["metas_workspace_id"], dataset_id=POWERBI_CONFIG["metas_dataset_id"])
        if self.client.dataset_id != METAS_DATASET_ID:
            raise ValueError("Metas exige Ranking_Metas_V2. Corrija POWERBI_METAS_DATASET_ID para " + METAS_DATASET_ID)
        self.snapshot = None
        if METAS_DATASET_MIGRATED:
            logger.warning("POWERBI_METAS_DATASET_ID legado migrado explicitamente para Ranking_Metas_V2; atualize a variável do serviço.")

    def _get_month_filter(self) -> str:
        return self.period.dax_date(self.period.start)

    def _get_month_range(self) -> tuple[str, str]:
        return self.period.dax_date(self.period.start), self.period.dax_date(self.period.end)

    def fetch_snapshot(self) -> dict:
        model = self.client.get_dataset_info()
        if model.get("id") != METAS_DATASET_ID or model.get("name") != "Ranking_Metas_V2":
            raise DaxQueryError("O dataset configurado não corresponde ao Ranking_Metas_V2 validado.")
        refresh = self.client.get_latest_refresh()
        if self.period.mode == "daily":
            self._validate_daily_refresh(refresh)
        start, end = self._get_month_range()
        query = get_metas_snapshot_query(start, end)
        rows = self.client.execute_dax(query, use_cache=False, strict=True)
        if not rows or len(rows) != 1:
            raise DaxQueryError("Snapshot de Metas deve retornar exatamente uma linha.")
        expected = {f"[{name}]" for name in re.findall(r'"([^\"]+)",', query)}
        missing = expected - rows[0].keys()
        if len(expected) != 87 or missing:
            raise DaxQueryError("Campos obrigatórios ausentes no snapshot: " + ", ".join(sorted(missing)))
        values = {}
        for key in expected:
            value = rows[0][key]
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
                raise DaxQueryError(f"Campo numérico inválido: {key}")
            if value is None and "_Meta" in key:
                raise DaxQueryError(f"Meta mensal não configurada: {key}")
            # BLANK da medida com o campo presente representa ausência de movimento.
            values[key[1:-1]] = value if value is not None else 0
        self._validate_values(values)
        self.snapshot = {
            "schema_version": 1, "workspace_id": self.client.workspace_id, "dataset_id": self.client.dataset_id,
            "model_name": model["name"], "period": self.period.metadata(), "values": values,
            "query_sha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
            "source_refresh": {key: refresh.get(key) for key in ("requestId", "status", "startTime", "endTime")} if refresh else None,
            "source_policy": "current_loaded_bi" if self.period.mode == "current_snapshot" else "completed_refresh",
        }
        logger.info("Metas V2: %s a %s; 87 campos coletados sem cache", self.period.start, self.period.end)
        return self.snapshot

    def _validate_daily_refresh(self, refresh):
        if not refresh or refresh.get("status") != "Completed" or not refresh.get("endTime"):
            raise DaxQueryError("Envio diário bloqueado: a última atualização do V2 não foi concluída.")
        try:
            completed = datetime.fromisoformat(refresh["endTime"].replace("Z", "+00:00")).astimezone(TIMEZONE)
        except (TypeError, ValueError) as error:
            raise DaxQueryError("Data de atualização do V2 inválida.") from error
        if completed.date() < self.period.end:
            raise DaxQueryError("Envio diário bloqueado: atualização anterior à referência D-1.")

    @staticmethod
    def _validate_values(values):
        liquid = values["Comercial_Realizado"] + values["Operacional_Realizado"]
        if abs(values["GS_Realizado"] - liquid) > 0.01:
            raise DaxQueryError("Realizado GS não corresponde aos cartões Comercial e Operacional.")
        for index in range(1, 4):
            meta = values[f"GS_Meta{index}"]
            expected = liquid / meta if meta else 0
            if abs(values[f"GS_Pct{index}"] - expected) > 0.000001:
                raise DaxQueryError("Percentual GS diverge do contexto do BI.")
        for prefix, *_ in METAS_DEPARTMENTS:
            if abs(values[f"{prefix}_Bruto"] - values[f"{prefix}_Repasse"] - values[f"{prefix}_Liquido_Card"]) > 0.01:
                raise DaxQueryError(f"Bruto, repasse e líquido inconsistentes: {prefix}")

    @staticmethod
    def snapshot_to_report(snapshot) -> tuple[dict, list, dict]:
        v = snapshot["values"]
        def goals(prefix):
            return {**{f"meta{n}": format_currency(v[f"{prefix}_Meta{n}"]) for n in range(1, 4)},
                    **{f"pct_meta{n}": v[f"{prefix}_Pct{n}"] * 100 for n in range(1, 4)}}
        total = {**goals("GS"), "realizado": format_currency(v["GS_Realizado"]),
                 "total_geral": format_currency(v["Total_Geral"]), "administracao": format_currency(v["Administracao"]),
                 "realizado_com_repasse": format_currency(v["GS_Realizado"] + v["Repasse_Total"]),
                 "percent": format_percent(v["GS_Pct1"] * 100)}
        departments = [{"nome": name, **goals(name), "realizado": format_currency(v[f"{name}_Realizado"]),
                        "percent": format_percent(v[f"{name}_Pct1"] * 100)} for name in ("Comercial", "Operacional")]
        for prefix in ("CORPORATE", "EDUCACAO", "EXPANSAO", "FRANCHISING", "TAX", "PJ"):
            bruto = v[f"{prefix}_Bruto"]
            departments.append({"nome": DEPARTMENT_NAMES[prefix], **goals(prefix),
                                "realizado": format_currency(bruto), "repasse": format_currency(v[f"{prefix}_Repasse"]),
                                "liquido": format_currency(v[f"{prefix}_Liquido_Card"]),
                                "repasse_pct": v[f"{prefix}_Repasse"] / bruto * 100 if bruto else 0,
                                "percent": format_percent(v[f"{prefix}_Pct1"] * 100)})
        revenues = {"outras": format_currency(v["Outras_Receitas"]), "intercompany": format_currency(v["Intercompany"]),
                    "repasse_total": format_currency(v["Repasse_Total"]), "sem_categoria": format_currency(v["Sem_Categoria"]),
                    "total_geral": format_currency(v["Total_Geral"]), "administracao": format_currency(v["Administracao"])}
        return total, departments, revenues

    def fetch_all_data(self) -> tuple[dict, list, dict]:
        return self.snapshot_to_report(self.fetch_snapshot())


if __name__ == "__main__":
    fetcher = PowerBIDataFetcher()
    print(json.dumps(fetcher.fetch_snapshot(), ensure_ascii=False, indent=2))
