from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta

@dataclass
class Task:
    description: str  # The activity description
    time: int  # Duration in minutes
    frequency: str  # e.g., 'daily', 'weekly', 'once'
    completion_status: bool = False
    priority: str = 'medium'  # 'high', 'medium', 'low'
    target_time: str = "12:00"  # Format: "HH:MM"
    due_date: date = field(default_factory=date.today)

    def mark_completed(self) -> Optional['Task']:
        """Marks the task as completed. If it's recurring, returns a newly generated Task for the next date."""
        self.completion_status = True
        
        if self.frequency.lower() == 'daily':
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                priority=self.priority,
                target_time=self.target_time,
                due_date=self.due_date + timedelta(days=1)
            )
        elif self.frequency.lower() == 'weekly':
            return Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                priority=self.priority,
                target_time=self.target_time,
                due_date=self.due_date + timedelta(days=7)
            )
        return None

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
    name: str
    time_available: int
    pets: List[Pet]

    def __init__(self, name: str, time_available: int):
        """Initializes a new owner with a name and daily available time constraint."""
        self.name = name
        self.time_available = time_available  # total daily minutes available
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        """Registers a new pet under this owner."""
        self.pets.append(pet)

    def get_all_pet_tasks(self) -> List[Task]:
        """Collects all tasks from all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_pending_tasks(self) -> List[Task]:
        """Filters all tasks, returning only the pending ones for today or earlier."""
        # Note: In a fully-fleshed app, we seamlessly filter by `due_date <= date.today()` so future rollovers stay hidden until tomorrow!
        return [t for t in self.get_all_pet_tasks() if not t.completion_status and t.due_date <= date.today()]
        
    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Filters and returns tasks specifically belonging to one pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def update_time_available(self, minutes: int) -> None:
        """Updates the owner's daily available time constraint."""
        self.time_available = minutes


class Scheduler:
    owner: Owner
    daily_plan: List[Task]
    explanation: List[str]
    warnings: List[str]

    def __init__(self, owner: Owner):
        self.owner = owner
        self.daily_plan = []
        self.explanation = []
        self.warnings = []

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sorts tasks chronologically by their HH:MM target_time.
        """
        return sorted(tasks, key=lambda t: t.target_time)

    def generate_plan(self) -> None:
        """Retrieves and schedules pending tasks based on priority weights, target_time, and available time, while reliably checking for conflicts."""
        pending_tasks = self.owner.get_pending_tasks()
        
        # 1. Advanced Algorithm: Weighted Prioritization!
        priority_map = {"high": 3, "medium": 2, "low": 1}
        # Sort tasks strictly by priority descending, then chronologically inside that priority
        priority_sorted_tasks = sorted(pending_tasks, key=lambda t: (-priority_map.get(t.priority.lower(), 1), t.target_time))

        self.daily_plan = []
        self.explanation = []
        self.warnings = []
        time_left: int = int(self.owner.time_available)

        def time_to_mins(t_str: str) -> int:
            h, m = t_str.split(':')
            return int(h) * 60 + int(m)

        # 2. Select tasks explicitly honoring the priority sorting to securely lock most important slots first
        accepted_tasks = []
        for task in priority_sorted_tasks:
            if time_left >= task.time:
                accepted_tasks.append(task)
                time_left -= task.time
                self.explanation.append(f"Accepted '{task.description}' ({task.priority.upper()} priority). Time remaining: {time_left}m.")
            else:
                self.explanation.append(f"Rejected '{task.description}' - Insufficient time ({time_left}m < {task.time}m).")

        # 3. Final structural processing: safely sort ONLY the successfully accepted tasks strictly chronologically!
        self.daily_plan = self.sort_by_time(accepted_tasks)

        # 4. Conflict Detection mathematically computed safely explicitly over the final sorted chronological daily_plan subset
        for i, task in enumerate(self.daily_plan):
            task_start = time_to_mins(task.target_time)
            task_end = task_start + task.time
            for j in range(i + 1, len(self.daily_plan)):
                scheduled_task = self.daily_plan[j]
                sched_start = time_to_mins(scheduled_task.target_time)
                sched_end = sched_start + scheduled_task.time
                
                # Check absolute math interval overlapping exactly:
                if task_start < sched_end and sched_start < task_end:
                    warning_str = f"⚠️ WARNING: '{task.description}' ({task.target_time}) conflicts with '{scheduled_task.description}' ({scheduled_task.target_time})!"
                    if warning_str not in self.warnings:
                        self.warnings.append(warning_str)

    def get_plan_details(self) -> str:
        """Returns a formatted string of the generated daily plan and reasoning/warnings."""
        if not self.daily_plan and not self.explanation:
            return "No plan generated yet."
        
        details = "Daily Plan:\n"
        for task in self.daily_plan:
            details += f"- [ ] {task.target_time} | {task.description} ({task.time} mins)\n"
            
        if self.warnings:
            details += "\nSchedule Warnings:\n"
            for w in self.warnings:
                details += f"{w}\n"
            
        details += "\nScheduler Reasoning:\n"
        for exp in self.explanation:
            details += f"- {exp}\n"
            
        return details
