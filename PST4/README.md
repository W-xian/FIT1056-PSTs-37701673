# Music School Management System (MSMS)- PST4

## Overview

This project is a Music School Management System Developed using Python and Streamlit. The system provides a simple graphical user interface (GUI) that allows users to manage students, teachers, courses and daily lesson activities. Data is stored in JSON file so that changes can be saved and loaded again when the application is restarted.

## Features

### Student Management
- Choose one function at a time 
- List all students include ID, name and enrolled course IDs
- Find students by ID or student name
- register a new student
- Update student information
- Remove a student

### Teacher Management
- Choose one function at a time 
- List all teachers include ID, name and speciality
- Find teachers by ID or student name
- Add a new teacher
- Update teacher name and speciality
- Remove a teacher

### Course Management 
- Add a new course
- Assign a teacher to the course
- Update a course
- view course

### Daily Roster
- Select a weekday to view scheduled lessons
- Display lesson information in a table
- Check students into their enrolled courses

## Assumptions
- A teacher must already exist before a course can be created.
- A student is registered into a course by matching the selected instrument with an existing course
- Student check-in is only valid when the student is enrolled in the selected course.
- The application uses the existing JSON file as the persistent data source,
- Course IDs should continue from the highest existing course ID rather than reusing IDs from deleted courses.

## Known Limitation
- Removing a student does not currently remove all references to that student from related course data.
- Removing a teacher does not automatically remove or reassign courses that reference that teacher.
- The application assumes the JSON file contains valid references between students, teachers and courses.
- The Daily Roster only displays lessons that already exist in the course lesson data.

## How to Run

1. Open the terminal and navigate to the PST4 folder
2. Make sure Streamlit and pandas are installed.
3. Run the application using:

```bash
streamlit run main.py
```
