from typing import Dict, Any, List, Union
from student import Student
from company import Company


def check_eligibility(
    student: Union[Student, Dict[str, Any]],
    company: Union[Company, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check if a student meets all eligibility criteria for a company job role.

    Demonstrates:
    - Conditionals (if, elif, else)
    - String operations & case-insensitive skill comparison
    - List manipulations
    - Dictionary response structure

    Returns a detailed breakdown dictionary:
    {
        "is_eligible": bool,
        "reasons": List[str],              # Ineligibility explanations
        "missing_skills": List[str],       # Specific missing skills
        "criteria_results": {              # Step-by-step breakdown
            "cgpa": {"met": bool, "detail": str},
            "branch": {"met": bool, "detail": str},
            "backlogs": {"met": bool, "detail": str},
            "graduation_year": {"met": bool, "detail": str},
            "skills": {"met": bool, "detail": str}
        }
    }
    """
    # Extract student attributes whether input is Student instance or dict
    if isinstance(student, Student):
        s_name = student.name
        s_cgpa = student.cgpa
        s_branch = student.branch
        s_backlogs = student.backlogs
        s_grad_year = student.graduation_year
        s_skills = student.skills
    else:
        s_name = student.get("name", "Unknown")
        s_cgpa = float(student.get("cgpa", 0.0))
        s_branch = str(student.get("branch", "")).strip().upper()
        s_backlogs = int(student.get("backlogs", 0))
        s_grad_year = int(student.get("graduation_year", 0))
        s_skills = student.get("skills", [])

    # Extract company criteria whether input is Company instance or dict
    if isinstance(company, Company):
        c_name = company.company_name
        c_min_cgpa = company.min_cgpa
        c_branches = company.eligible_branches
        c_max_backlogs = company.max_backlogs
        c_grad_years = company.eligible_graduation_years
        c_skills = company.required_skills
    else:
        c_name = company.get("company_name", "Unknown")
        c_min_cgpa = float(company.get("min_cgpa", 0.0))
        c_branches = [str(b).strip().upper() for b in company.get("eligible_branches", [])]
        c_max_backlogs = int(company.get("max_backlogs", 0))
        c_grad_years = [int(y) for y in company.get("eligible_graduation_years", [])]
        c_skills = company.get("required_skills", [])

    reasons = []
    criteria_results = {}

    # 1. CGPA Check
    if s_cgpa >= c_min_cgpa:
        criteria_results["cgpa"] = {
            "met": True,
            "detail": f"CGPA {s_cgpa:.2f} meets minimum requirement of {c_min_cgpa:.2f}."
        }
    else:
        diff = round(c_min_cgpa - s_cgpa, 2)
        criteria_results["cgpa"] = {
            "met": False,
            "detail": f"CGPA {s_cgpa:.2f} is below minimum requirement of {c_min_cgpa:.2f} (short by {diff})."
        }
        reasons.append(f"Insufficient CGPA: {s_cgpa:.2f} < {c_min_cgpa:.2f}")

    # 2. Branch Check
    norm_c_branches = [b.upper() for b in c_branches]
    if s_branch in norm_c_branches:
        criteria_results["branch"] = {
            "met": True,
            "detail": f"Branch '{s_branch}' is eligible ({', '.join(norm_c_branches)})."
        }
    else:
        criteria_results["branch"] = {
            "met": False,
            "detail": f"Branch '{s_branch}' is not in allowed list: {', '.join(norm_c_branches)}."
        }
        reasons.append(f"Branch '{s_branch}' not eligible. Allowed: {', '.join(norm_c_branches)}")

    # 3. Active Backlogs Check
    if s_backlogs <= c_max_backlogs:
        criteria_results["backlogs"] = {
            "met": True,
            "detail": f"Active backlogs ({s_backlogs}) is within permitted limit ({c_max_backlogs})."
        }
    else:
        criteria_results["backlogs"] = {
            "met": False,
            "detail": f"Active backlogs ({s_backlogs}) exceeds maximum permitted ({c_max_backlogs})."
        }
        reasons.append(f"Active backlogs ({s_backlogs}) exceed maximum limit of {c_max_backlogs}")

    # 4. Graduation Year Check
    if s_grad_year in c_grad_years:
        criteria_results["graduation_year"] = {
            "met": True,
            "detail": f"Graduation year ({s_grad_year}) matches eligible batch ({', '.join(map(str, c_grad_years))})."
        }
    else:
        criteria_results["graduation_year"] = {
            "met": False,
            "detail": f"Graduation year ({s_grad_year}) not in eligible years ({', '.join(map(str, c_grad_years))})."
        }
        reasons.append(f"Graduation year {s_grad_year} is not eligible. Allowed: {', '.join(map(str, c_grad_years))}")

    # 5. Technical Skills Check (case-insensitive string comparison)
    student_skills_lower = {str(s).strip().lower() for s in s_skills}
    missing_skills = []

    for req_skill in c_skills:
        req_clean = str(req_skill).strip()
        if req_clean.lower() not in student_skills_lower:
            missing_skills.append(req_clean)

    if not missing_skills:
        criteria_results["skills"] = {
            "met": True,
            "detail": f"All required skills satisfied: {', '.join(c_skills)}."
        }
    else:
        criteria_results["skills"] = {
            "met": False,
            "detail": f"Missing mandatory skills: {', '.join(missing_skills)}."
        }
        reasons.append(f"Missing mandatory skills: {', '.join(missing_skills)}")

    # Final eligibility determination
    is_eligible = (len(reasons) == 0)

    return {
        "is_eligible": is_eligible,
        "reasons": reasons,
        "missing_skills": missing_skills,
        "criteria_results": criteria_results
    }


def find_eligible_students(
    students: List[Union[Student, Dict[str, Any]]],
    company: Union[Company, Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Evaluates a list of students against a company requirement.
    Returns:
    - eligible_records: List of tuples/dicts with student and eligibility result
    - ineligible_records: List of tuples/dicts with student and ineligibility reasons
    """
    eligible = []
    ineligible = []

    for student in students:
        result = check_eligibility(student, company)
        record = {
            "student": student.to_dict() if isinstance(student, Student) else student,
            "result": result
        }
        if result["is_eligible"]:
            eligible.append(record)
        else:
            ineligible.append(record)

    return eligible, ineligible
