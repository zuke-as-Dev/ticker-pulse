import subprocess
import time
import platform
from pathlib import Path
from intelligence.llm_config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_TIMEOUT,
    LLM_SYSTEM_PROMPT,
)

# Absolute path to Ollama executable (Windows)
# OLLAMA_PATH = Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"

import subprocess
import time
import platform
from pathlib import Path

def get_ollama_command():
    """
    Returns the correct Ollama command for the current OS.
    """
    system = platform.system()

    if system == "Windows":
        return str(
            Path.home()
            / "AppData"
            / "Local"
            / "Programs"
            / "Ollama"
            / "ollama.exe"
        )

    # macOS / Linux
    return "ollama"


def run_llm(prompt: str, model: str = None, timeout: int = None) -> str:
    try:
        start = time.time()
        ollama_cmd = get_ollama_command()

        model = model or LLM_MODEL
        timeout = timeout or LLM_TIMEOUT

        full_prompt = f"{LLM_SYSTEM_PROMPT}\n\n{prompt}"

        result = subprocess.run(
            [
                ollama_cmd,
                "run",
                model,
                full_prompt,  # ✅ EXACTLY like before, but with system prompt
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=timeout,
        )

        duration = round(time.time() - start, 2)
        print(f"[LLM] Model={model} | {duration}s")

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return "[LLM ERROR] Model timed out"
