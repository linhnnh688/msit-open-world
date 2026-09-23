"""JSONL dataset helpers shared by training scripts and notebooks."""

import json
import os
from typing import Any, Dict, List


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    """Load a JSONL file; returns [] if the path does not exist."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
