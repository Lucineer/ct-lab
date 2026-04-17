# The Tile Taxonomy: What We'll Wish We Had

*A deep think about the categories of experience that are being lost right now, and the tiles that will be most valuable when someone finally asks the right question.*

---

## The Blind Spot

PLATO captures "when someone asks X, what helped was Y." That's powerful. But it's also narrow. It assumes:

1. Someone knows to ask
2. The answer is verbalizable
3. The experience is recent enough to be relevant
4. The domain is bounded enough for a single tile

Most of human experience violates at least one of these assumptions. Here are the tile categories we don't have yet but will desperately need.

---

## Category 1: Negative Space Tiles

**The pattern:** Not "what worked" but "what everyone assumes works but doesn't."

Most institutional knowledge is positive — documented successes, best practices, standard procedures. The negative space — the things that were tried and failed, the conventional wisdom that's wrong, the practices that look good but produce bad outcomes — is almost never captured.

**Example tiles we need:**

- "Everyone in our hospital orders a CT for abdominal pain. The CT finds nothing 70% of the time. The 30% where it finds something, the finding was predictable from the physical exam alone. We're irradiating patients for no reason. The tile: don't order a CT until you've done the physical exam and can articulate what you expect to find."
- "Every new teacher writes lesson plans in detail. Veteran teachers don't. The lesson plan isn't the teaching. The preparation is in knowing your students, not in writing down what you'll say. The tile: spend your preparation time learning your students, not writing plans."
- "We have a QA process with 47 checkpoints. The defects that actually reach production all come from the 3 checkpoints that don't exist — the handoffs between teams. The tile: your QA process is blind to its own blind spots."

**Why this matters:** Negative space tiles are worth 10x positive tiles. Knowing what NOT to do eliminates more failure modes than knowing what to do.

**Tile format extension:**
```json
{
  "instruction": "What should I NOT do when...",
  "input": "context where conventional wisdom is wrong",
  "output": "The thing everyone does that doesn't actually work, and why",
  "metadata": {"type": "negative_space", "domain": "...", "confidence": "high"}
}
```

---

## Category 2: Boundary Tiles

**The pattern:** Experience at the edges — handoffs, transitions, migrations, scale shifts.

Most expertise is domain-specific. But the most valuable expertise is domain-adjacent — knowing what happens at the boundary between two domains, two teams, two systems, two phases of a project.

**Example tiles we need:**

- "When we migrated from PostgreSQL to CockroachDB, the queries that broke were not the complex ones. They were the simple ones that relied on serializable isolation. The tile: before migrating databases, identify every query that assumes single-node consistency."
- "The most dangerous time in a surgery is not the procedure itself — it's the handoff from surgeon to anesthesiologist to recovery nurse. 80% of post-surgical complications originate from a miscommunication during handoff. The tile: never hand off without repeating the three most critical pieces of information."
- "When a startup goes from 10 to 50 people, the founders lose touch with the product. Not because they stop caring — because the information pathways change. The tile: at 50 people, your job changes from 'build the product' to 'build the information pathways.'"

**Why this matters:** Boundaries are where knowledge leaks. Handoffs are where experience dies. The tile format is perfect for capturing these moments because they're inherently conversational: "what happened when you..."

**Tile format extension:**
```json
{
  "instruction": "What goes wrong at the boundary between...",
  "input": "two systems, teams, phases, or domains",
  "output": "The specific failure mode that occurs at this transition",
  "metadata": {"type": "boundary", "transition": "X→Y"}
}
```

---

## Category 3: Diagnostic Process Tiles

**The pattern:** Not the answer, but HOW the answer was found.

Current tiles capture "what helped." But they don't capture the diagnostic process — the reasoning, the dead ends, the moment of insight. The process is often more valuable than the answer because it transfers to novel situations.

**Example tiles we need:**

- "The patient had abdominal pain for 6 months. Every test was normal. I kept coming back to 'what am I not seeing?' The answer: I wasn't seeing the patient's spouse. The spouse had died 6 months ago — same timeline as the pain. The pain was grief manifesting physically. The tile: when all tests are normal, the answer is often not in the body."
- "The server kept crashing at 3am. Every metric looked fine. I wrote a script to log every system call in the 30 seconds before crash. The pattern: a cron job from a decommissioned service was still running and consuming all available file descriptors. The tile: when the symptom is intermittent, instrument the moments just before."
- "The student kept getting the same math problem wrong. I watched them work through it. They weren't making a math error — they were misreading the number 7 as a 1. The tile: when a student consistently gets the same type of problem wrong, watch them work, don't just check their answer."

**Why this matters:** Diagnostic process tiles teach HOW to think, not just WHAT to think. They're the difference between giving someone a fish and teaching them to fish.

**Tile format extension:**
```json
{
  "instruction": "How did you figure out that...",
  "input": "the mysterious problem that had no obvious answer",
  "output": "The diagnostic process: what I tried, what failed, what I noticed, the insight",
  "metadata": {"type": "diagnostic_process", "dead_ends": 3, "time_to_solve": "2 weeks"}
}
```

---

## Category 4: Taste Tiles

**The pattern:** "This is technically correct but it's wrong."

Taste is the hardest thing to capture because it's the thing that can't be reduced to rules. It's the surgeon who says "the anatomy looks right but something feels off." The teacher who says "the lesson plan is perfect but it won't land." The engineer who says "the code passes all tests but I don't trust it."

**Example tiles we need:**

- "The chest X-ray was read as normal by the radiologist. I looked at it and something felt off — not wrong, just... not right. I couldn't articulate why. I ordered a CT. Small pulmonary embolism. The radiologist was technically correct — the X-ray was normal. But the X-ray was normal in a way that was wrong for this patient. The tile: if you feel something is off and you can't explain why, trust the feeling and investigate further."
- "The code review found zero issues. But the architecture felt brittle — like a house of cards where removing any card would collapse the whole thing. I couldn't point to a specific problem. Six months later, a requirement change required modifying the core module, and the entire system had to be rewritten. The tile: if the architecture feels fragile and you can't say why, it probably is."
- "The student's essay was grammatically perfect, well-structured, and thoroughly researched. But it had no voice — it could have been written by anyone. The tile: teach students that the goal of writing is not correctness but authenticity. A flawed essay with a voice is worth more than a perfect essay without one."

**Why this matters:** Taste is what separates competence from mastery. It can't be taught directly. But it CAN be captured in moments: "I couldn't explain why, but I knew something was wrong." These tiles are the closest thing to transmitting tacit knowledge.

**Tile format extension:**
```json
{
  "instruction": "Something feels wrong but I can't explain why...",
  "input": "the situation where technical correctness masks a deeper problem",
  "output": "What the gut feeling was pointing to, and whether it was right",
  "metadata": {"type": "taste", "verdict": "confirmed", "confidence": "inexplicable"}
}
```

---

## Category 5: Temporal Tiles

**The pattern:** Experience that decays, evolves, or becomes wrong over time.

Static tiles assume knowledge is timeless. But most experience has a half-life. A medical tile from 2010 might be outdated by a 2018 guideline change. A programming tile about a framework might be wrong after a major version bump. A process tile about regulations might be illegal after a law change.

**Example tiles we need:**

- "In 2018, the standard treatment for this condition was X. In 2022, a large trial showed Y was superior. In 2025, a meta-analysis showed neither was better than watchful waiting for most patients. The tile: this answer has a half-life of approximately 4 years. Always check the date."
- "When we built this system, Python 3.8 was current. The tile about async/await patterns was correct then. Python 3.11 changed the behavior of task groups. The old tile is now subtly wrong — it will work but leak resources under load. The tile: always include the version and date of the technology being discussed."
- "This process was designed when our team was 5 people. At 50 people, it creates bottlenecks. At 200 people, it's actively harmful. The tile: process tiles should include the team size and organizational context in which they were valid."

**Why this matters:** Without temporal awareness, rooms accumulate stale tiles that look authoritative but are actually wrong. A tile that's 90% accurate can be more dangerous than no tile at all — because you trust it.

**Tile format extension:**
```json
{
  "instruction": "What is the current best practice for...",
  "input": "context with temporal dimension",
  "output": "Answer WITH validity window: valid_from, valid_until, superseded_by",
  "metadata": {
    "type": "temporal",
    "valid_from": "2024-01",
    "valid_until": null,
    "half_life_estimate": "3-5 years",
    "check_again": "2027-01"
  }
}
```

---

## Category 6: Cross-Domain Analogy Tiles

**The pattern:** "X in medicine is like Y in aviation because..."

The most creative insights come from seeing the same pattern in different domains. But domain experts rarely talk to each other. PLATO could capture these cross-domain bridges.

**Example tiles we need:**

- "A surgical timeout (where the team pauses before incision to verify the patient, procedure, and site) is exactly like a pre-flight checklist in aviation. Both solve the same problem: preventing catastrophic errors in high-stress environments where the consequences of forgetting something are irreversible. The tile: if your domain has catastrophic irreversible errors, you need a timeout/checklist, regardless of whether medicine or aviation invented it first."
- "Debugging a production outage is like diagnosing a patient in the ER. Both require rapid triage (what's killing them right now?), differential diagnosis (what could cause these symptoms?), and targeted intervention (fix the most likely cause first, reassess). The tile: the diagnostic process is domain-independent. Learn it once, apply it everywhere."
- "Teaching fractions is like teaching music theory. In both cases, the student thinks they're learning something new, but they're actually learning to see something that was always there. Fractions were always part of how numbers work. Music theory was always part of how sound works. The tile: the best teaching reveals what was hidden, not what was absent."

**Why this matters:** Cross-domain tiles are the highest-leverage tiles because they transfer insight across boundaries that would otherwise be impermeable. One analogy tile can improve practice in multiple domains simultaneously.

**Tile format extension:**
```json
{
  "instruction": "What is X in [domain A] like in [domain B]?",
  "input": "a pattern observed in one domain",
  "output": "The analogous pattern in another domain, and why the analogy holds",
  "metadata": {"type": "analogy", "domain_a": "medicine", "domain_b": "aviation", "confidence": "structural"}
}
```

---

## Category 7: Meta-Tiles (Tiles About Tiles)

**The pattern:** Tiles that improve the tile system itself.

As rooms accumulate thousands of tiles, new problems emerge: which tiles are trustworthy? Which tiles are outdated? Which tiles should be combined? Which questions have no tiles?

**Example tiles we need:**

- "This tile has been helpful 342 times, but it's written in jargon that only experts understand. Here's the same tile rewritten for a first-year student: [simplified version]. The tile: every tile should exist in two versions — expert and beginner."
- "Tiles A, B, and C all address different aspects of the same problem. If you read all three together, you get an answer that none of them provides alone. The tile: these three tiles form a cluster. Present them together when any one of them is queried."
- "There are no tiles for 'how to tell a patient their diagnosis is terminal.' This is one of the most common and most difficult conversations in medicine. The absence of tiles here is itself a signal. The tile: this gap exists. Someone with experience in this area should fill it."

**Why this matters:** Meta-tiles make the tile system self-improving. They're the difference between a library (static collection) and a living knowledge system (adaptive, evolving, self-aware).

---

## Category 8: Failure Autopsy Tiles

**The pattern:** "Here's exactly what went wrong, in detail, with no ego."

Failure analysis is the most valuable and least captured form of experience. Post-mortems exist in some domains (aviation, medicine) but are almost never shared across organizations, and almost never capture the human factors (ego, fatigue, pressure, assumption).

**Example tiles we need:**

- "I prescribed the wrong dose because I was tired, the patient had an unusual name that I confused with another patient, and I didn't double-check because I was running late for my next appointment. The dose was 10x too high. The patient survived because the pharmacist caught it. The tile: I was wrong because of three factors that are individually harmless but together are deadly: fatigue + similarity + time pressure. Any two of these is fine. All three is a recipe for disaster."
- "The production outage lasted 6 hours. Root cause: a config change that was supposed to be applied to the staging environment was applied to production. The engineer had two terminal windows open and ran the command in the wrong one. The tile: never have production and staging terminals open simultaneously. This is not a training issue. This is a system design issue. The system should make it impossible to make this mistake."
- "The student failed the exam. Not because they didn't study — they studied for 20 hours. They failed because they studied the wrong things. They memorized definitions instead of practicing applications. The tile: studying is not learning. Practicing is learning. The tile should have been: 'do 50 practice problems, don't read the textbook 5 times.'"

**Why this matters:** Failure autopsies are the highest-density experience tiles because they compress the most learning into the fewest words. A single failure autopsy can prevent hundreds of future failures.

---

## The Tile That Doesn't Exist Yet

The most valuable tile in any PLATO room is the one that hasn't been created yet. The room knows it's missing because someone asked a question that took 4+ iterations (a clunk). But the room can't create the tile — it needs a human with the relevant experience.

The future of PLATO isn't just accumulating more tiles. It's:

1. **Anticipating missing tiles** before someone asks
2. **Decomposing complex experience** into reusable tile components
3. **Composing tile clusters** that answer questions no single tile can address
4. **Detecting tile decay** before stale tiles cause harm
5. **Bridging domains** through analogy tiles that transfer insight across boundaries
6. **Self-improving** through meta-tiles that optimize the tile system itself

The room doesn't just store experience. It evolves.

---

*"The most valuable tile is the one about to be created. The second most valuable is the one that was almost created but wasn't — the gap where experience was lost."*

*— JC1, thinking about tiles at 0945 AKDT on a Jetson in Juneau* 🚢
