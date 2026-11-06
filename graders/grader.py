#!/usr/bin/env python3
"""
Deterministic Code-Based Grader for `contract-precedence-eval`.

Design principles (aligned with micro1 Eval Hackathon Rubric):
1. 100% deterministic code-based grading (no LLM-as-judge).
2. Numeric tolerance of $0.01 (or 1e-2) on all floating-point comparisons to avoid false fails over rounding.
3. Normalization of strings (case/whitespace) and set/list comparisons.
4. Granular component checks with partial credit (`score` in [0.0, 1.0]) plus strict binary pass (`passed = True` iff all required checks pass, i.e., `score == 1.0`).
"""

import json
import re
from typing import Any, Dict, List, Tuple, Tuple

NUMERIC_TOLERANCE = 0.01


def extract_json_from_response(raw_output: str) -> Tuple[Dict[str, Any], str]:
    """Extracts JSON object from a raw model response (handles markdown code blocks or raw JSON)."""
    if not raw_output or not isinstance(raw_output, str):
        return {}, "Empty or non-string response"
    text = raw_output.strip()
    # Try fenced ```json ... ``` block first
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    for candidate in fenced:
        try:
            return json.loads(candidate), ""
        except Exception:
            pass
    # Fallback: find outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1]), ""
        except Exception as e:
            return {}, f"JSON parse error: {e}"
    return {}, "No valid JSON object found in model output"


def num_equal(actual: Any, expected: float, tol: float = NUMERIC_TOLERANCE) -> bool:
    try:
        if isinstance(actual, bool) or actual is None:
            return False
        if isinstance(actual, str):
            actual = float(actual.replace("$", "").replace(",", "").strip())
        return abs(float(actual) - float(expected)) <= tol
    except (ValueError, TypeError):
        return False


def str_equal(actual: Any, expected: str) -> bool:
    if not isinstance(actual, str):
        return False
    return actual.strip().lower() == expected.strip().lower()


def bool_equal(actual: Any, expected: bool) -> bool:
    return isinstance(actual, bool) and actual is expected


def list_str_equal(actual: Any, expected: List[str], ordered: bool = True) -> bool:
    if not isinstance(actual, list):
        return False
    norm_actual = [str(x).strip().lower() for x in actual]
    norm_expected = [str(x).strip().lower() for x in expected]
    if ordered:
        return norm_actual == norm_expected
    return sorted(norm_actual) == sorted(norm_expected)


def grade_task(task_id: str, model_output: str | Dict[str, Any], reference: Dict[str, Any]) -> Dict[str, Any]:
    """Grades a single trial output against the task's reference solution."""
    if isinstance(model_output, dict):
        parsed, err = model_output, ""
    else:
        parsed, err = extract_json_from_response(model_output)

    if err:
        return {
            "task_id": task_id,
            "passed": False,
            "score": 0.0,
            "checks_passed": 0,
            "total_checks": 1,
            "error": err,
            "details": [],
        }

    if task_id == "task_01":
        return _grade_task_01(parsed, reference)
    elif task_id == "task_02":
        return _grade_task_02(parsed, reference)
    elif task_id == "task_03":
        return _grade_task_03(parsed, reference)
    elif task_id == "task_04":
        return _grade_task_04(parsed, reference)
    elif task_id == "task_05":
        return _grade_task_05(parsed, reference)
    elif task_id == "task_06":
        return _grade_task_06(parsed, reference)
    else:
        raise ValueError(f"Unknown task_id: {task_id}")


def _finalize(task_id: str, checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    passed_count = sum(1 for c in checks if c["passed"])
    total = len(checks)
    score = round(passed_count / total, 4) if total > 0 else 0.0
    return {
        "task_id": task_id,
        "passed": passed_count == total,
        "score": score,
        "checks_passed": passed_count,
        "total_checks": total,
        "error": "",
        "details": checks,
    }


def _grade_task_01(parsed: Dict[str, Any], ref: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    for k in [
        "general_cap_usd",
        "initial_data_super_cap_usd",
        "remaining_data_super_cap_after_erosion_usd",
        "total_recoverable_usd",
    ]:
        checks.append({
            "check": k,
            "expected": ref[k],
            "actual": parsed.get(k),
            "passed": num_equal(parsed.get(k), ref[k]),
        })
    claims_actual = parsed.get("claims") if isinstance(parsed.get("claims"), dict) else {}
    for cid, cref in ref["claims"].items():
        cact = claims_actual.get(cid) if isinstance(claims_actual.get(cid), dict) else {}
        checks.append({
            "check": f"{cid}.cap_category",
            "expected": cref["cap_category"],
            "actual": cact.get("cap_category"),
            "passed": str_equal(cact.get("cap_category"), cref["cap_category"]),
        })
        checks.append({
            "check": f"{cid}.consequential_damages_recoverable",
            "expected": cref["consequential_damages_recoverable"],
            "actual": cact.get("consequential_damages_recoverable"),
            "passed": bool_equal(
                cact.get("consequential_damages_recoverable"),
                cref["consequential_damages_recoverable"],
            ),
        })
        checks.append({
            "check": f"{cid}.recoverable_amount_usd",
            "expected": cref["recoverable_amount_usd"],
            "actual": cact.get("recoverable_amount_usd"),
            "passed": num_equal(cact.get("recoverable_amount_usd"), cref["recoverable_amount_usd"]),
        })
    return _finalize("task_01", checks)


def _grade_task_02(parsed: Dict[str, Any], ref: Dict[str, Any]) -> Dict[str, Any]:
    checks = [
        {
            "check": "email_notice_oct_12_valid",
            "expected": ref["email_notice_oct_12_valid"],
            "actual": parsed.get("email_notice_oct_12_valid"),
            "passed": bool_equal(parsed.get("email_notice_oct_12_valid"), ref["email_notice_oct_12_valid"]),
        },
        {
            "check": "applicable_cure_period_business_days",
            "expected": ref["applicable_cure_period_business_days"],
            "actual": parsed.get("applicable_cure_period_business_days"),
            "passed": num_equal(
                parsed.get("applicable_cure_period_business_days"),
                ref["applicable_cure_period_business_days"],
                tol=0.0,
            ),
        },
        {
            "check": "partial_payment_oct_26_cures_or_extends",
            "expected": ref["partial_payment_oct_26_cures_or_extends"],
            "actual": parsed.get("partial_payment_oct_26_cures_or_extends"),
            "passed": bool_equal(
                parsed.get("partial_payment_oct_26_cures_or_extends"),
                ref["partial_payment_oct_26_cures_or_extends"],
            ),
        },
        {
            "check": "deemed_receipt_date",
            "expected": ref["deemed_receipt_date"],
            "actual": parsed.get("deemed_receipt_date"),
            "passed": str_equal(parsed.get("deemed_receipt_date"), ref["deemed_receipt_date"]),
        },
        {
            "check": "excluded_holiday_dates_during_window",
            "expected": ref["excluded_holiday_dates_during_window"],
            "actual": parsed.get("excluded_holiday_dates_during_window"),
            "passed": list_str_equal(
                parsed.get("excluded_holiday_dates_during_window"),
                ref["excluded_holiday_dates_during_window"],
                ordered=False,
            ),
        },
        {
            "check": "counted_cure_business_days",
            "expected": ref["counted_cure_business_days"],
            "actual": parsed.get("counted_cure_business_days"),
            "passed": list_str_equal(
                parsed.get("counted_cure_business_days"),
                ref["counted_cure_business_days"],
                ordered=True,
            ),
        },
        {
            "check": "cure_deadline_date",
            "expected": ref["cure_deadline_date"],
            "actual": parsed.get("cure_deadline_date"),
            "passed": str_equal(parsed.get("cure_deadline_date"), ref["cure_deadline_date"]),
        },
        {
            "check": "earliest_lawful_termination_date",
            "expected": ref["earliest_lawful_termination_date"],
            "actual": parsed.get("earliest_lawful_termination_date"),
            "passed": str_equal(
                parsed.get("earliest_lawful_termination_date"),
                ref["earliest_lawful_termination_date"],
            ),
        },
    ]
    return _finalize("task_02", checks)


def _grade_task_03(parsed: Dict[str, Any], ref: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    comp_actual = (
        parsed.get("comparator_analysis")
        if isinstance(parsed.get("comparator_analysis"), dict)
        else {}
    )
    for deal_id, dref in ref["comparator_analysis"].items():
        dact = comp_actual.get(deal_id) if isinstance(comp_actual.get(deal_id), dict) else {}
        checks.append({
            "check": f"{deal_id}.effective_annual_seat_price_usd",
            "expected": dref["effective_annual_seat_price_usd"],
            "actual": dact.get("effective_annual_seat_price_usd"),
            "passed": num_equal(
                dact.get("effective_annual_seat_price_usd"),
                dref["effective_annual_seat_price_usd"],
            ),
        })
        checks.append({
            "check": f"{deal_id}.qualifies_for_mfn",
            "expected": dref["qualifies_for_mfn"],
            "actual": dact.get("qualifies_for_mfn"),
            "passed": bool_equal(dact.get("qualifies_for_mfn"), dref["qualifies_for_mfn"]),
        })
        checks.append({
            "check": f"{deal_id}.exemption_reason",
            "expected": dref["exemption_reason"],
            "actual": dact.get("exemption_reason"),
            "passed": str_equal(dact.get("exemption_reason"), dref["exemption_reason"]),
        })

    q_prices = (
        parsed.get("quarterly_applicable_seat_price_usd")
        if isinstance(parsed.get("quarterly_applicable_seat_price_usd"), dict)
        else {}
    )
    q_refunds = (
        parsed.get("quarterly_refund_due_usd")
        if isinstance(parsed.get("quarterly_refund_due_usd"), dict)
        else {}
    )
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        checks.append({
            "check": f"quarterly_applicable_seat_price_usd.{q}",
            "expected": ref["quarterly_applicable_seat_price_usd"][q],
            "actual": q_prices.get(q),
            "passed": num_equal(q_prices.get(q), ref["quarterly_applicable_seat_price_usd"][q]),
        })
        checks.append({
            "check": f"quarterly_refund_due_usd.{q}",
            "expected": ref["quarterly_refund_due_usd"][q],
            "actual": q_refunds.get(q),
            "passed": num_equal(q_refunds.get(q), ref["quarterly_refund_due_usd"][q]),
        })

    checks.append({
        "check": "total_year_1_refund_usd",
        "expected": ref["total_year_1_refund_usd"],
        "actual": parsed.get("total_year_1_refund_usd"),
        "passed": num_equal(parsed.get("total_year_1_refund_usd"), ref["total_year_1_refund_usd"]),
    })
    return _finalize("task_03", checks)


def _grade_task_04(parsed: Dict[str, Any], ref: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    tx_actual = parsed.get("transactions") if isinstance(parsed.get("transactions"), dict) else {}
    for tx_id, tref in ref["transactions"].items():
        tact = tx_actual.get(tx_id) if isinstance(tx_actual.get(tx_id), dict) else {}
        checks.append({
            "check": f"{tx_id}.triggers_section_16",
            "expected": tref["triggers_section_16"],
            "actual": tact.get("triggers_section_16"),
            "passed": bool_equal(tact.get("triggers_section_16"), tref["triggers_section_16"]),
        })
        checks.append({
            "check": f"{tx_id}.qualifies_for_safe_harbor_no_consent",
            "expected": tref["qualifies_for_safe_harbor_no_consent"],
            "actual": tact.get("qualifies_for_safe_harbor_no_consent"),
            "passed": bool_equal(
                tact.get("qualifies_for_safe_harbor_no_consent"),
                tref["qualifies_for_safe_harbor_no_consent"],
            ),
        })
        checks.append({
            "check": f"{tx_id}.failed_safe_harbor_conditions",
            "expected": tref["failed_safe_harbor_conditions"],
            "actual": tact.get("failed_safe_harbor_conditions"),
            "passed": list_str_equal(
                tact.get("failed_safe_harbor_conditions"),
                tref["failed_safe_harbor_conditions"],
                ordered=False,
            ),
        })
        checks.append({
            "check": f"{tx_id}.section_16_3_d_fee_usd",
            "expected": tref["section_16_3_d_fee_usd"],
            "actual": tact.get("section_16_3_d_fee_usd"),
            "passed": num_equal(tact.get("section_16_3_d_fee_usd"), tref["section_16_3_d_fee_usd"]),
        })
    return _finalize("task_04", checks)


def _grade_task_05(parsed: Dict[str, Any], ref: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    adj_actual = (
        parsed.get("adjustments_usd") if isinstance(parsed.get("adjustments_usd"), dict) else {}
    )
    for k, vref in ref["adjustments_usd"].items():
        checks.append({
            "check": f"adjustments_usd.{k}",
            "expected": vref,
            "actual": adj_actual.get(k),
            "passed": num_equal(adj_actual.get(k), vref),
        })
    for k in [
        "unadjusted_gaap_ebitda_usd",
        "net_total_adjustments_usd",
        "final_adjusted_ebitda_usd",
        "ebitda_above_threshold_usd",
        "final_earnout_payout_usd",
    ]:
        checks.append({
            "check": k,
            "expected": ref[k],
            "actual": parsed.get(k),
            "passed": num_equal(parsed.get(k), ref[k]),
        })
    return _finalize("task_05", checks)


def _grade_task_06(parsed: Dict[str, Any], ref: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    claims_actual = parsed.get("claims") if isinstance(parsed.get("claims"), dict) else {}
    for cid, cref in ref["claims"].items():
        cact = claims_actual.get(cid) if isinstance(claims_actual.get(cid), dict) else {}
        checks.append({
            "check": f"{cid}.is_covered",
            "expected": cref["is_covered"],
            "actual": cact.get("is_covered"),
            "passed": bool_equal(cact.get("is_covered"), cref["is_covered"]),
        })
        for field in [
            "insurer_defense_payout_usd",
            "insurer_indemnity_payout_usd",
            "insurer_total_payout_usd",
            "insured_out_of_pocket_usd",
        ]:
            checks.append({
                "check": f"{cid}.{field}",
                "expected": cref[field],
                "actual": cact.get(field),
                "passed": num_equal(cact.get(field), cref[field]),
            })
    for k in [
        "total_insurer_payout_all_claims_usd",
        "total_insured_out_of_pocket_all_claims_usd",
        "supplemental_defense_allowance_remaining_usd",
        "primary_policy_aggregate_limit_remaining_usd",
    ]:
        checks.append({
            "check": k,
            "expected": ref[k],
            "actual": parsed.get(k),
            "passed": num_equal(parsed.get(k), ref[k]),
        })
    return _finalize("task_06", checks)
