# Music School Management System (MSMS) — PST5

## 1. Overview

PST5 extends the Music School Management System with finance management, payment records, application logging, data backups, and lesson cancellation.

## 2. Features

- **Finance Management:** Record payments, view payment history, and export finance and attendance reports to CSV.
- **Lesson Management:** View lessons by day and cancel lessons by lesson ID.
- **Logging:** Record important application events and errors.
- **Data Backup:** Create timestamped backups of application data.
- **Data Consistency:** Update student-course enrolment records when students or courses are removed, and prevent deleting teachers who still have assigned courses.

## 3. Project Structure

- `app/` — Application logic and administrative utilities.
- `data/` — JSON application data and backups.
- `gui/` — Streamlit dashboard and interface pages.
- `tests/` — Automated tests.
- `main.py` — Application entry point.

## 4. Design Rationale

- **JSON:** Reuses the existing data storage format.
- **CSV:** Allows finance and attendance reports to be opened in spreadsheet software.
- **Separate utilities:** Keeps logging and backup operations separate from the main application logic.
- **Automated testing:** Verifies core functionality and helps prevent regressions.

## 5. Assumptions

- Each student, teacher, and course has a unique ID.
- Payments are associated with student IDs.
- Application data is stored in JSON files.
- The application is run from the PST5 directory with the required Python packages installed.

## 6. Testing

The automated tests cover:

1. Course creation.
2. Recording payments and retrieving payment history.
3. Handling students without payment records.
4. Cancelling existing and nonexistent lessons.
5. Removing students and cleaning course enrolment records.
6. Removing courses and cleaning student enrolment records.
7. Preventing deletion of teachers who still have assigned courses.

## 7. Known Limitations

- JSON storage may be less suitable for concurrent access than a database.
- Teachers with assigned courses cannot be deleted until their course assignments are handled.
- Automated tests do not cover every possible GUI interaction.

## 8. Running the Application

Run the following command from the PST5 directory:

```bash
python3 -m streamlit run main.py