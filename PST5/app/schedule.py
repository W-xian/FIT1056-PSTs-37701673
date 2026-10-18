import json
import datetime
import csv
import logging

from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path

        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.finance_log = []

        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 1
        self.next_lesson_id = 1

        self._load_data()


    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        
                for s in data.get("students", []):
                    student = StudentUser(s["id"],s["name"])
                    student.enrolled_course_ids = s.get("enrolled_course_ids" , [])
                    self.students.append(student)

                for t in data.get("teachers",[]):
                    teacher =TeacherUser(t["id"], t["name"],t["speciality"])
                    self.teachers.append(teacher)

                for c in data.get("courses",[]):
                    course = Course(
                        c["id"],
                        c["name"],
                        c["instrument"],
                        c["teacher_id"]
                        )
                    course.enrolled_student_ids = c.get("enrolled_student_ids",[])
                    course.lessons = c.get("lessons",[])
                
                    self.courses.append(course)
                    
                self.attendance_log = data.get("attendance", [])
                self.finance_log = data.get("finance_log", [])

                self.next_student_id = data.get("next_student_id", 1)
                self.next_teacher_id = data.get("next_teacher_id", 1)

                self.next_lesson_id = data.get(
                    "next_lesson_id",
                    max(
                        (
                            lesson["lesson_id"]
                            for course in self.courses
                            for lesson in course.lessons
                            ),
                            default=0
                            ) + 1
                        )
                
                if self.courses:
                    self.next_course_id = max(course.id for course in self.courses) + 1
                else:
                    self.next_course_id = 1

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,
            "finance_log": self.finance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id,
            "next_lesson_id": self.next_lesson_id
        }
        # TODO: Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def get_lessons_by_day(self, day):
        lessons_for_day = []
        for course in self.courses:
            for lesson in course.lessons:

                if lesson["day"].lower() == day.lower():
                    lessons_for_day.append({
                    "course_name": course.name,
                    "instrument": course.instrument,
                    "teacher_id": course.teacher_id,
                    "lesson_id": lesson["lesson_id"],
                    "start_time": lesson["start_time"],
                    "room": lesson["room"]
                })
        return lessons_for_day
    
    def cancel_lesson(self, lesson_id, reason):
        """Cancels a lesson by its ID and records the reason."""

        for course in self.courses:
            for lesson in course.lessons:
                if lesson["lesson_id"] == lesson_id:
                    course.lessons.remove(lesson)
                    self._save_data()

                    logging.warning(
                        "Lesson ID %s was cancelled. Reason: %s",
                        lesson_id,
                        reason
                    )

                    print(f"Lesson {lesson_id} cancelled successfully.")
                    return True

        logging.warning(
            "Lesson cancellation failed: lesson_id=%s not found",
            lesson_id
        )
        print(f"Error: Lesson {lesson_id} not found.")
        return False
    
    def add_student(self, name, course_id):
        course = self.find_course_by_id(course_id)

        if not course:
            print("Error: Course not found.")
            return
        
        student_id = self.next_student_id
        new_student = StudentUser(student_id, name)

        new_student.enrolled_course_ids.append(course_id)
        course.enrolled_student_ids.append(student_id)

        self.students.append(new_student)
        self.next_student_id += 1

        self._save_data()

        print(
            f"Student '{name}' added with ID {student_id}"
            f" and enrolled in '{course.name}'."
        )

    def register_new_student(self, name, instrument):
        """Registers a new student into a course matching the instrument."""

        logging.info(
             "Registering new student: name=%s, instrument=%s",
             name,
             instrument
             )

        matching_course = None

        for course in self.courses:
            if course.instrument.lower() == instrument.lower():
                matching_course = course
                break

        if matching_course is None:
            logging.warning(
                "Student registration failed: no course for instrument=%s",
                instrument
                )
            return None

        student_id = self.next_student_id
        new_student = StudentUser(student_id, name)

        new_student.enrolled_course_ids.append(matching_course.id)
        matching_course.enrolled_student_ids.append(student_id)

        self.students.append(new_student)
        self.next_student_id += 1

        self._save_data()

        logging.info(
            "Student registered successfully: student_id=%s, name=%s",
            student_id,
            name
            )
        return new_student

    def add_teacher(self, name, speciality):
        teacher_id = self.next_teacher_id
        new_teacher = TeacherUser(teacher_id, name, speciality)
        self.teachers.append(new_teacher)
        self.next_teacher_id += 1
        self._save_data()
        print(f"Core: Teacher '{name}' added successfully with ID {teacher_id}. ")

    def add_course(self, name, instrument, teacher_id):
        teacher = None 

        for t in self.teachers:
            if t.id == teacher_id:
                teacher = t 
                break
        if not teacher:
            print("Error: Teacher not found.")
            return
        
        course_id =self.next_course_id
        new_course = Course(course_id, name ,instrument, teacher_id)
        self.courses.append(new_course)
        self.next_course_id += 1
        self._save_data()
        print(f"Course '{name}' added successfully with ID {course_id}.")


    def update_course(self, course_id, **fields):
        for course in self.courses:
            if course.id == course_id:
                for key, value in fields.items():
                    setattr(course, key, value)

                self._save_data()
                print(f"Course {course_id} updated.")
                return

        print(f"Error: Course with ID {course_id} is not found.")


    def remove_course(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                # Remove this course from every enrolled student's records
                for student in self.students:
                    if course_id in student.enrolled_course_ids:
                        student.enrolled_course_ids.remove(course_id)
                        
                        
                self.courses.remove(course)
                self._save_data()
                
                print(f"Course {course_id} removed.")
                return True
            
            
        print(f"Error: Course with ID {course_id} is not found.")
        return False

    def list_students(self):
        print("\n--- Student List ---")
        if not self.students:
            print("No students in the system.")
            return
    
        for student in self.students:
            print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_course_ids}")

    def list_teachers(self):
        print("\n--- Teacher List ---")
        if not self.teachers:
            print("No teacher in the system.")
            return
            
        for teacher in self.teachers:
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

    def update_student (self,student_id, **fields):
        for student in self.students:
            if student.id == student_id:
                for key,value in fields.items():
                    setattr(student,key,value)

                self._save_data()
                print(f" Student {student_id} updated.")
                return
        
        print(f"Error: Student with ID {student_id} is not found.")

    def update_teacher(self, teacher_id, **fields):
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                for key,value in fields.items():
                    setattr(teacher,key,value)
             
                self._save_data()
                print(f"Teacher {teacher_id} updated.")
                return

        print(f"Error: Teacher with ID {teacher_id} is not found.")

    def remove_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                # Remove the student from every course's enrolment list
                for course in self.courses:
                    if student_id in course.enrolled_student_ids:
                        course.enrolled_student_ids.remove(student_id)

                self.students.remove(student)
                self._save_data()

                print(f"Student {student_id} removed.")
                return True
    
        print(f"Error: Student with ID {student_id} is not found.")
        return False


    def remove_teacher(self, teacher_id):
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                assigned_courses = [
                    course for course in self.courses
                    if course.teacher_id == teacher_id
                    ]
                
                if assigned_courses:
                    print(
                        f"Cannot remove teacher {teacher_id}: "
                        f"the teacher is still assigned to courses."
                        )
                    return False

                self.teachers.remove(teacher)
                self._save_data()

                print(f"Teacher {teacher_id} removed.")
                return True

        print(f"Error: Teacher with ID {teacher_id} is not found.")
        return False
        
    def check_in(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
        if course_id not in student.enrolled_course_ids:
            print("Error: Student is not enrolled in this course.")
            return False
        timestamp = datetime.datetime.now().isoformat()

        check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
        }
        self.attendance_log.append(check_in_record)
        self._save_data()

        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    
    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None        

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def record_payment(self, student_id, amount, method):
        """Adds a payment record to the finance log."""

        # Check whether the student exists
        student = self.find_student_by_id(student_id)

        if not student:
            logging.warning(
                "Payment failed: student_id=%s not found",
                student_id
                )
            print("Error: Student not found.")
            return False

        # Create the payment record
        payment_record = {
            "student_id": student_id,
            "amount": amount,
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Save the payment record
        self.finance_log.append(payment_record)
        self._save_data()

        logging.info(
            "Payment recorded: student_id=%s, amount=%s, method=%s",
            student_id,
            amount,
            method
            )


        print(f"Payment of {amount} for student {student_id} recorded.")
        return True

    def get_payment_history(self, student_id):
        """Returns all payment records for a given student."""

        return [
            payment
            for payment in self.finance_log
            if payment["student_id"] == student_id
        ]

    def export_report(self, kind, out_path):
        """Exports finance or attendance records to a CSV file."""

        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]

        elif kind == "attendance":
            data_to_export = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]

        else:
            print("Error: Unknown report type.")
            return False

        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_to_export)

        print(f"{kind.capitalize()} report exported to {out_path}.")
        return True
 