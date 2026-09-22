"""Robust parsing of model outputs into attribute dictionaries.

MLLM outputs often wrap JSON in markdown fences or append trailing prose.
These helpers reproduce the "We extract a set of normalized attributes and
values from the output texts" step of Stage 1 (paper Section 3.4).
"""

from typing import Any, Dict, Optional
import json
import re


def _extract_first_balanced(text: str, opener: str = "{", closer: str = "}") -> Optional[str]:
    """Return the first balanced {...} substring of `text`, or None."""
    start = text.find(opener)
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Extract the first parseable JSON object from free-form text.

    Handles ```json fences, nested braces and truncated outputs. Values that
    fail to parse are skipped rather than raising.
    """
    if not text:
        return None
    # Strip markdown code fences if present.
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    candidates = []
    if fence:
        candidates.append(fence.group(1))
    candidates.append(text)

    for cand in candidates:
        raw = _extract_first_balanced(cand)
        if raw is None:
            continue
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            # Try to repair common issues: trailing commas.
            repaired = re.sub(r",\s*([}\]])", r"\1", raw)
            try:
                obj = json.loads(repaired)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                continue
    return None


def parse_attributes(text: str) -> Dict[str, Any]:
    """Parse model output into a flat attribute dictionary.

    Accepts either {"Attributes": {...}} (the AGTD output format shown in
    Figures 1 and 8 of the paper) or a bare attribute dictionary. Returns {}
    when nothing parseable is found.
    """
    obj = extract_json_object(text)
    if obj is None:
        return {}
    # Unwrap {"Attributes": {...}} if present (any casing).
    for key in ("Attributes", "attributes", "ATTRIBUTES"):
        if key in obj and isinstance(obj[key], dict):
            return {str(k): v for k, v in obj[key].items()}
    return {str(k): v for k, v in obj.items()}


def format_attributes(attrs: Dict[str, Any]) -> str:
    """Serialize attributes in the unified AGTD output format of the paper."""
    return json.dumps({"Attributes": attrs}, ensure_ascii=False, indent=2)
