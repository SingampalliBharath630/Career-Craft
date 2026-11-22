import os
from typing import List, Dict, Any, Optional, Tuple
from company import Company
from file_handler import load_json, save_json

DEFAULT_COMPANIES_FILE = os.path.join(os.path.dirname(__file__), "data", "companies.json")


class CompanyManager:
    """
    Manages company job criteria: Add, View, Search, Update, Delete, and Persistence.
    Demonstrates OOP, functions, dictionaries, lists, and file handling.
    """

    def __init__(self, filepath: str = DEFAULT_COMPANIES_FILE):
        self.filepath = filepath
        self.companies: List[Company] = []
        self.load_data()

    def load_data(self) -> None:
        """Loads companies from JSON file into Company objects."""
        raw_list = load_json(self.filepath, default=[])
        self.companies = [Company.from_dict(item) for item in raw_list if isinstance(item, dict)]

    def save_data(self) -> bool:
        """Saves current company objects as list of dictionaries into JSON file."""
        data = [company.to_dict() for company in self.companies]
        return save_json(self.filepath, data)

    def get_all_companies(self) -> List[Company]:
        """Returns list of all Company objects."""
        return self.companies

    def get_all_as_dicts(self) -> List[Dict[str, Any]]:
        """Returns all companies as dictionaries."""
        return [c.to_dict() for c in self.companies]

    def find_by_id(self, company_id: str) -> Optional[Company]:
        """Finds a company by company ID (case-insensitive)."""
        target = company_id.strip().lower()
        for c in self.companies:
            if c.company_id.strip().lower() == target:
                return c
        return None

    def add_company(self, company: Company) -> Tuple[bool, str]:
        """
        Adds a new company requirement if company ID is unique.
        Automatically saves to JSON file.
        """
        if self.find_by_id(company.company_id) is not None:
            return False, f"Company/Job with ID '{company.company_id}' already exists!"

        self.companies.append(company)
        self.save_data()
        return True, f"Company '{company.company_name}' ({company.job_title}) added successfully."

    def update_company(self, company_id: str, updated_fields: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Updates an existing company's requirements and persists changes.
        """
        company = self.find_by_id(company_id)
        if not company:
            return False, f"Company with ID '{company_id}' not found."

        if "company_name" in updated_fields and updated_fields["company_name"]:
            company.company_name = str(updated_fields["company_name"]).strip()
        if "job_title" in updated_fields and updated_fields["job_title"]:
            company.job_title = str(updated_fields["job_title"]).strip()
        if "min_cgpa" in updated_fields:
            company.min_cgpa = round(float(updated_fields["min_cgpa"]), 2)
        if "eligible_branches" in updated_fields:
            company.eligible_branches = Company.normalize_branches(updated_fields["eligible_branches"])
        if "required_skills" in updated_fields:
            company.required_skills = Company.normalize_skills(updated_fields["required_skills"])
        if "max_backlogs" in updated_fields:
            company.max_backlogs = int(updated_fields["max_backlogs"])
        if "eligible_graduation_years" in updated_fields:
            company.eligible_graduation_years = Company.normalize_years(updated_fields["eligible_graduation_years"])

        self.save_data()
        return True, f"Company '{company.company_name}' requirements updated successfully."

    def delete_company(self, company_id: str) -> Tuple[bool, str]:
        """Deletes a company requirement by ID and saves to JSON."""
        company = self.find_by_id(company_id)
        if not company:
            return False, f"Company with ID '{company_id}' not found."

        self.companies.remove(company)
        self.save_data()
        return True, f"Company '{company.company_name}' ({company_id}) deleted successfully."

    def search_companies(self, query: str) -> List[Company]:
        """Search companies by ID, Name, or Job Title (case-insensitive substring match)."""
        q = query.strip().lower()
        if not q:
            return self.companies

        results = []
        for c in self.companies:
            if (q in c.company_id.lower() or
                q in c.company_name.lower() or
                q in c.job_title.lower()):
                results.append(c)
        return results
