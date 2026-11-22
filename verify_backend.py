"""
Unit tests / verification script for CareerCraft backend logic.
Validates Student, Company, StudentManager, CompanyManager, and Eligibility Checker.
"""
from student import Student
from company import Company
from student_manager import StudentManager
from company_manager import CompanyManager
from eligibility import check_eligibility, find_eligible_students
import os

def test_all():
    print("=== Testing CareerCraft Core Functionality ===")

    # 1. Test Student validation & creation
    is_valid, errors = Student.validate_details(
        student_id="S999",
        name="Test Student",
        email="test@univ.edu",
        branch="CSE",
        cgpa="8.5",
        backlogs="0",
        skills="Java, python, JAVA , AWS",
        graduation_year="2027"
    )
    assert is_valid, f"Validation failed: {errors}"
    s = Student("S999", "Test Student", "test@univ.edu", "CSE", 8.5, 0, ["Java", "python", "JAVA", "AWS"], 2027)
    assert "Java" in s.skills and "AWS" in s.skills
    assert len([x for x in s.skills if x.lower() == "java"]) == 1, "Duplicate normalized skill found"
    print("[PASS] Student validation and skill normalization")

    # 2. Test Company validation & creation
    is_c_valid, c_errors = Company.validate_details(
        company_id="C999",
        company_name="TestCorp",
        job_title="Software Dev",
        min_cgpa="7.0",
        eligible_branches=["CSE", "it"],
        required_skills=["Java", "SQL"],
        max_backlogs="0",
        eligible_graduation_years=[2027]
    )
    assert is_c_valid, f"Company validation failed: {c_errors}"
    c = Company("C999", "TestCorp", "Software Dev", 7.0, ["CSE", "it"], ["Java", "SQL"], 0, [2027])
    assert "IT" in c.eligible_branches
    print("[PASS] Company validation and branch normalization")

    # 3. Test Eligibility cases based on prompt sample records:
    # Company TechNova: min_cgpa 7.0, branches [IT, CSE], backlogs 0, skills [Java, SQL], grad_year 2027
    technova = Company("C201", "TechNova", "Associate Software Engineer", 7.0, ["IT", "CSE"], ["Java", "SQL"], 0, [2027])

    # Rahul: IT, CGPA 8.5, no backlogs, Java and SQL, 2027 -> ELIGIBLE
    rahul = Student("S101", "Rahul", "rahul@test.com", "IT", 8.5, 0, ["Java", "SQL"], 2027)
    res_rahul = check_eligibility(rahul, technova)
    assert res_rahul["is_eligible"] is True, "Rahul should be eligible"
    print("[PASS] Rahul eligibility verified: Eligible")

    # Priya: CSE, CGPA 6.8, no backlogs, Java and SQL, 2027 -> INELIGIBLE (CGPA < 7.0)
    priya = Student("S102", "Priya", "priya@test.com", "CSE", 6.8, 0, ["Java", "SQL"], 2027)
    res_priya = check_eligibility(priya, technova)
    assert res_priya["is_eligible"] is False, "Priya should be ineligible due to CGPA"
    assert any("CGPA" in r for r in res_priya["reasons"]), "Priya should fail CGPA criterion"
    print(f"[PASS] Priya eligibility verified: Ineligible ({res_priya['reasons']})")

    # Kiran: ECE, CGPA 8.2, no backlogs, Java and SQL, 2027 -> INELIGIBLE (Branch ECE not in [IT, CSE])
    kiran = Student("S104", "Kiran", "kiran@test.com", "ECE", 8.2, 0, ["Java", "SQL"], 2027)
    res_kiran = check_eligibility(kiran, technova)
    assert res_kiran["is_eligible"] is False, "Kiran should be ineligible due to branch"
    assert any("Branch" in r for r in res_kiran["reasons"]), "Kiran should fail Branch criterion"
    print(f"[PASS] Kiran eligibility verified: Ineligible ({res_kiran['reasons']})")

    # Arjun: IT, CGPA 8.0, 1 backlog, Java and SQL, 2027 -> INELIGIBLE (Backlog 1 > 0)
    arjun = Student("S105", "Arjun", "arjun@test.com", "IT", 8.0, 1, ["Java", "SQL"], 2027)
    res_arjun = check_eligibility(arjun, technova)
    assert res_arjun["is_eligible"] is False, "Arjun should be ineligible due to backlogs"
    assert any("backlog" in r.lower() for r in res_arjun["reasons"]), "Arjun should fail Backlog criterion"
    print(f"[PASS] Arjun eligibility verified: Ineligible ({res_arjun['reasons']})")

    # Missing Skills Test
    missing_skill_stud = Student("S108", "NoSQL Student", "nosql@test.com", "IT", 8.0, 0, ["Java"], 2027)
    res_skill = check_eligibility(missing_skill_stud, technova)
    assert res_skill["is_eligible"] is False
    assert "SQL" in res_skill["missing_skills"]
    print(f"[PASS] Missing skills check verified: Missing {res_skill['missing_skills']}")

    # 4. Test StudentManager JSON persistence & sorting
    sm = StudentManager()
    assert len(sm.get_all_students()) >= 5
    sorted_cgpa = sm.sort_students(sort_by="cgpa", reverse=True)
    assert sorted_cgpa[0].cgpa >= sorted_cgpa[-1].cgpa
    print(f"[PASS] StudentManager loaded {len(sm.get_all_students())} students and sorted by CGPA correctly")

    # 5. Test CompanyManager JSON persistence
    cm = CompanyManager()
    assert len(cm.get_all_companies()) >= 3
    print(f"[PASS] CompanyManager loaded {len(cm.get_all_companies())} companies correctly")

    print("\nALL BACKEND UNIT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all()
