"""
sample_pipeline.py

Executable example for running the PreMortem AI pipeline
using sample inputs.
"""

import json
from pathlib import Path

from premortem_ai.pipelines.run_pipeline import run_pipeline
from premortem_ai.api.schemas import PipelineRequest  # adjust if needed


EXAMPLES_DIR = Path(__file__).parent


def main():
    with open(EXAMPLES_DIR / "sample_pipeline.json") as f:
        payload = json.load(f)

    request = PipelineRequest(**payload)

    context = run_pipeline(request)

    print("\n--- PIPELINE COMPLETE ---")
    print(f"Discovered risks: {len(context.risks)}")
    print("Stages executed:", list(context.stage_timings.keys()))


if __name__ == "__main__":
    main()
