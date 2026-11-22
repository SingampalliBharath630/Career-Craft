import streamlit as st
import pandas as pd
from student import Student
from company import Company
from student_manager import StudentManager
from company_manager import CompanyManager
from eligibility import check_eligibility, find_eligible_students

# Set page configuration
st.set_page_config(
    page_title="CareerCraft – Student Placement Readiness Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for modern, clean, responsive UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-eligible {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-ineligible {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


def init_managers():
    """Initialize StudentManager and CompanyManager in session state for responsive updates."""
    if "student_mgr" not in st.session_state:
        st.session_state.student_mgr = StudentManager()
    if "company_mgr" not in st.session_state:
        st.session_state.company_mgr = CompanyManager()


init_managers()
student_mgr: StudentManager = st.session_state.student_mgr
company_mgr: CompanyManager = st.session_state.company_mgr

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/graduation-cap.png", width=70)
st.sidebar.title("CareerCraft Portal")
st.sidebar.caption("Student Placement Readiness System")

nav_options = [
    "📊 Dashboard",
    "➕ Add Student",
    "👥 View Students",
    "🔍 Search & Update Student",
    "🗑️ Delete Student",
    "🏢 Add Company Job Requirement",
    "💼 View Companies",
    "🎯 Check Individual Eligibility",
    "📋 Eligible Candidates for Job",
    "🔎 Filter & Sort Students",
    "💾 Data Management & Reload"
]

menu = st.sidebar.radio("Navigate", nav_options, index=0)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tech Stack**: Python 3, Streamlit, JSON Storage, OOP, Built-in Collections.")


# Helper to convert student list to formatted dataframe
def students_to_dataframe(students):
    if not students:
        return pd.DataFrame()
    data = []
    for s in students:
        data.append({
            "Student ID": s.student_id,
            "Name": s.name,
            "Email": s.email,
            "Branch": s.branch,
            "CGPA": f"{s.cgpa:.2f}",
            "Backlogs": s.backlogs,
            "Graduation Year": s.graduation_year,
            "Skills": ", ".join(s.skills)
        })
    return pd.DataFrame(data)


# Helper to convert company list to formatted dataframe
def companies_to_dataframe(companies):
    if not companies:
        return pd.DataFrame()
    data = []
    for c in companies:
        data.append({
            "Company ID": c.company_id,
            "Company Name": c.company_name,
            "Job Title": c.job_title,
            "Min CGPA": f"{c.min_cgpa:.2f}",
            "Eligible Branches": ", ".join(c.eligible_branches),
            "Max Backlogs": c.max_backlogs,
            "Graduation Batches": ", ".join(map(str, c.eligible_graduation_years)),
            "Required Skills": ", ".join(c.required_skills)
        })
    return pd.DataFrame(data)


# ==========================================
# 1. DASHBOARD
# ==========================================
if menu == "📊 Dashboard":
    st.markdown('<div class="main-title">Placement Readiness Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Overview of registered students, active corporate hiring requirements, and live qualification metrics.</div>', unsafe_allow_html=True)

    all_students = student_mgr.get_all_students()
    all_companies = company_mgr.get_all_companies()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(all_students))
    with col2:
        st.metric("Total Companies", len(all_companies))
    with col3:
        st.metric("Active Openings", len(all_companies))
    with col4:
        # Calculate average CGPA
        avg_cgpa = (sum(s.cgpa for s in all_students) / len(all_students)) if all_students else 0.0
        st.metric("Average CGPA", f"{avg_cgpa:.2f}")

    st.markdown("---")

    # Quick Job Eligibility Snapshot
    st.subheader("🎯 Live Job Eligibility Match Counter")
    if all_companies:
        company_options = {f"{c.company_name} - {c.job_title} ({c.company_id})": c for c in all_companies}
        selected_company_key = st.selectbox("Select Company Requirement to inspect eligibility pool:", list(company_options.keys()))
        selected_company = company_options[selected_company_key]

        eligible, ineligible = find_eligible_students(all_students, selected_company)

        snap1, snap2, snap3 = st.columns(3)
        with snap1:
            st.metric("Eligible Candidates", len(eligible), delta=f"{len(eligible)} qualified")
        with snap2:
            st.metric("Ineligible Candidates", len(ineligible), delta=f"-{len(ineligible)} disqualified", delta_color="inverse")
        with snap3:
            ratio = (len(eligible) / len(all_students) * 100) if all_students else 0.0
            st.metric("Eligibility Rate", f"{ratio:.1f}%")

        if eligible:
            st.write("##### Quick view of eligible candidates:")
            eligible_studs = [Student.from_dict(item["student"]) for item in eligible]
            st.dataframe(students_to_dataframe(eligible_studs), use_container_width=True)
        else:
            st.warning("No students currently meet all the criteria for this role.")
    else:
        st.info("No companies registered yet. Add company requirements from the sidebar.")

    # High level statistics
    st.markdown("---")
    c_left, c_right = st.columns(2)
    with c_left:
        st.write("##### Branch-wise Student Distribution")
        if all_students:
            branch_counts = {}
            for s in all_students:
                branch_counts[s.branch] = branch_counts.get(s.branch, 0) + 1
            st.bar_chart(pd.DataFrame(list(branch_counts.items()), columns=["Branch", "Students"]).set_index("Branch"))
        else:
            st.write("No student records available.")
    with c_right:
        st.write("##### Graduation Year Distribution")
        if all_students:
            year_counts = {}
            for s in all_students:
                year_counts[str(s.graduation_year)] = year_counts.get(str(s.graduation_year), 0) + 1
            st.bar_chart(pd.DataFrame(list(year_counts.items()), columns=["Graduation Year", "Students"]).set_index("Graduation Year"))
        else:
            st.write("No student records available.")


# ==========================================
# 2. ADD STUDENT
# ==========================================
elif menu == "➕ Add Student":
    st.markdown('<div class="main-title">Register New Student</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Enter academic, personal, and technical skill records for placement tracking.</div>', unsafe_allow_html=True)

    with st.form("add_student_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("Student ID *", placeholder="e.g. S108").strip()
            name = st.text_input("Full Name *", placeholder="e.g. Aditi Sharma").strip()
            email = st.text_input("Email Address *", placeholder="e.g. aditi.sharma@example.com").strip()
            branch = st.selectbox("Department / Branch *", ["CSE", "IT", "ECE", "EEE", "MECH", "CIVIL", "AIDS", "AIML"])

        with c2:
            cgpa = st.number_input("CGPA (0.0 to 10.0) *", min_value=0.0, max_value=10.0, value=7.50, step=0.01)
            backlogs = st.number_input("Active Backlogs *", min_value=0, max_value=20, value=0, step=1)
            graduation_year = st.selectbox("Graduation Year *", [2024, 2025, 2026, 2027, 2028], index=2)
            skills = st.text_input("Technical Skills (comma-separated) *", placeholder="e.g. Java, Python, SQL, Docker")

        submitted = st.form_submit_button("Save Student Record", use_container_width=True)

        if submitted:
            is_valid, error_msgs = Student.validate_details(
                student_id, name, email, branch, cgpa, backlogs, skills, graduation_year
            )
            if not is_valid:
                for err in error_msgs:
                    st.error(f"❌ {err}")
            else:
                new_student = Student(
                    student_id=student_id,
                    name=name,
                    email=email,
                    branch=branch,
                    cgpa=cgpa,
                    backlogs=backlogs,
                    skills=skills,
                    graduation_year=graduation_year
                )
                success, msg = student_mgr.add_student(new_student)
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")


# ==========================================
# 3. VIEW STUDENTS
# ==========================================
elif menu == "👥 View Students":
    st.markdown('<div class="main-title">Student Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">View all registered students in the CareerCraft system.</div>', unsafe_allow_html=True)

    all_students = student_mgr.get_all_students()
    if all_students:
        st.write(f"Showing **{len(all_students)}** registered students:")
        df = students_to_dataframe(all_students)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No students found. Use 'Add Student' to register candidates.")


# ==========================================
# 4. SEARCH & UPDATE STUDENT
# ==========================================
elif menu == "🔍 Search & Update Student":
    st.markdown('<div class="main-title">Search & Update Student</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Lookup by Student ID or Name and update academic profile details.</div>', unsafe_allow_html=True)

    search_query = st.text_input("Search student by ID or Name:", placeholder="Type name or ID (e.g. Rahul or S101)...")
    matching_students = student_mgr.search_students(search_query) if search_query else student_mgr.get_all_students()

    if matching_students:
        student_map = {f"{s.student_id} - {s.name} ({s.branch}, CGPA: {s.cgpa})": s for s in matching_students}
        selected_key = st.selectbox("Select Student to edit:", list(student_map.keys()))
        selected_student = student_map[selected_key]

        st.markdown("#### Edit Details:")
        with st.form("update_student_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Student ID (Read-only)", value=selected_student.student_id, disabled=True)
                new_name = st.text_input("Full Name", value=selected_student.name)
                new_email = st.text_input("Email Address", value=selected_student.email)
                branch_list = ["CSE", "IT", "ECE", "EEE", "MECH", "CIVIL", "AIDS", "AIML"]
                current_b_idx = branch_list.index(selected_student.branch) if selected_student.branch in branch_list else 0
                new_branch = st.selectbox("Branch / Department", branch_list, index=current_b_idx)

            with col2:
                new_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=float(selected_student.cgpa), step=0.01)
                new_backlogs = st.number_input("Active Backlogs", min_value=0, max_value=20, value=int(selected_student.backlogs), step=1)
                year_list = [2024, 2025, 2026, 2027, 2028]
                current_y_idx = year_list.index(selected_student.graduation_year) if selected_student.graduation_year in year_list else 2
                new_year = st.selectbox("Graduation Year", year_list, index=current_y_idx)
                new_skills_str = st.text_input("Technical Skills (comma-separated)", value=", ".join(selected_student.skills))

            update_btn = st.form_submit_button("Update Student Record", use_container_width=True)
            if update_btn:
                is_valid, errs = Student.validate_details(
                    selected_student.student_id, new_name, new_email, new_branch, new_cgpa, new_backlogs, new_skills_str, new_year
                )
                if not is_valid:
                    for err in errs:
                        st.error(f"❌ {err}")
                else:
                    success, msg = student_mgr.update_student(
                        selected_student.student_id,
                        {
                            "name": new_name,
                            "email": new_email,
                            "branch": new_branch,
                            "cgpa": new_cgpa,
                            "backlogs": new_backlogs,
                            "graduation_year": new_year,
                            "skills": new_skills_str
                        }
                    )
                    if success:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
    else:
        st.warning("No students matched your search query.")


# ==========================================
# 5. DELETE STUDENT
# ==========================================
elif menu == "🗑️ Delete Student":
    st.markdown('<div class="main-title">Delete Student Record</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Safely remove a student profile and commit changes immediately.</div>', unsafe_allow_html=True)

    all_students = student_mgr.get_all_students()
    if all_students:
        options = {f"{s.student_id} - {s.name} ({s.branch}, CGPA: {s.cgpa})": s.student_id for s in all_students}
        selected_label = st.selectbox("Choose student to remove:", list(options.keys()))
        target_id = options[selected_label]

        st.warning(f"⚠️ Are you sure you want to delete **{selected_label}**? This action will permanently update `students.json`.")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Confirm Delete", type="primary"):
                success, msg = student_mgr.delete_student(target_id)
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
    else:
        st.info("No students available to delete.")


# ==========================================
# 6. ADD COMPANY JOB REQUIREMENT
# ==========================================
elif menu == "🏢 Add Company Job Requirement":
    st.markdown('<div class="main-title">Add Company & Job Criteria</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Configure recruitment eligibility parameters for corporate partners.</div>', unsafe_allow_html=True)

    with st.form("add_company_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            company_id = st.text_input("Company ID *", placeholder="e.g. C204").strip()
            company_name = st.text_input("Company Name *", placeholder="e.g. Infosys / Google").strip()
            job_title = st.text_input("Job Title *", placeholder="e.g. Systems Engineer").strip()
            min_cgpa = st.number_input("Minimum CGPA Required *", min_value=0.0, max_value=10.0, value=7.0, step=0.01)

        with c2:
            max_backlogs = st.number_input("Maximum Permitted Active Backlogs *", min_value=0, max_value=10, value=0, step=1)
            branches_str = st.text_input("Eligible Branches (comma-separated) *", placeholder="e.g. CSE, IT, ECE", value="CSE, IT")
            grad_years_str = st.text_input("Eligible Graduation Years (comma-separated) *", placeholder="e.g. 2026, 2027", value="2027")
            skills_str = st.text_input("Required Mandatory Technical Skills (comma-separated) *", placeholder="e.g. Java, SQL, Python")

        submitted = st.form_submit_button("Save Company Requirement", use_container_width=True)
        if submitted:
            is_valid, errs = Company.validate_details(
                company_id, company_name, job_title, min_cgpa, branches_str, skills_str, max_backlogs, grad_years_str
            )
            if not is_valid:
                for err in errs:
                    st.error(f"❌ {err}")
            else:
                new_company = Company(
                    company_id=company_id,
                    company_name=company_name,
                    job_title=job_title,
                    min_cgpa=min_cgpa,
                    eligible_branches=branches_str,
                    required_skills=skills_str,
                    max_backlogs=max_backlogs,
                    eligible_graduation_years=grad_years_str
                )
                success, msg = company_mgr.add_company(new_company)
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")


# ==========================================
# 7. VIEW COMPANIES
# ==========================================
elif menu == "💼 View Companies":
    st.markdown('<div class="main-title">Company Job Openings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">View all registered corporate requirements and eligibility benchmarks.</div>', unsafe_allow_html=True)

    all_companies = company_mgr.get_all_companies()
    if all_companies:
        st.write(f"Showing **{len(all_companies)}** company job openings:")
        df = companies_to_dataframe(all_companies)
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("Manage Existing Company Requirements")
        comp_map = {f"{c.company_name} - {c.job_title} ({c.company_id})": c for c in all_companies}
        sel_c_label = st.selectbox("Select Company to modify or delete:", list(comp_map.keys()))
        target_company = comp_map[sel_c_label]

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            with st.expander("✏️ Edit Requirement Details"):
                with st.form("edit_company_form"):
                    e_name = st.text_input("Company Name", value=target_company.company_name)
                    e_title = st.text_input("Job Title", value=target_company.job_title)
                    e_min_cgpa = st.number_input("Min CGPA", min_value=0.0, max_value=10.0, value=float(target_company.min_cgpa), step=0.01)
                    e_backlogs = st.number_input("Max Backlogs", min_value=0, max_value=10, value=int(target_company.max_backlogs))
                    e_branches = st.text_input("Eligible Branches", value=", ".join(target_company.eligible_branches))
                    e_years = st.text_input("Graduation Years", value=", ".join(map(str, target_company.eligible_graduation_years)))
                    e_skills = st.text_input("Required Skills", value=", ".join(target_company.required_skills))

                    if st.form_submit_button("Update Requirement"):
                        is_v, c_errs = Company.validate_details(target_company.company_id, e_name, e_title, e_min_cgpa, e_branches, e_skills, e_backlogs, e_years)
                        if not is_v:
                            for err in c_errs:
                                st.error(err)
                        else:
                            company_mgr.update_company(target_company.company_id, {
                                "company_name": e_name,
                                "job_title": e_title,
                                "min_cgpa": e_min_cgpa,
                                "max_backlogs": e_backlogs,
                                "eligible_branches": e_branches,
                                "eligible_graduation_years": e_years,
                                "required_skills": e_skills
                            })
                            st.success("Updated successfully!")
                            st.rerun()

        with action_col2:
            with st.expander("🗑️ Delete Company Requirement"):
                st.write(f"Delete **{target_company.company_name} - {target_company.job_title}**?")
                if st.button("Confirm Company Delete", type="primary"):
                    company_mgr.delete_company(target_company.company_id)
                    st.success("Deleted successfully!")
                    st.rerun()

    else:
        st.info("No companies found. Use 'Add Company Job Requirement' to create entries.")


# ==========================================
# 8. CHECK INDIVIDUAL ELIGIBILITY
# ==========================================
elif menu == "🎯 Check Individual Eligibility":
    st.markdown('<div class="main-title">Individual Eligibility Evaluation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Detailed diagnostic breakdown testing a specific student against a specific job opening.</div>', unsafe_allow_html=True)

    all_students = student_mgr.get_all_students()
    all_companies = company_mgr.get_all_companies()

    if not all_students:
        st.warning("Please add student records first.")
    elif not all_companies:
        st.warning("Please add company job requirements first.")
    else:
        col_s, col_c = st.columns(2)
        with col_s:
            s_options = {f"{s.name} ({s.student_id}, {s.branch})": s for s in all_students}
            selected_student_key = st.selectbox("Select Student:", list(s_options.keys()))
            selected_student = s_options[selected_student_key]

        with col_c:
            c_options = {f"{c.company_name} - {c.job_title}": c for c in all_companies}
            selected_company_key = st.selectbox("Select Company Requirement:", list(c_options.keys()))
            selected_company = c_options[selected_company_key]

        st.markdown("---")

        # Evaluate eligibility dynamically using check_eligibility function
        eval_result = check_eligibility(selected_student, selected_company)
        is_eligible = eval_result["is_eligible"]
        reasons = eval_result["reasons"]
        missing_skills = eval_result["missing_skills"]
        criteria = eval_result["criteria_results"]

        # Display Eligibility Banner
        if is_eligible:
            st.success(f"🎉 **ELIGIBLE**: {selected_student.name} meets all placement requirements for **{selected_company.company_name} - {selected_company.job_title}**!")
        else:
            st.error(f"🚫 **NOT ELIGIBLE**: {selected_student.name} does NOT meet the requirements for **{selected_company.company_name} - {selected_company.job_title}**.")

        # Breakdown in tabular format
        st.subheader("Criteria-by-Criteria Diagnostics")

        criteria_rows = [
            {
                "Criteria": "Minimum CGPA",
                "Company Requirement": f"≥ {selected_company.min_cgpa:.2f}",
                "Student Value": f"{selected_student.cgpa:.2f}",
                "Status": "✅ Pass" if criteria["cgpa"]["met"] else "❌ Fail",
                "Explanation": criteria["cgpa"]["detail"]
            },
            {
                "Criteria": "Branch / Department",
                "Company Requirement": ", ".join(selected_company.eligible_branches),
                "Student Value": selected_student.branch,
                "Status": "✅ Pass" if criteria["branch"]["met"] else "❌ Fail",
                "Explanation": criteria["branch"]["detail"]
            },
            {
                "Criteria": "Active Backlogs",
                "Company Requirement": f"≤ {selected_company.max_backlogs}",
                "Student Value": str(selected_student.backlogs),
                "Status": "✅ Pass" if criteria["backlogs"]["met"] else "❌ Fail",
                "Explanation": criteria["backlogs"]["detail"]
            },
            {
                "Criteria": "Graduation Year",
                "Company Requirement": ", ".join(map(str, selected_company.eligible_graduation_years)),
                "Student Value": str(selected_student.graduation_year),
                "Status": "✅ Pass" if criteria["graduation_year"]["met"] else "❌ Fail",
                "Explanation": criteria["graduation_year"]["detail"]
            },
            {
                "Criteria": "Technical Skills",
                "Company Requirement": ", ".join(selected_company.required_skills),
                "Student Value": ", ".join(selected_student.skills),
                "Status": "✅ Pass" if criteria["skills"]["met"] else "❌ Fail",
                "Explanation": criteria["skills"]["detail"]
            }
        ]

        st.dataframe(pd.DataFrame(criteria_rows), use_container_width=True)

        if not is_eligible:
            st.markdown("##### Specific Reasons for Disqualification:")
            for idx, r in enumerate(reasons, 1):
                st.write(f"{idx}. {r}")

            if missing_skills:
                st.warning(f"💡 **Missing Technical Skills to acquire**: {', '.join(missing_skills)}")


# ==========================================
# 9. ELIGIBLE CANDIDATES FOR JOB
# ==========================================
elif menu == "📋 Eligible Candidates for Job":
    st.markdown('<div class="main-title">Eligible Candidates by Job Opening</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Filter and export candidates who qualify for a selected corporate recruitment drive.</div>', unsafe_allow_html=True)

    all_students = student_mgr.get_all_students()
    all_companies = company_mgr.get_all_companies()

    if not all_companies:
        st.warning("No companies configured yet.")
    elif not all_students:
        st.warning("No students registered yet.")
    else:
        c_options = {f"{c.company_name} - {c.job_title} ({c.company_id})": c for c in all_companies}
        selected_company_key = st.selectbox("Select Target Company Job:", list(c_options.keys()))
        target_company = c_options[selected_company_key]

        eligible, ineligible = find_eligible_students(all_students, target_company)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Eligible Candidates", len(eligible))
        with col2:
            st.metric("Ineligible Candidates", len(ineligible))

        tabs = st.tabs(["✅ Eligible Candidates List", "❌ Ineligible Candidates Breakdown"])

        with tabs[0]:
            if eligible:
                st.success(f"{len(eligible)} candidate(s) meet all criteria!")
                eligible_studs = [Student.from_dict(item["student"]) for item in eligible]
                df_el = students_to_dataframe(eligible_studs)
                st.dataframe(df_el, use_container_width=True)
            else:
                st.warning("Zero students are currently eligible for this opening.")

        with tabs[1]:
            if ineligible:
                ineligible_rows = []
                for item in ineligible:
                    s_data = item["student"]
                    res = item["result"]
                    ineligible_rows.append({
                        "ID": s_data["student_id"],
                        "Name": s_data["name"],
                        "Branch": s_data["branch"],
                        "CGPA": f"{s_data['cgpa']:.2f}",
                        "Backlogs": s_data["backlogs"],
                        "Disqualification Reasons": " | ".join(res["reasons"]),
                        "Missing Skills": ", ".join(res["missing_skills"]) if res["missing_skills"] else "None"
                    })
                st.dataframe(pd.DataFrame(ineligible_rows), use_container_width=True)
            else:
                st.info("No students are ineligible.")


# ==========================================
# 10. FILTER & SORT STUDENTS
# ==========================================
elif menu == "🔎 Filter & Sort Students":
    st.markdown('<div class="main-title">Search, Filter & Sort Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Advanced querying using Python built-in lists, sorting, conditionals, and filtering.</div>', unsafe_allow_html=True)

    all_students = student_mgr.get_all_students()

    # Extract unique branches, skills, and years for dropdown filters
    all_branches = sorted(list(set(s.branch for s in all_students)))
    all_skills = set()
    for s in all_students:
        for sk in s.skills:
            all_skills.add(sk)
    all_skills = sorted(list(all_skills))

    with st.expander("Filter Criteria Options", expanded=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            sel_branch = st.selectbox("Filter by Branch:", ["All"] + all_branches)
            search_name = st.text_input("Search Name / ID:", placeholder="Substring search...")
        with f_col2:
            min_cgpa_filter = st.slider("Minimum CGPA:", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
            sel_skill = st.selectbox("Must possess skill:", ["All"] + all_skills)
        with f_col3:
            max_backlogs_filter = st.number_input("Max Backlogs Allowed:", min_value=0, max_value=10, value=5)
            grad_year_filter = st.selectbox("Graduation Year:", ["All", 2024, 2025, 2026, 2027, 2028])

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        sort_by = st.selectbox("Sort records by:", [
            ("CGPA", "cgpa"),
            ("Name", "name"),
            ("Graduation Year", "graduation_year"),
            ("Student ID", "student_id"),
            ("Backlogs", "backlogs")
        ], format_func=lambda x: x[0])[1]
    with s_col2:
        sort_order = st.radio("Sort Order:", ["Descending", "Ascending"], horizontal=True)
        reverse = (sort_order == "Descending")

    # Apply Filtering
    gy = int(grad_year_filter) if grad_year_filter != "All" else None
    filtered = student_mgr.filter_students(
        branch=sel_branch,
        min_cgpa=min_cgpa_filter,
        skill=sel_skill,
        max_backlogs=max_backlogs_filter,
        graduation_year=gy
    )

    if search_name:
        filtered = [s for s in filtered if search_name.lower() in s.name.lower() or search_name.lower() in s.student_id.lower()]

    # Apply Sorting
    sorted_result = student_mgr.sort_students(filtered, sort_by=sort_by, reverse=reverse)

    st.write(f"Matched **{len(sorted_result)}** students:")
    if sorted_result:
        st.dataframe(students_to_dataframe(sorted_result), use_container_width=True)
    else:
        st.info("No students match the chosen filter combinations.")


# ==========================================
# 11. DATA MANAGEMENT & RELOAD
# ==========================================
elif menu == "💾 Data Management & Reload":
    st.markdown('<div class="main-title">Data Management & Persistence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">View raw JSON data files, reload cache, or reset sample data.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Force Reload from JSON Files"):
            student_mgr.load_data()
            company_mgr.load_data()
            st.success("Successfully reloaded all records from JSON files on disk!")
            st.rerun()

    tabs = st.tabs(["📄 students.json", "📄 companies.json"])
    with tabs[0]:
        st.write(f"File Path: `{student_mgr.filepath}`")
        st.json(student_mgr.get_all_as_dicts())

    with tabs[1]:
        st.write(f"File Path: `{company_mgr.filepath}`")
        st.json(company_mgr.get_all_as_dicts())
