from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    name: str
    type: str  # e.g., 'walk', 'feeding', 'meds', 'grooming'
    duration: int  # in minutes
    priority: str  # 'high', 'medium', 'low'

    def update_duration(self, minutes: int) -> None:
        pass

    def update_priority(self, level: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str, time_available: int):
        self.name = name
        self.time_available = time_available
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_time_available(self, minutes: int) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.daily_plan: List[Task] = []
        self.explanation: str = ""

    def generate_plan(self) -> None:
        pass

    def get_plan_details(self) -> str:
        pass
