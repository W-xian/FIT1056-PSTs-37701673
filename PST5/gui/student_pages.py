import streamlit as st


def _rows(people):
    return [{"ID": person.id, "Name": person.name, "Courses": ", ".join(str(course_id) for course_id in person.enrolled_course_ids)}
            for person in people]


def show_student_management_page(manager):
    """Display only the management function chosen by the user."""
    st.header("Student Management")
    action = st.selectbox(
        "Choose a function",
        ["List Students", "Find Student", "Register Student",
         "Update Student", "Remove Student"],
        key="student_action"
    )
    people = manager.students

    if action == "List Students":
        st.subheader("Student List")
        if people:
            st.dataframe(_rows(people), hide_index=True)
        else:
            st.info("No students registered.")

    elif action == "Find Student":
        st.subheader("Find a Student")
        search_by = st.radio("Search by", ["ID", "Name"],
                             horizontal=True, key="student_search_by")
        with st.form("student_search_form"):
            query = st.text_input("Enter " + search_by.lower())
            submitted = st.form_submit_button("Find Student")
        if submitted:
            query = query.strip()
            if not query:
                st.warning("Please enter an ID or name.")
            elif search_by == "ID" and not query.isdecimal():
                st.warning("Please enter a whole-number ID.")
            else:
                if search_by == "ID":
                    matches = [person for person in people if person.id == int(query)]
                else:
                    matches = [person for person in people
                               if query.casefold() in person.name.casefold()]
                if matches:
                    st.dataframe(_rows(matches), hide_index=True)
                else:
                    st.info("No matching student found.")

    elif action == "Register Student":
        st.subheader("Register New Student")
        with st.form("student_registration_form"):
            name = st.text_input("Student Name")
            detail = st.text_input("First Instrument")
            submitted = st.form_submit_button("Register Student")
        if submitted:
            if not name.strip() or not detail.strip():
                st.warning("Please enter both name and instrument.")
            else:
                student = manager.register_new_student(name.strip(), detail.strip())
                if student is None:
                    st.error("No course matches this instrument. Create a matching course first.")
                else:
                    st.success(f"Successfully registered {name.strip()}!")

    elif action == "Update Student":
        st.subheader("Update Student")
        if not people:
            st.info("No students available to update.")
            return
        person = st.selectbox(
            "Select Student to Update", people,
            format_func=lambda person: f"{person.id} - {person.name}",
            key="student_update_select"
        )
        with st.form(f"update_student_form_{person.id}"):
            name = st.text_input("Student Name", value=person.name)
            submitted = st.form_submit_button("Update Student")
        if submitted:
            if not name.strip():
                st.warning("Please enter a name.")
            else:
                manager.update_student(person.id, name=name.strip())
                st.success("Student updated successfully!")

    elif action == "Remove Student":
        st.subheader("Remove Student")
        if not people:
            st.info("No students available to remove.")
            return
        person = st.selectbox(
            "Select Student to Remove", people,
            format_func=lambda person: f"{person.id} - {person.name}",
            key="student_remove_select"
        )
        if st.button("Remove Student"):
            manager.remove_student(person.id)
            st.session_state["student_message"] = "Student removed successfully."
            st.rerun()

    if "student_message" in st.session_state:
        st.success(st.session_state.pop("student_message"))
