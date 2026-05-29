from pathlib import Path

from launchpad.scanner import ScanOptions, scan_path


def test_scan_detects_secret_and_todos(tmp_path: Path):
    (tmp_path / 'sample.py').write_text('# TODO: improve
password = "super-secret-value"
', encoding='utf-8')
    summary = scan_path(ScanOptions(root_path=tmp_path, limit_findings=10))
    assert summary.files_scanned >= 1
    assert any(f.type == 'todo_comment' for f in summary.findings)
    assert any(f.type == 'potential_secret' for f in summary.findings)
