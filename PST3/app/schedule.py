import json
from app.student import StudentUser
from app.teacher import TeacherUser, Course
# ... inside the ScheduleManager class ...
import datetime

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
            
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        # ... (next_id counters) ...
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 1

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

                self.next_student_id = data.get("next_student_id", 1)
                self.next_teacher_id = data.get("next_teacher_id", 1)
                self.next_course_id = data.get("next_course_id", 1)

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # TODO: Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            # ... (next_id counters) ...
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id
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
        for s in self.students:
            if s.id == student_id:
                self.students.remove(s)

                self._save_data()

                print(f"Student {s.id} removed. ")
                return
        print(f"Error: Student with ID {student_id} is not found")
    

    def remove_teacher(self,teacher_id):
        for t in self.teachers:
            if t.id == teacher_id:
                self.teachers.remove(t)

                self._save_data()

                print(f"Teacher {t.id} removed.")
                return
        
        print(f"Error: Teacher with ID {teacher_id} is not found.")
        
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

 