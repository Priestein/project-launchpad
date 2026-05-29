from pathlib import Path

from launchpad.scanner import ScanOptions, scan_path

summary = scan_path(ScanOptions(root_path=Path('.')))
print(summary.model_dump_json(indent=2))
