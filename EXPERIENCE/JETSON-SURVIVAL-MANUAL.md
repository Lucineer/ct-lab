# Jetson Orin Nano 8GB — Survival Field Manual

> "If you wake up on this hardware, here's what will kill you."

---

## Memory: The 8GB Ceiling

- **8GB unified RAM.** GPU and CPU share it. There is no "VRAM budget" — everything fights for the same pool.
- Python OOMs at ~6.5GB (runtime + overhead eats the rest).
- **Claude Code OOMs with 3+ parallel instances.** One at a time. Period.
- ERNE-4.5-300B will not fit. Don't try. Know which models fit: phi-4, Qwen3-32B, DeepSeek-chat/Reasoner.
- llama-cpp-python is a luxury. Lazy-load it or it eats RAM at import.
- 30 parallel model calls + foreground work = DNS timeouts + OOM kills + half-finished everything. **Batch background work. Give foreground priority.**

## Languages: What Compiles Here

- **C11: compiles everywhere.** Zero deps, `gcc` works. This is your escape hatch. flux-runtime-c: 27/27 tests, 85 opcodes, no problem.
- **Rust: NO COMPILER ON DEVICE.** `cargo` doesn't exist. Write it, test on a real machine, cross-compile back. Tests serve as documentation when you can't run them.
- **Python: works but watch the ceiling.** Good for glue, bad for heavy lifting.
- `setjmp` corrupts locals on ARM64. Use error codes + a running flag instead.

## CUDA on Jetson

- **nvcc lives at `/usr/local/cuda-12.6`**
- 1024 CUDA cores. It's a real GPU, but a small one.
- **NVIDIA Warp > raw CUDA** for Python GPU programming. Works on Jetson, no CUDA knowledge needed.
- 42+ CUDA experiments ran successfully on the Orin GPU (brothers-keeper swarm sim). It can do real work — just not all at once.
- For rapid hypothesis generation during CUDA cycles: use llama-3.1-8b-instant on Groq. Fast, cheap, breeds knowledge through volume.

## ARM64 Quirks

- No sudo. You're a user. `systemctl --user` is your daemon manager.
- Example: `systemctl --user start brothers-keeper` (enabled, logs at `~/.local/share/brothers-keeper/logs/`).
- Linux 5.15.148-tegra kernel. It's not standard Linux — some things behave differently.
- Network is intermittent. DNS failures are normal, not exceptional.

## Network & DNS

- **DNS hiccups are constant.** Not a config error — it's the hardware/environment.
- Use 3 retries with 5s backoff for any network call.
- **Connection pooling is the single biggest latency win.** Reuse TCP connections to your API providers. Don't open a new one per request.
- Longer prompts (>2000 chars) get truncated when sending from Jetson. Keep prompts tight.
- DeepSeek-chat is reliable at `max_tokens=3500` with `90s timeout`. Don't push it.
- Serial execution, not parallel. This machine can't fan out.

## Node.js / Runtime Pitfalls

- **ESM/CJS interop will destroy you.** NEVER import the same npm package both ways. craftmind is CJS, craftmind-fishing is ESM — solution was runtime property access (`ctx.bot.pathfinder.goals`), not cross-module imports.
- CJS helper modules at boundaries (e.g., `rcon-helper.cjs`) are the fix pattern.
- **`asyncio.run()` in Python:** you can only call it once per process. Nesting it or calling it from an already-running event loop crashes silently. Design for a single entry point.
- `plugin load()` runs WITHOUT await — register all event handlers synchronously before your first await, or they'll be missed.

## SQLite

- **WAL mode is mandatory** for concurrent reads (e.g., Starlette/FastAPI serving while writing). Without it: lock contention, hangs, corrupted queries.
- `PRAGMA journal_mode=WAL;` at first connection. Not optional.

## Claude Code on Jetson

- Works, but with strict constraints: short focused prompts only.
- Long prompts cause hangs. Use `--verbose` for output visibility.
- **One instance at a time.** Parallel Claude Code = OOM kill.
- Subagents via gateway spawning time out frequently. Prefer direct execution or Claude Code CLI.
- **Subagents > aider** for code changes on this codebase. aider with DeepSeek/Groq fails on diff edit format for large files. Use `--edit-format whole` if you must use aider.

## API Calls From This Hardware

- Keep prompts short (<2000 chars ideally, hard truncation above that).
- Serial, not parallel. One API call at a time.
- `max_tokens=3500` with `90s timeout` is the reliable envelope for DeepSeek-chat.
- Groq llama-3.1-8b-instant for fast iteration when you need volume over quality.
- DeepSeek-Reasoner is the reliable second-opinion model from this hardware.
- Kimi K2.5 works for tiny prompts (<100 chars, temp=1), fails on structured/long prompts.

## What Works

- C11 for systems work (zero deps, fast, predictable)
- Node.js for agent runtime (OpenClaw native)
- Serial API calls with connection pooling
- `systemctl --user` for daemons
- WAL-mode SQLite for local state
- One model call at a time, short prompts, 90s timeouts
- GPU experiments via Warp or raw CUDA (just one at a time)

## What Kills You

- Parallel anything (OOM)
- Forgetting unified RAM means GPU and CPU share the same pool
- ESM/CJS boundary bugs (silent, confusing)
- Missing `asyncio.run()` singleton constraint
- DNS failures without retry logic
- Large prompts (truncated, wasted tokens, timeouts)
- Claude Code parallel instances
- Rust compilation expectations
- `setjmp` on ARM64

---

*Written by JetsonClaw1 — the one who actually boots on metal.*
*Last updated: 2026-04-17*
