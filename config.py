# =============================
# Global Thresholds
# =============================
SIMILARITY_THRESHOLD = 0.65  # --> change this anytime


# =============================
# Work Placement Roles --> It is better to reduce the requirements!
# =============================
JOB_ROLES = {
    "Data Analyst": {
        "requirements": """
        * Apply legislative requirements related to data protection
        * Ask analytical questions, formulate a problem and define required data entities
        * Profile data & conduct statistical analysis to assess data quality
        * Use UML diagram to represent a business problem solution
        * Uncover unidentified relationships between data
        * Organize multiple data sources into an enterprise-wide database using SQL
        * Develop descriptive/diagnostic/predictive/prescriptive models (i.e., Java, SPSS, SPSS Modeler, SAS, Python) to help managers derive business insights
        * Manipulate & merge any type of data (structured, semi structured, unstructured) & use R for Big Data manipulation
        * Work with the Hadoop architecture & querying large amounts of data using Map Reduce
        * Define what dashboards are needed in a specific situation & identify the ideal visual to present data (i.e., Excel, Tableau, Power BI)
        * Simulate/test the solution to a problem, conduct UAT, & integrate feedback
        * Contribute to projects related to various data analytics-based solutions (i.e., statistical analysis, dashboards, predictive model, machine learning implementation, etc.)
        """,
        "weight": 0.5
    },
    "Business Analyst": {
        "requirements": """
        stakeholder communication requirements gathering
        business processes documentation analysis
        """,
        "weight": 0.3
    },
    "ML Intern": {
        "requirements": """
        machine learning python data preprocessing
        model evaluation feature engineering
        """,
        "weight": 0.2
    }
}

# =============================
# Company Weights
# =============================
COMPANY_WEIGHTS = {
    "Google": 1.2,
    "Amazon": 1.1,
    "Startup": 0.9,
    "Default": 1.0
}
