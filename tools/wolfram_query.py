"""
Wolfram Alpha Query Tool — Symbolic Math Solving & Verification
Connects to the Wolfram Alpha API for equation solving, integration,
differentiation, eigenvalues, and step-by-step solutions.
"""

import json
import os
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WOLFRAM_APP_ID = os.environ.get("WOLFRAM_APP_ID", "")
WOLFRAM_FULL_URL = "https://api.wolframalpha.com/v2/query"
WOLFRAM_SHORT_URL = "https://api.wolframalpha.com/v1/result"

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class WolframResult:
    """Result from a Wolfram Alpha query."""
    query: str
    success: bool
    result_text: str               # Main result (plaintext)
    step_by_step: Optional[str]    # Step-by-step solution if available
    pods: list[dict]               # All returned pods (title → plaintext)
    image_urls: list[str]          # Any plot/diagram URLs
    error_message: Optional[str]


# ---------------------------------------------------------------------------
# Core query functions
# ---------------------------------------------------------------------------

def query_wolfram_full(
    query: str,
    app_id: Optional[str] = None,
    include_pods: Optional[list[str]] = None,
) -> WolframResult:
    """
    Send a full query to Wolfram Alpha v2 API.

    Args:
        query:        Math expression or natural-language question,
                      e.g. "integrate x^2 sin(x) dx" or "eigenvalues {{1,2},{3,4}}"
        app_id:       Wolfram Alpha App ID. Falls back to WOLFRAM_APP_ID env var.
        include_pods: Optional list of pod titles to include (filters output).

    Returns:
        WolframResult with all parsed data.
    """
    aid = app_id or WOLFRAM_APP_ID
    if not aid:
        return WolframResult(
            query=query,
            success=False,
            result_text="",
            step_by_step=None,
            pods=[],
            image_urls=[],
            error_message="WOLFRAM_APP_ID not set. Get a free key at https://developer.wolframalpha.com",
        )

    params: dict = {
        "input": query,
        "appid": aid,
        "output": "json",
        "format": "plaintext,image",
        "podstate": "Step-by-step solution",
    }
    if include_pods:
        params["includepodid"] = ",".join(include_pods)

    try:
        resp = requests.get(WOLFRAM_FULL_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        return WolframResult(
            query=query,
            success=False,
            result_text="",
            step_by_step=None,
            pods=[],
            image_urls=[],
            error_message=f"Request failed: {exc}",
        )

    query_result = data.get("queryresult", {})
    success = query_result.get("success", False)

    if not success:
        return WolframResult(
            query=query,
            success=False,
            result_text="",
            step_by_step=None,
            pods=[],
            image_urls=[],
            error_message=query_result.get("error", {}).get("msg", "Query unsuccessful."),
        )

    # Parse pods
    pods_raw = query_result.get("pods", [])
    pods: list[dict] = []
    result_text = ""
    step_by_step = None
    image_urls: list[str] = []

    for pod in pods_raw:
        pod_title = pod.get("title", "")
        subpods = pod.get("subpods", [])

        texts: list[str] = []
        for sp in subpods:
            plaintext = sp.get("plaintext", "")
            if plaintext:
                texts.append(plaintext)
            img = sp.get("img", {})
            if img.get("src"):
                image_urls.append(img["src"])

        pod_text = "\n".join(texts)
        pods.append({"title": pod_title, "text": pod_text})

        # Capture main result
        if pod_title in ("Result", "Results", "Solution", "Exact result"):
            result_text = pod_text
        # Capture step-by-step
        if "step-by-step" in pod_title.lower() or "steps" in pod_title.lower():
            step_by_step = pod_text

    # Fallback: if no explicit Result pod, use the second pod (first is Input)
    if not result_text and len(pods) >= 2:
        result_text = pods[1].get("text", "")

    return WolframResult(
        query=query,
        success=True,
        result_text=result_text,
        step_by_step=step_by_step,
        pods=pods,
        image_urls=image_urls,
        error_message=None,
    )


def query_wolfram_short(
    query: str,
    app_id: Optional[str] = None,
) -> str:
    """
    Get a quick one-line answer from Wolfram Alpha (Short Answers API).

    Args:
        query:  Math expression, e.g. "integral of x^2 from 0 to 1"
        app_id: Wolfram Alpha App ID.

    Returns:
        Short answer string, or error message.
    """
    aid = app_id or WOLFRAM_APP_ID
    if not aid:
        return "Error: WOLFRAM_APP_ID not set."

    params = {"i": query, "appid": aid}
    try:
        resp = requests.get(WOLFRAM_SHORT_URL, params=params, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as exc:
        return f"Error: {exc}"


# ---------------------------------------------------------------------------
# Convenience helpers for common math operations
# ---------------------------------------------------------------------------

def solve_equation(equation: str, variable: str = "x") -> WolframResult:
    """Solve an equation for a variable."""
    return query_wolfram_full(f"solve {equation} for {variable}")


def compute_integral(expression: str, variable: str = "x", bounds: Optional[tuple] = None) -> WolframResult:
    """Compute a definite or indefinite integral."""
    if bounds:
        query = f"integrate {expression} d{variable} from {bounds[0]} to {bounds[1]}"
    else:
        query = f"integrate {expression} d{variable}"
    return query_wolfram_full(query)


def compute_derivative(expression: str, variable: str = "x", order: int = 1) -> WolframResult:
    """Compute the nth derivative of an expression."""
    ordinal = {1: "", 2: "second ", 3: "third ", 4: "fourth "}
    ord_str = ordinal.get(order, f"{order}th ")
    return query_wolfram_full(f"{ord_str}derivative of {expression} with respect to {variable}")


def compute_eigenvalues(matrix: str) -> WolframResult:
    """Compute eigenvalues of a matrix. Pass matrix as '{{a,b},{c,d}}'."""
    return query_wolfram_full(f"eigenvalues {matrix}")


def solve_ode(equation: str, function: str = "y(x)") -> WolframResult:
    """Solve an ordinary differential equation."""
    return query_wolfram_full(f"solve ODE {equation}")


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_wolfram_result(result: WolframResult) -> str:
    """Pretty-print a Wolfram result for the agent to consume."""
    if not result.success:
        return f"❌ Wolfram query failed: {result.error_message}"

    lines = [f"### Wolfram Alpha: `{result.query}`\n"]

    if result.result_text:
        lines.append(f"**Result:** {result.result_text}\n")

    if result.step_by_step:
        lines.append(f"**Step-by-step:**\n```\n{result.step_by_step}\n```\n")

    if result.pods:
        lines.append("**All pods:**")
        for pod in result.pods:
            if pod["text"]:
                lines.append(f"- **{pod['title']}:** {pod['text']}")

    if result.image_urls:
        lines.append("\n**Plots/Diagrams:**")
        for url in result.image_urls[:3]:
            lines.append(f"- {url}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if not WOLFRAM_APP_ID:
        print("⚠️  Set WOLFRAM_APP_ID environment variable first.")
        print("   Get a free key at: https://developer.wolframalpha.com")
        sys.exit(1)

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "integrate x^2 sin(x) dx"
    print(f"🔍 Querying Wolfram Alpha: {query}\n")

    result = query_wolfram_full(query)
    print(format_wolfram_result(result))
