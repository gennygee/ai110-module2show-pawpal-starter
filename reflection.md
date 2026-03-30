# PawPal+ Project Reflection

## 1. System Design

**Core User Actions:**
1. Add a pet (and owner information).
2. Schedule a care task (e.g., walk, feeding, meds) with its duration and priority.
3. View today's tasks generated as a daily plan based on constraints.

**a. Initial design**

The system revolves around four main objects to manage a user's pet care schedule:

1. **Owner**
   - **Attributes**: `name` (string), `time_available` (integer, minutes per day), `pets` (list of Pet objects)
   - **Methods**: `add_pet(pet)`, `update_time_available(minutes)`
   - **Responsibility**: Holds the user's constraints and ties to their pets.

2. **Pet**
   - **Attributes**: `name` (string), `species` (string), `tasks` (list of Task objects)
   - **Methods**: `add_task(task)`, `remove_task(task)`, `get_tasks()`
   - **Responsibility**: Represents the pet requiring care and holds the master list of all individual care tasks.

3. **Task**
   - **Attributes**: `name` (string), `type` (string: walk, feeding, meds, grooming), `duration` (integer in minutes), `priority` (integer or string: high/med/low)
   - **Methods**: `update_duration(minutes)`, `update_priority(level)`
   - **Responsibility**: Represents a specific care action the pet needs.

4. **Scheduler**
   - **Attributes**: `owner` (Owner object), `pet` (Pet object), `daily_plan` (list of Task objects), `explanation` (string)
   - **Methods**: `generate_plan()`, `get_plan_details()`
   - **Responsibility**: Takes the owner's constraints (available time) and the pet's tasks (priorities, durations) to construct an actionable daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

Our scheduler mathematically checks for colliding task durations, but it intentionally makes the tradeoff to **soft-warn** the user about overlapping tasks rather than aggressively crashing the application or forcibly shifting the tasks to new timeslots itself. 

This tradeoff is entirely reasonable for this scenario because pet owners often natively multitask (e.g., taking the dog for a walk while technically simultaneously supervising the cat's "Play Time"). A complex conflict-resolving algorithm might over-engineer the process and artificially block the user. A lightweight warning gives the owner full control while keeping them safely informed!

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
