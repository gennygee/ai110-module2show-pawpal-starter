from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, timedelta

def test_task_completion():
    """Verify that calling mark_completed() changes the task's status."""
    task = Task(description="Testing", time=10, frequency="once")
    assert not task.completion_status, "Task should be incomplete initially."
    task.mark_completed()
    assert task.completion_status, "Task should be completed."

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Testing Pet", species="Dog")
    task = Task(description="Testing Task", time=10, frequency="daily")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1, "Pet should have 1 task after adding."

def test_sorting_correctness():
    """Verify tasks are returned in chronological order based on target_time."""
    owner = Owner(name="Test Owner", time_available=120)
    scheduler = Scheduler(owner=owner)
    
    t1 = Task(description="Dinner", time=10, frequency="daily", target_time="18:00")
    t2 = Task(description="Breakfast", time=10, frequency="daily", target_time="08:00")
    t3 = Task(description="Lunch", time=10, frequency="daily", target_time="12:00")
    
    # Sort them using our new algorithmic helper
    sorted_tasks = scheduler.sort_by_time([t1, t2, t3])
    
    assert sorted_tasks[0].description == "Breakfast", "08:00 should come first"
    assert sorted_tasks[1].description == "Lunch", "12:00 should come second"
    assert sorted_tasks[2].description == "Dinner", "18:00 should come last"

def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    task = Task(description="Daily Walk", time=30, frequency="daily", due_date=date.today())
    
    # Mark it completed, which functionally returns the rolled-over exact mathematical clone!
    new_task = task.mark_completed()
    
    assert new_task is not None, "A recurring task must successfully return a totally new instance upon completion."
    assert new_task.due_date == date.today() + timedelta(days=1), "The new task should be scheduled precisely 1 day in the future."
    assert new_task.completion_status is False, "The newly generated task should NOT be pre-completed."

def test_conflict_detection():
    """Verify that the Scheduler mathematically flags duplicate/overlapping interval times."""
    owner = Owner(name="Test Owner", time_available=120)
    pet = Pet(name="Doggo", species="Dog")
    owner.add_pet(pet)
    
    # Inject exact overlapping target_times
    t1 = Task(description="Walk 1", time=30, frequency="daily", target_time="10:00")
    t2 = Task(description="Walk 2", time=30, frequency="daily", target_time="10:00")
    
    pet.add_task(t1)
    pet.add_task(t2)
    
    scheduler = Scheduler(owner=owner)
    scheduler.generate_plan()
    
    # Verify the warning was successfully appended safely without crashing!
    assert len(scheduler.warnings) > 0, "Scheduler must have generated at least one warning for the overlap."
    assert "conflicts with" in scheduler.warnings[0], "The warning message should explicitly mention a math conflict."
