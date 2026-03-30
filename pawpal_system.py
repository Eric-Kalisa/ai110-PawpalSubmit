from __future__ import annotations
"""Core domain models and scheduling helpers for the PawPal app."""

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Any, Dict, List, Optional


def _parse_task_time(value: str) -> time:
    """Parse a task time string into a time object.

    Accepts 24-hour format (HH:MM) and 12-hour format (H:MM AM/PM).
    """
    for fmt in ("%H:%M", "%I:%M %p"):
        try:
            return datetime.strptime(value.strip(), fmt).time()
        except ValueError:
            continue
    raise ValueError("Task time must use HH:MM or H:MM AM/PM format.")


@dataclass
class Task:
    """Represents one pet-care activity with schedule and completion state."""

    description: str
    time: str
    frequency: str
    completed: bool = False

    def __post_init__(self) -> None:
        """Run validation after object creation."""
        self.validate()

    def validate(self) -> None:
        """Validate required task fields and time format."""
        if not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        _parse_task_time(self.time)
        if not self.frequency.strip():
            raise ValueError("Task frequency cannot be empty.")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Reset this task to incomplete status."""
        self.completed = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary view of the task."""
        return {
            "description": self.description,
            "time": self.time,
            "frequency": self.frequency,
            "completed": self.completed,
        }


@dataclass
class Pet:
    """Stores pet profile data and its list of care tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task if it is not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task if it exists in the list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks not yet completed."""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return only tasks already completed."""
        return [task for task in self.tasks if task.completed]


@dataclass
class Owner:
    """Represents a pet owner and the pets under their care."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet if it is not already linked to this owner."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet if it is currently linked to this owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Return tasks for all pets as pet-task pairs."""
        all_tasks: List[Dict[str, Any]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append({"pet": pet.name, "task": task})
        return all_tasks


@dataclass
class Scheduler:
    """Central task manager that retrieves and organizes tasks across pets."""

    owner: Owner

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Return all tasks owned by this scheduler's owner."""
        return self.owner.get_all_tasks()

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks for one pet by name."""
        pet = self._find_pet(pet_name)
        return pet.get_tasks() if pet else []

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Return only incomplete tasks across all pets."""
        return [item for item in self.get_all_tasks() if not item["task"].completed]

    def get_completed_tasks(self) -> List[Dict[str, Any]]:
        """Return only completed tasks across all pets."""
        return [item for item in self.get_all_tasks() if item["task"].completed]

    def organize_tasks(self, completed_first: bool = False) -> List[Dict[str, Any]]:
        """Sort tasks by completion grouping, then time, pet name, and description."""
        return sorted(
            self.get_all_tasks(),
            key=lambda item: (
                0 if item["task"].completed == completed_first else 1,
                _parse_task_time(item["task"].time),
                item["pet"].lower(),
                item["task"].description.lower(),
            ),
        )

    def get_tasks_by_frequency(self, frequency: str) -> List[Dict[str, Any]]:
        """Return tasks matching a frequency label, case-insensitively."""
        target_frequency = frequency.strip().lower()
        return [
            item
            for item in self.get_all_tasks()
            if item["task"].frequency.strip().lower() == target_frequency
        ]

    def mark_task_complete(self, pet_name: str, description: str) -> bool:
        """Mark a matching task complete and return True on success."""
        task = self._find_task(pet_name, description)
        if task is None:
            return False
        task.mark_complete()
        return True

    def mark_task_incomplete(self, pet_name: str, description: str) -> bool:
        """Mark a matching task incomplete and return True on success."""
        task = self._find_task(pet_name, description)
        if task is None:
            return False
        task.mark_incomplete()
        return True

    def summary(self) -> Dict[str, int]:
        """Return aggregate counts for pets and task statuses."""
        all_tasks = self.get_all_tasks()
        return {
            "pets": len(self.owner.pets),
            "tasks": len(all_tasks),
            "completed": sum(1 for item in all_tasks if item["task"].completed),
            "pending": sum(1 for item in all_tasks if not item["task"].completed),
        }

    def _find_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name, case-insensitively."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.strip().lower():
                return pet
        return None

    def _find_task(self, pet_name: str, description: str) -> Optional[Task]:
        """Find a task by pet and description, case-insensitively."""
        pet = self._find_pet(pet_name)
        if pet is None:
            return None
        for task in pet.tasks:
            if task.description.lower() == description.strip().lower():
                return task
        return None
