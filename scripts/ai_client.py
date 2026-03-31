from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import requests

from common import load_global_config


def _load_env_file(path: str) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def resolve_ai_settings() -> dict[str, Any]:
    config = load_global_config()["ai_execution"]
    for candidate in config.get("candidate_env_files", []):
        _load_env_file(candidate)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not available")

    model = os.getenv("MONTHLY_BUILDS_OPENAI_MODEL") or os.getenv("OPENAI_MODEL") or config["default_model"]
    base_url = os.getenv("OPENAI_BASE_URL") or config["endpoint"]
    return {
        "endpoint": base_url,
        "model": model,
        "api_key_present": True,
        "env_files": config.get("candidate_env_files", []),
        "env_var_names": config.get("env_var_names", []),
        "timeout_seconds": int(config["timeout_seconds"]),
        "temperature": float(config["temperature"]),
        "max_tokens": int(config["max_tokens"]),
    }


def chat_json(messages: list[dict[str, str]], *, model: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    settings = resolve_ai_settings()
    payload = {
        "model": model or settings["model"],
        "messages": messages,
        "temperature": settings["temperature"],
        "max_tokens": settings["max_tokens"],
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        settings["endpoint"],
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=settings["timeout_seconds"],
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return json.loads(content), {
        "model": data.get("model", payload["model"]),
        "usage": data.get("usage", {}),
        "response_id": data.get("id"),
    }
