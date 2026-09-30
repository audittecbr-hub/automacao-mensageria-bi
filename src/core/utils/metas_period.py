"""Uma referência imutável para consultas, imagens e legendas de Metas."""
from calendar import monthrange
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("America/Sao_Paulo")
MONTHS = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
          "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")


@dataclass(frozen=True)
class MetasPeriod:
    start: date
    end: date
    captured_at: datetime
    mode: str = "daily"

    @classmethod
    def daily(cls, reference_date: date | None = None, *, now: datetime | None = None):
        captured = (now or datetime.now(TIMEZONE)).astimezone(TIMEZONE)
        reference = reference_date or captured.date() - timedelta(days=1)
        if reference > captured.date():
            raise ValueError("A referência de Metas não pode estar no futuro.")
        return cls(reference.replace(day=1), reference, captured)

    @classmethod
    def current_snapshot(cls, *, now: datetime | None = None):
        captured = (now or datetime.now(TIMEZONE)).astimezone(TIMEZONE)
        current = captured.date()
        end = current.replace(day=monthrange(current.year, current.month)[1])
        return cls(current.replace(day=1), end, captured, "current_snapshot")

    @property
    def label(self) -> str:
        return f"{MONTHS[self.start.month - 1]}/{self.start.year}"

    @property
    def header(self) -> str:
        if self.mode == "current_snapshot":
            return f"{self.label} · Fotografia do BI em {self.captured_at:%d/%m %H:%M}"
        return f"{self.label} · Até {self.end:%d/%m/%Y} (D-1)"

    @staticmethod
    def dax_date(value: date) -> str:
        return f"DATE({value.year}, {value.month}, {value.day})"

    def metadata(self) -> dict:
        return {"mode": self.mode, "start_date": self.start.isoformat(),
                "end_date": self.end.isoformat(), "label": self.label,
                "captured_at": self.captured_at.isoformat(), "timezone": str(TIMEZONE)}
