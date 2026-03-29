from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner
    owner = Owner(name="Genny", time_available=90)  # 1.5 hours available

    # 2. Create at least two Pets
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # 3. Add at least three Tasks with different times
    walk_task = Task(description="Morning Walk", time=45, frequency="daily", priority="high")
    feed_dog_task = Task(description="Feed Buddy", time=10, frequency="daily", priority="high")
    play_cat_task = Task(description="Laser Pointer Play", time=20, frequency="daily", priority="medium")
    brush_cat_task = Task(description="Brushing", time=30, frequency="weekly", priority="low")
    
    dog.add_task(walk_task)
    dog.add_task(feed_dog_task)
    cat.add_task(play_cat_task)
    cat.add_task(brush_cat_task)
    
    # 4. Initialize Scheduler and generate plan
    scheduler = Scheduler(owner=owner)
    scheduler.generate_plan()
    
    # 5. Print out the formatted schedule to the terminal
    print("=" * 40)
    print(" 🐾 Today's PawPal+ Schedule 🐾")
    print("=" * 40)
    print(f"Owner: {owner.name} | Total Available Time: {owner.time_available} mins")
    print("-" * 40)
    print(scheduler.get_plan_details())
    print("=" * 40)

if __name__ == "__main__":
    main()
