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
    def __init__(self, owner: Owner):
        self.owner = owner
        self.daily_plan: List[Task] = []
        self.explanation: List[str] = []
        self.warnings: List[str] = []

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sorts tasks chronologically by their HH:MM target_time.
        """
        return sorted(tasks, key=lambda t: t.target_time)

    def generate_plan(self) -> None:
        """Retrieves and schedules pending tasks based on target_time and available time, while checking for conflicts."""
        pending_tasks = self.owner.get_pending_tasks()
        sorted_tasks = self.sort_by_time(pending_tasks)

        self.daily_plan = []
        self.explanation = []
        self.warnings = []
        time_left = self.owner.time_available

        def time_to_mins(t_str: str) -> int:
            h, m = t_str.split(':')
            return int(h) * 60 + int(m)

        for task in sorted_tasks:
            if time_left >= task.time:
                # Lightweight Conflict Detection
                task_start = time_to_mins(task.target_time)
                task_end = task_start + task.time
                
                conflict_found = False
                for scheduled_task in self.daily_plan:
                    sched_start = time_to_mins(scheduled_task.target_time)
                    sched_end = sched_start + scheduled_task.time
                    
                    # Logic: if task begins before the other ends, AND ends after the other begins, they overlap.
                    if task_start < sched_end and sched_start < task_end:
                        conflict_found = True
                        self.warnings.append(f"⚠️ WARNING: '{task.description}' ({task.target_time}) conflicts with '{scheduled_task.description}' ({scheduled_task.target_time})!")

                self.daily_plan.append(task)
                time_left -= task.time
                
                if conflict_found:
                    self.explanation.append(f"Scheduled '{task.description}' at {task.target_time} ({task.time}m) WITH CONFLICT. Time remaining: {time_left}m.")
                else:
                    self.explanation.append(f"Scheduled '{task.description}' at {task.target_time} ({task.time}m). Time remaining: {time_left}m.")
            else:
                self.explanation.append(f"Skipped '{task.description}' at {task.target_time} ({task.time}m) - Not enough time remaining (has {time_left}m).")

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
