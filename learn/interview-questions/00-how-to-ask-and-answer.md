# How to Ask and Answer Interview Questions

Before diving into specific questions, learn the frameworks that make every answer stronger.

---

## Answering Behavioral Questions — The STAR Method

Structure every behavioral answer with **STAR**:

| Step | What to say | Time |
|------|-------------|------|
| **S**ituation | Set the scene — what was the project, team, or context? | 10–15 sec |
| **T**ask | What were you responsible for? What was the goal? | 10–15 sec |
| **A**ction | What did you specifically do? (Use "I", not "we") | 30–40 sec |
| **R**esult | What happened? Quantify if possible (saved X hours, reduced Y bugs). | 10–15 sec |

### Example

> **Q: Tell me about a time you fixed a difficult bug.**
>
> **S:** Our team's API was returning incorrect totals on the billing page. Customers were filing support tickets daily.
>
> **T:** I was assigned to investigate since I had built the original calculation logic.
>
> **A:** I added logging around the price computation pipeline, discovered a floating-point rounding error that compounded across line items, and replaced the float math with Python's `Decimal` type. I also wrote regression tests covering 15 edge cases.
>
> **R:** Support tickets for billing errors dropped to zero within a week, and the regression tests caught two similar bugs in later PRs before they shipped.

---

## Answering Technical Questions — Think Out Loud

Interviewers care as much about your _process_ as your answer. Use this structure:

1. **Restate** the question to confirm you understand it
2. **Clarify** — ask 1–2 questions about constraints or assumptions
3. **Plan** — describe your approach _before_ writing code
4. **Implement** — write clean code, narrating as you go
5. **Verify** — walk through an example input; mention edge cases
6. **Analyze** — state time and space complexity

### Phrases that help

| Situation | Say this |
|-----------|----------|
| Thinking | "Let me think about this for a moment..." |
| Stuck | "I'm not sure about X, but my instinct is Y because..." |
| Changing approach | "Actually, I think a better approach would be..." |
| Unsure of syntax | "I'd look this up in practice, but the idea is..." |
| Don't know | "I haven't worked with that, but my approach would be to..." |

---

## Asking Clarifying Questions

Good clarifying questions _before_ you solve show maturity. Here are examples by category:

### For coding problems
- "Can the input be empty or null?"
- "Are there duplicate values? How should I handle them?"
- "Is the input sorted?"
- "What should I return if there's no valid answer?"
- "Are we optimizing for time or space?"

### For system design
- "How many users are we designing for?"
- "What's the expected read-to-write ratio?"
- "Do we need real-time data or is eventual consistency okay?"
- "What's our latency target?"
- "Is this a greenfield system or are we extending something existing?"

### For behavioral
- "Would you like me to focus on a technical example or a team/leadership example?"
- "Should this be from a professional setting, or is a school project okay?"

---

## Questions to Ask Your Interviewer

Always have 2–3 ready. These show genuine interest and help you evaluate the company.

### About the team
- "What does a typical day look like for someone in this role?"
- "How is the team structured? Who would I be working with directly?"
- "What does the onboarding process look like for new engineers?"

### About the work
- "What's the biggest technical challenge the team is facing right now?"
- "How do you balance new features vs. technical debt?"
- "What does the deployment process look like?"

### About growth
- "How do you support engineers who want to learn new technologies?"
- "What does the path from junior to mid-level look like here?"
- "How is performance evaluated?"

### About culture
- "How does the team handle disagreements about technical decisions?"
- "What's one thing you'd change about working here?"
- "What do you personally enjoy most about this team?"

### Questions to avoid
- Anything easily found on the company website (shows you didn't research)
- Salary/benefits in the first technical round (save for recruiter)
- "Did I get the job?" (they can't answer this on the spot)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Rambling past 2 minutes | Practice with a timer. Set a hard limit. |
| Saying "we" for everything | Use "I" to describe your specific contribution |
| No concrete numbers | Add metrics: "reduced load time by 40%", "handled 10K requests/sec" |
| Memorizing scripts | Know your stories, but speak naturally — bullet points, not essays |
| Not asking questions | Always ask at least 2. Silence signals disinterest. |
| Apologizing for what you don't know | Frame gaps as growth areas: "I haven't used X yet, but I've been studying it" |

---

## Preparation Checklist

- [ ] Prepare 5 STAR stories covering: teamwork, conflict, failure, leadership, technical challenge
- [ ] Practice answering each out loud (not silently reading)
- [ ] Time yourself — behavioral answers under 90 sec, technical under 5 min
- [ ] Prepare 3 questions to ask your interviewer
- [ ] Research the company's tech stack, recent blog posts, and product
- [ ] Do at least 2 mock interviews before the real thing
