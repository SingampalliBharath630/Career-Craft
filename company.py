from typing import List, Dict, Any, Tuple


class Company:
    """
    Company class representing a recruiting company and its placement criteria.
    Demonstrates OOP, class definition, validation, encapsulation, and dictionary conversion.
    """

    def __init__(
        self,
        company_id: str,
        company_name: str,
        job_title: str,
        min_cgpa: float,
        eligible_branches: List[str],
        required_skills: List[str],
        max_backlogs: int,
        eligible_graduation_years: List[int]
    ):
        self.company_id = company_id.strip()
        self.company_name = company_name.strip()
        self.job_title = job_title.strip()
        self.min_cgpa = round(float(min_cgpa), 2)
        self.eligible_branches = self.normalize_branches(eligible_branches)
        self.required_skills = self.normalize_skills(required_skills)
        self.max_backlogs = int(max_backlogs)
        self.eligible_graduation_years = self.normalize_years(eligible_graduation_years)

    @staticmethod
    def normalize_branches(branches_input: Any) -> List[str]:
        """Normalize branch names to uppercase and strip whitespace."""
        if isinstance(branches_input, str):
            raw = [b.strip().upper() for b in branches_input.split(",") if b.strip()]
        elif isinstance(branches_input, list):
            raw = [str(b).strip().upper() for b in branches_input if str(b).strip()]
        else:
            raw = []
        return sorted(list(set(raw)))

    @staticmethod
    def normalize_skills(skills_input: Any) -> List[str]:
        """Normalize skill names consistently."""
        if isinstance(skills_input, str):
            raw = [s.strip() for s in skills_input.split(",") if s.strip()]
        elif isinstance(skills_input, list):
            raw = [str(s).strip() for s in skills_input if str(s).strip()]
        else:
            raw = []

        normalized = []
        seen = set()
        for skill in raw:
            key = skill.lower()
            if key and key not in seen:
                seen.add(key)
                if key.upper() in ["SQL", "AWS", "AI", "ML", "UI", "UX", "HTML", "CSS", "JS", "PHP", "API"]:
                    normalized.append(key.upper())
                else:
                    normalized.append(skill.capitalize())
        return normalized

    @staticmethod
    def normalize_years(years_input: Any) -> List[int]:
        """Normalize graduation years into list of integers."""
        years = []
        if isinstance(years_input, str):
            raw = [y.strip() for y in years_input.split(",") if y.strip()]
            for item in raw:
                try:
                    years.append(int(item))
                except ValueError:
                    pass
        elif isinstance(years_input, list):
            for item in years_input:
                try:
                    years.append(int(item))
                except (ValueError, TypeError):
                    pass
        return sorted(list(set(years)))

    @classmethod
    def validate_details(
        cls,
        company_id: str,
        company_name: str,
        job_title: str,
        min_cgpa: Any,
        eligible_branches: Any,
        required_skills: Any,
        max_backlogs: Any,
        eligible_graduation_years: Any
    ) -> Tuple[bool, List[str]]:
        """
        Validates company details and criteria.
        Returns (is_valid, list_of_error_messages).
        """
        errors = []

        if not company_id or not str(company_id).strip():
            errors.append("Company ID cannot be empty.")

        if not company_name or not str(company_name).strip():
            errors.append("Company Name cannot be empty.")

        if not job_title or not str(job_title).strip():
            errors.append("Job Title cannot be empty.")

        try:
            cgpa_val = float(min_cgpa)
            if cgpa_val < 0.0 or cgpa_val > 10.0:
                errors.append("Minimum CGPA must be between 0.0 and 10.0.")
        except (ValueError, TypeError):
            errors.append("Minimum CGPA must be a valid decimal number.")

        branches = cls.normalize_branches(eligible_branches)
        if not branches:
            errors.append("At least one eligible branch must be specified.")

        skills = cls.normalize_skills(required_skills)
        if not skills:
            errors.append("At least one required technical skill must be specified.")

        try:
            backlog_val = int(max_backlogs)
            if backlog_val < 0:
                errors.append("Maximum backlogs cannot be negative.")
        except (ValueError, TypeError):
            errors.append("Maximum active backlogs must be a non-negative integer.")

        years = cls.normalize_years(eligible_graduation_years)
        if not years:
            errors.append("At least one eligible graduation year must be specified.")

        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert company object to dictionary for JSON persistence."""
        return {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "job_title": self.job_title,
            "min_cgpa": self.min_cgpa,
            "eligible_branches": self.eligible_branches,
            "required_skills": self.required_skills,
            "max_backlogs": self.max_backlogs,
            "eligible_graduation_years": self.eligible_graduation_years
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Company":
        """Instantiate Company object from a dictionary."""
        return cls(
            company_id=str(data.get("company_id", "")),
            company_name=str(data.get("company_name", "")),
            job_title=str(data.get("job_title", "")),
            min_cgpa=float(data.get("min_cgpa", 0.0)),
            eligible_branches=data.get("eligible_branches", []),
            required_skills=data.get("required_skills", []),
            max_backlogs=int(data.get("max_backlogs", 0)),
            eligible_graduation_years=data.get("eligible_graduation_years", [])
        )
