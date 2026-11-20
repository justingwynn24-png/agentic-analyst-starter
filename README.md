# Agentic Analyst Starter

Three free Agent Skills for people who live in spreadsheets, recurring reports and decision memos. Written by a working analyst who runs multi-AI systems.

They work in any assistant that supports the open [Agent Skills](https://agentskills.io) standard, including Claude and Claude Code, ChatGPT and Codex, Gemini CLI, GitHub Copilot and Cursor.

| Skill | What it does |
|---|---|
| `data-qa` | Checks whether a file is safe to build on. Gives a profile, a ranked list of problems and a verdict: Ready, Ready with caveats, or Not ready. |
| `decision-memo` | Turns notes into a one-page memo with the bottom line first, three sourced facts, honest options and the exact ask with a date. |
| `meeting-prep` | Writes a one-page brief: what to know, your ask, likely questions with answers, and the numbers to have ready. |

## Install

Copy the folders in `skills/` to wherever your assistant looks for skills. For Claude Code:

```bash
git clone https://github.com/justingwynn24-png/agentic-analyst-starter.git
mkdir -p ~/.claude/skills
cp -r agentic-analyst-starter/skills/* ~/.claude/skills/
```

For other clients, see their skills documentation. Each skill is a plain folder with a `SKILL.md`.

## Try it in two minutes

Ask your assistant: *"Run data-qa on samples/sales-pipeline-sample.csv."*

The sample has planted problems: a duplicate account ID (`A00006`), a total row mixed in with the data, a blank amount and a 480,000 outlier. The skill should find all four and return **Not ready**. To check them yourself without an assistant, run the profiler. It uses only Python's standard library:

```bash
python3 skills/data-qa/scripts/profile_csv.py samples/sales-pipeline-sample.csv --key account_id
```

It lists the duplicate, the total row and the blank as problems, shows the outlier in the `amount_usd` profile row, and ends with `Not ready`. Without `--key` it skips the duplicate check.

## The full kit

The **[Agentic Analyst Kit](https://gwynnvoice.gumroad.com/l/agentic-analyst-kit)** adds seven more skills, plus playbooks, templates and sample data:

- variance analysis
- recurring reports
- chart audit
- model documentation
- forecast stress test
- request triage
- a data-handling guardrail

The playbooks cover the Monday morning run, month-end close, twelve prompt patterns and what not to paste. The kit costs $49 and includes free updates.

## License

MIT, see [LICENSE](LICENSE). The skills in this repository are free to use, change and share. The full kit is sold separately under its own license.

A product of Echoed Words LLC. It is not affiliated with or endorsed by Anthropic, OpenAI, Google, GitHub or any other assistant vendor. Product names appear only to say where the skills run.
