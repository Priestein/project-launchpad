from __future__ import annotations

import json
from pathlib import Path

from .models import ScanSummary


def render_markdown_report(summary: ScanSummary) -> str:
    lines = [
        '# Project Launchpad Scan Report',
        '',
        f'- Root path: `{summary.root_path}`',
        f'- Scanned at: `{summary.scanned_at.isoformat()}`',
        f'- Files scanned: `{summary.files_scanned}`',
        f'- Directories scanned: `{summary.directories_scanned}`',
        f'- Findings: `{len(summary.findings)}`',
        f'- Risk score: `{summary.risk_score}`',
        '',
        '## Findings',
    ]
    if not summary.findings:
        lines.append('No issues found.')
        return '\n'.join(lines)
    for finding in summary.findings:
        lines.append(f'- **{finding.severity.upper()}** `{finding.type}` in `{finding.path}`')
        lines.append(f'  - Message: {finding.message}')
        if finding.line is not None:
            lines.append(f'  - Line: {finding.line}')
        if finding.snippet:
            lines.append(f'  - Snippet: `{finding.snippet}`')
    return '\n'.join(lines)


def save_json_report(summary: ScanSummary, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(summary.model_dump(mode='json'), indent=2), encoding='utf-8')
    return destination


def save_markdown_report(summary: ScanSummary, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_markdown_report(summary), encoding='utf-8')
    return destination
