import streamlit as st
import pandas as pd

import streamlit as st


def show_course_management_page(manager):
    st.header("Course Management")

    action = st.selectbox(
        "Choose a function",
        [
            "List Courses",
            "Add Course",
            "Update Course",
            "Remove Course"
        ],
        key="course_action"
    )

    if "course_message" in st.session_state:
        st.success(st.session_state.pop("course_message"))

    # List courses
    if action == "List Courses":
        st.subheader("Course List")

        if not manager.courses:
            st.info("No courses available.")
            return

        teacher_names = {
            teacher.id: teacher.name
            for teacher in manager.teachers
        }

        course_data = []

        for course in manager.courses:
            teacher_name = teacher_names.get(
                course.teacher_id,
                "Teacher unavailable"
            )

            # Count students whose IDs still exist in the system.
            student_ids = {
                student.id for student in manager.students
            }

            enrolled_count = len(
                set(course.enrolled_student_ids) & student_ids
            )

            course_data.append({
                "ID": course.id,
                "Name": course.name,
                "Instrument": course.instrument,
                "Teacher ID": course.teacher_id,
                "Teacher Name": teacher_name,
                "Enrolled Students": enrolled_count
            })

        st.dataframe(course_data, hide_index=True)

    # Add a course
    elif action == "Add Course":
        st.subheader("Add Course")

        if not manager.teachers:
            st.info("Please register a teacher first.")
            return

        teacher_options = {
            teacher.id: f"{teacher.id} - {teacher.name}"
            for teacher in manager.teachers
        }

        with st.form("add_course_form"):
            name = st.text_input("Course Name")
            instrument = st.text_input("Instrument")

            teacher_id = st.selectbox(
                "Select Teacher",
                list(teacher_options),
                format_func=lambda teacher_id: teacher_options[teacher_id]
            )

            submitted = st.form_submit_button("Add Course")

        if submitted:
            if name.strip() and instrument.strip():
                manager.add_course(
                    name.strip(),
                    instrument.strip(),
                    teacher_id
                )

                st.session_state["course_message"] = (
                    "Course added successfully!"
                )
                st.rerun()

            else:
                st.warning(
                    "Please enter both course name and instrument."
                )

    # Update a course
    elif action == "Update Course":
        st.subheader("Update Course")

        if not manager.courses:
            st.info("No courses available to update.")
            return

        if not manager.teachers:
            st.info("Please register a teacher first.")
            return

        course_options = {
            course.id: course
            for course in manager.courses
        }

        course_id = st.selectbox(
            "Select Course to Update",
            list(course_options),
            format_func=lambda course_id: (
                f"{course_id} - {course_options[course_id].name}"
            ),
            key="update_course_select"
        )

        course = course_options[course_id]

        teacher_options = {
            teacher.id: f"{teacher.id} - {teacher.name}"
            for teacher in manager.teachers
        }

        teacher_ids = list(teacher_options)

        if course.teacher_id in teacher_ids:
            current_teacher_index = teacher_ids.index(
                course.teacher_id
            )
        else:
            current_teacher_index = None
            st.warning(
                "The assigned teacher is unavailable. "
                "Please select another teacher."
            )

        with st.form(f"update_course_form_{course.id}"):
            name = st.text_input(
                "Course Name",
                value=course.name
            )

            instrument = st.text_input(
                "Instrument",
                value=course.instrument
            )

            teacher_id = st.selectbox(
                "Select Teacher",
                teacher_ids,
                index=current_teacher_index,
                format_func=lambda teacher_id: teacher_options[teacher_id]
            )

            submitted = st.form_submit_button("Update Course")

        if submitted:
            if not name.strip() or not instrument.strip():
                st.warning(
                    "Please enter both course name and instrument."
                )

            elif teacher_id is None:
                st.warning("Please select a teacher.")

            else:
                manager.update_course(
                    course.id,
                    name=name.strip(),
                    instrument=instrument.strip(),
                    teacher_id=teacher_id
                )

                st.session_state["course_message"] = (
                    "Course updated successfully!"
                )
                st.rerun()

    # Remove a course
    elif action == "Remove Course":
        st.subheader("Remove Course")

        if not manager.courses:
            st.info("No courses available to remove.")
            return

        course_options = {
            course.id: course
            for course in manager.courses
        }

        course_id = st.selectbox(
            "Select Course to Remove",
            list(course_options),
            format_func=lambda course_id: (
                f"{course_id} - {course_options[course_id].name}"
            ),
            key="remove_course_select"
        )

        if st.button("Remove Course"):
            manager.remove_course(course_id)

            st.session_state["course_message"] = (
                "Course removed successfully!"
            )
            st.rerun()

    