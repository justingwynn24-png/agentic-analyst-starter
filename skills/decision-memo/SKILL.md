---
name: decision-memo
description: Turns analysis, notes, or a messy draft into a one-page decision memo in BLUF form (bottom line up front): the recommendation, the three facts that carry it, the options considered with their trade-offs, the risks, and the exact ask with a date and a decider. Use when the user needs to brief a manager, a board, or a committee, says "write this up", "I need a memo", "make the case", or has to get a yes or no from someone.
license: MIT. See LICENSE in the repository root.
metadata:
  author: Echoed Words LLC
  kit: agentic-analyst-kit
  version: "1.0"
---

# Decision memo

You write a memo that a busy decider can act on after reading the first three lines. One page. The structure is fixed (`assets/bluf-memo-template.md`); the judgment is in what you leave out.

## Steps

1. **Find the decision.** State in one sentence what the reader is being asked to decide, by when, and what happens if they do not decide. If the material does not contain a decision, say so and ask the user what they want the reader to do. A memo without an ask is a report; do not write one by accident.
2. **Write the bottom line first.** One or two sentences: the recommendation and the single strongest reason. No background before it.
3. **Pick the three facts that carry the recommendation.** Each fact is a number or a dated event with its source. If you have ten facts, choose three and move the rest to the appendix. If you have fewer than three hard facts, say the recommendation rests on judgment and name the judgment.
4. **Lay out the options honestly.** Two to four, including "do nothing" when it is real. For each: cost, benefit, main risk, in one line each. The recommended option should win on the facts in step 3, not on adjectives.
5. **Name the risks of the recommendation itself** and what would be done about each. A memo that lists only the risks of the alternatives reads as advocacy and loses trust.
6. **Write the ask.** Who decides, what exactly they are approving (amount, scope, dates), by what date, and what the author needs from them beyond the yes (a signature, a message to a team, a budget line).
7. **Appendix.** Sources, the full option comparison, assumptions, and the calculation behind any number in the body.

## Rules

- No adjective without a number beside it. "Significant savings" becomes "$42,000 a year, 6% of the line."
- Every number in the body traces to a source in the appendix.
- Write for the reader's level: a department head needs the decision and the dollars; a board needs the decision, the dollars, and the risk; a technical reviewer needs the appendix.
- Keep it to one page. If it does not fit, the options section is the first thing to cut, then the risks, never the bottom line or the ask.
- Do not soften the recommendation to seem balanced. Balance lives in the options and risks sections.
- If the user's draft argues for something the facts do not support, say so before writing, and offer the memo the facts do support.

## Example opening

> **Bottom line.** Renew the data platform contract for one year at $184,000, not three years at $498,000. The one-year term costs $18,000 more per year but keeps the option to move to the shared enterprise platform in FY27, which is expected to cut this line by 60%.
>
> **Decision needed from** the Deputy Director **by** November 15, because the current contract lapses December 31 and procurement needs 30 days.
