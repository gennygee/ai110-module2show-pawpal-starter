from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling mark_completed() changes the task's status."""
    task = Task(description="Testing", time=10, frequency="daily")
    assert not task.completion_status, "Task should be incomplete initially."
    
    task.mark_completed()
    
    assert task.completion_status, "Task should be completed after mark_completed() is called."

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Testing Pet", species="Dog")
    task = Task(description="Testing Task", time=10, frequency="daily")
    
    assert len(pet.get_tasks()) == 0, "New pet should have 0 tasks."
    
    pet.add_task(task)
    
    assert len(pet.get_tasks()) == 1, "Pet should have 1 task after adding."
    assert pet.get_tasks()[0] == task, "The added task should be in the pet's task list."
