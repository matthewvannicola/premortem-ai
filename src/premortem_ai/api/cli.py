"""
cli.py

Command-line interface for executing the PreMortem AI pipeline.
Uses the new run_pipeline(PipelineRequest) functional API.
"""

import argparse
import json
import sys

from premortem_ai.models import PipelineRequest
from premortem_ai.pipelines import run_pipeline
from premortem_ai.exceptions import ValidationError, ModelInvocationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a PreMortem AI project analysis from the command line."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to text file containing project description.")
    group.add_argument("--text", type=str, help="Project description as raw text.")

    parser.add_argument("--model", type=str, default=None, help="Model override.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")

    return parser


def load_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        raise RuntimeError(f"Failed to load file '{path}': {exc}")


def main():
    parser = build_parser()
    args = parser.parse_args()

    # ------------------------------------
    # Load project description
    # ------------------------------------
    if args.file:
        description = load_text(args.file)
    else:
        description = args.text

    # ------------------------------------
    # Build PipelineRequest
    # ------------------------------------
    request = PipelineRequest(
        project_description=description,
        model_version_override=args.model,
        include_metadata=True,
    )

    # ------------------------------------
    # Run pipeline
    # ------------------------------------
    try:
        response = run_pipeline(request)
    except (ValidationError, ModelInvocationError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"[UNEXPECTED ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    # ------------------------------------
    # Output JSON
    # ------------------------------------
    payload = response.model_dump()

    if args.pretty:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload))


if __name__ == "__main__":
    main()
