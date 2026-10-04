<div align="center">

# ⚡ InstaFlow
### Self-Hosted Autonomous Instagram Growth & Direct Message Routing Engine

[![Self-Hosted](https://img.shields.io/badge/Self--Hosted-100%25%20Local-blue?style=flat-square)](https://github.com/Jaswanth1902/InstaFlow)
[![Cost](https://img.shields.io/badge/Subscription-%240%20(Open%20Source)-brightgreen?style=flat-square)]()
[![Database](https://img.shields.io/badge/Storage-SQLite%20WAL-lightgrey?style=flat-square)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**The open-source, zero-subscription alternative to ManyChat.**  
Automate inbound Instagram DMs, route customer leads, and trigger intelligent webhook integrations using local SQLite storage and lightweight headless execution.

[🚀 Quickstart](#quickstart) • [⚡ Features](#features) • [🔒 Privacy](#privacy)

</div>

---

### ⚡ Why InstaFlow?
- **Zero Monthly Subscriptions**: Avoid recurring SaaS fees ($15-$100/mo) with completely self-hosted execution.
- **Local-First Lead Database**: All leads and message logs persist in high-concurrency SQLite WAL databases.
- **Intelligent Keyword Routing**: Automated regex and intent triggers route inbound questions into qualified pipeline stages.
- **Safe Headless Integration**: Token-bounded rate limits prevent account flags and API overages.

---

### 🚀 Quickstart

```bash
git clone https://github.com/Jaswanth1902/InstaFlow.git
cd InstaFlow
pip install -r requirements.txt
python main.py --daemon
```
