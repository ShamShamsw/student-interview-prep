# Tech Career Paths — Overview for Beginners

Not sure which direction to go? This guide breaks down the most common software / data careers so you can make an informed choice before investing months of study time.

---

## How to use this guide

1. Read each section briefly.
2. Notice which one makes you think "that sounds like something I'd actually enjoy."
3. Follow the **Getting started** links inside that section.
4. You do **not** have to pick forever — many people switch tracks after their first job.

---

## Career map at a glance

```
                     ┌─────────────┐
                     │   Software  │
            ┌────────┤  Engineering├────────┐
            │        └─────────────┘        │
            ▼                               ▼
     ┌─────────────┐                 ┌─────────────┐
     │  Frontend   │                 │   Backend   │
     └──────┬──────┘                 └──────┬──────┘
            │                               │
            └──────────┬────────────────────┘
                       ▼
                ┌─────────────┐
                │  Fullstack  │
                └─────────────┘

                     ┌─────────────┐
                     │    Data     │
            ┌────────┤   Careers   ├────────┐
            │        └─────────────┘        │
            ▼                               ▼
     ┌─────────────┐                 ┌──────────────┐
     │    Data     │                 │    Data      │
     │   Science   │                 │  Engineering │
     └──────┬──────┘                 └──────────────┘
            │
            ▼
     ┌─────────────┐
     │   Machine   │
     │   Learning  │
     │  / MLOps    │
     └─────────────┘

     ┌─────────────┐    ┌──────────────┐    ┌────────────┐
     │  DevOps /   │    │   QA /       │    │  Cyber-    │
     │   Cloud     │    │   Testing    │    │  security  │
     └─────────────┘    └──────────────┘    └────────────┘
```

---

## Frontend Development

### What you build
User interfaces — everything a person sees and clicks in a browser or mobile app. Buttons, layouts, forms, animations, dashboards.

### Day-to-day work
- Writing HTML, CSS, and JavaScript
- Building components in React, Vue, or Angular
- Fetching data from APIs and rendering it
- Making sites responsive (work on phone + desktop)
- Working closely with designers

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| HTML & CSS | The skeleton and styling of every web page |
| JavaScript (ES6+) | Makes pages interactive |
| React (or Vue) | Industry-standard component frameworks |
| Browser DevTools | Debugging and performance profiling |
| REST APIs (consuming) | Pulling data from the backend |
| Git | Version control — universal requirement |

### Typical job titles
- Frontend Developer
- UI Developer
- React Developer
- Web Developer

### Salary range (US, entry-level)
$65,000 – $100,000 / year

### Good fit if you...
- Enjoy visual results you can immediately see
- Care about user experience and design
- Like quick feedback loops (change code, refresh browser)

### Getting started in this repo
- [Frontend Interview Questions](../interview-questions/03-frontend.md)
- [Python Cheatsheet](../cheatsheets/PYTHON_CHEATSHEET.md) (general CS fundamentals still apply)

### External resources
- [The Odin Project (free)](https://www.theodinproject.com/)
- [freeCodeCamp Responsive Web Design (free)](https://www.freecodecamp.org/)
- [MDN Web Docs (reference)](https://developer.mozilla.org/)

---

## Backend Development

### What you build
The server side — APIs, databases, authentication, business logic, and everything that runs behind the scenes to power an app.

### Day-to-day work
- Building REST or GraphQL APIs
- Writing database queries (SQL)
- Handling authentication (JWT, OAuth)
- Writing background jobs and scheduled tasks
- Optimizing slow queries and services

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| Python / Node.js / Java / Go | Pick one backend language |
| SQL (PostgreSQL, MySQL) | Every backend touches a database |
| REST API design | Standard communication pattern |
| Authentication & authorization | Security fundamentals |
| Docker basics | Containerizing services |
| Git | Version control — universal requirement |

### Typical job titles
- Backend Developer
- API Developer
- Software Engineer (Backend)
- Node.js / Python Developer

### Salary range (US, entry-level)
$70,000 – $110,000 / year

### Good fit if you...
- Like solving logic problems more than visual work
- Enjoy thinking about data flow and system behavior
- Care about performance, reliability, and security

### Getting started in this repo
- [Backend Interview Questions](../interview-questions/04-backend.md)
- [Python coding problems](../../languages/python/problems/)

### External resources
- [FastAPI tutorial (Python)](https://fastapi.tiangolo.com/tutorial/)
- [SQLZoo (SQL practice)](https://sqlzoo.net/)
- [CS50 Web (free, Harvard)](https://cs50.harvard.edu/web/)

---

## Fullstack Development

### What you build
Both the frontend and backend — you own the entire feature from database to browser.

### Day-to-day work
- All of the frontend and backend work above
- Connecting a frontend to a backend API you built yourself
- Deploying full applications end-to-end
- Often working in smaller teams or as a solo contributor

### Core skills to learn
Everything in Frontend + Backend, plus:
| Skill | Why it matters |
|-------|---------------|
| Next.js / Remix | React frameworks with built-in backend capabilities |
| Database design | Schema design, relationships, migrations |
| Deployment (Vercel, Heroku, AWS) | Getting your app live |
| CI/CD basics | Automating builds and tests |

### Typical job titles
- Fullstack Developer
- Software Engineer
- Web Application Developer

### Salary range (US, entry-level)
$75,000 – $115,000 / year

### Good fit if you...
- Want to understand the full picture
- Like variety — switching between UI and servers
- Want to build complete side projects solo

### Getting started in this repo
- [Fullstack Interview Questions](../interview-questions/05-fullstack.md)
- [Mock Interview Guide](MOCK_INTERVIEW_GUIDE.md)

---

## Data Science

### What you build
Insights, models, and analyses that help businesses make better decisions using data — dashboards, statistical reports, predictive models.

### Day-to-day work
- Cleaning and transforming messy data (most of the job)
- Exploratory data analysis (EDA)
- Building and evaluating statistical models
- Creating visualizations and presenting to stakeholders
- Writing SQL for data extraction

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| Python (pandas, NumPy) | Data manipulation |
| Statistics & probability | Foundation of all data science |
| SQL | Pulling data from databases |
| Matplotlib / seaborn | Visualization |
| scikit-learn | Machine learning library |
| Excel / Google Sheets | Still widely used for reporting |

### Typical job titles
- Data Scientist
- Data Analyst
- Business Intelligence (BI) Analyst
- Quantitative Analyst

### Salary range (US, entry-level)
$70,000 – $105,000 / year

### Good fit if you...
- Enjoy statistics and math
- Like telling stories with data
- Are curious about "why" patterns exist
- Enjoy working with Excel or spreadsheets today

### Difference from Machine Learning
Data Science is broader and more focused on analysis and decision-making. ML is a sub-area focused on building predictive models and deploying them at scale.

### Getting started in this repo
- [Data Science Interview Questions](../interview-questions/08-data-science.md)
- [Data Science Cheatsheet](../cheatsheets/DATA_SCIENCE_CHEATSHEET.md)
- [Excel Formulas Cheatsheet](../cheatsheets/EXCEL_FORMULAS_CHEATSHEET.md)
- [Data Science Guide](DATA_SCIENCE_GUIDE.md)
- [Mini-project: Excel-Style Data Analysis](../../languages/python/mini-projects/06-excel-data-analysis/README.md)
- [Mini-project: EDA](../../languages/python/mini-projects/07-exploratory-data-analysis/README.md)

### External resources
- [Kaggle Learn (free, hands-on)](https://www.kaggle.com/learn)
- [StatQuest YouTube (statistics explained visually)](https://www.youtube.com/@StatQuest)
- [fast.ai (practical ML, free)](https://www.fast.ai/)

---

## Machine Learning Engineering / MLOps

### What you build
Production ML systems — models that run at scale, retrain automatically, serve predictions to millions of users, and don't drift silently into garbage.

### Day-to-day work
- Training and evaluating ML models
- Building feature pipelines
- Deploying models as APIs or batch jobs
- Monitoring model performance in production
- A/B testing model versions

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| Python (scikit-learn, PyTorch / TensorFlow) | Model building |
| Statistics & linear algebra | ML math foundation |
| SQL + data pipelines | Feature engineering at scale |
| Docker & Kubernetes | Containerized model serving |
| MLflow / Weights & Biases | Experiment tracking |
| Cloud (AWS SageMaker, GCP Vertex AI) | Where models live in production |

### Typical job titles
- Machine Learning Engineer
- MLOps Engineer
- Applied Scientist
- AI Engineer

### Salary range (US, entry-level)
$90,000 – $140,000 / year

### Good fit if you...
- Love both software engineering and math/statistics
- Enjoy building systems, not just notebooks
- Want to work on cutting-edge AI products

### Path to get here
Most ML Engineers first work as a Data Scientist or Backend Engineer, then specialize. Do not try to start directly with ML before having solid Python + statistics fundamentals.

### Getting started in this repo
- [Data Science Cheatsheet](../cheatsheets/DATA_SCIENCE_CHEATSHEET.md)
- [Data Science Interview Questions](../interview-questions/08-data-science.md)
- [Data Science Capstone Project](../../languages/python/projects/data-science-capstone/README.md)

---

## Data Engineering

### What you build
The plumbing of data — pipelines that collect, move, clean, and store data reliably so that analysts and scientists have good data to work with.

### Day-to-day work
- Building ETL / ELT pipelines
- Designing data warehouse schemas
- Maintaining Airflow DAGs or dbt models
- Optimizing slow queries and storage
- Ensuring data quality and freshness

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| SQL (advanced) | Primary language of data warehouses |
| Python (pipeline scripting) | Automation and data processing |
| Airflow / Prefect | Pipeline orchestration |
| dbt | SQL transformation framework |
| Spark | Large-scale distributed processing |
| Cloud storage (S3, GCS) | Where raw data lives |
| Data warehouse (Snowflake, BigQuery, Redshift) | Analytical query layer |

### Typical job titles
- Data Engineer
- Analytics Engineer
- Platform Data Engineer
- ETL Developer

### Salary range (US, entry-level)
$80,000 – $120,000 / year

### Good fit if you...
- Like building reliable, automated systems
- Enjoy SQL and backend-style work
- Care more about data infrastructure than analysis

### Getting started in this repo
- [Data Engineering Interview Questions](../interview-questions/09-data-engineering.md)
- [SQL Analytics Cheatsheet](../cheatsheets/SQL_ANALYTICS_CHEATSHEET.md)
- [SQL Analytics Mini-Project](../../languages/python/mini-projects/08-sql-analytics/README.md)
- [SQL Problems 11–14](../../languages/sql/problems/)

---

## DevOps / Cloud Engineering

### What you build
Deployment pipelines, infrastructure, monitoring, and the automation that lets developers ship code quickly and reliably.

### Day-to-day work
- Writing infrastructure as code (Terraform, CloudFormation)
- Managing CI/CD pipelines (GitHub Actions, Jenkins)
- Container orchestration (Kubernetes)
- Monitoring and alerting (Datadog, Prometheus)
- Cloud cost optimization

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| Linux CLI | Foundation of all server work |
| Docker & Kubernetes | Containers everywhere |
| Terraform | Infrastructure as code |
| GitHub Actions / Jenkins | CI/CD pipelines |
| AWS / GCP / Azure | Cloud platforms |
| Bash / Python scripting | Automation |

### Typical job titles
- DevOps Engineer
- Site Reliability Engineer (SRE)
- Cloud Engineer
- Platform Engineer

### Salary range (US, entry-level)
$75,000 – $115,000 / year

### Good fit if you...
- Enjoy automation ("why do this manually?")
- Like systems thinking and reliability problems
- Are comfortable in the terminal

---

## QA / Software Testing

### What you build
Confidence that software works correctly — test plans, automated test suites, bug reports.

### Day-to-day work
- Writing unit, integration, and end-to-end tests
- Finding bugs before users do
- Building test automation frameworks
- Reviewing requirements for testability

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| Any programming language (Python preferred) | Test automation |
| pytest / Jest | Testing frameworks |
| Selenium / Playwright | Browser automation |
| API testing (Postman) | Backend validation |
| SQL | Database verification |

### Typical job titles
- QA Engineer
- Software Development Engineer in Test (SDET)
- Test Automation Engineer

### Salary range (US, entry-level)
$55,000 – $90,000 / year

### Good fit if you...
- Have a "break things" mindset
- Are detail-oriented
- Want to code but also care deeply about quality

---

## Cybersecurity

### What you build
Defenses against attacks — firewalls, security audits, incident response plans, penetration tests.

### Day-to-day work
- Identifying vulnerabilities in systems
- Monitoring for threats and breaches
- Writing security policies
- Ethical hacking / penetration testing
- Security code reviews

### Core skills to learn
| Skill | Why it matters |
|-------|---------------|
| Networking fundamentals | TCP/IP, DNS, HTTP are attack surfaces |
| Linux | Most infrastructure runs on Linux |
| Python / Bash | Scripting for automation and tooling |
| Common vulnerabilities (OWASP Top 10) | What to look for |
| Cryptography basics | How secrets are protected |

### Typical job titles
- Security Analyst
- Penetration Tester
- Security Engineer
- SOC Analyst

### Salary range (US, entry-level)
$65,000 – $105,000 / year

### Good fit if you...
- Enjoy thinking like an attacker
- Are interested in how systems can be broken (legally)
- Like the detective aspect of tracing incidents

---

## Side-by-side comparison

| Career | Math heavy | Visual work | Systems thinking | Entry difficulty | Avg entry salary (US) |
|--------|-----------|-------------|-----------------|-----------------|----------------------|
| Frontend | Low | High | Low | Moderate | $65k–$100k |
| Backend | Low–Med | Low | High | Moderate | $70k–$110k |
| Fullstack | Low–Med | Med | High | Moderate–Hard | $75k–$115k |
| Data Science | High | Med | Med | Moderate–Hard | $70k–$105k |
| ML Engineering | High | Low | High | Hard | $90k–$140k |
| Data Engineering | Med | Low | High | Moderate–Hard | $80k–$120k |
| DevOps / Cloud | Low | Low | High | Moderate | $75k–$115k |
| QA / Testing | Low | Low | Med | Easy–Moderate | $55k–$90k |
| Cybersecurity | Med | Low | High | Moderate | $65k–$105k |

> **Note:** Salaries vary widely by location, company size, and experience. These are rough US national averages for entry-level roles as of 2025–2026.

---

## "Which one should I start with?"

### You don't know what you like yet
→ Start with **Fullstack** (you see the whole picture and can pivot)

### You're good at / enjoy math and statistics
→ **Data Science** → then specialize into ML or Data Engineering

### You want to get hired fast with the least prerequisites
→ **Frontend** or **QA** — lower barrier, strong demand

### You love automating and hate doing things manually
→ **DevOps / Cloud** or **Data Engineering**

### You want the highest salary ceiling
→ **ML Engineering** (most competitive, requires the most breadth)

---

## Next steps

1. Pick a track that interests you
2. Open the matching interview questions file to see what skills are expected
3. Follow the [Learning Path](../paths/LEARNING_PATH.md) for your track
4. Build one project from the [mini-projects](../../languages/python/mini-projects/) or [projects](../../languages/python/projects/) directories
