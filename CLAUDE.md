# Insurance automation: rules for Claude

The discovery-to-prototype workflow from `product-workflow`, run as Claude Code skills in `.claude/commands/`, applied to internal AI tools for claims handlers.

## Naming
- **Fernway** is a made-up stand-in for the real company. Never use the real company's name, its people's names or other identifying details in this repo, in prototypes or on screens. All data is synthetic and labelled as synthetic on screen.
- The repo is public: no job-search or interview material goes here.

## Active context and run
- **Context folder:** `context/`
- **Run folder:** `runs/override-signal/`

## Base product
Fernway already runs an internal claims platform its handlers use every day, with AI automations that engineers build. Every prototype extends or changes that platform; it never designs a claims system from scratch. Where we don't know how the base product works, state the assumption in the run's `RUN.md` and keep the prototype easy to fit into it.

## Rules
- Company, product, customer and design facts come from the context skills (`pm-company-context-overview`, `pm-company-context-glossary`, `pm-company-context-personas`, `pm-company-context-design-system`), which read the context folder, then Notion via MCP, then ask me. Never from the model's memory
- Follow `pm-0-standard` for everything a reader sees
- Work only in the active run folder; read its `RUN.md` first. Nothing carries over between runs
- Every number is calculated by code and can be traced
- Skills hold general method only. Case details go in the run's `RUN.md`
- Don't change a skill unless I ask
- Key documents I review, annotate or share (discovery guide and notes, solution concept, MVP review) live in Notion under the parent page in `context/company.md`. Create the page and give me the link; don't summarise it in chat
- Unsure which run something belongs to: ask

## Workflow
| Step | Who | Skill | Output |
|---|---|---|---|
| 1. Data and context arrive | Claude | `pm-1-data-discovery` (Initial review) | Run folder, `RUN.md` with findings, questions and the ask word for word |
| 2. Discovery guide | Claude | `pm-2-discovery-interview` | Notion page |
| 3. Interview | me | | Notes in that page |
| 4. Research synthesis | Claude | `pm-1-data-discovery` (Answer) | Tested claims in `RUN.md` |
| 5. Spec: solution concept | Claude | `pm-3-problem-to-solution-concept` | Notion page |
| 6. Design | Claude | `pm-4-solution-design` | Screen specs and images in `design/` |
| 7. Prototype | Claude | `pm-5-mvp-build` | One HTML file, tests and a headless check in `build/` |
| 8. MVP review | me + Claude | `pm-6-mvp-review` | Notion page |

Show results in chat first and commit once per step.

## Setup
`pip install -q -r requirements.txt` · checks: `node build/test_mvp.js` and `node build/check_mvp.js` in a run folder (Playwright is pre-installed in cloud sessions)
