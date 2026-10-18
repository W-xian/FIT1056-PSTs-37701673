# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    lessons = manager.get_lessons_by_day(day)

    if lessons:
        df = pd.DataFrame(lessons)
        st.dataframe(df, use_container_width="stretch")
    else:
        st.info(f"No lessons scheduled for {day}.")
    
    # --- Student Check-in Section (now works correctly) ---
    st.subheader("Student Check-in")

    if manager.students and manager.courses:

        student_list = {
            f"{s.id} - {s.name}": s.id
            for s in manager.students
        }

        course_list = {
            f"{c.id} - {c.name}": c.id
            for c in manager.courses
        }

    with st.form("check_in_form"):

        student_list = {
           f"{s.id} - {s.name}": s.id
           for s in manager.students
       }

        course_list = {
           f"{c.id} - {c.name}": c.id
           for c in manager.courses
       }

        selected_student_name = st.selectbox(
           "Select Student",
           student_list.keys()
       )

        selected_course_name = st.selectbox(
           "Select Course",
            course_list.keys()
       )

        submitted = st.form_submit_button(
           "Check-in Student"
       )

        if submitted:
           # Convert the selected names back to IDs
           student_id = student_list[selected_student_name]
           course_id = course_list[selected_course_name]

           # This call now works because we implemented the method in PST3.
           success = manager.check_in(student_id, course_id)

           if success:
              st.success(f"Checked in {selected_student_name} for {selected_course_name}!")
           else:
               # The manager's print statements will go to the console, but we can add a GUI error too.
               st.error("Check-in failed. See console for details. (Is the student enrolled in that course?)")

        else:
   
            st.info("Please make sure there is a atleast one student and one course before check in")