from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import ScanSummary
from .reporting import save_json_report, save_markdown_report
from .scanner import ScanOptions, scan_path

logger = logging.getLogger(__name__)
app = FastAPI(title=settings.app_name, version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])


@app.get('/health')
def health() -> dict[str, str]:
    logger.info('Health check requested')
    return {'status': 'ok', 'service': settings.app_name}


@app.get('/scan', response_model=ScanSummary)
def scan(root_path: str = Query(default=settings.default_scan_root)) -> ScanSummary:
    path = Path(root_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail='Path does not exist')
    return scan_path(ScanOptions(root_path=path, max_file_size_bytes=settings.max_file_size_bytes, limit_findings=settings.report_limit))


@app.post('/reports/json')
def generate_json_report(root_path: str = Query(default=settings.default_scan_root), output_path: str = 'docs/reports/latest-report.json') -> dict[str, str]:
    path = Path(root_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail='Path does not exist')
    summary = scan_path(ScanOptions(root_path=path, max_file_size_bytes=settings.max_file_size_bytes, limit_findings=settings.report_limit))
    destination = save_json_report(summary, Path(output_path))
    return {'report_path': str(destination)}


@app.post('/reports/markdown')
def generate_markdown_report(root_path: str = Query(default=settings.default_scan_root), output_path: str = 'docs/reports/latest-report.md') -> dict[str, str]:
    path = Path(root_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail='Path does not exist')
    summary = scan_path(ScanOptions(root_path=path, max_file_size_bytes=settings.max_file_size_bytes, limit_findings=settings.report_limit))
    destination = save_markdown_report(summary, Path(output_path))
    return {'report_path': str(destination)}
