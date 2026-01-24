# 🚀 Ticker Pulse

**Ticker Pulse** is a local-first AI market monitoring agent that continuously scans financial news, filters relevant articles for tracked instruments, summarizes key developments, determines directional bias, and delivers concise alerts via Telegram.

The project is being built incrementally with a strong focus on **correctness, reliability, and signal quality** before scaling features or automation.

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
## Project Status

### Phase 7.A — Core Signal Integrity & RSS Expansion ✅
- Expanded RSS coverage across crypto, forex, commodities, global and Indian equities
- Implemented robust article normalization and relevance filtering
- Stabilized LLM summarization into clean, structured bullet points
- Added reliable short-term bias classification with reasoning
- Switched Telegram output to HTML for consistent, production-safe formatting
- Verified cross-platform execution on Windows and macOS
