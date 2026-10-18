# tests/test_schedule_manager.py
import pytest
import os
import json
import tempfile
from app.schedule import ScheduleManager
from app.student import StudentUser
from app.teacher import TeacherUser

# A pytest fixture creates a clean environment for each test function.
@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "test_data.json"
    # ARRANGE: Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(data_path=test_file)

def test_create_course(fresh_manager):
    # ARRANGE: Add a teacher first.
    from app.teacher import TeacherUser
    teacher = TeacherUser(1, "Test Teacher", "Piano")
    fresh_manager.teachers.append(teacher)

    # ACT: Add a course.
    fresh_manager.add_course("Beginner Piano", "Piano", 1)

    # ASSERT: Check the result.
    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].name == "Beginner Piano"

def test_record_payment_and_history(fresh_manager):
    # ARRANGE: Add a test student.
    student = StudentUser(1, "Test Student")
    fresh_manager.students.append(student)

    # ACT: Record a payment.
    result = fresh_manager.record_payment(
        1, 100.00, "Credit Card"
    )

    # ACT 2: Get payment history.
    history = fresh_manager.get_payment_history(1)

    # ASSERT: Check the results.
    assert result is True
    assert len(history) == 1
    assert history[0]["amount"] == 100.00
    assert history[0]["method"] == "Credit Card"
    
def test_get_payment_history_no_results(fresh_manager):
    # ARRANGE: Use a student ID with no payment records.
    student_id = 999

    # ACT: Get payment history.
    history = fresh_manager.get_payment_history(student_id)

    # ASSERT: No payment records should be returned.
    assert history == []


def test_cancel_lesson():
    with tempfile.TemporaryDirectory() as temp_dir:
        data_path = os.path.join(temp_dir, "test.json")
        initial_data = {
            "students": [],
            "teachers": [],
            "courses": [
                {
                    "id": 1,
                    "name": "Piano",
                    "instrument": "Piano",
                    "teacher_id": 1,
                    "enrolled_student_ids": [],
                    "lessons": [
                        {
                            "lesson_id": 1,
                            "day": "Monday",
                            "start_time": "16:00",
                            "room": "Room A"
                        }
                    ]
                }
            ],
            "attendance": [],
            "finance_log": [],
            "next_student_id": 1,
            "next_teacher_id": 1,
            "next_course_id": 2,
            "next_lesson_id": 2
        }

        with open(data_path, "w") as f:
            json.dump(initial_data, f)

        manager = ScheduleManager(data_path)

        assert manager.cancel_lesson(1, "Test cancellation") is True
        assert manager.courses[0].lessons == []

        with open(data_path) as f:
            saved_data = json.load(f)

        assert saved_data["courses"][0]["lessons"] == []


def test_cancel_nonexistent_lesson():
    with tempfile.TemporaryDirectory() as temp_dir:
        data_path = os.path.join(temp_dir, "test.json")

        with open(data_path, "w") as f:
            json.dump(
                {
                    "students": [],
                    "teachers": [],
                    "courses": [],
                    "attendance": [],
                    "finance_log": []
                },
                f
            )

        manager = ScheduleManager(data_path)

        assert manager.cancel_lesson(999, "Not found") is False

def test_remove_student_cleans_course_enrolment(fresh_manager):
    # Arrange
    teacher = TeacherUser(1, "Test Teacher", "Piano")
    student = StudentUser(1, "Test Student")

    fresh_manager.teachers.append(teacher)
    fresh_manager.students.append(student)
    fresh_manager.add_course("Beginner Piano", "Piano", 1)

    course = fresh_manager.courses[0]
    student.enrolled_course_ids.append(course.id)
    course.enrolled_student_ids.append(student.id)

    # Act
    result = fresh_manager.remove_student(student.id)

    # Assert
    assert result is True
    assert student not in fresh_manager.students
    assert student.id not in course.enrolled_student_ids


def test_remove_course_cleans_student_enrolment(fresh_manager):
    # Arrange
    teacher = TeacherUser(1, "Test Teacher", "Piano")
    student = StudentUser(1, "Test Student")

    fresh_manager.teachers.append(teacher)
    fresh_manager.students.append(student)
    fresh_manager.add_course("Beginner Piano", "Piano", 1)

    course = fresh_manager.courses[0]
    student.enrolled_course_ids.append(course.id)
    course.enrolled_student_ids.append(student.id)

    # Act
    result = fresh_manager.remove_course(course.id)

    # Assert
    assert result is True
    assert course not in fresh_manager.courses
    assert course.id not in student.enrolled_course_ids


def test_cannot_remove_teacher_with_assigned_courses(fresh_manager):
    # Arrange
    teacher = TeacherUser(1, "Test Teacher", "Piano")
    fresh_manager.teachers.append(teacher)
    fresh_manager.add_course("Beginner Piano", "Piano", 1)

    # Act
    result = fresh_manager.remove_teacher(teacher.id)

    # Assert
    assert result is False
    assert teacher in fresh_manager.teachers
    assert fresh_manager.courses[0].teacher_id == teacher.id
