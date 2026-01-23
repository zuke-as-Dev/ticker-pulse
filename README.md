# 🚀 Ticker Pulse

**Ticker Pulse** is a local-first AI market monitoring agent that continuously scans financial news, filters relevant articles for tracked instruments, summarizes key developments, determines directional bias, and delivers concise alerts via Telegram.

The project is being built incrementally with a strong focus on **correctness, reliability, and signal quality** before scaling features or automation.

---

## 🎯 Current Goal

Build a **trustworthy core intelligence pipeline** that can:

1. Reliably fetch real market news  
2. Correctly identify which articles matter for a given instrument  
3. Produce accurate summaries aligned to the instrument  
4. Classify directional bias without hallucination  
5. Deliver clean, readable Telegram alerts  

Only after this core is proven will advanced automation (dynamic instruments, auto-profiling, multi-user support) be expanded.

---

## 🧠 What Ticker Pulse Does (So Far)

- Continuously fetches market news via RSS
- Normalizes and deduplicates articles
- Filters articles based on relevance logic
- Uses a **local LLM** to:
  - Summarize news
  - Classify market bias (Bullish / Bearish / Neutral)
- Sends structured alerts to Telegram
- Runs fully locally (Windows & macOS)
- Supports configurable scan intervals
- Persists agent state safely (crash-resistant)

---

## 📌 Project Status

### ✅ Completed Phases

- **Phase 0** — Repository setup, Git workflow, environment setup  
- **Phase 1** — Telegram bot integration  
- **Phase 2** — Agent runner & scheduler  
- **Phase 3** — Instrument configuration (YAML-based, temporary)  
- **Phase 4** — RSS ingestion pipeline  
- **Phase 5** — Article deduplication & basic relevance filtering  
- **Phase 6** — Local LLM summarization & bias classification  
- **Phase 7.0** — End-to-end alerts (RSS → AI → Telegram)  
- **Phase 7.0.1** — Cross-platform stability (Windows + macOS), Telegram formatting, bias emojis  
- **Phase 7.2.1** — Telegram-based instrument tracking with persistent storage and manual confirmation fallback  

> ⚠️ Note: Phase 7.2.1 establishes the **control plane** for tracking instruments.  
> The execution engine still uses a fixed test instrument set.

---

## 🔒 Current Focus — Phase 7.A (Active)

**Phase 7.A — Core Intelligence Reliability**

This phase intentionally pauses dynamic instrument expansion to focus on the **core promise of the agent**:

- Improve RSS source coverage & diagnostics  
- Verify feed health and market reach  
- Fix keyword matching & entity anchoring  
- Improve relevance filtering (reduce false positives)  
- Ensure summaries align with the correct instrument  
- Prevent cross-instrument contamination (e.g., Nvidia news → unrelated stocks)  

> The goal of Phase 7.A is **trust**.  
> If the agent is not reliable at its core, additional features are meaningless.

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Local LLM (via Ollama)**
- RSS ingestion (`feedparser`)
- Telegram Bot API
- Persistent JSON state
- Cross-platform (Windows / macOS)

---

## 🚧 What’s Intentionally Deferred

These will be addressed **after Phase 7.A**:

- Removing YAML as runtime source of truth  
- Fully automatic instrument profiling  
- Dynamic multi-instrument attribution  
- Multi-user support  
- Deployment & monetization  

---

## 🧭 Development Philosophy

- Correctness > automation  
- Precision > volume  
- Deterministic logic before AI guesses  
- Features are added only when the underlying signal is trustworthy  

---

## 📍 Next Step

➡️ Begin **Phase 7.A — RSS ingestion, filtering, and summarization hardening**