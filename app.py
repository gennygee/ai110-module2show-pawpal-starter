import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- 1. INITIALIZE SESSION STATE ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", time_available=120)

st.subheader("Owner Details")
new_owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
new_time = st.number_input("Time Available (minutes)", min_value=10, max_value=720, value=st.session_state.owner.time_available)
if new_owner_name != st.session_state.owner.name:
    st.session_state.owner.name = new_owner_name
if new_time != st.session_state.owner.time_available:
    st.session_state.owner.update_time_available(new_time)

st.divider()

# --- 2. ADD PET SECTION ---
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name}!")

if st.session_state.owner.pets:
    st.write("**Current Pets:**")
    for p in st.session_state.owner.pets:
        st.write(f"- {p.name} ({p.species})")
else:
    st.info("No pests yet. Add one above.")

st.divider()

# --- 3. ADD TASK SECTION ---
st.subheader("Add a Task")
st.caption("Select a pet and assign it a care task.")

if not st.session_state.owner.pets:
    st.warning("Please add a pet first before adding tasks!")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Select Pet", pet_names)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_desc = st.text_input("Task Description", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"], index=0)
    
    if st.button("Add Task"):
        target_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        new_task = Task(description=task_desc, time=int(duration), priority=priority, frequency=frequency)
        target_pet.add_task(new_task)
        st.success(f"Added task '{task_desc}' for {target_pet.name}!")
        
    all_tasks = st.session_state.owner.get_all_pet_tasks()
    if all_tasks:
        st.write("**All Current Tasks:**")
        task_data = [{"Pet": p.name, "Task": t.description, "Time": t.time, "Priority": t.priority} 
                     for p in st.session_state.owner.pets for t in p.tasks]
        st.table(task_data)

st.divider()

# --- 4. GENERATE SCHEDULE ---
st.subheader("Build Today's Schedule")
st.caption("Calls the Scheduler logic to build a plan based on the owner's time constraints.")

if st.button("Generate Schedule"):
    if not st.session_state.owner.get_all_pet_tasks():
        st.warning("You must add at least one task before scheduling!")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)
        scheduler.generate_plan()
        
        st.markdown("### Your Plan")
        st.text(scheduler.get_plan_details())
