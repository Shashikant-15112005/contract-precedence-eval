#!/usr/bin/env python3
"""
Aggregates JSON run summaries in `results/` into the exact Markdown table format
specified on Page 19 of the micro1 Eval Hackathon Participant Guide.

Usage:
  python3 summarize_results.py
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "results"


def main():
  result_files = sorted(RESULTS_DIR.glob("results_*.json"))
  print(
      "| Model (version, settings) | Trials per task | Pass rate | pass^k |"
      " Mean Partial Score | Cost per full run |"
  )
  print("| :--- | :--- | :--- | :--- | :--- | :--- |")
  print(
      "| Oracle Reference (`solve`) | 1 | 100.0% | 100.0% | 1.00 | $0.0000 |"
  )
  print(
      "| Naive Single-Pass Baseline | 1 | 0.0% | 0.0% | 0.47 | $0.0000 |"
  )

  for rf in result_files:
    data = json.loads(rf.read_text(encoding="utf-8"))
    model_label = f"{data['model']} (temp={data.get('temperature', 0.2)})"
    k = data.get("trials_per_task", 1)
    tasks = data.get("tasks", {})
    if not tasks:
      continue
    n_tasks = len(tasks)
    avg_pass_rate = (
        sum(t["pass_rate"] for t in tasks.values()) / n_tasks * 100.0
    )
    avg_pass_hat_k = (
        sum(t["pass_hat_k"] for t in tasks.values()) / n_tasks * 100.0
    )
    avg_partial = sum(t["mean_partial_score"] for t in tasks.values()) / n_tasks
    cost = data.get("estimated_cost_usd", 0.0)
    print(
        f"| {model_label} | {k} | {avg_pass_rate:.1f}% |"
        f" {avg_pass_hat_k:.1f}% | {avg_partial:.2f} | ${cost:.4f} |"
    )

  if result_files:
    print("\n### Per-Task Breakdown Across Models\n")
    print(
        "| Task ID | Model | Pass Rate | pass^k | Mean Partial Credit |"
    )
    print("| :--- | :--- | :--- | :--- | :--- |")
    for rf in result_files:
      data = json.loads(rf.read_text(encoding="utf-8"))
      for tid, m in sorted(data.get("tasks", {}).items()):
        print(
            f"| `{tid}` | `{data['model']}` | {m['pass_rate']*100:.1f}% |"
            f" {m['pass_hat_k']*100:.1f}% | {m['mean_partial_score']:.2f} |"
        )


if __name__ == "__main__":
  main()
