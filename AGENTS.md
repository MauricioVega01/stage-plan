# Global development rules (Antigravity)

- Inspect the actual repository and current Git status before editing. Never assume a documented file exists.
- For multi-file changes, explain a short plan first and implement in small verifiable batches.
- Prefer minimal diffs and existing architecture over broad rewrites or new frameworks.
- Do not delete user data, run destructive commands, alter databases, install dependencies, publish repositories, deploy, or expose servers without explicit approval.
- Never print, copy to logs, commit, or transmit credentials, cookies, tokens, private user data or `.env` files.
- Do not run an internet-facing tunnel or bind a development server publicly without explicit approval.
- Validate real behavior after edits; distinguish tested facts from untested assumptions. Never claim tests passed without executing them.
- Preserve accessibility, error handling, performance, and backward compatibility.
- Report changed files, tests run, outstanding risks, and how to roll back.
- For non-trivial architectural flows, state machines, hardware communication (e.g. POS/Printers), or ticket workflows, provide clear Mermaid diagrams (`sequenceDiagram`, `flowchart TD`, `stateDiagram-v2`).
- When working on frontends or UI layouts, leverage local browser/DevTools tools or browser subagents to inspect rendering and prevent visual regressions.
- Respect workspace AGENTS.md and relevant skills; project rules add to these defaults.
