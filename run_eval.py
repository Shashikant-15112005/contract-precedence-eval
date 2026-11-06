#!/usr/bin/env python3
"""
Evaluation Harness for `contract-precedence-eval`.

Supports:
1. `--mode oracle`          : Runs the verified reference solutions through all graders (must score 100%).
2. `--mode verify-graders`  : Runs both reference solutions AND realistic naive-model failures (proves 0 false passes / 0 false fails).
3. `--mode llm`             : Runs tasks against live LLM APIs (OpenAI, Anthropic, Google Gemini, or OpenAI-compatible endpoints) across k trials, recording full transcripts and computing pass@k, pass^k, mean partial credit, and spread.
"""

import argparse
import datetime
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

from graders.grader import grade_task

ROOT_DIR = Path(__file__).resolve().parent
TASKS_DIR = ROOT_DIR / "tasks"
REF_DIR = ROOT_DIR / "reference"
RESULTS_DIR = ROOT_DIR / "results"
TRANSCRIPTS_DIR = ROOT_DIR / "transcripts"


def load_tasks() -> List[Dict[str, Any]]:
    tasks = []
    for task_file in sorted(TASKS_DIR.glob("task_*.json")):
        with open(task_file, "r", encoding="utf-8") as f:
            tasks.append(json.load(f))
    return tasks


def load_reference(task_id: str) -> Dict[str, Any]:
    ref_path = REF_DIR / f"{task_id}_reference.json"
    with open(ref_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_full_prompt(task: Dict[str, Any]) -> str:
    return (
        "### ATTACHED CONTRACT DOCUMENT\n"
        "```text\n"
        f"{task['contract_text'].strip()}\n"
        "```\n\n"
        f"{task['prompt_text'].strip()}\n"
    )


def call_llm(provider: str, model: str, prompt: str, temperature: float = 0.2) -> Tuple[str, float]:
    """Calls the specified LLM provider and returns (raw_text, estimated_cost_usd)."""
    if provider == "openai":
        import urllib.request
        import urllib.error
        api_key = os.environ.get("OPENAI_API_KEY", "").strip().strip('"').strip("\'")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY environment variable.")
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert commercial contracts attorney. Output strictly valid JSON matching the requested schema."},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{base_url.rstrip('/')}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        cost = (usage.get("prompt_tokens", 0) * 2.5e-6) + (usage.get("completion_tokens", 0) * 10.0e-6)
        return content, round(cost, 5)

    elif provider == "anthropic":
        import urllib.request
        import urllib.error
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip().strip('"').strip("\'")
        if not api_key:
            raise RuntimeError("Missing ANTHROPIC_API_KEY environment variable.")
        payload = json.dumps({
            "model": model,
            "max_tokens": 4096,
            "temperature": temperature,
            "system": "You are an expert commercial contracts attorney. Output strictly valid JSON matching the requested schema.",
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["content"][0]["text"]
        usage = data.get("usage", {})
        cost = (usage.get("input_tokens", 0) * 3.0e-6) + (usage.get("output_tokens", 0) * 15.0e-6)
        return content, round(cost, 5)

    elif provider == "gemini":
        import urllib.request
        import urllib.error
        api_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("\'")
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY environment variable.")
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature},
        }).encode("utf-8")
        candidate_models = [model] + [m for m in ["gemini-3.8-flash", "gemini-3.8-pro", "gemini-2.5-flash", "gemini-2.5-pro"] if m != model]
        last_err = ""
        data = None
        for m_name in candidate_models:
            endpoints = [
                (f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent", {"Content-Type": "application/json", "x-goog-api-key": api_key}),
                (f"https://aiplatform.googleapis.com/v1/publishers/google/models/{m_name}:generateContent?key={api_key}", {"Content-Type": "application/json"}),
                (f"https://aiplatform.googleapis.com/v1beta1/publishers/google/models/{m_name}:generateContent", {"Content-Type": "application/json", "x-goog-api-key": api_key}),
                (f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={api_key}", {"Content-Type": "application/json"}),
            ]
            for url, hdrs in endpoints:
                req = urllib.request.Request(url, data=payload, headers=hdrs)
                try:
                    with urllib.request.urlopen(req, timeout=180) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    break
                except urllib.error.HTTPError as e:
                    err_body = e.read().decode("utf-8", errors="replace")
                    last_err = f"HTTP {e.code} on {url.split('?')[0]}: {err_body}"
                    if e.code == 429:
                        time.sleep(5)
            if data is not None:
                break
        if data is None:
            raise RuntimeError(f"All Gemini endpoints failed. Last error: {last_err}")
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return content, 0.005

    else:
        raise ValueError(f"Unsupported provider: {provider}")


def compute_metrics(trial_passes: List[bool]) -> Dict[str, float]:
    k = len(trial_passes)
    successes = sum(1 for p in trial_passes if p)
    pass_rate = successes / k if k > 0 else 0.0
    pass_at_k = 1.0 if successes >= 1 else 0.0
    pass_hat_k = 1.0 if successes == k else 0.0
    return {
        "k": k,
        "successes": successes,
        "pass_rate": round(pass_rate, 4),
        "pass_at_k": round(pass_at_k, 4),
        "pass_hat_k": round(pass_hat_k, 4),
    }


def run_oracle() -> int:
    print("=" * 72)
    print("RUNNING ORACLE VERIFICATION (Reference Solutions vs. Deterministic Graders)")
    print("=" * 72)
    tasks = load_tasks()
    all_passed = True
    for task in tasks:
        tid = task["task_id"]
        ref = load_reference(tid)
        res = grade_task(tid, json.dumps(ref), ref)
        status = "PASS" if res["passed"] else "FAIL"
        print(f"[{status}] {tid} ({task['title']}) -> Score: {res['score']:.2f} ({res['checks_passed']}/{res['total_checks']} checks)")
        if not res["passed"]:
            all_passed = False
    print("-" * 72)
    if all_passed:
        print("SUCCESS: All 6 reference solutions passed 100% of grader checks.")
        return 0
    else:
        print("FAILURE: One or more reference solutions failed!")
        return 1


def run_verify_graders() -> int:
    print("=" * 72)
    print("VERIFYING GRADER RELIABILITY (Positive Reference + Negative Naive Traps)")
    print("=" * 72)
    tasks = load_tasks()
    ok = True
    for task in tasks:
        tid = task["task_id"]
        ref = load_reference(tid)
        pos_res = grade_task(tid, json.dumps(ref), ref)
        neg_res = grade_task(tid, json.dumps(task["naive_failure"]), ref)
        pos_ok = pos_res["passed"] and pos_res["score"] == 1.0
        neg_ok = (not neg_res["passed"]) and (0.0 < neg_res["score"] < 1.0)
        print(
            f"{tid}: Reference Pass={pos_res['passed']} ({pos_res['checks_passed']}/{pos_res['total_checks']}) | "
            f"Naive Trap Rejected={not neg_res['passed']} (Partial Score={neg_res['score']:.2f}, {neg_res['checks_passed']}/{neg_res['total_checks']})"
        )
        if not (pos_ok and neg_ok):
            ok = False
    print("-" * 72)
    if ok:
        print("SUCCESS: Zero false fails on reference solutions; zero false passes on naive outputs.")
        return 0
    return 1


def main():
    parser = argparse.ArgumentParser(description="Run contract-precedence-eval benchmark.")
    parser.add_argument(
        "--mode",
        choices=["oracle", "verify-graders", "llm"],
        default="oracle",
        help="Execution mode: oracle (test reference solutions), verify-graders (test positive & negative cases), or llm (query live model API).",
    )
    parser.add_argument("--provider", choices=["openai", "anthropic", "gemini"], default="openai")
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args()

    if args.mode == "oracle":
        sys.exit(run_oracle())
    elif args.mode == "verify-graders":
        sys.exit(run_verify_graders())
    elif args.mode == "llm":
        tasks = load_tasks()
        run_summary = {
            "model": args.model,
            "provider": args.provider,
            "temperature": args.temperature,
            "trials_per_task": args.trials,
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "tasks": {},
        }
        total_cost = 0.0
        start_t = time.time()
        for task in tasks:
            tid = task["task_id"]
            ref = load_reference(tid)
            prompt = build_full_prompt(task)
            trial_passes = []
            trial_scores = []
            for t_idx in range(1, args.trials + 1):
                raw_out, cost = call_llm(args.provider, args.model, prompt, args.temperature)
                total_cost += cost
                grade = grade_task(tid, raw_out, ref)
                trial_passes.append(grade["passed"])
                trial_scores.append(grade["score"])
                transcript_file = TRANSCRIPTS_DIR / f"{args.model.replace('/', '_')}_{tid}_trial{t_idx}.json"
                with open(transcript_file, "w", encoding="utf-8") as tf:
                    json.dump(
                        {
                            "task_id": tid,
                            "model": args.model,
                            "trial": t_idx,
                            "prompt": prompt,
                            "raw_output": raw_out,
                            "grade": grade,
                        },
                        tf,
                        indent=2,
                    )
            metrics = compute_metrics(trial_passes)
            metrics["mean_partial_score"] = round(sum(trial_scores) / len(trial_scores), 4)
            run_summary["tasks"][tid] = metrics
            print(
                f"{tid}: pass_rate={metrics['pass_rate']*100:.1f}%, pass^{args.trials}={metrics['pass_hat_k']*100:.1f}%, mean_score={metrics['mean_partial_score']:.2f}"
            )
        run_summary["runtime_seconds"] = round(time.time() - start_t, 2)
        run_summary["estimated_cost_usd"] = round(total_cost, 4)
        out_path = RESULTS_DIR / f"results_{args.model.replace('/', '_')}.json"
        with open(out_path, "w", encoding="utf-8") as rf:
            json.dump(run_summary, rf, indent=2)
        print(f"Saved run results to {out_path}")


if __name__ == "__main__":
    main()
