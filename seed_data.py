"""
Comprehensive Seed Data Script for Online Examination Analytics Tool.
Seeds:
- Multiple students across different semesters & sections
- Standard exams for CO1 through CO6
- 75+ syllabus-accurate DSA questions (12-15 per CO) covering all 6 syllabus modules
- 30+ comprehensive revision flashcards
- Realistic historical student attempts and answers to populate all analytics, charts, and rankings.
"""

from datetime import datetime, timedelta
import random
from database import SessionLocal, Base, engine
from models.models import (
    Student,
    Exam,
    Question,
    ExamAttempt,
    AttemptQuestion,
    AttemptAnswer,
    Flashcard,
    StudentFlashcardProgress
)
from algorithms.randomization import randomize_question_options

def seed():
    db = SessionLocal()
    try:
        # Check if data already seeded
        if db.query(Question).count() >= 50:
            print("Database already contains seed questions. Skipping.")
            return

        print("Seeding Students...")
        students_data = [
            {"student_id": "STU101", "name": "Aarav Sharma", "roll_number": "22CS101", "department": "Computer Science & Engg", "semester": 4, "section": "A"},
            {"student_id": "STU102", "name": "Bhavna Patel", "roll_number": "22CS102", "department": "Computer Science & Engg", "semester": 4, "section": "A"},
            {"student_id": "STU103", "name": "Chirag Verma", "roll_number": "22CS103", "department": "Information Technology", "semester": 4, "section": "B"},
            {"student_id": "STU104", "name": "Divya Reddy", "roll_number": "22CS104", "department": "Computer Science & Engg", "semester": 4, "section": "A"},
            {"student_id": "STU105", "name": "Eshan Gupta", "roll_number": "22CS105", "department": "Information Technology", "semester": 4, "section": "B"},
            {"student_id": "STU106", "name": "Fatima Sheikh", "roll_number": "23CS106", "department": "Computer Science & Engg", "semester": 3, "section": "A"},
            {"student_id": "STU107", "name": "Gautam Nair", "roll_number": "23CS107", "department": "Computer Science & Engg", "semester": 3, "section": "B"},
            {"student_id": "STU108", "name": "Harini Krishnan", "roll_number": "21CS108", "department": "Computer Science & Engg", "semester": 6, "section": "A"},
        ]

        student_objs = []
        for s in students_data:
            existing = db.query(Student).filter(Student.student_id == s["student_id"]).first()
            if not existing:
                st = Student(**s)
                db.add(st)
                student_objs.append(st)
            else:
                student_objs.append(existing)
        db.commit()

        print("Seeding Exams...")
        exams_data = [
            {"title": "CO1 Comprehensive Assessment: Algorithm Strategy Selection", "course_outcome": "CO1", "semester": 4, "duration_minutes": 10, "pass_marks": 3.0},
            {"title": "CO2 Mid-Term: Linear-Time String Matching & Suffix Structures", "course_outcome": "CO2", "semester": 4, "duration_minutes": 10, "pass_marks": 3.0},
            {"title": "CO3 Deep Dive: Advanced Dynamic Programming & Subsets", "course_outcome": "CO3", "semester": 4, "duration_minutes": 10, "pass_marks": 3.0},
            {"title": "CO4 Network Flow & Bipartite Matching Examination", "course_outcome": "CO4", "semester": 4, "duration_minutes": 10, "pass_marks": 3.0},
            {"title": "CO5 NP-Completeness Reductions & Approximation Algorithms", "course_outcome": "CO5", "semester": 4, "duration_minutes": 10, "pass_marks": 3.0},
            {"title": "CO6 Randomized Algorithms & Parallel Work-Span Analysis", "course_outcome": "CO6", "semester": 4, "duration_minutes": 10, "pass_marks": 3.0},
        ]

        exam_objs = {}
        for e in exams_data:
            existing = db.query(Exam).filter(Exam.title == e["title"]).first()
            if not existing:
                ex = Exam(**e)
                db.add(ex)
                db.flush()
                exam_objs[ex.course_outcome] = ex
            else:
                exam_objs[existing.course_outcome] = existing
        db.commit()

        print("Seeding Syllabus Questions...")
        raw_questions = [
            # ==================== CO1: Problem-Class Signatures & Algorithm Strategy ====================
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Pattern search", "difficulty": "Easy",
                "text": "When designing a large-scale text search engine requiring exact pattern search across multiple streaming documents, which algorithm signature avoids backtracking in the text stream?",
                "option_a": "Knuth-Morris-Pratt (KMP) using prefix failure transitions",
                "option_b": "Naive sliding window with nested index resets",
                "option_c": "Binary search on unsorted document tokens",
                "option_d": "Depth-First Search on the document grammar tree",
                "correct_option": "A",
                "explanation": "KMP precomputes a failure function (LPS array) that allows linear scanning of the text stream without ever moving the text pointer backward."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Fuzzy matching/edit distance", "difficulty": "Medium",
                "text": "Which problem-class signature indicates that a problem should be solved via dynamic programming rather than greedy sequence alignment?",
                "option_a": "Optimal substructure and overlapping subproblems across edit prefixes",
                "option_b": "Greedy choice property with strictly non-overlapping intervals",
                "option_c": "Independent disjoint components solvable by topological sort",
                "option_d": "Absence of recursive relation between prefix edits",
                "correct_option": "A",
                "explanation": "Sequence alignment exhibits overlapping subproblems where alignment of prefixes S[1..i] and T[1..j] depends on optimal alignments of smaller subproblems."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Document similarity", "difficulty": "Medium",
                "text": "For measuring document similarity in large textual datasets, which signature distinguishes polynomial rolling hash fingerprints from quadratic character comparisons?",
                "option_a": "O(1) sliding window hash updates enabling O(N) token comparison",
                "option_b": "Strict monotonic increase of character ASCII sums",
                "option_c": "Requiring complete document matrix inversion",
                "option_d": "Guaranteed zero probability of collisions without modular bounds",
                "correct_option": "A",
                "explanation": "Polynomial rolling hashes allow updating the hash of an incoming word/character in O(1) time by removing the trailing element and adding the leading element."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Citation-flow analysis", "difficulty": "Hard",
                "text": "In a citation-flow network where influential papers act as capacities and references form directed edges, which algorithmic paradigm identifies the structural bottleneck?",
                "option_a": "Max-Flow Min-Cut duality",
                "option_b": "Bellman-Ford negative cycle detection",
                "option_c": "Kruskal minimum spanning forest",
                "option_d": "Huffman greedy coding tree",
                "correct_option": "A",
                "explanation": "By modeling citation dependencies as a network with edge capacities, the Min-Cut identifies the minimal bottleneck disconnect in citation flow."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Scheduling", "difficulty": "Hard",
                "text": "When formulating an exam scheduling problem with non-overlapping slot constraints and teacher availability conflicts, reaching an NP-hard signature means we should select:",
                "option_a": "Approximation or branch-and-bound heuristics",
                "option_b": "Greedy single-pass earliest deadline first without verification",
                "option_c": "Floyd-Warshall all-pairs shortest paths",
                "option_d": "Linear-time Tarjan strongly connected components",
                "correct_option": "A",
                "explanation": "Conflict-constrained scheduling maps to Graph Coloring / Vertex Cover which are NP-hard; polynomial exact solutions do not exist unless P=NP."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Large-prime primality", "difficulty": "Medium",
                "text": "In cryptographic hashing for document authenticity, testing whether a 1024-bit integer is prime is best approached using which algorithm class?",
                "option_a": "Monte Carlo randomized algorithm (Miller-Rabin)",
                "option_b": "Deterministic sieve of Eratosthenes up to sqrt(N)",
                "option_c": "Brute force trial division by odd integers",
                "option_d": "Breadth-First Search on factors",
                "correct_option": "A",
                "explanation": "Miller-Rabin is a polynomial-time Monte Carlo randomized test that can determine primality of 1024-bit primes with negligible error probability."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "String algorithms", "difficulty": "Easy",
                "text": "If multiple search patterns P1, P2, ... Pk must be queried simultaneously inside a document text, what algorithmic structure is signature for this problem class?",
                "option_a": "Aho-Corasick automaton built over a Trie",
                "option_b": "Repeated naive linear scan for each pattern",
                "option_c": "Binary indexed tree (Fenwick tree)",
                "option_d": "Disjoint set union (DSU)",
                "correct_option": "A",
                "explanation": "Aho-Corasick constructs a finite-state automaton with failure links over a trie to find all pattern occurrences in O(N + total_matches)."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Max-flow", "difficulty": "Medium",
                "text": "A university system allocates exam invigilators to exam rooms under capacity bounds. Which algorithmic reduction models this efficiently?",
                "option_a": "Bipartite Maximum Matching via Max-Flow (Ford-Fulkerson)",
                "option_b": "Dijkstra single-source shortest path",
                "option_c": "Topological sort on DAG",
                "option_d": "Prefix sum scan",
                "correct_option": "A",
                "explanation": "Bipartite matching reduces directly to max-flow by introducing source and sink with unit capacities to candidate assignments."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Dynamic programming", "difficulty": "Easy",
                "text": "When a problem requires finding the longest common subsequence of two DNA sequences of length 10^3, why is Dynamic Programming chosen over Backtracking?",
                "option_a": "Backtracking takes O(2^N) exponential time whereas DP takes O(N*M) polynomial time",
                "option_b": "Backtracking cannot find an optimal solution",
                "option_c": "Dynamic programming uses O(1) memory always",
                "option_d": "DNA sequences cannot be indexed recursively",
                "correct_option": "A",
                "explanation": "DP avoids solving repeated subproblems by caching prefix solutions, reducing time from exponential O(2^N) to O(NM)."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "NP-hard approximation", "difficulty": "Hard",
                "text": "When evaluating an optimization problem proven to be NP-hard, which property confirms that a PTAS (Polynomial-Time Approximation Scheme) is applicable?",
                "option_a": "For any fixed epsilon > 0, an approximation ratio of (1 + epsilon) can be achieved in polynomial time in N",
                "option_b": "The exact optimal solution can be found in O(N^2) time",
                "option_c": "The problem has no pseudo-polynomial algorithm",
                "option_d": "The error bound must be exactly 0",
                "correct_option": "A",
                "explanation": "A PTAS guarantees a (1 + epsilon) approximation factor running in time polynomial in input size N for every fixed constant epsilon > 0."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Suffix structures", "difficulty": "Hard",
                "text": "For finding the Longest Repeated Substring in a static genomic sequence of length 10^6, what is the most space-efficient advanced data structure strategy?",
                "option_a": "Suffix Array combined with Kasai LCP Array",
                "option_b": "Full uncompressed Suffix Trie",
                "option_c": "Adjacency matrix of all substrings",
                "option_d": "Recursive edit distance matrix",
                "correct_option": "A",
                "explanation": "A Suffix Array with an LCP array takes only O(N) integers of space, compared to the heavy pointer overhead of an uncompressed suffix trie."
            },
            {
                "course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System",
                "topic": "Randomized algorithms", "difficulty": "Easy",
                "text": "What distinguishes a Las Vegas algorithm strategy from a Monte Carlo algorithm strategy in computational problem solving?",
                "option_a": "Las Vegas always produces the correct answer with random running time; Monte Carlo has fixed running time with possible bounded error",
                "option_b": "Las Vegas algorithm gives approximate answers; Monte Carlo gives exact answers",
                "option_c": "Las Vegas cannot use pseudo-random generators",
                "option_d": "Monte Carlo algorithms can never be parallelized",
                "correct_option": "A",
                "explanation": "Las Vegas algorithms (like Randomized Quicksort) never err on output correctness; Monte Carlo algorithms (like Miller-Rabin) have bounded error probability."
            },

            # ==================== CO2: Linear-Time String Algorithms & Suffix Structures ====================
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "KMP", "difficulty": "Medium",
                "text": "In the Knuth-Morris-Pratt (KMP) string matching algorithm, what does the failure function (LPS array) entry lps[i] represent?",
                "option_a": "Length of the longest proper prefix of pattern[0..i] that is also a suffix of pattern[0..i]",
                "option_b": "The total number of occurrences of pattern[0..i] in text",
                "option_c": "The index where pattern[i] mismatches in text",
                "option_d": "The character frequency count of pattern[i]",
                "correct_option": "A",
                "explanation": "lps[i] stores the length of the longest proper prefix of pattern[0..i] that matches a suffix of pattern[0..i]."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Failure function", "difficulty": "Easy",
                "text": "What is the worst-case time complexity of preprocessing the LPS array in KMP for a pattern of length M?",
                "option_a": "O(M)",
                "option_b": "O(M^2)",
                "option_c": "O(M log M)",
                "option_d": "O(2^M)",
                "correct_option": "A",
                "explanation": "Computing the LPS array takes linear time O(M) because the prefix pointer increments at most M times and decrements along failure links."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Z-function", "difficulty": "Medium",
                "text": "In the Z-algorithm for a string S of length N, what does the array value Z[i] represent for index i > 0?",
                "option_a": "The length of the longest substring starting at S[i] that is also a prefix of S",
                "option_b": "The frequency of character S[i] in the entire string",
                "option_c": "The edit distance between S[0..i] and S[i..N-1]",
                "option_d": "The position of the next mismatch in S",
                "correct_option": "A",
                "explanation": "Z[i] is the length of the longest common prefix between S and the suffix of S starting at index i."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Rabin-Karp", "difficulty": "Easy",
                "text": "How does the Rabin-Karp algorithm achieve an average-case time complexity of O(N + M)?",
                "option_a": "By using a polynomial rolling hash to calculate the next window's hash in O(1) time",
                "option_b": "By sorting the characters of both strings lexicographically",
                "option_c": "By building a suffix tree over the pattern",
                "option_d": "By testing every character pair with binary search",
                "correct_option": "A",
                "explanation": "Rolling hash updates the window hash in O(1) arithmetic operations: subtract oldest character term, multiply by base, add new character."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Polynomial rolling hash", "difficulty": "Medium",
                "text": "When computing polynomial rolling hash H = sum(S[i] * B^(m-1-i)) mod P, why is double hashing (using two distinct primes P1 and P2) employed?",
                "option_a": "To reduce the probability of hash collision to near-zero (approx 1 / (P1 * P2))",
                "option_b": "To double the speed of string comparison",
                "option_c": "To eliminate the need for modular arithmetic",
                "option_d": "To allow negative characters in the pattern",
                "correct_option": "A",
                "explanation": "With two large 32-bit primes, the collision probability drops to ~10^-18, making hash collisions virtually impossible."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Suffix arrays", "difficulty": "Medium",
                "text": "For a string S of length N, what is a Suffix Array SA?",
                "option_a": "An array of integers giving starting positions of all suffixes of S sorted in lexicographical order",
                "option_b": "An array containing every suffix stored as a complete string",
                "option_c": "The reverse of the prefix array of S",
                "option_d": "A hash table storing pointers to vowels in S",
                "correct_option": "A",
                "explanation": "A suffix array stores the starting indices 0 <= SA[i] < N of all suffixes sorted in lexicographical order, taking O(N) space."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "LCP", "difficulty": "Medium",
                "text": "What is the relationship between the Suffix Array SA and the Longest Common Prefix (LCP) array?",
                "option_a": "LCP[i] stores the length of the longest common prefix between suffix SA[i] and suffix SA[i-1]",
                "option_b": "LCP[i] stores the length of the suffix starting at index i",
                "option_c": "LCP[i] counts how many times suffix SA[i] repeats in S",
                "option_d": "LCP[i] is always equal to lps[i] from KMP",
                "correct_option": "A",
                "explanation": "LCP array stores the lengths of the longest common prefixes between consecutive suffixes in the sorted suffix array."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Kasai algorithm", "difficulty": "Hard",
                "text": "Kasai's algorithm constructs the LCP array from a Suffix Array in O(N) time. What core invariant ensures this linear time bound?",
                "option_a": "When moving from suffix i to suffix i+1, the LCP value can decrease by at most 1",
                "option_b": "The suffixes are already sorted in reverse topological order",
                "option_c": "Character comparisons are performed backwards using a stack",
                "option_d": "Every character is compared at most twice per suffix",
                "correct_option": "A",
                "explanation": "Kasai proves that if LCP of suffix i is k, then LCP of suffix i+1 is at least k - 1. Thus the counter k increments at most N times and decrements at most N times."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Suffix automaton", "difficulty": "Hard",
                "text": "What is the upper bound on the number of states (vertices) and transitions (edges) in a Suffix Automaton for a string of length N?",
                "option_a": "At most 2N - 1 states and at most 3N - 4 transitions",
                "option_b": "Exactly N^2 states and N^2 transitions",
                "option_c": "O(N log N) states and O(N log N) transitions",
                "option_d": "O(2^N) states in worst case",
                "correct_option": "A",
                "explanation": "A Suffix Automaton (DAWG) for string of length N is linear in size: at most 2N - 1 states and at most 3N - 4 transitions."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Aho-Corasick intuition", "difficulty": "Medium",
                "text": "In the Aho-Corasick automaton, what role do the 'dictionary suffix links' (exit links) play?",
                "option_a": "They allow jumping directly to the next matching pattern in the trie without checking all ancestors",
                "option_b": "They reset the search back to root on every vowel",
                "option_c": "They sort the patterns alphabetically during search",
                "option_d": "They delete matched patterns from the trie dynamically",
                "correct_option": "A",
                "explanation": "Dictionary suffix links bypass intermediate non-terminal trie nodes to point directly to the nearest node representing an accepted pattern."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "SA-IS conceptual understanding", "difficulty": "Hard",
                "text": "In the SA-IS (Suffix Array Induced Sorting) algorithm that constructs Suffix Arrays in linear O(N) time, how are characters classified?",
                "option_a": "Into S-type (suffix smaller than next) and L-type (suffix larger than next) based on lexicographical order",
                "option_b": "Into vowels and consonants",
                "option_c": "Into prefix characters and suffix characters",
                "option_d": "Into prime and composite character encodings",
                "correct_option": "A",
                "explanation": "SA-IS partitions suffixes into S-type (lexicographically smaller than suffix i+1) and L-type (larger than suffix i+1), using LMS-substrings for linear induction."
            },
            {
                "course_outcome": "CO2", "module_name": "Module 2 — String Algorithms",
                "topic": "Naive string matching", "difficulty": "Easy",
                "text": "What is the worst-case time complexity of Naive string matching when searching for pattern P = 'AAA' in text T = 'AAAAAA'?",
                "option_a": "O((N - M + 1) * M)",
                "option_b": "O(N + M)",
                "option_c": "O(log N)",
                "option_d": "O(M log N)",
                "correct_option": "A",
                "explanation": "When repetitive characters cause mismatches only at the end of the pattern, naive search compares M characters for each of the (N - M + 1) alignments."
            },

            # ==================== CO3: Advanced Dynamic Programming ====================
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Levenshtein edit distance", "difficulty": "Easy",
                "text": "In the standard Wagner-Fischer algorithm for Levenshtein edit distance between strings of length N and M, what operations are permitted?",
                "option_a": "Insertion, Deletion, and Substitution of a single character",
                "option_b": "Insertion and deletion only",
                "option_c": "Substring reversal and character swap",
                "option_d": "Rotation and transposition only",
                "correct_option": "A",
                "explanation": "Standard Levenshtein distance defines unit cost for insertion, deletion, and substitution of single characters."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Damerau-Levenshtein", "difficulty": "Medium",
                "text": "What additional elementary operation does Damerau-Levenshtein distance introduce beyond standard Levenshtein distance?",
                "option_a": "Transposition of two adjacent characters",
                "option_b": "Cyclic rotation of entire string",
                "option_c": "Block deletion of identical characters",
                "option_d": "Reversal of arbitrary substrings",
                "correct_option": "A",
                "explanation": "Damerau-Levenshtein includes adjacent character transposition (e.g., 'teh' -> 'the') as an elementary edit operation."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Needleman-Wunsch", "difficulty": "Medium",
                "text": "What fundamental difference distinguishes the Needleman-Wunsch algorithm from the Smith-Waterman algorithm in sequence alignment?",
                "option_a": "Needleman-Wunsch computes global alignment while Smith-Waterman computes local alignment by capping negative scores at 0",
                "option_b": "Needleman-Wunsch is greedy while Smith-Waterman uses dynamic programming",
                "option_c": "Needleman-Wunsch is for amino acids while Smith-Waterman is only for integers",
                "option_d": "Smith-Waterman runs in linear O(N) time while Needleman-Wunsch takes O(2^N)",
                "correct_option": "A",
                "explanation": "Smith-Waterman finds the highest-scoring local region by resetting negative cell values to 0; Needleman-Wunsch aligns the entire sequences globally."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Interval DP", "difficulty": "Medium",
                "text": "In Interval DP (such as Matrix Chain Multiplication or Optimal BST), what is the typical outer loop iteration variable?",
                "option_a": "Subarray/interval length L from 2 up to N",
                "option_b": "Character ASCII codes",
                "option_c": "Matrix determinant values",
                "option_d": "Random index permutation",
                "correct_option": "A",
                "explanation": "Interval DP builds solutions from smallest sub-intervals to larger ones; thus the outer loop iterates over chain length L from 2 to N."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Matrix Chain Multiplication", "difficulty": "Medium",
                "text": "What is the time complexity of finding the optimal parenthesization of N matrices using standard Dynamic Programming?",
                "option_a": "O(N^3)",
                "option_b": "O(N^2)",
                "option_c": "O(N log N)",
                "option_d": "O(2^N)",
                "correct_option": "A",
                "explanation": "There are O(N^2) sub-intervals [i, j], and finding the optimal split point k takes O(N) comparisons, resulting in O(N^3) overall time."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Bitmask DP", "difficulty": "Hard",
                "text": "In solving the Traveling Salesperson Problem (TSP) using Held-Karp Bitmask DP, what does the state DP(mask, u) represent?",
                "option_a": "Minimum cost of visiting exactly the subset of vertices encoded by 'mask', ending at vertex u",
                "option_b": "Number of edges connected to vertex u",
                "option_c": "Maximum flow through the vertex subset mask",
                "option_d": "The shortest path from u to source without visiting other nodes",
                "correct_option": "A",
                "explanation": "In Held-Karp, the integer bitmask tracks which subset of vertices has been visited, and u denotes the current terminal vertex. Complexity is O(2^N * N^2)."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "DP on trees", "difficulty": "Medium",
                "text": "When solving the Maximum Independent Set on a tree using DP, why can an optimal solution be found in linear O(V) time?",
                "option_a": "Because trees have no cycles and every sub-tree rooted at child v is an independent subproblem",
                "option_b": "Because trees are bipartite with equal sized partitions",
                "option_c": "Because greedy vertex degree sorting is always exact on trees",
                "option_d": "Because trees can have at most 3 vertices",
                "correct_option": "A",
                "explanation": "A tree's acyclic topological structure allows computing optimal states bottom-up from leaves to root in a single post-order traversal in O(V) time."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Tree diameter", "difficulty": "Easy",
                "text": "How can the diameter of an unweighted tree be calculated using Dynamic Programming in a single DFS traversal?",
                "option_a": "At each node u, track the two largest depths among its children subtrees; diameter through u is depth1 + depth2",
                "option_b": "Sum all edge weights across the entire tree",
                "option_c": "Count the number of leaf nodes and divide by 2",
                "option_d": "Run Floyd-Warshall on the adjacency matrix",
                "correct_option": "A",
                "explanation": "The longest path passing through node u is the sum of the top two deepest paths down into u's distinct children subtrees."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Rerooting", "difficulty": "Hard",
                "text": "What is the primary benefit of the Tree Rerooting technique in Tree DP?",
                "option_a": "It computes the answer for all N possible roots in O(N) time instead of O(N^2) by transferring root states in O(1)",
                "option_b": "It changes the tree into a complete binary search tree",
                "option_c": "It eliminates all negative edge weights",
                "option_d": "It finds the maximum flow between leaf pairs",
                "correct_option": "A",
                "explanation": "Tree rerooting calculates subtree answers in a first DFS pass, then updates parent-to-child root transitions in a second DFS, achieving O(N) total time."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "SOS DP", "difficulty": "Hard",
                "text": "Sum Over Subsets (SOS DP) computes F[mask] = sum of A[submask] for all submasks of mask. What is its time complexity compared to iterating all submasks naively?",
                "option_a": "O(N * 2^N) using bit-by-bit DP instead of O(3^N) naive submask iteration",
                "option_b": "O(2^N) instead of O(N!)",
                "option_c": "O(N^2) instead of O(2^N)",
                "option_d": "O(log N) instead of O(N)",
                "correct_option": "A",
                "explanation": "Naive submask iteration takes sum(C(N, k) * 2^k) = 3^N time. SOS DP uses dimensional prefix sums over bit positions to achieve O(N * 2^N)."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "When DP is wrong", "difficulty": "Medium",
                "text": "Under which condition will Dynamic Programming fail to produce a correct optimal solution?",
                "option_a": "When the problem violates the principle of optimal substructure (e.g. longest simple path in graphs with positive cycles)",
                "option_b": "When overlapping subproblems exist",
                "option_c": "When the state space is finite and bounded",
                "option_d": "When memoization is implemented using a hash table",
                "correct_option": "A",
                "explanation": "DP strictly requires optimal substructure: an optimal solution to the overall problem must be composed of optimal solutions to subproblems."
            },
            {
                "course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming",
                "topic": "Optimal BST", "difficulty": "Hard",
                "text": "In the Optimal Binary Search Tree problem with keys K1 < K2 < ... < Kn and search probabilities p_i, what DP recurrence is minimized?",
                "option_a": "cost[i][j] = sum(p_k) + min over r { cost[i][r-1] + cost[r+1][j] }",
                "option_b": "cost[i][j] = max(p_i, p_j) * depth",
                "option_c": "cost[i][j] = cost[i][j-1] + cost[i+1][j]",
                "option_d": "cost[i][j] = sum(cost of all AVL rotations)",
                "correct_option": "A",
                "explanation": "Choosing root Kr puts items [i..r-1] on left and [r+1..j] on right; every node in subtree increases depth by 1, adding total probability weight sum(p_k)."
            },

            # ==================== CO4: Network Flow ====================
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Ford-Fulkerson", "difficulty": "Easy",
                "text": "What fundamental invariant must hold at every vertex v (other than source s and sink t) in a valid network flow?",
                "option_a": "Flow conservation: Total incoming flow equals total outgoing flow",
                "option_b": "Total capacity equals total edge count",
                "option_c": "Incoming flow must exceed outgoing flow by 1",
                "option_d": "All outgoing edges must carry equal flow",
                "correct_option": "A",
                "explanation": "Flow conservation requires that for every vertex except source and sink, sum of flow entering equals sum of flow leaving."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Edmonds-Karp", "difficulty": "Medium",
                "text": "How does the Edmonds-Karp implementation specify the augmenting path in the Ford-Fulkerson method to guarantee polynomial running time?",
                "option_a": "By using Breadth-First Search (BFS) to always choose the shortest augmenting path (fewest edges)",
                "option_b": "By using Depth-First Search (DFS) with random edge exploration",
                "option_c": "By sorting edges by capacity in descending order",
                "option_d": "By running Dijkstra on edge capacities",
                "correct_option": "A",
                "explanation": "Edmonds-Karp uses BFS to select shortest augmenting paths, guaranteeing termination in O(V * E^2) time regardless of capacity magnitudes."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Max-flow/min-cut", "difficulty": "Easy",
                "text": "According to the Max-Flow Min-Cut Theorem, what is the relationship between the value of the maximum flow and the capacity of the minimum cut?",
                "option_a": "The maximum flow value is equal to the minimum s-t cut capacity",
                "option_b": "Maximum flow is strictly half the minimum cut capacity",
                "option_c": "Maximum flow always exceeds the minimum cut capacity",
                "option_d": "Minimum cut capacity is always equal to the number of vertices",
                "correct_option": "A",
                "explanation": "The Max-Flow Min-Cut theorem establishes that the maximum amount of flow passing from source to sink equals the total capacity of the minimum cut separating s and t."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Residual graph", "difficulty": "Medium",
                "text": "In a residual graph G_f, why are backward edges with capacity equal to current flow f(u, v) introduced?",
                "option_a": "To allow the algorithm to undo (cancel) previously sent flow along that edge",
                "option_b": "To detect negative cycles in bipartite graphs",
                "option_c": "To convert directed graphs into undirected graphs",
                "option_d": "To store vertex colors for bipartite matching",
                "correct_option": "A",
                "explanation": "Backward edges allow subsequent augmenting paths to redirect previously assigned flow if a better global route is discovered."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Bipartite matching", "difficulty": "Medium",
                "text": "How is the Maximum Bipartite Matching problem for graph G = (L union R, E) reduced to a Max-Flow problem?",
                "option_a": "Add source s connected to all L with capacity 1, connect all edges L->R with capacity 1, connect all R to sink t with capacity 1",
                "option_b": "Connect all vertices in L to each other with infinite capacity",
                "option_c": "Compute the Minimum Spanning Tree of G and remove leaves",
                "option_d": "Assign random edge weights and find shortest s-t path",
                "correct_option": "A",
                "explanation": "Unit capacities from source to L, across bipartite edges, and from R to sink ensure each vertex participates in at most one matched edge in integral flow."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Konig's theorem", "difficulty": "Hard",
                "text": "Konig's theorem states that in any bipartite graph, the size of the maximum matching is equal to:",
                "option_a": "The size of the minimum vertex cover",
                "option_b": "The total number of edges in the graph",
                "option_c": "The chromatic number of the graph",
                "option_d": "The diameter of the bipartite graph",
                "correct_option": "A",
                "explanation": "Konig's theorem proves equivalence between maximum matching cardinality and minimum vertex cover cardinality in bipartite graphs via min-cut duality."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Dinic intuition", "difficulty": "Hard",
                "text": "What key concept enables Dinic's algorithm to compute maximum flow in O(V^2 * E) time?",
                "option_a": "Constructing layered level graphs using BFS and finding blocking flows using DFS",
                "option_b": "Sorting edges in topological order",
                "option_c": "Running A* heuristic search from sink to source",
                "option_d": "Eliminating all backward edges",
                "correct_option": "A",
                "explanation": "Dinic builds a level graph using BFS, then pushes blocking flows along admissible edges in that level graph using DFS until no augmenting path of that length exists."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Project selection", "difficulty": "Hard",
                "text": "In the Project Selection problem (open-pit mining) with dependencies, how is the optimal closed set of maximum profit found?",
                "option_a": "By formulating an s-t min-cut network where infinite capacity edges prevent violating dependencies",
                "option_b": "By greedy topological sort of projects with highest profit",
                "option_c": "By finding the longest path on a DAG using DP",
                "option_d": "By finding Eulerian tours over project dependencies",
                "correct_option": "A",
                "explanation": "Infinite capacity edges between prerequisite projects ensure no cut can separate a project from its dependency, reducing optimal selection to Min-Cut."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Min-cost max-flow intuition", "difficulty": "Hard",
                "text": "In the Minimum-Cost Maximum-Flow (MCMF) problem, how is flow augmented to ensure minimum total cost?",
                "option_a": "By repeatedly finding augmenting paths with minimum total cost using Bellman-Ford / SPFA in the residual graph",
                "option_b": "By picking the augmenting path with maximum capacity only",
                "option_c": "By setting all edge capacities to 0",
                "option_d": "By running Kruskal's MST on cost weights",
                "correct_option": "A",
                "explanation": "Successive shortest path algorithms find the minimum cost augmenting path in residual graph G_f using edge costs (or reduced costs with potentials)."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Flow conservation", "difficulty": "Easy",
                "text": "If an edge (u, v) has capacity c(u, v) = 10 and current flow f(u, v) = 7, what is the residual capacity c_f(u, v) in the forward direction?",
                "option_a": "3",
                "option_b": "7",
                "option_c": "10",
                "option_d": "17",
                "correct_option": "A",
                "explanation": "The residual capacity in forward direction is c_f(u, v) = c(u, v) - f(u, v) = 10 - 7 = 3."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Image segmentation", "difficulty": "Medium",
                "text": "How does Min-Cut solve binary Image Segmentation (foreground vs background labeling)?",
                "option_a": "Foreground and background correspond to source and sink; edge weights encode pixel likelihood and neighbor smoothness",
                "option_b": "By sorting pixels by luminance and applying binary search",
                "option_c": "By running K-Means clustering on RGB values without graph edges",
                "option_d": "By finding Eulerian paths through pixel grids",
                "correct_option": "A",
                "explanation": "Pixels are connected to source/sink with data penalty capacities, and adjacent pixels are connected with smoothness capacities; min-cut minimizes boundary cost."
            },
            {
                "course_outcome": "CO4", "module_name": "Module 4 — Network Flow",
                "topic": "Capacity", "difficulty": "Easy",
                "text": "In an integral flow network where all capacities are positive integers, what does the Integrality Theorem guarantee?",
                "option_a": "There exists a maximum flow where the flow on every edge is an integer",
                "option_b": "All augmenting paths must have length 2",
                "option_c": "The number of vertices must equal the flow value",
                "option_d": "Flow cannot be computed if capacities are odd",
                "correct_option": "A",
                "explanation": "If edge capacities are integers, the Ford-Fulkerson algorithm terminates with integer flows on all edges throughout."
            },

            # ==================== CO5: NP-Completeness and Approximation ====================
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Decision vs optimization", "difficulty": "Easy",
                "text": "What is the primary difference between a decision problem and an optimization problem?",
                "option_a": "A decision problem has a binary YES/NO answer; an optimization problem seeks the minimum or maximum value of an objective function",
                "option_b": "Decision problems are always in P while optimization problems are always NP-complete",
                "option_c": "Optimization problems cannot be reduced to decision problems",
                "option_d": "Decision problems require floating point arithmetic",
                "correct_option": "A",
                "explanation": "Decision problems ask if a threshold can be met (YES/NO); optimization seeks the extreme value. An optimization problem can be solved via binary search over decision queries."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "P vs NP", "difficulty": "Easy",
                "text": "What is the formal definition of the complexity class NP?",
                "option_a": "The set of decision problems solvable in polynomial time by a non-deterministic Turing machine (or certifiable in polynomial time)",
                "option_b": "The set of problems that can Non-Polynomial time algorithms only",
                "option_c": "The set of problems that cannot be solved by any computer",
                "option_d": "Problems whose certificates require exponential time to verify",
                "correct_option": "A",
                "explanation": "NP contains decision problems where a candidate solution (certificate) can be verified in polynomial time on a deterministic computer."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Cook-Levin theorem", "difficulty": "Medium",
                "text": "What did the Cook-Levin theorem fundamentally establish in theoretical computer science?",
                "option_a": "The Boolean Satisfiability problem (SAT) is NP-complete",
                "option_b": "That P equals NP",
                "option_c": "That Quicksort runs in O(N log N) worst-case time",
                "option_d": "That all graph problems are polynomial-time solvable",
                "correct_option": "A",
                "explanation": "Cook and Levin proved that SAT is in NP and that every problem in NP can be reduced in polynomial time to SAT, making SAT the first proven NP-complete problem."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Reductions", "difficulty": "Medium",
                "text": "To prove that a new problem Y is NP-hard, which polynomial-time reduction must you demonstrate?",
                "option_a": "Reduce a known NP-hard problem X to problem Y (X <=p Y)",
                "option_b": "Reduce problem Y to a known NP-hard problem X (Y <=p X)",
                "option_c": "Reduce problem Y to 2-SAT",
                "option_d": "Reduce problem Y to sorting integers",
                "correct_option": "A",
                "explanation": "If a known hard problem X reduces to Y in polynomial time (X <=p Y), then an efficient solver for Y would solve X, proving Y is at least as hard as X."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "VERTEX-COVER", "difficulty": "Medium",
                "text": "What is the relationship between an Independent Set of size k and a Vertex Cover in an undirected graph G = (V, E)?",
                "option_a": "S is an independent set of G if and only if V \\ S is a vertex cover of size |V| - k",
                "option_b": "A vertex cover must always be disjoint from an independent set",
                "option_c": "Every vertex cover has size equal to the chromatic number",
                "option_d": "An independent set is always empty if a vertex cover exists",
                "correct_option": "A",
                "explanation": "Because an independent set has no edges between its vertices, every edge in E must have at least one endpoint in the complement set V \\ S, forming a vertex cover."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Vertex-cover 2-approximation", "difficulty": "Medium",
                "text": "How does the simple maximal-matching algorithm achieve a 2-approximation for the Minimum Vertex Cover problem?",
                "option_a": "It finds a maximal matching M and takes all endpoints of edges in M; since OPT must pick at least 1 endpoint per edge, |C| = 2|M| <= 2 * OPT",
                "option_b": "By sorting vertices by degree and picking the top half",
                "option_c": "By running DFS and picking all visited vertices",
                "option_d": "By converting the graph into a bipartite graph",
                "correct_option": "A",
                "explanation": "No two edges in matching M share a vertex, so OPT must take at least one vertex from each matched edge: OPT >= |M|. Our cover C has size 2|M| <= 2 * OPT."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "3-SAT", "difficulty": "Easy",
                "text": "While 3-SAT is NP-complete, what is the computational complexity of the 2-SAT problem?",
                "option_a": "Solvable in linear time O(V + E) using strongly connected components (Kosaraju/Tarjan on implication graph)",
                "option_b": "NP-hard and not approximable",
                "option_c": "Exponential time O(2^N)",
                "option_d": "Undecidable",
                "correct_option": "A",
                "explanation": "2-SAT can be represented as an implication graph where (a or b) becomes (~a -> b) and (~b -> a). It is satisfiable iff no variable and its negation belong to the same SCC."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Approximation ratio", "difficulty": "Medium",
                "text": "For a minimization problem with optimal cost OPT, an algorithm returning solution cost C has an approximation ratio alpha if:",
                "option_a": "C / OPT <= alpha for all problem instances (alpha >= 1)",
                "option_b": "OPT / C <= alpha where alpha < 1",
                "option_c": "C - OPT <= 0",
                "option_d": "C * OPT = alpha",
                "correct_option": "A",
                "explanation": "In minimization problems, the approximation ratio alpha is max(C/OPT, OPT/C) which simplifies to C <= alpha * OPT."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "PTAS", "difficulty": "Hard",
                "text": "What is the difference between a PTAS (Polynomial-Time Approximation Scheme) and an FPTAS (Fully Polynomial-Time Approximation Scheme)?",
                "option_a": "An FPTAS requires running time polynomial in both input size N and 1/epsilon, whereas a PTAS only requires polynomial time in N for fixed epsilon",
                "option_b": "PTAS applies only to maximization while FPTAS applies to minimization",
                "option_c": "FPTAS gives exact answers while PTAS gives approximate answers",
                "option_d": "PTAS runs in linear time while FPTAS runs in exponential time",
                "correct_option": "A",
                "explanation": "In PTAS, runtime can be O(N^(1/epsilon)) which is polynomial for constant epsilon. In FPTAS, runtime must be polynomial in (1/epsilon) as well, e.g. O((1/epsilon)^2 * N^3)."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "KNAPSACK", "difficulty": "Hard",
                "text": "The 0/1 Knapsack problem is NP-hard, but possesses an FPTAS. What property allows this FPTAS to exist?",
                "option_a": "Dynamic programming on scaled profit values where profit bounds can be trimmed in polynomial time",
                "option_b": "Knapsack weights are always powers of 2",
                "option_c": "Greedy ratio sorting gives exact answers on all integer sets",
                "option_d": "All items can be split into fractional parts",
                "correct_option": "A",
                "explanation": "By scaling profits by a factor K = epsilon * P_max / N, the pseudo-polynomial DP runs in O(N^2 * (1/epsilon)), yielding a valid FPTAS."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Parameterized complexity", "difficulty": "Hard",
                "text": "What does it mean for a problem parameterized by k to be Fixed-Parameter Tractable (FPT)?",
                "option_a": "It can be solved in time f(k) * N^O(1), where f is an arbitrary computable function depending only on parameter k",
                "option_b": "It can be solved in O(N^k) time",
                "option_c": "The parameter k must equal the number of vertices",
                "option_d": "It can only be solved if P = NP",
                "correct_option": "A",
                "explanation": "FPT isolates exponential growth strictly to parameter k (e.g. 2^k * N), remaining polynomial in input size N for any small fixed value of k."
            },
            {
                "course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation",
                "topic": "Kernelization", "difficulty": "Hard",
                "text": "In parameterized algorithms, what is the goal of a Kernelization reduction algorithm?",
                "option_a": "Preprocess the problem instance in polynomial time into an equivalent instance whose size is bounded strictly by a function of parameter k",
                "option_b": "Multiply all edge weights by the kernel coefficient",
                "option_c": "Transform an undirected graph into an operating system kernel",
                "option_d": "Ensure all vertices have odd degrees",
                "correct_option": "A",
                "explanation": "Kernelization uses polynomial-time data reduction rules to replace (I, k) with an equivalent smaller instance (I', k') where |I'| <= g(k)."
            },

            # ==================== CO6: Randomized and Parallel Algorithms ====================
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Las Vegas algorithms", "difficulty": "Easy",
                "text": "What is the expected running time of Randomized Quicksort on an input array of N distinct elements?",
                "option_a": "O(N log N)",
                "option_b": "O(N^2)",
                "option_c": "O(N)",
                "option_d": "O(log N)",
                "correct_option": "A",
                "explanation": "Randomized Quicksort chooses pivots uniformly at random, avoiding adversarial worst-case inputs and guaranteeing O(N log N) expected comparisons."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Monte Carlo algorithms", "difficulty": "Medium",
                "text": "In the Miller-Rabin randomized primality test, if an odd integer n is composite, what is the probability that a randomly chosen base a acts as a witness to its compositeness?",
                "option_a": "At least 3/4",
                "option_b": "At most 1/4",
                "option_c": "Exactly 1/2",
                "option_d": "0",
                "correct_option": "A",
                "explanation": "Rabin proved that for any composite odd integer n, at least 3/4 of the bases a in [2, n-2] are Miller-Rabin witnesses to n's compositeness."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Reservoir sampling", "difficulty": "Medium",
                "text": "When using Reservoir Sampling (Algorithm R) to select 1 item uniformly at random from a data stream of unknown length N, with what probability is the k-th item chosen into the reservoir?",
                "option_a": "1 / k",
                "option_b": "1 / N^2",
                "option_c": "1 / 2",
                "option_d": "(k - 1) / k",
                "correct_option": "A",
                "explanation": "At step k, the incoming item replaces the reservoir with probability 1/k. By induction, every item from 1 to N has an equal final probability 1/N of being in the reservoir."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Work/span model", "difficulty": "Medium",
                "text": "In the Work-Span parallel algorithm model, what do T1 and T_infinity represent?",
                "option_a": "T1 is Work (total time on 1 processor); T_infinity is Span (critical path length on an infinite number of processors)",
                "option_b": "T1 is the algorithm startup time; T_infinity is shutdown time",
                "option_c": "T1 is memory consumption; T_infinity is network bandwidth",
                "option_d": "T1 is average time; T_infinity is worst-case time",
                "correct_option": "A",
                "explanation": "Work T1 is the total computational work across all nodes in the DAG. Span T_infinity is the length of the longest dependency path (critical path)."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Brent's theorem", "difficulty": "Hard",
                "text": "According to Brent's Theorem, what upper bound does a parallel algorithm with work W and span S achieve when executed on P processors?",
                "option_a": "T_P <= W / P + S",
                "option_b": "T_P = W * S * P",
                "option_c": "T_P >= W * P",
                "option_d": "T_P = S / P",
                "correct_option": "A",
                "explanation": "Brent's scheduling theorem proves that execution time on P processors satisfies T_P <= (W - S)/P + S < W/P + S."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Parallel reduce", "difficulty": "Easy",
                "text": "What are the Work and Span of a balanced tree parallel reduction (e.g. summing N numbers) across processors?",
                "option_a": "Work = O(N), Span = O(log N)",
                "option_b": "Work = O(N log N), Span = O(N)",
                "option_c": "Work = O(1), Span = O(N)",
                "option_d": "Work = O(log N), Span = O(1)",
                "correct_option": "A",
                "explanation": "Summing N items takes N - 1 total operations (Work = O(N)), while the binary tree tree height gives critical path Span = O(log N)."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Parallel scan", "difficulty": "Hard",
                "text": "The Blelloch parallel scan (prefix sum) algorithm computes all prefix sums in Work = O(N) and Span = O(log N). What are its two conceptual phases?",
                "option_a": "Up-sweep (reduce tree) phase and Down-sweep (distribution) phase",
                "option_b": "Topological sort phase and DFS back-edge phase",
                "option_c": "Radix sorting phase and merge phase",
                "option_d": "Hashing phase and linear probe phase",
                "correct_option": "A",
                "explanation": "Blelloch's work-efficient scan performs an up-sweep tree reduction to accumulate partial sums, followed by a down-sweep tree traversal to distribute prefixes."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Universal hash families", "difficulty": "Hard",
                "text": "A family of hash functions H mapping universe U to table {0..m-1} is 2-universal if for any two distinct keys x != y:",
                "option_a": "Pr[h(x) = h(y)] <= 1 / m for a randomly chosen function h in H",
                "option_b": "Pr[h(x) = h(y)] = 0 always",
                "option_c": "h(x) + h(y) = m",
                "option_d": "m must be a power of 2",
                "correct_option": "A",
                "explanation": "A universal hash family guarantees that collision probability between any two distinct keys is at most 1/m, mimicking ideal random hashing."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Data-parallel", "difficulty": "Easy",
                "text": "Which characteristic identifies an embarrassingly parallel (or data-parallel) computation?",
                "option_a": "Computations on distinct data elements are completely independent and require no communication or synchronization",
                "option_b": "Every step requires synchronization with a central barrier",
                "option_c": "It can only run on quantum processors",
                "option_d": "The critical path span equals the total work",
                "correct_option": "A",
                "explanation": "Embarrassingly parallel workloads have zero dependency between tasks (e.g. mapping an arithmetic function over an array), achieving linear speedup with P processors."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Expected running time", "difficulty": "Medium",
                "text": "By linearity of expectation, if random variable X = sum(X_i), what property holds regardless of whether the X_i are independent?",
                "option_a": "E[X] = sum(E[X_i])",
                "option_b": "E[X] = product(E[X_i])",
                "option_c": "E[X] must be an integer",
                "option_d": "Var(X) = sum(Var(X_i)) always",
                "correct_option": "A",
                "explanation": "Linearity of expectation states that the expected value of a sum of random variables is always the sum of their individual expectations, without requiring independence."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Perfect hashing", "difficulty": "Hard",
                "text": "In the Fredman-Komlos-Szemeredi (FKS) two-level perfect hashing scheme for static sets of N keys, what space and query time bounds are achieved?",
                "option_a": "O(N) total space with O(1) worst-case lookup time without any collisions",
                "option_b": "O(N^2) space with O(log N) lookup time",
                "option_c": "O(1) space with O(N) lookup time",
                "option_d": "O(N log N) space with O(log N) lookup time",
                "correct_option": "A",
                "explanation": "FKS uses a primary hash table of size N and secondary tables of size s_i^2 where sum(s_i^2) = O(N), guaranteeing zero collisions and O(1) worst-case lookups."
            },
            {
                "course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms",
                "topic": "Parallel sorting", "difficulty": "Medium",
                "text": "What is the Span (critical path depth) of Batcher's Bitonic Sort network for sorting N numbers in parallel?",
                "option_a": "O(log^2 N)",
                "option_b": "O(N)",
                "option_c": "O(N log N)",
                "option_d": "O(1)",
                "correct_option": "A",
                "explanation": "Bitonic sort has log(N) stages, and each stage has up to log(N) comparison steps, leading to a span depth of O(log^2 N)."
            },
        ]

        question_objs = []
        for q in raw_questions:
            q_inst = Question(**q)
            db.add(q_inst)
            question_objs.append(q_inst)
        db.commit()
        print(f"Seeded {len(question_objs)} questions successfully.")

        print("Seeding Flashcards...")
        flashcards_data = [
            # CO1
            {"course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System", "topic": "Pattern search", "difficulty": "Easy",
             "front_question": "Why is KMP preferred over Naive search for streaming text?",
             "back_answer": "KMP uses a precomputed failure function (LPS array) so the text pointer never moves backwards, guaranteeing linear O(N + M) single-pass processing."},
            {"course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System", "topic": "Fuzzy matching/edit distance", "difficulty": "Medium",
             "front_question": "What is the problem signature for choosing Dynamic Programming in sequence comparison?",
             "back_answer": "Presence of overlapping subproblems and optimal substructure across prefixes: computing alignment of S[1..i] and T[1..j] relies on cached answers for smaller prefix pairs."},
            {"course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System", "topic": "Max-flow", "difficulty": "Medium",
             "front_question": "How do you model an assignment problem with capacity constraints using Max-Flow?",
             "back_answer": "Create a source vertex s connected to agents, agents connected to tasks with capacity constraints, and tasks connected to sink t. The maximum flow yields the optimal assignment."},
            {"course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System", "topic": "NP-hard approximation", "difficulty": "Hard",
             "front_question": "What should be your algorithmic strategy when a problem signature indicates NP-hardness?",
             "back_answer": "Since polynomial exact solutions are impossible (unless P=NP), select an approximation algorithm with a provable ratio, a PTAS/FPTAS scheme, or fixed-parameter tractability (FPT)."},
            {"course_outcome": "CO1", "module_name": "Module 1 — TextHack as a System", "topic": "Suffix structures", "difficulty": "Hard",
             "front_question": "Why use a Suffix Array + LCP array instead of a full Suffix Trie?",
             "back_answer": "An uncompressed suffix trie requires O(N^2) memory and heavy pointer overhead. A Suffix Array + LCP stores all information in only O(N) integer arrays."},

            # CO2
            {"course_outcome": "CO2", "module_name": "Module 2 — String Algorithms", "topic": "KMP", "difficulty": "Medium",
             "front_question": "What is the failure function in KMP and what does lps[i] hold?",
             "back_answer": "lps[i] holds the length of the longest proper prefix of pattern[0..i] that is also a suffix of pattern[0..i]. It enables skipping redundant character matches upon a mismatch."},
            {"course_outcome": "CO2", "module_name": "Module 2 — String Algorithms", "topic": "Z-function", "difficulty": "Medium",
             "front_question": "What does Z[i] represent in the Z-algorithm?",
             "back_answer": "Z[i] is the length of the longest common prefix between string S and the suffix starting at index i of S. The Z-array is computed in linear O(N) time."},
            {"course_outcome": "CO2", "module_name": "Module 2 — String Algorithms", "topic": "Rabin-Karp", "difficulty": "Easy",
             "front_question": "How does Rabin-Karp achieve O(1) rolling hash updates?",
             "back_answer": "H_next = (BASE * (H_curr - S[i] * BASE^(M-1)) + S[i+M]) mod MOD. Removing the leading character and appending the trailing character is done via O(1) arithmetic operations."},
            {"course_outcome": "CO2", "module_name": "Module 2 — String Algorithms", "topic": "Kasai algorithm", "difficulty": "Hard",
             "front_question": "What invariant allows Kasai's algorithm to compute the LCP array in O(N)?",
             "back_answer": "If the LCP of suffix i is k, then the LCP of suffix i+1 is at least k - 1. Because the common prefix length decreases by at most 1 each step, the total comparisons are bounded by 2N."},
            {"course_outcome": "CO2", "module_name": "Module 2 — String Algorithms", "topic": "Suffix automaton", "difficulty": "Hard",
             "front_question": "What is the size complexity of a Suffix Automaton for string length N?",
             "back_answer": "At most 2N - 1 states and at most 3N - 4 transitions. It represents all distinct substrings in linear space and recognizes any substring in O(length) time."},

            # CO3
            {"course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming", "topic": "Levenshtein edit distance", "difficulty": "Easy",
             "front_question": "What is the state transition for Levenshtein edit distance DP[i][j]?",
             "back_answer": "If S[i-1] == T[j-1]: DP[i][j] = DP[i-1][j-1]. Otherwise: DP[i][j] = 1 + min(DP[i-1][j] (delete), DP[i][j-1] (insert), DP[i-1][j-1] (replace))."},
            {"course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming", "topic": "Needleman-Wunsch", "difficulty": "Medium",
             "front_question": "What is the difference between Needleman-Wunsch and Smith-Waterman?",
             "back_answer": "Needleman-Wunsch aligns entire sequences globally (allowing negative scores). Smith-Waterman resets negative values to 0 to find the highest-scoring local alignment region."},
            {"course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming", "topic": "Interval DP", "difficulty": "Medium",
             "front_question": "How are subproblems ordered in Interval DP like Matrix Chain Multiplication?",
             "back_answer": "By interval length L from 2 up to N. A larger interval [i, j] is solved by partitioning at split point k (i <= k < j) using solutions already computed for smaller lengths."},
            {"course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming", "topic": "Bitmask DP", "difficulty": "Hard",
             "front_question": "How does Held-Karp solve TSP using Bitmask DP in O(2^N * N^2)?",
             "back_answer": "DP(mask, u) = min cost of visiting the subset of cities in 'mask', ending at city u. Transition: DP(mask | (1<<v), v) = min over u of (DP(mask, u) + dist[u][v])."},
            {"course_outcome": "CO3", "module_name": "Module 3 — Advanced Dynamic Programming", "topic": "SOS DP", "difficulty": "Hard",
             "front_question": "Why is SOS (Sum Over Subsets) DP O(N * 2^N) instead of O(3^N)?",
             "back_answer": "Instead of naively enumerating all submasks for each mask, SOS DP uses bitwise prefix sums across one bit dimension at a time: DP[i][mask] = DP[i-1][mask] + (DP[i-1][mask ^ 2^i] if bit i is on)."},

            # CO4
            {"course_outcome": "CO4", "module_name": "Module 4 — Network Flow", "topic": "Ford-Fulkerson", "difficulty": "Easy",
             "front_question": "What is an augmenting path in a network flow residual graph?",
             "back_answer": "A simple directed path from source s to sink t in the residual graph where every edge has residual capacity c_f(u, v) > 0."},
            {"course_outcome": "CO4", "module_name": "Module 4 — Network Flow", "topic": "Edmonds-Karp", "difficulty": "Medium",
             "front_question": "Why does BFS in Edmonds-Karp guarantee O(V * E^2) running time?",
             "back_answer": "BFS always selects the shortest augmenting path (fewest edges). The distance from s to any vertex in the residual graph increases monotonically, bounding total augmentations to O(VE)."},
            {"course_outcome": "CO4", "module_name": "Module 4 — Network Flow", "topic": "Max-flow/min-cut", "difficulty": "Easy",
             "front_question": "What is the Max-Flow Min-Cut Theorem?",
             "back_answer": "The maximum flow value from source s to sink t in a capacitated network equals the minimum capacity of an s-t cut that separates s and t."},
            {"course_outcome": "CO4", "module_name": "Module 4 — Network Flow", "topic": "Konig's theorem", "difficulty": "Hard",
             "front_question": "What is Konig's Theorem in Bipartite Graphs?",
             "back_answer": "In any bipartite graph, the size of the Maximum Matching is exactly equal to the size of the Minimum Vertex Cover."},
            {"course_outcome": "CO4", "module_name": "Module 4 — Network Flow", "topic": "Dinic intuition", "difficulty": "Hard",
             "front_question": "What are the two alternating phases of Dinic's Algorithm?",
             "back_answer": "1. BFS builds a level graph (assigning distance from source). 2. DFS finds and pushes blocking flows along admissible level-edges until no augmenting paths of that length exist."},

            # CO5
            {"course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation", "topic": "P vs NP", "difficulty": "Easy",
             "front_question": "What is the definition of class P and class NP?",
             "back_answer": "P: Decision problems solvable in polynomial time by a deterministic Turing machine. NP: Decision problems whose candidate solutions can be verified in polynomial time."},
            {"course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation", "topic": "Cook-Levin theorem", "difficulty": "Medium",
             "front_question": "What is the significance of the Cook-Levin Theorem?",
             "back_answer": "It proved that Boolean Satisfiability (SAT) is NP-complete, establishing the foundational benchmark to prove all other NP-complete problems via polynomial reduction."},
            {"course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation", "topic": "Vertex-cover 2-approximation", "difficulty": "Medium",
             "front_question": "How does the Maximal Matching algorithm achieve a 2-approximation for Vertex Cover?",
             "back_answer": "Find a maximal matching M and pick both endpoints of each edge. Since OPT must select at least one vertex from each disjoint edge, |Cover| = 2|M| <= 2 * OPT."},
            {"course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation", "topic": "PTAS", "difficulty": "Hard",
             "front_question": "What is a PTAS (Polynomial-Time Approximation Scheme)?",
             "back_answer": "An algorithm that takes an instance and an error parameter epsilon > 0, producing a solution within factor (1 + epsilon) of OPT in polynomial time in N for any fixed epsilon."},
            {"course_outcome": "CO5", "module_name": "Module 5 — NP-Completeness and Approximation", "topic": "Kernelization", "difficulty": "Hard",
             "front_question": "What is kernelization in parameterized complexity?",
             "back_answer": "A polynomial-time algorithm that reduces an input instance (I, k) to an equivalent smaller instance (I', k') whose size |I'| is bounded strictly by a function g(k) of parameter k."},

            # CO6
            {"course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms", "topic": "Las Vegas algorithms", "difficulty": "Easy",
             "front_question": "What defines a Las Vegas randomized algorithm?",
             "back_answer": "It always returns the correct answer; only its running time is a random variable (e.g. Randomized Quicksort)."},
            {"course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms", "topic": "Monte Carlo algorithms", "difficulty": "Medium",
             "front_question": "What defines a Monte Carlo randomized algorithm?",
             "back_answer": "It has deterministic running time, but may produce an incorrect answer with a bounded error probability (e.g. Miller-Rabin primality test)."},
            {"course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms", "topic": "Work/span model", "difficulty": "Medium",
             "front_question": "What are Work (T1) and Span (T_infinity) in parallel computing?",
             "back_answer": "Work T1 is the total execution time on 1 processor (total computational operations). Span T_infinity is the critical path length on infinite processors."},
            {"course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms", "topic": "Brent's theorem", "difficulty": "Hard",
             "front_question": "What is Brent's Theorem for parallel execution?",
             "back_answer": "T_P <= W / P + S. It bounds the running time on P processors by total work W divided by P plus the critical path span S."},
            {"course_outcome": "CO6", "module_name": "Module 6 — Randomized and Parallel Algorithms", "topic": "Parallel scan", "difficulty": "Hard",
             "front_question": "What is the Blelloch Parallel Scan algorithm?",
             "back_answer": "A work-efficient parallel prefix-sum algorithm with Work O(N) and Span O(log N), executed in an up-sweep reduce phase and a down-sweep distribution phase."},
        ]

        for fc in flashcards_data:
            f_inst = Flashcard(**fc)
            db.add(f_inst)
        db.commit()
        print(f"Seeded {len(flashcards_data)} flashcards successfully.")

        print("Seeding Sample Historical Exam Attempts...")
        # Create completed attempts for students across various exams
        all_exams = db.query(Exam).all()
        all_students = db.query(Student).all()

        # Seed sample attempts to generate rich analytics data
        sample_attempts_count = 0
        for student in all_students:
            # Each student takes 2-3 exams
            sample_exams = random.sample(all_exams, k=min(3, len(all_exams)))
            for exam_idx, exam in enumerate(sample_exams):
                # Fetch 5 questions from this exam's CO
                co_questions = db.query(Question).filter(Question.course_outcome == exam.course_outcome).all()
                if len(co_questions) < 5:
                    continue
                selected_5 = random.sample(co_questions, 5)

                # Randomize student performance (e.g. 3 to 5 correct answers)
                target_score = random.choice([3.0, 4.0, 4.0, 5.0, 2.0, 4.0])
                num_correct = int(target_score)

                # Attempt date in the past
                days_ago = random.randint(1, 20)
                attempt_time = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(1, 10))

                attempt = ExamAttempt(
                    exam_id=exam.id,
                    student_id=student.id,
                    started_at=attempt_time,
                    submitted_at=attempt_time + timedelta(minutes=random.randint(4, 9)),
                    is_submitted=True,
                    score=target_score,
                    total_marks=5.0,
                    accuracy_pct=(num_correct / 5.0) * 100.0,
                    time_taken_seconds=random.randint(150, 450)
                )
                db.add(attempt)
                db.flush()

                # Build attempt questions and answers
                for q_order, q in enumerate(selected_5, start=1):
                    shuffled_opts, orig_map = randomize_question_options(
                        q.option_a, q.option_b, q.option_c, q.option_d
                    )

                    aq = AttemptQuestion(
                        attempt_id=attempt.id,
                        question_id=q.id,
                        question_order=q_order,
                        option_a_text=shuffled_opts['A'],
                        option_b_text=shuffled_opts['B'],
                        option_c_text=shuffled_opts['C'],
                        option_d_text=shuffled_opts['D'],
                        option_a_orig=orig_map['A'],
                        option_b_orig=orig_map['B'],
                        option_c_orig=orig_map['C'],
                        option_d_orig=orig_map['D']
                    )
                    db.add(aq)

                    # Determine if this question is answered correctly
                    is_corr = q_order <= num_correct
                    correct_display_key = None
                    for disp_key, orig_key in orig_map.items():
                        if orig_key == q.correct_option:
                            correct_display_key = disp_key
                            break

                    if is_corr:
                        selected_display = correct_display_key
                    else:
                        # Choose a wrong display key
                        wrong_keys = [k for k in ['A', 'B', 'C', 'D'] if k != correct_display_key]
                        selected_display = random.choice(wrong_keys)

                    time_spent = random.randint(20, 65)
                    ans = AttemptAnswer(
                        attempt_id=attempt.id,
                        question_id=q.id,
                        selected_option=selected_display,
                        is_correct=is_corr,
                        time_taken_seconds=time_spent
                    )
                    db.add(ans)

                sample_attempts_count += 1

        db.commit()
        print(f"Seeded {sample_attempts_count} historical attempts successfully.")

        print("Seeding Complete!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
