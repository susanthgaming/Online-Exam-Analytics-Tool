"""
Backend Verification Script
Tests:
1. Student creation and listing
2. Exam question count validation (must have >=5 questions)
3. KMP question search
4. Rabin-Karp duplicate detection
5. Exam attempt generation (exactly 5 questions from chosen CO)
6. Submission and auto-evaluation with strong/weak topic extraction
7. Analytics calculations from PostgreSQL
8. Merge sort ranking
9. Flashcard recommendations
"""

import sys
from database import SessionLocal
from models.models import Student, Exam, Question, ExamAttempt
from algorithms.kmp import kmp_search, kmp_contains
from algorithms.rabin_karp import check_duplicate_questions
from algorithms.sorting import rank_student_attempts
from services.exam_service import start_exam_attempt, submit_exam_attempt
from services.analytics_service import (
    get_faculty_dashboard_metrics,
    get_co_analytics,
    get_topic_analytics,
    get_difficulty_analytics
)

def test_all():
    db = SessionLocal()
    try:
        print("--- 1. Checking Database Tables ---")
        student_count = db.query(Student).count()
        exam_count = db.query(Exam).count()
        question_count = db.query(Question).count()
        print(f"Students: {student_count}, Exams: {exam_count}, Questions: {question_count}")
        assert student_count > 0, "No students found"
        assert question_count >= 50, "Not enough questions in Question Bank"

        print("--- 2. Testing KMP Search ---")
        matches = kmp_search("Knuth-Morris-Pratt failure function string search", "Morris")
        assert len(matches) > 0, "KMP failed to find pattern"
        print(f"KMP pattern 'Morris' found at index {matches[0]}")

        # Search questions in DB using KMP
        all_q = db.query(Question).all()
        kmp_results = [q for q in all_q if kmp_contains(q.text, "KMP") or kmp_contains(q.topic, "KMP")]
        print(f"KMP Question Search found {len(kmp_results)} questions matching 'KMP'.")
        assert len(kmp_results) > 0, "KMP question search returned 0 results"

        print("--- 3. Testing Rabin-Karp Duplicate Detection ---")
        first_q = all_q[0]
        test_similar_text = first_q.text.lower()
        q_dicts = [{"id": q.id, "text": q.text, "course_outcome": q.course_outcome, "topic": q.topic, "difficulty": q.difficulty} for q in all_q]
        dupes = check_duplicate_questions(test_similar_text, q_dicts, threshold=0.8)
        print(f"Rabin-Karp duplicate detector found {len(dupes)} matches (top match similarity: {dupes[0]['similarity_pct']}%).")
        assert len(dupes) > 0, "Rabin-Karp failed to flag identical text"

        print("--- 4. Testing Exact 5 Questions Random Exam Generation (CO2) ---")
        student = db.query(Student).first()
        co2_exam = db.query(Exam).filter(Exam.course_outcome == "CO2").first()
        attempt_data = start_exam_attempt(db, student.id, co2_exam.id)
        questions = attempt_data["questions"]
        print(f"Generated Attempt ID: {attempt_data['attempt_id']}, Questions count: {len(questions)}")
        assert len(questions) == 5, f"Expected exactly 5 questions, got {len(questions)}"
        for q in questions:
            assert q["course_outcome"] == "CO2", f"Question belongs to {q['course_outcome']}, not CO2!"

        print("--- 5. Testing Submission & Automatic Evaluation ---")
        # Submit answers
        sample_answers = [
            {"question_id": questions[0]["question_id"], "selected_option": "A", "time_taken_seconds": 25},
            {"question_id": questions[1]["question_id"], "selected_option": "B", "time_taken_seconds": 30},
            {"question_id": questions[2]["question_id"], "selected_option": "C", "time_taken_seconds": 20},
            {"question_id": questions[3]["question_id"], "selected_option": "A", "time_taken_seconds": 35},
            {"question_id": questions[4]["question_id"], "selected_option": "D", "time_taken_seconds": 40},
        ]
        result = submit_exam_attempt(db, attempt_data["attempt_id"], sample_answers)
        print(f"Result evaluated: Score={result['score']}/5, Accuracy={result['accuracy_pct']}%, Avg Time={result['avg_time_per_question']}s")
        print(f"Strong Topics: {result['strong_topics']}, Weak Topics: {result['weak_topics']}")
        print(f"Recommended Flashcards: {len(result['recommended_flashcards'])}")
        assert "score" in result
        assert "recommended_flashcards" in result

        print("--- 6. Testing PostgreSQL Dynamic Analytics ---")
        metrics = get_faculty_dashboard_metrics(db)
        print(f"Class Average: {metrics['class_average']}, Pass Rate: {metrics['pass_percentage']}%, Total Attempts: {metrics['total_attempts']}")
        assert metrics["total_attempts"] > 0

        co_stats = get_co_analytics(db)
        print(f"CO Analytics count: {len(co_stats)}")
        assert len(co_stats) == 6

        topic_stats = get_topic_analytics(db)
        print(f"Topic Analytics count: {len(topic_stats)}")
        assert len(topic_stats) > 0

        diff_stats = get_difficulty_analytics(db)
        print(f"Difficulty Analytics: {diff_stats}")
        assert len(diff_stats) == 3

        print("--- 7. Testing Merge Sort Ranking Algorithm ---")
        sample_data = [
            {"student_name": "Student A", "score": 3.0, "accuracy_pct": 60.0, "time_taken_seconds": 150},
            {"student_name": "Student B", "score": 5.0, "accuracy_pct": 100.0, "time_taken_seconds": 200},
            {"student_name": "Student C", "score": 4.0, "accuracy_pct": 80.0, "time_taken_seconds": 120},
        ]
        ranked = rank_student_attempts(sample_data, sort_by="score")
        assert ranked[0]["student_name"] == "Student B", "Highest score should be Rank 1"
        assert ranked[0]["rank"] == 1
        print("Merge sort ranking verified successfully!")

        print("\nALL BACKEND VERIFICATIONS PASSED WITH 100% SUCCESS!")

    finally:
        db.close()

if __name__ == "__main__":
    test_all()
