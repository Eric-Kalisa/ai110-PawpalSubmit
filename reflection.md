# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four main classes:
- `Owner`: stores owner name, available hours, and a list of pets; responsible for adding/removing pets and updating availability.
- `Pet`: stores pet name, species, age, owner reference, and a list of tasks; responsible for managing tasks and returning tasks sorted by priority.
- `Task`: stores title, duration, priority, category, and notes; responsible for serializing itself to a dictionary and validating its own data.
- `Scheduler`: owns an `Owner` and a `Pet`, and holds the built schedule and skipped tasks; responsible for scheduling flow with methods like `build_schedule()`, `prioritize()`, `fits_in_window()`, `explain()`, and `summary()`.

**b. Design changes**

- Did your design change during implementation? Yes 
- If yes, describe at least one change and why you made it.

# Priority enum should support ordering
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Add validation to Pet initialization
def __post_init__(self):
    if self not in self.owner.pets:
        self.owner.add_pet(self)

# Scheduler needs validation
def __post_init__(self):
    if self.pet not in self.owner.pets:
        raise ValueError("Pet must belong to the specified Owner")
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Enumeration of tasks; I initially thought this should be a list that should be appended by user input but as I read the prompt it was still unclear as to whether I should 
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
