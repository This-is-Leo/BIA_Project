from matcher import compute_single_role_similarity
from config import SIMILARITY_THRESHOLD

selected_role = "Data Analyst"

student_job_description = """
This internship requires strong SQL and Python skills.
You will analyze datasets, build dashboards, and present
insights to business stakeholders.
"""

result = compute_single_role_similarity(
    selected_role,
    student_job_description
)

threshold_pct = round(SIMILARITY_THRESHOLD * 100, 1)
similarity_pct = round(result["cosine_similarity"] * 100, 1)

passed = similarity_pct >= threshold_pct
print("---------------------------------------------------")
fin_status = "PASS – Proceed to Next Step" if passed else "Not Eligible Yet"
print(f"The required threshold: {threshold_pct} \nYour result is: {result['cosine_similarity'] * 100}")
print("=============================")
print(fin_status)
print("=============================")
print(result)
