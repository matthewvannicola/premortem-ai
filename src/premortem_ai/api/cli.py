"""
Command-line interface for executing the PreMortem AI pipeline locally.

Usage:
    python -m premortem_ai.api.cli run --text "project description..."
    python -m premortem_ai.api.cli run --input-file path/to/file.txt
"""

import argparse
import json
import sys
from premortem_ai.models.pipeline_request import PipelineRequest
from premortem_ai.models.pipeline_response import PipelineResponse
from premortem_ai.pipelines.run_pipeline import run_pipeline

from premortem_ai.exceptions import (
    ValidationError,
    ModelInvocationError,
    ConfigurationError,
    PipelineExecutionError,
)


def run_pipeline_cli(text: str = None, input_file: str = None, pretty: bool = False):
    """
    Execute the PreMortem AI pipeline from the command line.
    """

    # -------------------------------------------------------------
    # 1. Handle input source
    # -------------------------------------------------------------
    if not text and not input_file:
        print("ERROR: Provide --text or --input-file", file=sys.stderr)
        sys.exit(1)

    if input_file:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except Exception as exc:
            print(f"ERROR: Cannot read file: {exc}", file=sys.stderr)
            sys.exit(1)

    if not text:
        print("ERROR: Empty input text", file=sys.stderr)
        sys.exit(1)

    # -------------------------------------------------------------
    # 2. Build validated PipelineRequest
    # -------------------------------------------------------------
    try:
        request = PipelineRequest(project_description=text)
    except Exception as exc:
        print(f"[VALIDATION ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    # -------------------------------------------------------------
    # 3. Execute the full pipeline
    # -------------------------------------------------------------
    try:
        context = run_pipeline(request)

        # *** CRITICAL FIX ***
        response = PipelineResponse.from_context(context)

    except ValidationError as exc:
        print(f"[VALIDATION ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except ModelInvocationError as exc:
        print(f"[MODEL ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except ConfigurationError as exc:
        print(f"[CONFIG ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except PipelineExecutionError as exc:
        print(f"[PIPELINE ERROR] {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"[UNEXPECTED ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    # -------------------------------------------------------------
    # 4. Output results
    # -------------------------------------------------------------
    output = response.model_dump()

    if pretty:
        print(json.dumps(output, indent=4))
    else:
        print(json.dumps(output))


def main():
    parser = argparse.ArgumentParser(description="PreMortem AI CLI")

    subparsers = parser.add_subparsers(dest="command")

    # -------------------------------------------------------------
    # run command
    # -------------------------------------------------------------
    run_parser = subparsers.add_parser("run", help="Run full PreMortem AI pipeline")
    run_parser.add_argument("--text", type=str, help="Direct input text")
    run_parser.add_argument("--input-file", type=str, help="Text file containing project description")
    run_parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

    args = parser.parse_args()

    if args.command == "run":
        run_pipeline_cli(text=args.text, input_file=args.input_file, pretty=args.pretty)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
