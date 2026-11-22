import re
from typing import List, Dict, Any, Tuple


class Student:
    """
    Student class representing a candidate for campus placement.
    Demonstrates OOP, class definition, validation, encapsulation, and dictionary conversion.
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        branch: str,
        cgpa: float,
        backlogs: int,
        skills: List[str],
        graduation_year: int
    ):
        self.student_id = student_id.strip()
        self.name = name.strip()
        self.email = email.strip()
        self.branch = branch.strip().upper()
        self.cgpa = round(float(cgpa), 2)
        self.backlogs = int(backlogs)
        self.skills = self.normalize_skills(skills)
        self.graduation_year = int(graduation_year)

    @staticmethod
    def normalize_skills(skills_input: Any) -> List[str]:
        """
        String operation helper:
        Normalizes skills (strips whitespace, title cases, deduplicates while preserving order).
        Example: [' java ', 'SQL', 'JAVA'] -> ['Java', 'Sql']
        """
        if isinstance(skills_input, str):
            # Split comma separated string
            raw_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        elif isinstance(skills_input, list):
            raw_skills = [str(s).strip() for s in skills_input if str(s).strip()]
        else:
            raw_skills = []

        normalized = []
        seen = set()
        for skill in raw_skills:
            cleaned = skill.strip()
            # Canonical key for case-insensitive deduplication
            key = cleaned.lower()
            if key and key not in seen:
                seen.add(key)
                # Keep conventional readable casing: uppercase if short acronym (e.g., SQL, IT, AWS, AI), else title case
                if key.upper() in ["SQL", "AWS", "AI", "ML", "UI", "UX", "HTML", "CSS", "JS", "PHP", "API"]:
                    normalized.append(key.upper())
                else:
                    normalized.append(cleaned.capitalize())
        return normalized

    @classmethod
    def validate_details(
        cls,
        student_id: str,
        name: str,
        email: str,
        branch: str,
        cgpa: Any,
        backlogs: Any,
        skills: Any,
        graduation_year: Any
    ) -> Tuple[bool, List[str]]:
        """
        Validates student details using conditional statements and string checks.
        Returns (is_valid, list_of_error_messages).
        """
        errors = []

        # Validate Student ID
        if not student_id or not str(student_id).strip():
            errors.append("Student ID cannot be empty.")

        # Validate Name
        if not name or not str(name).strip():
            errors.append("Student Name cannot be empty.")
        elif len(str(name).strip()) < 2:
            errors.append("Student Name must be at least 2 characters long.")

        # Validate Email
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email or not re.match(email_pattern, str(email).strip()):
            errors.append("Invalid email address format (e.g., student@college.edu).")

        # Validate Branch
        if not branch or not str(branch).strip():
            errors.append("Branch/Department cannot be empty.")

        # Validate CGPA
        try:
            cgpa_val = float(cgpa)
            if cgpa_val < 0.0 or cgpa_val > 10.0:
                errors.append("CGPA must be between 0.0 and 10.0.")
        except (ValueError, TypeError):
            errors.append("CGPA must be a valid numeric decimal value.")

        # Validate Backlogs
        try:
            backlog_val = int(backlogs)
            if backlog_val < 0:
                errors.append("Backlogs cannot be negative.")
        except (ValueError, TypeError):
            errors.append("Active backlogs must be a valid non-negative integer.")

        # Validate Skills
        normalized_skills = cls.normalize_skills(skills)
        if not normalized_skills:
            errors.append("At least one technical skill must be specified.")

        # Validate Graduation Year
        try:
            year_val = int(graduation_year)
            if year_val < 2000 or year_val > 2100:
                errors.append("Graduation year must be between 2000 and 2100.")
        except (ValueError, TypeError):
            errors.append("Graduation year must be a valid 4-digit year.")

        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the student object into a dictionary for JSON serialization.
        """
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "branch": self.branch,
            "cgpa": self.cgpa,
            "backlogs": self.backlogs,
            "skills": self.skills,
            "graduation_year": self.graduation_year
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        Instantiates a Student object from a dictionary.
        """
        return cls(
            student_id=str(data.get("student_id", "")),
            name=str(data.get("name", "")),
            email=str(data.get("email", "")),
            branch=str(data.get("branch", "")),
            cgpa=float(data.get("cgpa", 0.0)),
            backlogs=int(data.get("backlogs", 0)),
            skills=data.get("skills", []),
            graduation_year=int(data.get("graduation_year", 2026))
        )
