from pawpal_system import Owner, Pet, Scheduler, Task


def build_sample_schedule() -> Scheduler:
	owner = Owner("Jordan")

	mochi = Pet(name="Mochi", species="Dog", age=4)
	luna = Pet(name="Luna", species="Cat", age=2)

	mochi.add_task(Task(description="Morning walk", time="07:30", frequency="Daily"))
	mochi.add_task(Task(description="Dinner", time="18:00", frequency="Daily"))
	luna.add_task(Task(description="Brush fur", time="20:15", frequency="Weekly"))

	owner.add_pet(mochi)
	owner.add_pet(luna)

	return Scheduler(owner)


def print_todays_schedule(scheduler: Scheduler) -> None:
	print("Today's Schedule")
	print("-" * 40)

	for item in scheduler.organize_tasks():
		pet_name = item["pet"]
		task = item["task"]
		status = "Done" if task.completed else "Pending"
		print(f"{task.time} | {pet_name:<5} | {task.description} ({task.frequency}) - {status}")


if __name__ == "__main__":
	scheduler = build_sample_schedule()
	print_todays_schedule(scheduler)
