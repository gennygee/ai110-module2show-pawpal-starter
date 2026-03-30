import streamlit as st
import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 Smart PawPal+ Scheduler")

# --- 1. INITIALIZE SESSION STATE ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", time_available=120)

st.subheader("Owner Details")
col_o1, col_o2 = st.columns(2)
with col_o1:
    new_owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
with col_o2:
    new_time = st.number_input("Time Available (minutes)", min_value=10, max_value=720, value=st.session_state.owner.time_available)

if new_owner_name != st.session_state.owner.name:
    st.session_state.owner.name = new_owner_name
if new_time != st.session_state.owner.time_available:
    st.session_state.owner.update_time_available(new_time)

st.divider()

# --- 2. ADD PET SECTION ---
st.subheader("Add a Pet")
pet_col1, pet_col2, pet_col3 = st.columns([2, 2, 1])
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with pet_col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with pet_col3:
    st.write("")
    st.write("")
    if st.button("Add Pet", use_container_width=True):
        new_pet = Pet(name=pet_name, species=species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet: {pet_name}!")

if st.session_state.owner.pets:
    st.write("**Current Pets:**")
    for p in st.session_state.owner.pets:
        st.caption(f"🐶 **{p.name}** ({p.species.title()})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- 3. ADD TASK SECTION ---
st.subheader("Add a Task")
if not st.session_state.owner.pets:
    st.warning("Please add a pet first before adding tasks!")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign to Pet:", pet_names)
    
    col1, col2 = st.columns(2)
    with col1:
        task_desc = st.text_input("Task Description", value="Morning walk")
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        target_input = st.time_input("Target Time", value=datetime.time(8, 0))
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)
        st.write("")
        if st.button("Add Task", use_container_width=True):
            target_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
            time_str = target_input.strftime("%H:%M")
            new_task = Task(description=task_desc, time=int(duration), priority=priority, frequency=frequency, target_time=time_str)
            target_pet.add_task(new_task)
            st.success(f"Added task '{task_desc}' for {target_pet.name} at {time_str}!")
        
    all_tasks = st.session_state.owner.get_all_pet_tasks()
    if all_tasks:
        st.write("---")
        st.write("**All Current Tasks Database:**")
        task_data = [{"Pet": p.name, "Time": t.target_time, "Task": t.description, "Duration": f"{t.time}m", "Priority": t.priority, "Completed": "✅" if t.completion_status else "❌"} 
                     for p in st.session_state.owner.pets for t in p.tasks]
        st.dataframe(task_data, use_container_width=True)

st.divider()

# --- 4. GENERATE SMART SCHEDULE ---
st.subheader("📅 Build Today's Smart Schedule")
st.caption("Calls the Scheduler logic to build a plan mathematically factoring in durations & overlapping timeslots.")

if st.button("Generate Optimal Schedule!", type="primary"):
    if not st.session_state.owner.get_pending_tasks():
        st.warning("You must add at least one pending task today before scheduling!")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)
        scheduler.generate_plan()
        
        st.markdown("### Your Sorted Daily Plan")
        
        # ⚠️ WARNING LOGIC - High Visibility UI Rule!
        if scheduler.warnings:
            st.error("⚠️ Math Conflict Warning Detected!")
            for w in scheduler.warnings:
                st.warning(w)
                
        if scheduler.daily_plan:
            plan_data = [{"Time": t.target_time, "Task": t.description, "Duration": f"{t.time}m", "Priority": t.priority} for t in scheduler.daily_plan]
            st.table(plan_data)
            st.success("Schedule generated securely!")
        else:
            st.info("No tasks could securely fit in the allotted time constraints.")
            
        with st.expander("View Underlying Scheduler Reasoning"):
            for exp in scheduler.explanation:
                st.caption(f"- {exp}")
