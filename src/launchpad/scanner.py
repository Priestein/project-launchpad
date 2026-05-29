from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .models import Finding, ScanSummary

SECRET_PATTERNS = {
    'aws_access_key_id': re.compile(r'AKIA[0-9A-Z]{16}'),
    'generic_api_key': re.compile(r'(?i)(api[_-]?key|secret|token)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}["\']?'),
    'private_key_block': re.compile(r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----'),
    'github_token': re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}'),
}
TEXT_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.yaml', '.yml', '.toml', '.md', '.txt', '.env', '.ini', '.cfg'}


@dataclass(frozen=True)
class ScanOptions:
    root_path: Path
    max_file_size_bytes: int = 1_000_000
    limit_findings: int = 50


def scan_path(options: ScanOptions) -> ScanSummary:
    root_path = options.root_path.resolve()
    findings: list[Finding] = []
    files_scanned = 0
    directories_scanned = 0

    for path in root_path.rglob('*'):
        if path.is_dir():
            directories_scanned += 1
            continue
        files_scanned += 1
        if path.stat().st_size > options.max_file_size_bytes:
            findings.append(Finding(type='oversized_file', severity='low', path=str(path), message='File exceeds configured size threshold.'))
            if len(findings) >= options.limit_findings:
                break
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != '.env':
            continue
        try:
            content = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        except OSError as exc:
            findings.append(Finding(type='read_error', severity='low', path=str(path), message=f'Could not read file: {exc}'))
            if len(findings) >= options.limit_findings:
                break
            continue
        for line_number, line in enumerate(content, start=1):
            lowered = line.lower()
            if 'todo' in lowered:
                findings.append(Finding(type='todo_comment', severity='info', path=str(path), line=line_number, message='TODO/FIXME marker found.', snippet=line.strip()))
            if 'password' in lowered or 'secret' in lowered or 'token' in lowered:
                if '=' in line or ':' in line:
                    findings.append(Finding(type='potential_secret', severity='medium', path=str(path), line=line_number, message='Potential secret-like assignment detected.', snippet=line.strip()))
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(line):
                    severity = 'high' if ('key' in label or 'token' in label or 'private' in label) else 'medium'
                    findings.append(Finding(type=label, severity=severity, path=str(path), line=line_number, message=f'Matched pattern: {label}.', snippet=line.strip()))
            if len(findings) >= options.limit_findings:
                break
        if len(findings) >= options.limit_findings:
            break

    return ScanSummary(root_path=str(root_path), files_scanned=files_scanned, directories_scanned=directories_scanned, findings=findings[: options.limit_findings])
