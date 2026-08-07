# Music School Management System (MSMS)

## Overview
This project is a simple in-memory prototype for a music school front desk system.

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

## Data Storage 
- student_db stores Student objects.
- teacher_db stores Teacher objects

The data is store in memory and reset when program exits by user


## Front Desk Functions
1. front_desk_register(name, instrument)
- register a new student and enrols them

2. front_desk enrol(student_id, instrument)
- Enrols an existing student.

3. front_desk enrol(term)
- searches both stuents and teachers.

## Menu Options 
1. Register New Student 
2. Enrol Existing Student
3. Lookup Student or Teacher
4. List All Students
5. List All Teachers
Q. Quit

## How to Run
1. Open terminal
2. Navigate to the PST1 folder
3. Run the program








