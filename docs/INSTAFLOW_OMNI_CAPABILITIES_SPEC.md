# 🌐 InstaFlow OMNI: The Universal Social Intelligence & Autonomous Action Platform
## Comprehensive Architectural Specification & Capability Blueprint

> **System**: InstaFlow OMNI (Evolution from personal lead bot to universal social intelligence engine)  
> **Platform Core**: Antigravity Layer 0 OS | AMD Ryzen 7 Host | SQLite WAL Central Data Fabric  
> **Integrated Skills**: `/agent-reach`, `/agent-council`, `/scrapling`, `/research`  
> **Multi-Vector Surfaces**: Instagram, X (Twitter), Pinterest, Reddit, GitHub, arXiv / Academic Repos  

---

## 1. Executive Vision & Core Thesis

Social platforms (Instagram Reels, X threads, Pinterest infographics, Reddit discussions) represent the fastest-moving unstructured firehose of human developer and creator knowledge. However, 95% of this knowledge is trapped, polluted with marketing clickbait ("slop"), unverified, or lost in "Saved" graveyards.

**InstaFlow OMNI** transforms Instagram into an autonomous, bi-directional intelligence workbench:
1. **Inbound Truth Engine**: Intercepts reels, video tutorials, and posts; strips marketing fluff; and cross-references claims against academic literature (arXiv/PubMed), practitioner forums (Reddit), and open-source code (GitHub).
2. **5-Persona Peer Review Council**: Evaluates claims, security risks, virality scores, and real-world viability before ingestion or action.
3. **Zero-Trust Teleoperation (`reach`)**: Dispatches heavy scraping, proxy rotation, and headless browser sessions to isolated remote/Docker containers while keeping all agent memory, credentials, and logic strictly local.
4. **Autonomous Contextual Outbound**: Provides intelligent, loop-safe DM lead dispatch and engagement automation replacing expensive, rigid SaaS tools.
5. **Reel-to-Skill Autonomous Compiler**: Automatically converts verified workflows into production-grade executable agent skills in `.agents/skills/`.

---

## 2. The 5 Core Capability Pillars

```
+---------------------------------------------------------------------------------------------------+
|                                     INSTAFLOW OMNI ARCHITECTURE                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   [ Inbound Surfaces ]                                                        [ Outbound Rails ]  |
|   - Instagram Reels / DMs / Comments                                          - Instant DMs       |
|   - X (Twitter) Threads                                                       - Lead Magnets      |
|   - Reddit (r/LocalLLaMA, r/Python)                                           - Auto-Comments     |
|   - Pinterest Infographics & Visuals                                          - Obsidian Notes    |
|   - arXiv Papers & GitHub Repos                                               - Agent Skills      |
|            |                                                                          ^           |
|            v                                                                          |           |
|   +---------------------------------------------------------------------------------------+       |
|   | PILLAR 1: MULTI-SURFACE INGESTION & ADAPTIVE HARVESTING (/scrapling)                  |       |
|   | - Undetectable Camoufox stealth browser & Playwright dynamic JS renderer              |       |
|   | - Token-bounded Scrapling (<400 tokens) stripping scripts, styles, SVGs, and ads      |       |
|   +---------------------------------------------------------------------------------------+       |
|            |                                                                          ^           |
|            v                                                                          |           |
|   +---------------------------------------------------------------------------------------+       |
|   | PILLAR 2: OMNICHANNEL TRUTH ENGINE & RESEARCH CROSS-REFERENCE (/research)             |       |
|   | - Vector 1: arXiv API & Academic Paper verification (formulas, benchmarks)            |       |
|   | - Vector 2: GitHub repo audit (stars, commits, MIT/Apache license check)              |       |
|   | - Vector 3: Reddit practitioner reality check (unfiltered hardware failure modes)     |       |
|   | - Vector 4: Pinterest & X trend triangulation and visual moodboard synthesis           |       |
|   +---------------------------------------------------------------------------------------+       |
|            |                                                                          ^           |
|            v                                                                          |           |
|   +---------------------------------------------------------------------------------------+       |
|   | PILLAR 3: 5-PERSONA COUNCIL DELIBERATION & DE-SLOP FILTER (/agent-council)            |       |
|   | - Architect (scalability) | Security Warden (threat model, prompt injection guard)     |       |
|   | - Performance (latency <16ms) | UI/UX Arbiter (anti-slop tone) | Contrarian (utility) |       |
|   | - Unanimous or Q-Score > 0.85 required to promote claim to truth databank             |       |
|   +---------------------------------------------------------------------------------------+       |
|            |                                                                          ^           |
|            v                                                                          |           |
|   +---------------------------------------------------------------------------------------+       |
|   | PILLAR 4: ZERO-TRUST REMOTE TELEOPERATION LAYER (/agent-reach)                         |       |
|   | - 'reach' execution tunnel crossing Windows / WSL2 / Docker boundary                  |       |
|   | - Host memory & tokens remain strictly local; remote workers execute isolated tasks   |       |
|   +---------------------------------------------------------------------------------------+       |
|            |                                                                          ^           |
|            v                                                                          |           |
|   +---------------------------------------------------------------------------------------+       |
|   | PILLAR 5: AUTONOMOUS ACTION, LEAD DISPATCH & SKILL COMPILATION (reel-to-skill)        |       |
|   | - Sub-16ms direct polling & context-aware DM responder with DWEL loop guard (<0.5ms)  |       |
|   | - Automatic generation of .agents/skills/<name>/SKILL.md & SQLite WAL vectors         |       |
|   +---------------------------------------------------------------------------------------+       |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Deep-Dive Specification by Pillar

### Pillar 1: Multi-Surface Ingestion & Adaptive Harvesting (`/scrapling`)
- **Instagram Direct Ingestion**:
  - Ingests video audio tracks, OCR on screen frames, caption text, and pinned comments.
  - Automatically resolves shortlinks (`linkinbio`, `bit.ly`, ManyChat redirect funnels) to discover canonical underlying tools.
- **Adaptive Scrapling Fetcher Cascade**:
  - *Fast Static*: `Fetcher` (curl_cffi with browser TLS impersonation) for open blog posts and GitHub releases.
  - *Cloudflare / WAF Bypass*: `StealthyFetcher` with Camoufox (C++ in-tree patches, hardware spoofing) to harvest protected community forums and gated tech blogs.
  - *Dynamic SPAs*: `DynamicFetcher` with Playwright for JavaScript-rendered sites (X, Pinterest, Reddit).
- **Token Clamping**: Raw HTML is distilled via `core/token_bounded_scrapling.py` to `<400` tokens, saving >90% token burn before LLM ingestion.

### Pillar 2: Omnichannel Truth Engine & Research Cross-Reference (`/research`)
When an influencer or tutorial posts a claim (e.g., *"This new RAG technique achieves 99% accuracy with 0 latency"*):
- **Academic Rigor (arXiv & Scholar)**:
  - Queries `export.arxiv.org/api/query` for original author preprints.
  - Extracts mathematical bounds, true baseline benchmarks, and citation credibility.
- **Practitioner Reality Check (Reddit & Hacker News)**:
  - Searches `r/LocalLLaMA`, `r/MachineLearning`, and StackOverflow.
  - Extracts real user complaints: *"Memory leak after 50 queries"*, *"Requires 48GB VRAM despite claims"*.
- **Open-Source Code Integrity (GitHub API)**:
  - Evaluates repository stars, open issues, release cadences, and license compatibility (MIT/Apache vs commercial-restricted SSPL).
- **Visual Intelligence (Pinterest & X)**:
  - Ingests architecture diagrams and infographic cheat-sheets from Pinterest and developer X threads to accompany text notes.

### Pillar 3: The 5-Persona Council Content & Claim Validator (`/agent-council`)
Every incoming tool, claim, or proposed outbound marketing response passes through the 5-Persona Council before entering the system memory:
1. **The Systems Architect**: Verifies structural decoupling, standard protocols, and whether this tool fits into the Antigravity OS stack.
2. **The Security Warden**: Scans links for phishing, verifies zero hardcoded tokens, and tests inbound DMs for prompt injection / jailbreak attacks.
3. **The Performance Engineer**: Benchmarks execution latency (<16ms target), memory footprint (<25MB target), and avoids bloated frameworks.
4. **The UI/UX & Anti-Slop Craftsman**: Enforces concise, authentic human voice (`li-human`), strips generic AI pleasantries ("delve", "game-changer", "testament"), and validates layout polish.
5. **The Contrarian (Devil's Advocate)**: Challenges the fundamental premise: *"Can this be done in 15 lines of pure Python without adding this new tool?"*

### Pillar 4: Zero-Trust Remote Teleoperation Layer (`/agent-reach`)
- **Local Isolation Invariant**: The local Ryzen 7 machine retains 100% of LLM reasoning, API keys, credentials, and SQLite databases.
- **Headless Fleet Scaling**:
  - When scraping hundreds of profiles or running continuous monitoring, InstaFlow dispatches headless browser sessions to remote Linux boxes, WSL2 instances, or Docker containers via `reach <target> exec`.
  - IP rotation, CAPTCHA solving, and bandwidth-heavy video processing happen off-host.
  - Clean, sanitized JSON telemetry is piped back across the encrypted `reach` tunnel.

### Pillar 5: Autonomous Action, Lead Dispatch & Skill Evolution
- **Contextual Lead Magnet Engine**:
  - Automatically identifies user intent from comments and DMs (e.g. distinguishing a student asking for beginner notes from a senior engineer asking for Docker configs).
  - Delivers dynamic, personalized assets (code snippets, cheatsheet links, benchmark reports).
- **DWEL Loop Interceptor (<0.5ms)**:
  - Tracks conversational directed acyclic graphs to terminate bot-to-bot infinite loops instantly.
- **Reel-to-Skill Synthesis**:
  - If a harvested tool scores `APPROVED` by the Council and meets the "Worth Doing Twice" threshold:
  - Autonomously scaffolds `.agents/skills/<tool_name>/SKILL.md` with verified code examples, reference commands, and registers it in `core/skill_index.json`.

---

## 4. Operational Invariants & Defensive Hardening

| Dimension | Potential Vulnerability | InstaFlow OMNI Defensive Invariant |
| :--- | :--- | :--- |
| **1. Meta Platform Bans** | High-velocity automated actions trigger bot bans. | **Human Velocity Envelope**: Randomized 3–7s inter-action delays, residential IP multiplexing via `reach`, strict daily quota caps. |
| **2. Prompt Injection in DMs** | Malicious users send payloads attempting to dump API keys or alter system instructions. | **Zeroize & Whitelist Guard**: Inbound DMs are sanitized; prompt injections are caught by Security Warden regex and discarded silently. |
| **3. Hallucinated Tools** | Influencers promote fake AI repositories or scam tokens. | **Adversarial Verification Gate**: If GitHub repo has zero commits in 30 days or fails build checks, claim is tagged `UNVERIFIED_SLOP`. |
| **4. Cloud SaaS Lock-In** | Expensive recurring subscription fees (ManyChat, Make.com, Zapier). | **100% Local-First**: Runs on local SQLite WAL, native Python, and self-hosted `reach` tunnels ($0/month SaaS cost). |

---

## 5. Phased Roadmap to OMNI Status

1. **Phase 1: Inbound Social Intelligence & Research Ingestion** (Weeks 1–2)
   - Wire `token_bounded_scrapling.py` and `research_engine.py` into `instaflow.discovery`.
   - Add arXiv API query bridge and Reddit search parser.
2. **Phase 2: 5-Persona Council Automated Decision Gate** (Weeks 2–3)
   - Implement programmatic Council evaluation pipeline returning structured Q-Scores (0.00 – 1.00).
   - Enforce automated rejection of tools with Q-Score < 0.80.
3. **Phase 3: AgentReach Remote Worker Integration** (Weeks 3–4)
   - Connect `reach` CLI bindings to dispatch headless browser and scraper containers on remote VPS/WSL.
4. **Phase 4: Multi-Surface Social Synthesis** (Weeks 4–5)
   - Expand discovery connectors beyond Instagram to X developer lists and Pinterest technical boards.
