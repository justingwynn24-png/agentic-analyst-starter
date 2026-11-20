---
name: meeting-prep
description: Builds a one-page prep brief for a meeting from the agenda, prior notes, open items, and whatever numbers the analyst is likely to be asked for. For each agenda item: what to know, the user's position or ask, likely questions with answers, and the numbers to have ready. Use when the user says "I have a meeting", "prep me", "what should I know before", "they're going to ask about", or pastes an agenda or an invite.
license: MIT. See LICENSE in the repository root.
metadata:
  author: Echoed Words LLC
  kit: agentic-analyst-kit
  version: "1.0"
---

# Meeting prep

You write the page the analyst reads in the five minutes before the meeting. It is not minutes and not a summary of the documents; it is what to say, what will be asked, and the numbers to have at hand.

## Inputs

- The agenda or invite (required). If there is no agenda, ask for the purpose in one line and build from that.
- Prior notes or minutes, if any.
- The analyst's open items: what they owe others and what others owe them.
- Any report, memo, or dataset that will be discussed.
- The analyst's goal for the meeting, in one sentence. If they have not said, ask: "What do you want to walk out with?"

## Steps

1. **State the purpose of the meeting** as the analyst should understand it: a decision, an update, a negotiation, or a status check. Name what the analyst wants to leave with.
2. **For each agenda item**, write:
   - What to know: three bullets at most, each a fact with a number or a date.
   - Your position or ask: one line. If the analyst has no stake in the item, write "listen; no ask".
   - Likely questions and the answers: two or three, in the voice the analyst would use.
   - Numbers to have ready: the exact figures, with their source and as-of date.
3. **Open items**: a two-column list, "I owe" and "I am owed", each with the person and the date promised. Anything overdue goes first.
4. **Risks in the room**: anything likely to come up that is not on the agenda, and the one-line answer.
5. **After the meeting**: three blank lines for decisions, actions, and the next date, so the brief becomes the record.

Use `assets/prep-brief-template.md`.

## Rules

- One page. If it runs long, cut the "what to know" bullets before the questions and answers.
- Every number carries a source and an as-of date; a number the analyst cannot defend should not be in the brief.
- Write answers the analyst can say aloud, in plain words, not in document voice.
- Do not invent what other attendees think. Where their position is unknown, say "position unknown; ask early".
- If a document to be discussed contains a number that contradicts another document, flag it at the top; that is the question that will be asked.

## Example excerpt

> **2. Q3 obligations status**
> - Obligated $4.21M of $5.60M (75.2%) as of Sept 30; plan was 78% (source: status report, Oct 2).
> - The gap is two contracts awaiting award, $162K, expected mid-October.
> - **Ask:** confirm the award dates so the Q4 pacing memo can go out Friday.
> - *Likely question:* "Are we going to lapse?" *Answer:* "No. With the two awards we are at 78% and the Q4 pipeline covers the rest; the risk is the fleet order, not the total."
