from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError

from matcher import compute_single_role_similarity, build_role_cache
from config import JOB_ROLES, SIMILARITY_THRESHOLD

app = FastAPI(title="BIA Work Placement Pre-Approval Checker")


# ---------------- STARTUP ----------------
@app.on_event("startup")
def startup():
    build_role_cache()


# ---------------- VALIDATION ERROR HANDLER ----------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return HTMLResponse(
        status_code=400,
        content="""
        <html>
        <head>
            <title>Input Required</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f9;
                }
                .container {
                    max-width: 720px;
                    margin: 50px auto;
                    background: white;
                    padding: 35px;
                    border-radius: 12px;
                    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
                }
                h2 {
                    color: #003366;
                    margin-top: 0;
                }
                .warning {
                    padding: 18px;
                    border-radius: 10px;
                    background-color: #fff3cd;
                    border-left: 6px solid #f9a825;
                    color: #856404;
                    font-size: 15px;
                }
                .actions {
                    margin-top: 30px;
                }
                .btn {
                    text-decoration: none;
                    padding: 12px 18px;
                    border-radius: 6px;
                    font-size: 14px;
                    display: inline-block;
                    background-color: #003366;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>BIA Work Placement – Input Required</h2>
                <div class="warning">
                    Internship responsibilities cannot be empty. Please paste the job responsibilities before submitting.
                </div>
                <div class="actions">
                    <a href="/" class="btn">Go Back</a>
                </div>
            </div>
        </body>
        </html>
        """
    )


# ---------------- FORM PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def form_page():
    roles_options = "".join(
        f"<option value='{r}'>{r}</option>" for r in JOB_ROLES.keys()
    )

    return f"""
    <html>
    <head>
        <title>BIA Work Placement Pre-Approval</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f7fa;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 800px;
                margin: 50px auto;
                background: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #003366;
                margin-bottom: 10px;
            }}
            h2 {{
                color: #555;
                font-weight: normal;
                margin-top: 0;
            }}
            label {{
                font-weight: bold;
                margin-top: 20px;
                display: block;
            }}
            select, textarea {{
                width: 100%;
                padding: 10px;
                margin-top: 8px;
                border-radius: 6px;
                border: 1px solid #ccc;
                font-size: 14px;
            }}
            textarea {{
                resize: vertical;
            }}
            button {{
                margin-top: 25px;
                background-color: #003366;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 6px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #0055aa;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h1>BIA Work Placement Pre-Approval Check</h1>
            <h2>Step 1: Internship Role & Responsibilities</h2>

            <form action="/match" method="post">
                <label>Select Intended Role</label>
                <select name="role">
                    {roles_options}
                </select>

                <label>Paste Job Responsibilities</label>
                <textarea name="responsibilities" rows="10"
                placeholder="Paste the internship responsibilities exactly as written in the job posting..."></textarea>

                <button type="submit">Check Eligibility</button>
            </form>

            <div class="footer">
                Business Insights & Analytics
            </div>
        </div>
    </body>
    </html>
    """


# ---------------- MATCH RESULT ----------------
@app.post("/match", response_class=HTMLResponse)
def match_result(
    role: str = Form(...),
    responsibilities: str = Form(...)
):
    result = compute_single_role_similarity(role, responsibilities)

    score = result["cosine_similarity"]
    threshold = SIMILARITY_THRESHOLD
    passed = score >= threshold

    percent = round(score * 100, 1)
    threshold_pct = round(threshold * 100, 1)

    status_text = "PASS – Proceed to Next Step" if passed else "Not Eligible Yet"
    status_color = "#2e7d32" if passed else "#c62828"
    bar_color = "#4caf50" if passed else "#ef5350"

    explanation = (
        "Your internship responsibilities align well with the approved BIA role requirements."
        if passed else
        "This internship does not sufficiently align with the approved BIA role requirements."
    )

    return f"""
    <html>
    <head>
        <title>Match Result</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
            }}
            .container {{
                max-width: 720px;
                margin: 50px auto;
                background: white;
                padding: 35px;
                border-radius: 12px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #003366;
                margin-top: 0;
            }}
            .status {{
                margin: 25px 0;
                padding: 18px;
                border-radius: 10px;
                background-color: #f9f9f9;
                border-left: 6px solid {status_color};
            }}
            .status-title {{
                font-size: 20px;
                font-weight: bold;
                color: {status_color};
            }}
            .progress {{
                margin: 20px 0;
                background-color: #e0e0e0;
                border-radius: 20px;
                overflow: hidden;
                height: 18px;
            }}
            .progress-bar {{
                height: 100%;
                width: {percent}%;
                background-color: {bar_color};
            }}
            .meta {{
                font-size: 14px;
                color: #555;
            }}
            .explanation {{
                margin-top: 15px;
                font-size: 15px;
                color: #333;
            }}
            .actions {{
                margin-top: 30px;
                display: flex;
                gap: 15px;
            }}
            .btn {{
                text-decoration: none;
                padding: 12px 18px;
                border-radius: 6px;
                font-size: 14px;
                display: inline-block;
            }}
            .btn-primary {{
                background-color: #003366;
                color: white;
            }}
            .btn-secondary {{
                background-color: #eeeeee;
                color: #333;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h2>BIA Work Placement – Match Result</h2>

            <p class="meta"><b>Selected Role:</b> {role}</p>

            <div class="status">
                <div class="status-title">{status_text}</div>

                <div class="progress">
                    <div class="progress-bar"></div>
                </div>

                <p class="meta">
                    Similarity Score: <b>{percent}%</b><br>
                    Required Threshold: <b>{threshold_pct}%</b>
