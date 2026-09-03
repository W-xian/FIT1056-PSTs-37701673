# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons = manager.get_lessons_by_day(day)
    for lesson in lessons:
        print(f"Course: {lesson['course_name']}")
        print(f"Instrument: {lesson['instrument']}")
        print(f"Teacher ID: {lesson['teacher_id']}")
        print(f"Lesson ID: {lesson['lesson_id']}")
        print(f"Start Time: {lesson['start_time']}")
        print(f"Room: {lesson['room']}")
        print()

def switch_course(manager, student_id, from_course_id, to_course_id):
    student = manager.find_student_by_id(student_id)
    from_course = manager.find_course_by_id(from_course_id)
    to_course = manager.find_course_by_id(to_course_id)

    if not student or not from_course or not to_course:
        print("Error:Invalid student or course ID.")
        return False 

    if from_course_id in student.enrolled_course_ids:
        student.enrolled_course_ids.remove(from_course_id)

    if student_id in from_course.enrolled_student_ids:
        from_course.enrolled_student_ids.remove(student_id)

    if to_course_id not in student.enrolled_course_ids:
        student.enrolled_course_ids.append(to_course_id)

    if student_id not in to_course.enrolled_student_ids:
        to_course.enrolled_student_ids.append(student_id)

    manager._save_data()
    print("course switched successfully.")
    return True

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager()
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1.  Add Student")
        print("2.  Add teacher")
        print("3.  Add Course")
        print("4.  List student")
        print("5.  List teacher")
        print("6.  Student check-in")
        print("7.  View daily roster")
        print("8.  Switch course")
        print("9.  update student")
        print("10. update teacher")
        print("11. remove student")
        print("12. remove teacher")
        print("Q. Quit")

        choice = input("Enter choice: ")
        if choice == '1':
            name = (input("Enter student name: "))
        
            manager.add_student(name)

        elif choice == '2':
            name = input("Enter teacher name: ")
            speciality = input("Enter speciality: ")

            manager.add_teacher(name,speciality)

        elif choice == '3':
            name = input("Enter course name: ")
            instrument = input("Enter new instrument: ")

            try:
                 teacher_id = int(input("Enter the teacher_id: "))

            except ValueError:
                  print("Sorry, please enter a number.")
                  continue

            manager.add_course(name,instrument,teacher_id)

        elif choice == '4':
            manager.list_students()

        elif choice == '5':
            manager.list_teachers()

        elif choice == '6':
            try:
                  student_id = int(input("Enter student ID: "))
                  course_id = int(input("Enter course ID: "))
            except ValueError:
                  print("Sorry, please enter a number.")
                  continue

        elif choice == '7':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)


        elif choice == '8':
            student_id = int(input("Enter student ID: "))
            from_course_id = int(input("Enter current course ID: "))
            to_course_id = int(input("Enter new course ID: "))

            switch_course(manager, student_id,from_course_id,to_course_id)

        elif choice == '9':
            student_id = int(input("Enter student ID: "))
            field = input("What do you want to update? ")
            new_value = input ("Enter new value: ")
            
            manager.update_student(student_id,**{field: new_value})

        elif choice == '10':
            teacher_id = int(input("Enter teacher ID: "))
            field = input("What do you want to update? ")
            new_value = input ("Enter new value: ")
                    
            manager.update_student(teacher_id,**{field: new_value})

        elif choice == '11':
            student_id = int(input("Enter student ID: "))

            manager.remove_student(student_id)

        elif choice == '12':
            teacher_id = int(input("Enter teacher ID: "))
        
            manager.remove_teacher(teacher_id)
        
        elif choice.lower() == 'q':
            break
        
if __name__ == "__main__":
    main()