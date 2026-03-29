from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    description: str  # The activity description
    time: int  # Duration in minutes
    frequency: str  # e.g., 'daily', 'twice daily'
    completion_status: bool = False
    priority: str = 'medium'  # 'high', 'medium', 'low'

    def mark_completed(self) -> None:
        """Marks the task as completed."""
        self.completion_status = True

    def update_time(self, minutes: int) -> None:
        """Updates the duration of the task."""
        self.time = minutes

    def update_priority(self, level: str) -> None:
        """Updates the priority level of the task."""
        self.priority = level


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a new task to the pet's list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Removes a task from the pet's list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Returns all tasks associated with the pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, time_available: int):
        """Initializes a new owner with a name and daily available time constraint."""
        self.name = name
        self.time_available = time_available  # total daily minutes available
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Registers a new pet under this owner."""
        self.pets.append(pet)

    def get_all_pet_tasks(self) -> List[Task]:
        """Collects all tasks from all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def update_time_available(self, minutes: int) -> None:
        """Updates the owner's daily available time constraint."""
        self.time_available = minutes


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.daily_plan: List[Task] = []
        self.explanation: List[str] = []

    def generate_plan(self) -> None:
        """Retrieves tasks from the owner and schedules based on priority and available time."""
        # The Scheduler "talks" to the Owner by calling `owner.get_all_pet_tasks()`
        all_tasks = self.owner.get_all_pet_tasks()
        
        # Filter incomplete tasks
        pending_tasks = [t for t in all_tasks if not t.completion_status]
        
        # Sort by priority (high > medium > low) and then by time duration
        priority_map = {"high": 3, "medium": 2, "low": 1}
        # Shorter tasks of equal priority get scheduled first safely
        sorted_tasks = sorted(pending_tasks, key=lambda t: (priority_map.get(t.priority.lower(), 0), -t.time), reverse=True)

        self.daily_plan = []
        self.explanation = []
        time_left = self.owner.time_available

        for task in sorted_tasks:
            if time_left >= task.time:
                self.daily_plan.append(task)
                time_left -= task.time
                self.explanation.append(f"Scheduled '{task.description}' ({task.time}m, Priority: {task.priority}). Time remaining: {time_left}m.")
            else:
                self.explanation.append(f"Skipped '{task.description}' ({task.time}m) - Not enough time remaining (has {time_left}m).")

    def get_plan_details(self) -> str:
        """Returns a formatted string of the generated daily plan and reasoning."""
        if not self.daily_plan and not self.explanation:
            return "No plan generated yet."
        
        details = "Daily Plan:\n"
        for task in self.daily_plan:
            details += f"- [ ] {task.description} ({task.time} mins, {task.priority} priority, {task.frequency})\n"
            
        details += "\nScheduler Reasoning:\n"
        for exp in self.explanation:
            details += f"- {exp}\n"
            
        return details
