# tests/test_schedule_manager.py
import pytest
import os
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
