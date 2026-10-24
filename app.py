import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="K-SIWAP | Skills & Jobs", page_icon="🎯", layout="wide")

# -------------------- Demo data (clearly labelled synthetic data) --------------------
JOBS = pd.DataFrame([
    {"job_id":"J001","company":"Mysuru Digital Labs","title":"Junior Python Developer","sector":"IT","district":"Mysuru","skills":"Python,SQL,Git","degree":"BE/BTech/BCA/MCA","salary_min":22000,"salary_max":35000,"job_type":"Direct Job","period":"2026-10","indicator_type":"Job posting (demo)"},
    {"job_id":"J002","company":"Bengaluru DataWorks","title":"Data Analyst Trainee","sector":"IT","district":"Bengaluru Urban","skills":"SQL,Excel,Python,Power BI","degree":"Any degree","salary_min":20000,"salary_max":32000,"job_type":"Job Fair","period":"2026-10","indicator_type":"Job posting (demo)"},
    {"job_id":"J003","company":"Karnataka Auto Systems","title":"Graduate Trainee","sector":"Automotive","district":"Bengaluru Urban","skills":"Excel,Communication,Problem Solving","degree":"BE/BTech","salary_min":23000,"salary_max":38000,"job_type":"Direct Job","period":"2026-09","indicator_type":"Job posting (demo)"},
    {"job_id":"J004","company":"SkillBridge Services","title":"Technical Support Associate","sector":"IT Services","district":"Mysuru","skills":"Communication,Networking,Troubleshooting","degree":"Any degree","salary_min":18000,"salary_max":28000,"job_type":"Job Fair","period":"2026-09","indicator_type":"Job posting (demo)"},
    {"job_id":"J005","company":"GreenGrid Energy","title":"Operations Assistant","sector":"Energy","district":"Belagavi","skills":"Excel,Communication,Reporting","degree":"Any degree","salary_min":19000,"salary_max":30000,"job_type":"Direct Job","period":"2026-08","indicator_type":"Job posting (demo)"},
    {"job_id":"J006","company":"NorthStar Analytics","title":"SQL Reporting Intern","sector":"IT","district":"Dharwad","skills":"SQL,Excel,Python","degree":"BE/BTech/BCA","salary_min":15000,"salary_max":25000,"job_type":"Job Fair","period":"2026-10","indicator_type":"Job posting (demo)"},
    {"job_id":"J007","company":"Mysuru Retail Group","title":"Sales Consultant","sector":"Retail","district":"Mysuru","skills":"Communication,Negotiation,Customer Service","degree":"Any degree","salary_min":20000,"salary_max":35000,"job_type":"Direct Job","period":"2026-10","indicator_type":"Job posting (demo)"},
])
FAIRS = pd.DataFrame([
    {"name":"Mysuru Skills & Jobs Fair","district":"Mysuru","date":"2026-11-12","organizer":"Demo District Skill Office","companies":18,"roles":42},
    {"name":"Bengaluru Digital Careers Fair","district":"Bengaluru Urban","date":"2026-11-20","organizer":"Demo Job Fair Team","companies":35,"roles":90},
    {"name":"North Karnataka Career Connect","district":"Dharwad","date":"2026-12-03","organizer":"Demo Regional Organizer","companies":14,"roles":28},
])
ANALYTICS = pd.DataFrame([
    {"period":"2026-08","district":"Mysuru","sector":"IT","occupation":"Data Analyst","value":45,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-09","district":"Mysuru","sector":"IT","occupation":"Data Analyst","value":54,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-10","district":"Mysuru","sector":"IT","occupation":"Data Analyst","value":63,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-08","district":"Bengaluru Urban","sector":"IT","occupation":"Python Developer","value":110,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-09","district":"Bengaluru Urban","sector":"IT","occupation":"Python Developer","value":126,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-10","district":"Bengaluru Urban","sector":"IT","occupation":"Python Developer","value":140,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-08","district":"Belagavi","sector":"Manufacturing","occupation":"Operations Assistant","value":28,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-09","district":"Belagavi","sector":"Manufacturing","occupation":"Operations Assistant","value":32,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
    {"period":"2026-10","district":"Belagavi","sector":"Manufacturing","occupation":"Operations Assistant","value":35,"unit":"postings","indicator_type":"Job posting (synthetic demo)","source":"Synthetic demo data"},
])

if "applications" not in st.session_state:
    st.session_state.applications = []
if "profile" not in st.session_state:
    st.session_state.profile = {"name":"","degree":"BE/BTech","district":"Mysuru","skills":[],"interest":"IT"}

st.title("🎯 K-SIWAP — Skills, Jobs & Labour-Market Intelligence")
st.caption("Hackathon prototype • Demo records are synthetic and must not be presented as real labour-market evidence.")
st.info("Prototype scope: student job matching, job-fair discovery, application tracking, skill-gap guidance, employer view, and sector analytics. Login, notifications, verified live jobs, and government data integrations are not connected yet.")

pages = st.tabs(["Student Portal", "Job Fairs", "Employer Workspace", "District & State Analytics", "Data Upload & Quality", "About / Safeguards"])

# -------------------- Student portal --------------------
with pages[0]:
    st.subheader("Student profile")
    c1,c2,c3 = st.columns(3)
    with c1:
        name = st.text_input("Name (demo profile)", value=st.session_state.profile["name"])
        degree = st.selectbox("Education", ["BE/BTech","BCA/MCA","BA/BCom/BSc","Diploma","Any degree"], index=["BE/BTech","BCA/MCA","BA/BCom/BSc","Diploma","Any degree"].index(st.session_state.profile["degree"]))
    with c2:
        district = st.selectbox("Preferred district", ["Mysuru","Bengaluru Urban","Belagavi","Dharwad","Any district"], index=["Mysuru","Bengaluru Urban","Belagavi","Dharwad","Any district"].index(st.session_state.profile["district"]))
        interest = st.selectbox("Preferred sector", ["IT","IT Services","Automotive","Manufacturing","Energy","Retail","Any sector"], index=0 if st.session_state.profile["interest"]=="IT" else ["IT","IT Services","Automotive","Manufacturing","Energy","Retail","Any sector"].index(st.session_state.profile["interest"]) if st.session_state.profile["interest"] in ["IT","IT Services","Automotive","Manufacturing","Energy","Retail","Any sector"] else 0)
    with c3:
        skills = st.multiselect("Your skills", ["Python","SQL","Excel","Power BI","Git","Communication","Networking","Troubleshooting","Problem Solving","Negotiation","Customer Service","Reporting"], default=st.session_state.profile["skills"])
        cv = st.file_uploader("Upload CV (optional; demo only)", type=["pdf","docx","txt"])
    if st.button("Save demo profile", type="primary"):
        st.session_state.profile = {"name":name,"degree":degree,"district":district,"skills":skills,"interest":interest}
        st.success("Profile saved for this browser session. CV contents are not parsed or stored by this prototype.")

    profile = st.session_state.profile
    def job_score(job):
        needed = {x.strip().lower() for x in job["skills"].split(",")}
        owned = {x.lower() for x in profile["skills"]}
        skill_score = 100 * len(needed & owned) / max(1,len(needed))
        location_bonus = 10 if profile["district"] in (job["district"],"Any district") else 0
        sector_bonus = 10 if profile["interest"] in (job["sector"],"Any sector") else 0
        return round(min(100, skill_score + location_bonus + sector_bonus))
    matched = JOBS.copy()
    matched["match_score"] = matched.apply(job_score, axis=1)
    if profile["district"] != "Any district":
        matched["location_match"] = matched["district"].eq(profile["district"])
    st.subheader("Job openings matched to your profile")
    st.caption("Match score is a simple demo heuristic based on entered skills, preferred district, and sector. It is not an AI hiring decision.")
    min_score = st.slider("Minimum match score",0,100,0,5)
    view = matched[matched["match_score"] >= min_score].sort_values("match_score",ascending=False)
    for _, j in view.iterrows():
        with st.container(border=True):
            left,right = st.columns([4,1])
            with left:
                st.markdown(f"**{j['title']}** — {j['company']}")
                st.write(f"{j['district']} • {j['sector']} • {j['job_type']} • ₹{j['salary_min']:,}–₹{j['salary_max']:,}/month")
                st.write(f"Required skills: {j['skills']}")
                needed = {x.strip().lower() for x in j["skills"].split(",")}
                owned = {x.lower() for x in profile["skills"]}
                gaps = sorted(needed-owned)
                st.caption("Skill gaps: " + (", ".join(gaps) if gaps else "No listed skill gaps"))
            with right:
                st.metric("Demo match", f"{j['match_score']}%")
                if st.button("Apply", key=f"apply_{j['job_id']}"):
                    if not any(a["job_id"]==j["job_id"] for a in st.session_state.applications):
                        st.session_state.applications.append({"job_id":j["job_id"],"title":j["title"],"company":j["company"],"status":"Submitted (demo)"})
                    st.success("Application added to demo tracker.")
    st.subheader("Application status")
    if st.session_state.applications:
        st.dataframe(pd.DataFrame(st.session_state.applications), use_container_width=True, hide_index=True)
    else:
        st.write("No demo applications yet. Use Apply on a job above.")

    st.subheader("Skill-gap learning plan")
    if profile["skills"]:
        all_needed = set()
        for s in JOBS["skills"]:
            all_needed.update(x.strip() for x in s.split(","))
        gaps = sorted(all_needed - set(profile["skills"]))
        st.write("Skills appearing in the demo job set that you have not selected:")
        st.write(", ".join(gaps) if gaps else "You selected all skills appearing in the demo job set.")
        st.caption("Suggested next step: choose one target role, practise the missing skills, and update your profile. Learning recommendations are indicative, not endorsements.")
    else:
        st.write("Select your current skills to see a basic gap list.")
    st.subheader("Mock interview practice")
    role = st.selectbox("Choose a role", sorted(JOBS["title"].unique()))
    questions = {
        "Junior Python Developer":["Explain a Python list vs tuple.","How would you handle an exception in Python?","Write the logic to count word frequencies in a sentence."],
        "Data Analyst Trainee":["How would you handle missing values?","Explain the difference between WHERE and HAVING in SQL.","How would you explain a chart to a non-technical manager?"],
        "Graduate Trainee":["Tell me about a time you solved a problem.","How do you prioritise multiple tasks?","How would you report a quality issue?"],
        "Technical Support Associate":["How would you troubleshoot a user who cannot connect to Wi-Fi?","How do you handle an upset customer?","What information would you collect before escalating an issue?"],
        "Operations Assistant":["How do you check a spreadsheet for errors?","How would you track daily operations?","Describe how you communicate a delay."],
        "SQL Reporting Intern":["Explain INNER JOIN vs LEFT JOIN.","How would you find duplicate records in SQL?","What makes a report reliable?"],
        "Sales Consultant":["How do you identify a customer's needs?","How would you respond to a price objection?","How do you follow up without pressuring a customer?"]
    }
    st.write("Answer these questions aloud or in your notes:")
    for i,q in enumerate(questions.get(role, ["Tell me about yourself.","Why are you interested in this role?","Describe a problem you solved."]),1):
        st.write(f"{i}. {q}")
    answer = st.text_area("Draft one answer for feedback checklist (optional)")
    if answer:
        st.caption(f"Draft length: {len(answer.split())} words. Checklist: answer the question directly, give a specific example, explain your action, and state the result.")

# -------------------- Job fairs --------------------
with pages[1]:
    st.subheader("Discover job fairs")
    st.write("Demo listings only. Organisers should verify event details before publication.")
    st.dataframe(FAIRS, use_container_width=True, hide_index=True)
    selected_fair = st.selectbox("Select a fair to register interest", FAIRS["name"].tolist())
    fair_email = st.text_input("Email (demo only; do not enter sensitive information)")
    if st.button("Register interest in fair"):
        st.success(f"Demo interest recorded for {selected_fair}. No email or external submission is sent.")
    st.subheader("Job-fair matching")
    fair_jobs = JOBS[JOBS["job_type"]=="Job Fair"].copy()
    fair_jobs["match_score"] = fair_jobs.apply(job_score, axis=1)
    st.dataframe(fair_jobs[["title","company","district","skills","salary_min","salary_max","match_score"]].sort_values("match_score",ascending=False), use_container_width=True, hide_index=True)
    st.caption("Future extension: organiser application forms, detailed JDs, ranked student-to-JD matching, and feedback from both sides.")

# -------------------- Employer workspace --------------------
with pages[2]:
    st.subheader("Employer workspace (prototype)")
    st.write("Review demo roles and their skill requirements. Candidate data is not real.")
    st.dataframe(JOBS[["company","title","sector","district","degree","skills","salary_min","salary_max"]], use_container_width=True, hide_index=True)
    st.markdown("**Create a draft job requirement**")
    with st.form("job_form"):
        company = st.text_input("Company name")
        title = st.text_input("Job title")
        sector = st.selectbox("Sector",["IT","IT Services","Automotive","Manufacturing","Energy","Retail","Other"])
        jd_skills = st.text_input("Required skills (comma-separated)")
        salary = st.number_input("Expected monthly salary (₹)", min_value=0, value=25000, step=1000)
        eligibility = st.text_input("Eligibility / degree")
        submitted = st.form_submit_button("Preview draft")
    if submitted:
        st.write({"company":company,"title":title,"sector":sector,"skills":jd_skills,"salary_monthly":salary,"eligibility":eligibility})
        st.info("Draft preview only; this prototype does not publish vacancies or contact candidates.")
    st.subheader("Candidate evaluation safeguards")
    st.write("- Use skills evidence and structured interview criteria; do not rely only on degree or certificates.")
    st.write("- Keep salary ranges transparent and confirm them with company policy.")
    st.write("- Track offer acceptance and joining outcomes only with appropriate consent and access controls.")

# -------------------- Analytics --------------------
with pages[3]:
    st.subheader("Job Demand & Sector Analytics")
    st.warning("All chart data on this tab is synthetic demo data. It is not official Karnataka employment data.")
    data = ANALYTICS.copy()
    c1,c2,c3 = st.columns(3)
    with c1: sectors = st.multiselect("Sector", sorted(data["sector"].unique()), default=sorted(data["sector"].unique()))
    with c2: districts = st.multiselect("District", sorted(data["district"].unique()), default=sorted(data["district"].unique()))
    with c3: periods = st.multiselect("Period", sorted(data["period"].unique()), default=sorted(data["period"].unique()))
    filt = data[data["sector"].isin(sectors) & data["district"].isin(districts) & data["period"].isin(periods)]
    k1,k2,k3 = st.columns(3)
    k1.metric("Demo records",len(filt))
    k2.metric("Demo posting indicators",int(filt["value"].sum()) if len(filt) else 0)
    k3.metric("Districts represented",filt["district"].nunique())
    if len(filt):
        sector_sum = filt.groupby("sector",as_index=False)["value"].sum()
        st.plotly_chart(px.bar(sector_sum,x="sector",y="value",title="Demo posting indicators by sector",labels={"value":"Posting indicator count","sector":"Sector"}),use_container_width=True)
        occ = filt.groupby("occupation",as_index=False)["value"].sum().sort_values("value",ascending=False).head(10)
        st.plotly_chart(px.bar(occ,x="value",y="occupation",orientation="h",title="Top occupations by selected demo indicator",labels={"value":"Posting indicator count","occupation":"Occupation"}),use_container_width=True)
        trend = filt.groupby(["period","district"],as_index=False)["value"].sum()
        st.plotly_chart(px.line(trend,x="period",y="value",color="district",markers=True,title="Demo period trend by district",labels={"value":"Posting indicator count","period":"Reporting period"}),use_container_width=True)
        st.dataframe(filt, use_container_width=True, hide_index=True)
        st.download_button("Download filtered analytics CSV",filt.to_csv(index=False).encode("utf-8"),"filtered_demo_analytics.csv","text/csv")
        st.subheader("Growth calculation (same demo indicator only)")
        choices = sorted(filt["period"].unique())
        if len(choices) >= 2:
            a,b = st.select_slider("Compare periods", options=choices, value=(choices[0],choices[-1]))
            selected = filt[filt["period"].isin([a,b])].groupby("period")["value"].sum()
            if a in selected.index and b in selected.index and selected[a] != 0:
                growth = (selected[b]-selected[a])/selected[a]*100
                st.write(f"Change in selected demo posting indicator from {a} to {b}: **{growth:.1f}%**.")
                st.caption("This is a change in a synthetic posting indicator, not proof of total employment growth.")
            else:
                st.write("Growth not calculable for this selection: missing or zero baseline.")
        else:
            st.write("Growth not calculated: at least two reporting periods are required.")
    else:
        st.info("No records match the selected filters.")
    st.subheader("District / state policy questions")
    st.write("This prototype can show district-wise demand indicators only where data exists. It does not estimate unemployment by degree or skill because no verified unemployment dataset is supplied.")
    st.write("Potential next analytics: job-fair participation, offers, joining rate, student feedback, employer feedback, and skill-gap summaries after collecting verified records.")

# -------------------- Upload and quality --------------------
with pages[4]:
    st.subheader("Upload a dataset")
    st.write("Accepted formats: CSV and Excel. For analytics, use fields such as period, district, sector, occupation, value, unit, indicator_type, source.")
    uploaded = st.file_uploader("Choose a CSV or Excel file", type=["csv","xlsx"], key="analytics_upload")
    if uploaded:
        try:
            up = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
            up.columns = [str(c).strip().lower().replace(" ","_") for c in up.columns]
            st.write("Preview")
            st.dataframe(up.head(100),use_container_width=True,hide_index=True)
            st.write("Shape:",up.shape)
            st.write("Missing values by column")
            missing = up.isna().sum().rename("missing_count").to_frame()
            st.dataframe(missing,use_container_width=True)
            required = {"period","district","sector","occupation","value"}
            absent = sorted(required-set(up.columns))
            if absent:
                st.error("Missing columns needed for the basic analytics view: " + ", ".join(absent))
            else:
                up["value_numeric"] = pd.to_numeric(up["value"],errors="coerce")
                invalid = int(up["value_numeric"].isna().sum())
                st.write(f"Rows with non-numeric or missing values: {invalid}")
                if invalid:
                    st.warning("Invalid values are flagged; they are not silently replaced with zero.")
                st.download_button("Download uploaded data with normalized headers",up.to_csv(index=False).encode("utf-8"),"validated_upload_preview.csv","text/csv")
            st.caption("Uploaded data is processed for this session. This demo does not establish that a dataset is official, licensed, or suitable for comparisons.")
        except Exception as e:
            st.error(f"Could not read this file: {e}")
    st.subheader("Expected analytics schema")
    st.code("period, district, sector, occupation, value, unit, indicator_type, source, source_url, access_date, limitations", language="text")

with pages[5]:
    st.subheader("Design, build, validate & prove")
    st.markdown("""
**Discover:** identify students, parents, employers, job-fair organisers, and district/state labour & skill departments as stakeholders.

**Define:** solve profile-to-job matching, skill-gap visibility, job-fair discovery, application tracking, and transparent labour-market analytics.

**Design:** student portal, job fairs, employer workspace, district/state analytics, data-quality and source screens.

**Build:** Python + Pandas + Streamlit + Plotly; CSV/Excel upload; simple matching score; charts and CSV export.

**Validate & prove:** test uploads, required columns, missing values, empty filters, rankings, period comparisons, and export consistency. Keep screenshots and expected-vs-actual test results.

**Risks, assumptions & safeguards**
- Demo jobs and analytics are synthetic; label them clearly.
- A job-posting count is not the same as an actual vacancy or total employment.
- Do not claim growth from one period; use comparable observations and disclose the formula.
- Do not compare districts with incompatible definitions, periods, units, or geography.
- Match scores are advisory and must not be used as automatic hiring decisions.
- CVs and personal data need consent, access control, secure storage, and a retention policy before real deployment.
- AI-generated recommendations should be reviewed by people and should not make final hiring or public-policy decisions.

**Deploy:** push `app.py` and `requirements.txt` to GitHub; on Render choose a Python web service, install dependencies with `pip install -r requirements.txt`, and use the start command `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`.

**Conclusion:** start with a reliable, transparent minimum viable prototype. Add verified labour-market sources, authentication, notifications, database storage, and AI features only after validating the data and privacy design.
""")
    st.caption("This is a hackathon starter, not a production recruitment platform. Do not enter real sensitive personal information.")



