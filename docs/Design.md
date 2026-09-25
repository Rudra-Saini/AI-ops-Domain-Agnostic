# UI / UX Design Guidelines

## 1. Dual-Mode Interface Concept
The web application (`apps/web`) serves two unified user interfaces switchable via the top navigation bar:
1. **Customer Megastore (`/?mode=customer`)**: Realistic modern shopping experience for Indian electronics.
2. **SRE Developer Cockpit (`/?mode=cockpit`)**: Dark-mode operational command center for system telemetry and AI self-healing.

---

## 2. Design System & Theming
* **Framework**: TailwindCSS with Lucide-React icons.
* **Palette**:
  * Cockpit Background: Deep slate (`#0B0F19`) and card slate (`#111827`).
  * Telemetry Accents: Neon Emerald (`#10B981`) for healthy, Amber (`#F59E0B`) for degraded, Rose (`#EF4444`) for critical/incident.
  * AI Indicator: Purple/Indigo gradient (`#6366F1` $\rightarrow$ `#A855F7`) representing GenAI / LangChain intelligence.

---

## 3. SRE Developer Cockpit Components
* **Microservice Topology Graph**: Visual node status for `API`, `AI Worker`, `Worker`, `Postgres`, `Redis`.
* **Streaming Log Terminal**: Millisecond-timestamped logs color-coded by severity (INFO, WARN, ERROR, CRITICAL).
* **Chaos Engineering Control Panel**: Quick-trigger buttons for inducing specific production crashes.
* **AI Diagnosis Modal**: Displays LLM-generated root cause, confidence rating (e.g. 96%), and unified syntax-highlighted code diff.
* **1-Click Self-Healing Action**: Green action button executing AST-verified hotpatching to restore service health in < 3 seconds.
