from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    owner = Owner(name="Genny", time_available=120)

    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Added conflicting tasks at 18:00
    t1 = Task(description="Evening Feed", time=10, frequency="daily", priority="high", target_time="18:00")
    t2 = Task(description="Evening Walk", time=45, frequency="daily", priority="high", target_time="18:00") # INTENTIONAL CONFLICT
    t3 = Task(description="Mid-day Grooming", time=30, frequency="weekly", priority="medium", target_time="13:00")
    t4 = Task(description="Late Night Play", time=20, frequency="daily", priority="low", target_time="21:00")
    
    dog.add_task(t1)
    dog.add_task(t2)
    cat.add_task(t3)
    cat.add_task(t4)
    
    # Generate schedule (Tests the new Conflict Detection logic natively building explanation warnings!)
    scheduler = Scheduler(owner=owner)
    scheduler.generate_plan()
    
    print("=" * 40)
    print(" 🐾 Today's PawPal+ Schedule (With Warnings!) 🐾")
    print("=" * 40)
    print(f"Owner: {owner.name} | Total Available Time: {owner.time_available} mins")
    print("-" * 40)
    print(scheduler.get_plan_details())
    print("=" * 40)

if __name__ == "__main__":
    main()
