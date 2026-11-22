import os
from typing import List, Dict, Any, Optional, Tuple
from student import Student
from file_handler import load_json, save_json

DEFAULT_STUDENTS_FILE = os.path.join(os.path.dirname(__file__), "data", "students.json")


class StudentManager:
    """
    Manages student records: Add, View, Search, Update, Delete, Sort, Filter, and Persistence.
    Demonstrates OOP, functions, dictionaries, lists, sorting, filtering, and string handling.
    """

    def __init__(self, filepath: str = DEFAULT_STUDENTS_FILE):
        self.filepath = filepath
        self.students: List[Student] = []
        self.load_data()

    def load_data(self) -> None:
        """Loads students from JSON file into Student objects."""
        raw_list = load_json(self.filepath, default=[])
        self.students = [Student.from_dict(item) for item in raw_list if isinstance(item, dict)]

    def save_data(self) -> bool:
        """Saves current student objects as list of dictionaries into JSON file."""
        data = [student.to_dict() for student in self.students]
        return save_json(self.filepath, data)

    def get_all_students(self) -> List[Student]:
        """Returns list of all Student objects."""
        return self.students

    def get_all_as_dicts(self) -> List[Dict[str, Any]]:
        """Returns all students as dictionaries for easy tabular rendering."""
        return [s.to_dict() for s in self.students]

    def find_by_id(self, student_id: str) -> Optional[Student]:
        """Finds a student by exact ID (case-insensitive)."""
        target = student_id.strip().lower()
        for s in self.students:
            if s.student_id.strip().lower() == target:
                return s
        return None

    def add_student(self, student: Student) -> Tuple[bool, str]:
        """
        Adds a new student if the student ID is unique.
        Automatically saves to JSON file.
        """
        if self.find_by_id(student.student_id) is not None:
            return False, f"Student with ID '{student.student_id}' already exists!"

        self.students.append(student)
        self.save_data()
        return True, f"Student '{student.name}' ({student.student_id}) added successfully."

    def update_student(self, student_id: str, updated_fields: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Updates an existing student's attributes and persists changes.
        """
        student = self.find_by_id(student_id)
        if not student:
            return False, f"Student with ID '{student_id}' not found."

        if "name" in updated_fields and updated_fields["name"]:
            student.name = str(updated_fields["name"]).strip()
        if "email" in updated_fields and updated_fields["email"]:
            student.email = str(updated_fields["email"]).strip()
        if "branch" in updated_fields and updated_fields["branch"]:
            student.branch = str(updated_fields["branch"]).strip().upper()
        if "cgpa" in updated_fields:
            student.cgpa = round(float(updated_fields["cgpa"]), 2)
        if "backlogs" in updated_fields:
            student.backlogs = int(updated_fields["backlogs"])
        if "skills" in updated_fields:
            student.skills = Student.normalize_skills(updated_fields["skills"])
        if "graduation_year" in updated_fields:
            student.graduation_year = int(updated_fields["graduation_year"])

        self.save_data()
        return True, f"Student '{student.name}' updated successfully."

    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """Deletes a student by ID and saves to JSON."""
        student = self.find_by_id(student_id)
        if not student:
            return False, f"Student with ID '{student_id}' not found."

        self.students.remove(student)
        self.save_data()
        return True, f"Student '{student.name}' ({student_id}) deleted successfully."

    def search_students(self, query: str) -> List[Student]:
        """
        Search students by ID or Name (case-insensitive substring match).
        """
        q = query.strip().lower()
        if not q:
            return self.students

        results = []
        for s in self.students:
            if q in s.student_id.lower() or q in s.name.lower():
                results.append(s)
        return results

    def filter_students(
        self,
        branch: Optional[str] = None,
        min_cgpa: Optional[float] = None,
        skill: Optional[str] = None,
        max_backlogs: Optional[int] = None,
        graduation_year: Optional[int] = None
    ) -> List[Student]:
        """
        Filters students according to given criteria.
        Demonstrates conditional checks and list comprehension.
        """
        filtered = self.students

        if branch and branch != "All":
            b_norm = branch.strip().upper()
            filtered = [s for s in filtered if s.branch == b_norm]

        if min_cgpa is not None:
            filtered = [s for s in filtered if s.cgpa >= float(min_cgpa)]

        if skill and skill != "All":
            sk_norm = skill.strip().lower()
            filtered = [
                s for s in filtered
                if any(sk_norm == item.lower() for item in s.skills)
            ]

        if max_backlogs is not None:
            filtered = [s for s in filtered if s.backlogs <= int(max_backlogs)]

        if graduation_year is not None:
            filtered = [s for s in filtered if s.graduation_year == int(graduation_year)]

        return filtered

    def sort_students(self, students_list: Optional[List[Student]] = None, sort_by: str = "name", reverse: bool = False) -> List[Student]:
        """
        Sorts students list.
        sort_by options: 'cgpa', 'name', 'graduation_year', 'student_id'
        Demonstrates Python sorted() and lambda keys.
        """
        records = students_list if students_list is not None else self.students

        if sort_by == "cgpa":
            return sorted(records, key=lambda s: s.cgpa, reverse=reverse)
        elif sort_by == "name":
            return sorted(records, key=lambda s: s.name.lower(), reverse=reverse)
        elif sort_by == "graduation_year":
            return sorted(records, key=lambda s: s.graduation_year, reverse=reverse)
        elif sort_by == "student_id":
            return sorted(records, key=lambda s: s.student_id.lower(), reverse=reverse)
        elif sort_by == "backlogs":
            return sorted(records, key=lambda s: s.backlogs, reverse=reverse)
        else:
            return records
