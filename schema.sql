-- PostgreSQL Schema for Online Examination Analytics Tool
-- Database: examination_analytics

-- 1. Students Table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INT NOT NULL,
    section VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Exams Table
CREATE TABLE IF NOT EXISTS exams (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    subject VARCHAR(100) NOT NULL DEFAULT 'Data Structures & Algorithms',
    course_outcome VARCHAR(10) NOT NULL, -- CO1 to CO6
    semester INT NOT NULL,
    duration_minutes INT NOT NULL DEFAULT 10,
    pass_marks FLOAT NOT NULL DEFAULT 3.0, -- Out of 5
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Questions Table
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    subject VARCHAR(100) NOT NULL DEFAULT 'Data Structures & Algorithms',
    course_outcome VARCHAR(10) NOT NULL, -- CO1 to CO6
    module_name VARCHAR(100) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    difficulty VARCHAR(20) NOT NULL, -- Easy, Medium, Hard
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option CHAR(1) NOT NULL, -- A, B, C, D
    marks FLOAT NOT NULL DEFAULT 1.0,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Exam Attempts Table
CREATE TABLE IF NOT EXISTS exam_attempts (
    id SERIAL PRIMARY KEY,
    exam_id INT REFERENCES exams(id) ON DELETE CASCADE,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    is_submitted BOOLEAN DEFAULT FALSE,
    score FLOAT DEFAULT 0.0,
    total_marks FLOAT DEFAULT 5.0,
    accuracy_pct FLOAT DEFAULT 0.0,
    time_taken_seconds INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Attempt Questions (The exact 5 randomized questions chosen for this attempt)
CREATE TABLE IF NOT EXISTS attempt_questions (
    id SERIAL PRIMARY KEY,
    attempt_id INT REFERENCES exam_attempts(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    question_order INT NOT NULL,
    option_a_text TEXT NOT NULL,
    option_b_text TEXT NOT NULL,
    option_c_text TEXT NOT NULL,
    option_d_text TEXT NOT NULL,
    option_a_orig CHAR(1) NOT NULL,
    option_b_orig CHAR(1) NOT NULL,
    option_c_orig CHAR(1) NOT NULL,
    option_d_orig CHAR(1) NOT NULL
);

-- 6. Attempt Answers (Student's submitted response per question)
CREATE TABLE IF NOT EXISTS attempt_answers (
    id SERIAL PRIMARY KEY,
    attempt_id INT REFERENCES exam_attempts(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    selected_option CHAR(1), -- 'A', 'B', 'C', 'D' or NULL if skipped
    is_correct BOOLEAN DEFAULT FALSE,
    time_taken_seconds INT DEFAULT 0
);

-- 7. Flashcards Table
CREATE TABLE IF NOT EXISTS flashcards (
    id SERIAL PRIMARY KEY,
    course_outcome VARCHAR(10) NOT NULL,
    module_name VARCHAR(100) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    difficulty VARCHAR(20) NOT NULL, -- Easy, Medium, Hard
    front_question TEXT NOT NULL,
    back_answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Student Flashcard Progress Table
CREATE TABLE IF NOT EXISTS student_flashcard_progress (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    flashcard_id INT REFERENCES flashcards(id) ON DELETE CASCADE,
    is_learned BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, flashcard_id)
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_questions_co ON questions(course_outcome);
CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic);
CREATE INDEX IF NOT EXISTS idx_attempts_student ON exam_attempts(student_id);
CREATE INDEX IF NOT EXISTS idx_attempts_exam ON exam_attempts(exam_id);
CREATE INDEX IF NOT EXISTS idx_answers_attempt ON attempt_answers(attempt_id);
CREATE INDEX IF NOT EXISTS idx_flashcards_co ON flashcards(course_outcome);
