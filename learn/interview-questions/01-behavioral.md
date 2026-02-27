# Behavioral Interview Questions

These appear in nearly every interview. Prepare a real story for each category using the [STAR method](00-how-to-ask-and-answer.md).

---

## About You

1. **Tell me about yourself.**
   _Keep it to 60 seconds. Cover: background → what you're working on now → why you're excited about this role._

2. **Why do you want this role?**
   _Connect your skills/interests to something specific about the company or team._

3. **Where do you see yourself in 2–3 years?**
   _Show ambition tied to growth in engineering, not just titles._

4. **What are your greatest strengths as a developer?**
   _Pick 2. Back each with a brief example._

5. **What's an area you're actively improving?**
   _Be honest, then explain what you're doing about it. "I'm working on X by doing Y."_

---

## Problem-Solving & Technical Thinking

6. **Tell me about the hardest technical problem you've solved.**
   _Walk through the problem, your debugging process, and the resolution._

7. **Describe a bug you found and how you tracked down the root cause.**
   _Emphasize your methodology: logs, tests, bisecting, reproducing._

8. **Tell me about a time you had to learn a new technology quickly.**
   _Show how you learn: docs, tutorials, building something small, asking for help._

9. **What do you do when you're completely stuck on a problem?**
   _Good answers: break it down, rubber-duck, search docs, ask a teammate, take a walk._

10. **Describe a time you made a mistake in your code. What happened?**
    _Show ownership, how you fixed it, and what you put in place to prevent it._

---

## Teamwork & Communication

11. **Tell me about a project where you worked with others.**
    _Focus on your specific role, how you coordinated, and what the team achieved._

12. **How do you handle disagreements about technical decisions?**
    _Show willingness to listen, use data/evidence, and commit once decided._

13. **Describe a time you gave or received constructive feedback.**
    _Show you can give feedback kindly and receive it without defensiveness._

14. **How do you handle code review comments you disagree with?**
    _Discuss, don't argue. Explain your reasoning, but be willing to learn._

15. **Tell me about a time you helped a teammate who was struggling.**
    _Shows empathy and team orientation._

---

## Work Style & Prioritization

16. **How do you prioritize when you have multiple deadlines?**
    _Talk about urgency vs. importance, communicating with stakeholders._

17. **Describe a time you had to balance quality with speed.**
    _Show judgment: when is "good enough" okay, when is thoroughness critical?_

18. **How do you stay organized when working on a large project?**
    _Tools, processes, breaking work into milestones._

19. **Tell me about a time you had to work with unclear requirements.**
    _Show you ask questions, make assumptions explicit, and iterate._

20. **What does a productive workday look like for you?**
    _Shows self-awareness about your own focus patterns._

---

## Motivation & Culture Fit

21. **Why should we hire you?**
    _Match your specific skills/traits to their specific needs. Be concrete._

22. **What kind of engineering culture do you thrive in?**
    _Be honest — this helps both sides evaluate fit._

23. **What's a side project or personal project you're proud of?**
    _Shows initiative and genuine interest in building things._

24. **How do you keep up with new technologies?**
    _Blogs, conferences, open source, courses, building things._

25. **What would your previous teammates or classmates say about you?**
    _Pick a genuine trait. Bonus if you can quote actual feedback._

---

## Tough / Curveball Questions

26. **Tell me about a time you failed.**
    _Show vulnerability, what you learned, and how you changed your approach._

27. **If you had two competing offers, how would you decide?**
    _Reveals what you actually value — growth, team, mission, technology._

28. **What's something you believe about software that most people disagree with?**
    _Tests independent thinking. Have a real opinion you can defend._

29. **There's only one position available. Why are you the best candidate?**
    _Don't put others down. Focus on what makes your combination of skills unique._

30. **Is there anything you'd like to ask us?**
    _Always say yes. See [Questions to Ask Your Interviewer](00-how-to-ask-and-answer.md#questions-to-ask-your-interviewer)._

---

## Practice Routine

- Pick 2 questions from different sections each day
- Answer out loud using STAR (set a 90-second timer)
- Record yourself once a week and listen back
- Track which stories you've used so you have variety across interviews

---

## Model Answers

Below are fully worked-through examples so you can see what a strong behavioral answer sounds like. Use these as templates, but always substitute your own real stories.

### Model Answer: "Tell me about yourself" (#1)

> "I'm a computer science student at [University] graduating this spring. Over the past two years, I've focused on full-stack development — I built a study session tracker as a personal project where I used Python and Flask for the backend and React for the frontend. Last summer, I interned at [Company] where I worked on their internal tooling team, building dashboards that helped the support team reduce ticket resolution time by 20%. I'm excited about this role because I love building tools that make people's workflows faster, and your team's focus on developer experience really resonates with me."

**Why this works:** It follows the past → present → future arc, includes a concrete metric (20% faster), and connects to the specific role.

### Model Answer: "Tell me about the hardest technical problem you've solved" (#6)

> **Situation:** During my internship, our team's CI pipeline started timing out randomly — builds that normally took 8 minutes were taking 45+ minutes, and sometimes failing entirely. Nobody could figure out why because the failures weren't consistent.
>
> **Task:** My manager asked me to investigate since I had the lightest sprint load that week. I needed to find the root cause and fix it without disrupting the team's deployments.
>
> **Action:** I started by collecting data — I pulled the last 30 days of build logs and plotted timing. I noticed the slow builds correlated with certain test files running. I dug into those tests and found one integration test was making real HTTP calls to a third-party API that had recently added rate limiting. When we hit the rate limit, the test would retry with exponential backoff, sometimes waiting minutes. I mocked the external API call in the test environment and added a network-isolation check to our CI config so no test could ever make real external calls.
>
> **Result:** Build times went back to a consistent 7-8 minutes. My manager was impressed enough to have me present the debugging process at our team retro, and the network-isolation pattern got adopted across three other teams' CI configs.

**Why this works:** Uses STAR structure clearly. Shows a methodical debugging approach (data collection → hypothesis → isolation → fix). The result has both a direct outcome and a broader impact.

### Model Answer: "How do you handle disagreements about technical decisions?" (#12)

> "In a group project last semester, my teammate wanted to use MongoDB for our e-commerce app, and I felt PostgreSQL was a better fit because we had highly relational data — users, orders, products, and reviews all linked together. Instead of just arguing my preference, I made a quick comparison doc: I listed the three most complex queries we'd need to support and showed how each would look in both databases. The relational version was dramatically simpler. My teammate actually agreed once they saw the concrete comparison, and we went with PostgreSQL. I learned that showing rather than telling is much more effective in technical disagreements — and that I should always be prepared to change my own mind if the evidence goes the other way."
