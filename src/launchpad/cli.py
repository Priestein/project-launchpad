from __future__ import annotations

import argparse
from pathlib import Path

from .config import settings
from .reporting import save_json_report, save_markdown_report
from .scanner import ScanOptions, scan_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='launchpad', description='Scan codebases for secrets, TODOs, and oversized files.')
    subparsers = parser.add_subparsers(dest='command', required=True)
    scan_parser = subparsers.add_parser('scan', help='Scan a path and print a JSON summary.')
    scan_parser.add_argument('root_path', nargs='?', default=settings.default_scan_root)
    scan_parser.add_argument('--json-output', default=None)
    scan_parser.add_argument('--markdown-output', default=None)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == 'scan':
        root_path = Path(args.root_path)
        if not root_path.exists():
            parser.error(f'Path does not exist: {root_path}')
        summary = scan_path(ScanOptions(root_path=root_path, max_file_size_bytes=settings.max_file_size_bytes, limit_findings=settings.report_limit))
        print(summary.model_dump_json(indent=2))
        if args.json_output:
            save_json_report(summary, Path(args.json_output))
        if args.markdown_output:
            save_markdown_report(summary, Path(args.markdown_output))
        return 0
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
