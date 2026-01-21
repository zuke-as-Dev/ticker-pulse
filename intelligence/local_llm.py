import subprocess
import time
from pathlib import Path

# Absolute path to Ollama executable (Windows)
OLLAMA_PATH = Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe"


def run_llm(prompt: str, model: str = "qwen2.5:7b", timeout: int = 120) -> str:
    """
    Runs a local LLM via Ollama (Windows-safe, UTF-8 safe).
    """
    try:
        start = time.time()

        result = subprocess.run(
            [str(OLLAMA_PATH), "run", model, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",      # 🔑 FORCE UTF-8
            errors="ignore",       # 🔑 DROP undecodable chars
            timeout=timeout
        )

        duration = round(time.time() - start, 2)
        print(f"[LLM] Completed in {duration}s")

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return "[LLM ERROR] Model timed out"
