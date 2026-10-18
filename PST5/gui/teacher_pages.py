import streamlit as st


def _rows(people):
    return [{"ID": person.id, "Name": person.name, "Speciality": person.speciality}
            for person in people]


def show_teacher_management_page(manager):
    """Display only the management function chosen by the user."""
    st.header("Teacher Management")
    action = st.selectbox(
        "Choose a function",
        ["List Teachers", "Find Teacher", "Register Teacher",
         "Update Teacher", "Remove Teacher"],
        key="teacher_action"
    )
    people = manager.teachers

    if action == "List Teachers":
        st.subheader("Teacher List")
        if people:
            st.dataframe(_rows(people), hide_index=True)
        else:
            st.info("No teachers registered.")

    elif action == "Find Teacher":
        st.subheader("Find a Teacher")
        search_by = st.radio("Search by", ["ID", "Name"],
                             horizontal=True, key="teacher_search_by")
        with st.form("teacher_search_form"):
            query = st.text_input("Enter " + search_by.lower())
            submitted = st.form_submit_button("Find Teacher")
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
                    st.info("No matching teacher found.")

    elif action == "Register Teacher":
        st.subheader("Register New Teacher")
        with st.form("teacher_registration_form"):
            name = st.text_input("Teacher Name")
            detail = st.text_input("Speciality")
            submitted = st.form_submit_button("Register Teacher")
        if submitted:
            if not name.strip() or not detail.strip():
                st.warning("Please enter both name and speciality.")
            else:
                manager.add_teacher(name.strip(), detail.strip())
                st.success(f"Successfully registered {name.strip()}!")

    elif action == "Update Teacher":
        st.subheader("Update Teacher")
        if not people:
            st.info("No teachers available to update.")
            return
        person = st.selectbox(
            "Select Teacher to Update", people,
            format_func=lambda person: f"{person.id} - {person.name}",
            key="teacher_update_select"
        )
        with st.form(f"update_teacher_form_{person.id}"):
            name = st.text_input("Teacher Name", value=person.name)
            speciality = st.text_input("Speciality", value=person.speciality)
            submitted = st.form_submit_button("Update Teacher")
        if submitted:
            if not name.strip() or not speciality.strip():
                st.warning("Please enter both name and speciality.")
            else:
                manager.update_teacher(person.id, name=name.strip(), speciality=speciality.strip())
                st.success("Teacher updated successfully!")

    elif action == "Remove Teacher":
        st.subheader("Remove Teacher")
        if not people:
            st.info("No teachers available to remove.")
            return
        person = st.selectbox(
            "Select Teacher to Remove", people,
            format_func=lambda person: f"{person.id} - {person.name}",
            key="teacher_remove_select"
        )
        if st.button("Remove Teacher"):
            manager.remove_teacher(person.id)
            st.session_state["teacher_message"] = "Teacher removed successfully."
            st.rerun()

    if "teacher_message" in st.session_state:
        st.success(st.session_state.pop("teacher_message"))
