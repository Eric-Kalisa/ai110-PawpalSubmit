from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
	task = Task(description="Morning walk", time="07:30", frequency="Daily")

	task.mark_complete()

	assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
	pet = Pet(name="Mochi", species="Dog", age=4)
	task = Task(description="Dinner", time="18:00", frequency="Daily")

	starting_count = len(pet.tasks)
	pet.add_task(task)

	assert len(pet.tasks) == starting_count + 1
