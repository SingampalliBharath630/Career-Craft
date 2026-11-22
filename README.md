# CareerCraft – Student Placement Readiness Portal

**CareerCraft** is a complete, beginner-friendly, and modular Student Placement Readiness system built in Python and Streamlit. It manages student profiles, technical skillsets, and academic metrics, evaluates student eligibility against corporate recruitment benchmarks, and persists all records cleanly in JSON format without reliance on heavy databases or external paid services.

---

## 🌟 Key Features

1. **Placement Readiness Dashboard**:
   - Total students registered, total companies, and active corporate openings.
   - Dynamic real-time calculation of eligible candidates and qualification rates for chosen jobs.
   - Visual branch-wise and graduation-year student distributions.

2. **Student Profile Management**:
   - Register students with complete validation: Student ID, Name, Email format, Branch, CGPA (0.0–10.0), Backlogs, Skills, and Graduation Year.
   - Tabular directory view.
   - Substring search and edit capabilities.
   - Safe deletion with immediate persistence.

3. **Company & Criteria Management**:
   - Configure corporate job openings: Company ID, Name, Job Role, Minimum CGPA, Eligible Branches, Maximum Allowed Backlogs, Eligible Graduation Batches, and Mandatory Technical Skills.
   - View, update, or remove job criteria.

4. **Dynamic Placement Eligibility Engine**:
   - Zero hardcoded results: evaluates students against company requirements dynamically.
   - Multi-criteria diagnostics:
     - CGPA qualification
     - Department / Branch matching
     - Active backlog clearance
     - Graduation year batch matching
     - Case-insensitive normalized technical skill comparison (e.g. `java`, `Java`, `JAVA` treated uniformly)
   - Diagnostic breakdown explaining exact reasons for disqualification and missing mandatory skills.

5. **Advanced Search, Filter, and Sort**:
   - Filter by Department, Minimum CGPA, Skill possession, Maximum backlogs, and Graduation Year.
   - Sort by CGPA (descending/ascending), Name, Student ID, Backlogs, or Graduation Year.

6. **Robust File Handling & Persistent Storage**:
   - All records stored in `data/students.json` and `data/companies.json`.
   - Data persists across server reboots.
   - Safe fallbacks for missing or corrupt files.

---

## 🧱 Demonstration of the 9 Core Python Programming Concepts

| Concept | File / Implementation | Explanation |
| :--- | :--- | :--- |
| **1. OOP and Classes** | `student.py`, `company.py`, `student_manager.py`, `company_manager.py` | Defined `Student` and `Company` classes with constructors (`__init__`), attributes, static validation methods, and serialization methods (`to_dict()`, `from_dict()`). |
| **2. Functions** | `eligibility.py`, `file_handler.py`, managers | Reusable, modular functions such as `check_eligibility()`, `find_eligible_students()`, `load_json()`, `save_json()`, etc. |
| **3. Strings** | `student.py`, `eligibility.py`, `company.py` | Regex email validation, `.strip()`, `.upper()`, `.lower()`, case-insensitive search and skill normalization (`Java` == `JAVA`). |
| **4. Dictionaries** | All modules & JSON files | Key-value records for student and company data, structured diagnostic response dictionaries in `check_eligibility()`. |
| **5. Sorting** | `student_manager.py`, `app.py` | Python's `sorted()` function with `key=lambda ...` and `reverse` flags to sort by CGPA, Name, or Batch. |
| **6. Filtering** | `student_manager.py`, `eligibility.py`, `app.py` | List comprehensions filtering records by branch, minimum CGPA threshold, backlogs, and specific skills. |
| **7. File Handling** | `file_handler.py`, `data/*.json` | `open()`, `json.dump()`, `json.load()` with error handling for non-existent or empty files and persistent write-backs on mutation. |
| **8. Conditional Statements** | `eligibility.py`, validation methods | `if`, `elif`, and `else` blocks checking input validity ranges (0.0 to 10.0 CGPA) and multi-factor eligibility logic. |
| **9. Lists** | Throughout application | Lists for storing students, company records, technical skills, eligible candidates, ineligibility reasons, and batch years. |

---

## 📁 Project Folder Structure

```
careercraft/
├── app.py                  # Main Streamlit Web Application
├── student.py              # Student class model and validation
├── company.py              # Company class model and validation
├── eligibility.py          # Dynamic eligibility evaluation engine
├── student_manager.py      # Student CRUD, filter, and sorting operations
├── company_manager.py      # Company CRUD operations
├── file_handler.py         # Safe JSON read/write persistence
├── verify_backend.py       # Automated unit tests for core logic
├── requirements.txt        # Python dependency manifest
├── README.md               # Documentation and execution instructions
└── data/
    ├── students.json       # JSON file containing persistent student records
    └── companies.json      # JSON file containing persistent company records
```

---

## 🚀 Execution Instructions (Windows PowerShell in VS Code)

### Step 1: Open Terminal in Project Directory
In Visual Studio Code, open the folder `c:\careercraft` and launch PowerShell (`Ctrl + ~`).

### Step 2: (Optional) Create & Activate a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 4: Run Backend Unit Tests
To verify all core logic and sample eligibility tests:
```powershell
python verify_backend.py
```

### Step 5: Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
Streamlit will automatically open your browser at `http://localhost:8501`.

---

## 🧪 Test Cases & Sample Data

### Configured Sample Company
**TechNova** (`C201`):
- Minimum CGPA: `7.0`
- Eligible Branches: `IT, CSE`
- Max Active Backlogs: `0`
- Required Skills: `Java, SQL`
- Eligible Graduation Year: `2027`

### Verified Student Test Results
| Student | Branch | CGPA | Backlogs | Skills | Year | Outcome | Diagnostics / Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Rahul Sharma** | IT | 8.5 | 0 | Java, SQL | 2027 | **ELIGIBLE** ✅ | Meets all 5 criteria |
| **Priya Patel** | CSE | 6.8 | 0 | Java, SQL | 2027 | **NOT ELIGIBLE** ❌ | CGPA 6.80 < 7.00 |
| **Sneha Reddy** | IT | 7.8 | 0 | Java, SQL | 2027 | **ELIGIBLE** ✅ | Meets all 5 criteria |
| **Kiran Rao** | ECE | 8.2 | 0 | Java, SQL | 2027 | **NOT ELIGIBLE** ❌ | Branch 'ECE' not in [CSE, IT] |
| **Arjun Verma** | IT | 8.0 | 1 | Java, SQL | 2027 | **NOT ELIGIBLE** ❌ | Active backlogs (1) > 0 |

---

## 🔒 Data Persistence Verification
1. Run `streamlit run app.py` and add a new student (e.g. `S110 - Aditi`).
2. Stop the Streamlit server (`Ctrl + C` in PowerShell).
3. Inspect `data/students.json` – the new student record will be saved.
4. Restart the application with `streamlit run app.py`. All newly added records persist cleanly.
