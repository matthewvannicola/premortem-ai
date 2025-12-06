"""
cli.py

Command-line interface for running PreMortem AI analysis locally.

This tool is intended for:
    - developers
    - data analysts
    - automation workflows
    - debugging pipeline output
    - batch processing

It wraps the AnalysisService and uses the same canonical models as the API layer.

Usage:
    python -m premortem_ai.api.cli --file ./project.txt
    python -m premortem_ai.api.cli --text "Describe your project here..."
"""

import argparse
import json
import sys

from premortem_ai.analysis_service import AnalysisService
from premortem_ai.models import PipelineRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a PreMortem AI project risk analysis from the command line."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file",
        type=str,
        help="Path to a text file containing a project description.",
    )
    group.add_argument(
        "--text",
        type=str,
        help="Raw project description text.",
    )

    parser.add_argument(
        "--max-risks",
        type=int,
        default=50,
        help="Optional override for maximum risks discovered (default: 50).",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Optional override for LLM model version.",
    )

    parser.add_argument(
        "--pipeline-version",
        type=str,
        default=None,
        help="Optional override for pipeline version.",
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )

    return parser


def load_project_description_from_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        raise RuntimeError(f"Failed to read file '{path}': {exc}") from exc


def main():
    parser = build_parser()
    args = parser.parse_args()

    # ----------------------------------------------------------------------
    # Determine project_description
    # ----------------------------------------------------------------------
    if args.file:
        project_description = load_project_description_from_file(args.file)
    else:
        project_description = args.text

    # ----------------------------------------------------------------------
    # Construct the canonical request
    # ----------------------------------------------------------------------
    req_dict = {
        "project_description": project_description,
        "max_risks": args.max_risks,
        "model_version_override": args.model,
        "pipeline_version_override": args.pipeline_version,
        "include_metadata": True,
    }

    request = PipelineRequest.from_api(req_dict)

    # ----------------------------------------------------------------------
    # Execute via service layer
    # ----------------------------------------------------------------------
    service = AnalysisService()

    try:
        response = service.run_analysis(request.model_dump())
    except Exception as exc:
        print(f"[ERROR] Analysis failed: {exc}", file=sys.stderr)
        sys.exit(1)

    # ----------------------------------------------------------------------
    # Output JSON
    # ----------------------------------------------------------------------
    payload = response.to_dict()

    if args.pretty:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload))


if __name__ == "__main__":
    main()
