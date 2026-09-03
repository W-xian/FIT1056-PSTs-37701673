# Music School Management System (MSMS)

### Overview

This project is an object-oriented Music School Management System (MSMS) for managing students, teachers, courses, attendance, and lesson schedules.
The system stores data in a JSON file so that information can persist between program runs.

## Requirements
-python 3.x

## Data models
### Student Class
- Stores student ID 
- Stores student name
- Stores enrolled instruments

### Teacher Class
- Stores teacher ID
- Stores teacher name
- stores speciality

### Course Class

- Stores course ID
- Stores course name
- Stores instrument
- Stores teacher ID
- Stores enrolled student IDs
- Stores lesson information

## Project Structure

- `main.py` - Handles the menu and user input.
- `app/user.py` - Contains the base User class.
- `app/student.py` - Contains the StudentUser class.
- `app/teacher.py` - Contains the TeacherUser and Course classes.
- `app/schedule.py` - Contains the ScheduleManager and application logic.
- `data/msms.json` - Stores persistent application data.

## Menu Options 
1. Add Student
2. Add teacher
3. Add course
4. List student
5. List teacher
6. Student check-in
7. view dialy roaster
8. Switch Course
9. Update student
10. Update teacher
11. remove student
12. remove teacher
Q. Quit

## How to Run
1. Open terminal
2. Navigate to the PST3 folder
3. Run the program
3. Run the program:

```bash
python3 main.py