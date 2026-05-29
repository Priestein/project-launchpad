from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class Finding(BaseModel):
    type: str
    severity: Literal['info', 'low', 'medium', 'high']
    path: str
    line: int | None = None
    message: str
    snippet: str | None = None


class ScanSummary(BaseModel):
    scanned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    root_path: str
    files_scanned: int
    directories_scanned: int
    findings: list[Finding]

    @property
    def risk_score(self) -> int:
        weights = {'info': 0, 'low': 1, 'medium': 3, 'high': 5}
        return sum(weights[f.severity] for f in self.findings)
