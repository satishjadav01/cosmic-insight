<div align="center">

  <h1>🌌 Cosmic Insight</h1>
  <p><b>Next-Generation Astrology, Numerology & Marriage Compatibility Engine</b></p>

  <p>
    <a href="https://github.com/satishjadav01/cosmic-insight/stargazers"><img src="https://img.shields.io/github/stars/satishjadav01/cosmic-insight?style=for-the-badge&color=7c3aed&logo=github" alt="Stars"></a>
    <a href="https://github.com/satishjadav01/cosmic-insight/network/members"><img src="https://img.shields.io/github/forks/satishjadav01/cosmic-insight?style=for-the-badge&color=9333ea&logo=github" alt="Forks"></a>
    <a href="https://github.com/satishjadav01/cosmic-insight/issues"><img src="https://img.shields.io/github/issues/satishjadav01/cosmic-insight?style=for-the-badge&color=c084fc&logo=github" alt="Issues"></a>
    <a href="https://github.com/satishjadav01/cosmic-insight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge&color=4c1d95" alt="License"></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
    <img src="https://img.shields.io/badge/Django_REST-Framework-red?style=for-the-badge&logo=django&logoColor=white" alt="DRF">
    <img src="https://img.shields.io/badge/ReportLab-PDF-ff69b4?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="ReportLab">
    <img src="https://img.shields.io/badge/AWS_Beanstalk-Deployed-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white" alt="AWS">
    <img src="https://img.shields.io/badge/Render-Ready-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render">
  </p>

  <br />

  <p align="center">
    <b>Cosmic Insight</b> is an advanced web application built on Django and Python. It delivers deep numerology predictions, celestial life plane assessments, marriage compatibility calculations, and automated high-quality PDF report generation.
    <br /><br />
    <a href="#-key-features">Explore Features</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-deployment">Deployment</a> •
    <a href="#-author">Author</a>
  </p>
</div>

---

## 📖 Overview

**Cosmic Insight** bridges ancient astrological wisdom with modern Web & API technology. By processing user birth details, life metrics, and cosmic plane patterns, it produces real-time insights, interactive compatibility scores, and downloadable PDF reports.

Whether you're calculating life path numbers, determining marriage compatibility, or generating comprehensive astrological dossiers, Cosmic Insight offers an end-to-end, enterprise-ready solution.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🔮 **Numerology Calculations** | Automated computation of driver numbers, conductor numbers, and planetary line placements. |
| ✈️ **Life Plane Grid Analysis** | Interactive 3x3 plane visualization detailing mental, emotional, and practical grids. |
| 💑 **Marriage Compatibility Engine** | Multi-factor matching algorithm calculating compatibility percentages and relationship traits. |
| 📄 **Automated PDF Report Engine** | Dynamic vector PDF document generation using ReportLab with customized styling and tables. |
| 🛡️ **Wizard Step Protection** | Custom navigation middleware (`NavigationGuardMiddleware`) preventing illegal wizard bypasses. |
| 🔐 **Authentication & Session Control** | OTP verification system, custom session state persistence, and user repository patterns. |
| ☁️ **Multi-Cloud Ready** | Turnkey support for deployment via AWS Elastic Beanstalk (`.ebextensions`) and Render (`render.yaml`). |

---

## 🛠️ Tech Stack & Language Icons

### **Backend Framework & Core**
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="18" height="18" /> **Python 3.11+**: Primary logic & numerical calculation algorithms
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="18" height="18" /> **Django 5.2**: Web server, MVC structure, ORM & authentication
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-plain.svg" width="18" height="18" /> **Django REST Framework (DRF)**: RESTful API endpoints & serialization

### **Frontend & UI**
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" width="18" height="18" /> **HTML5**: Semantic UI layouts and template rendering
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" width="18" height="18" /> **CSS3**: Custom glassmorphism, responsive grid styling & themes
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" width="18" height="18" /> **JavaScript (ES6+)**: Dynamic form interactions, validation, and AJAX updates

### **PDF Generation & Static Assets**
- 📄 **ReportLab**: High-performance PDF canvas and dynamic document layout engine
- 🎨 **WhiteNoise**: Efficient static asset serving for production environments

### **Deployment & Cloud**
- <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" width="22" height="22" /> **AWS Elastic Beanstalk**: Automated scaling infrastructure
- 🚀 **Render**: One-click cloud hosting support with gunicorn

---

## 📁 Project Structure

```bash
Cosmic-Insight-astrology/
├── .ebextensions/        # AWS Elastic Beanstalk configuration files
├── parts/                # Core Application Module
│   ├── utils/            # Calculation modules (numerology, match, protection, lucky)
│   ├── repositories.py   # Repository pattern for database abstraction
│   ├── Services.py       # Numerology & Marriage calculation services
│   ├── serializers.py    # DRF API Serializers
│   ├── views.py          # View handlers & PDF generation logic
│   └── urls.py           # Application URL routing
├── pro17/                # Django Project Root
│   ├── middleware.py     # Custom Navigation Guard Middleware
│   ├── settings.py       # Environment & App Configuration
│   └── urls.py           # Root URL Configuration
├── template/             # HTML5 Templates
│   ├── index.html        # Landing page
│   ├── profile.html      # User profile dashboard
│   ├── yourplane.html    # 3x3 Life plane grid view
│   └── table.html        # Results & numerology tables
├── Procfile              # Gunicorn process definition
├── render.yaml           # Render deployment configuration
├── build.sh              # Production build automation script
├── requirements.txt      # Python dependencies
└── manage.py             # Django CLI management script
```

---

## ⚡ Quick Start Guide

### Prerequisites
- **Python 3.10+** installed on your system
- **Git** installed

### 1. Clone the Repository
```bash
git clone https://github.com/satishjadav01/cosmic-insight.git
cd cosmic-insight/Cosmic-Insight-astrology-main
```

### 2. Create and Activate Virtual Environment
* **On Windows (PowerShell / CMD):**
  ```powershell
  python -m venv .venv
  \.venv\Scripts\activate
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Start Development Server
```bash
python manage.py migrate
python manage.py runserver
```

Open your browser and navigate to **`http://127.0.0.1:8000/`**.

---

## 🔌 API Endpoints Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Main landing page |
| `/DateofBirth/` | `GET / POST` | Birthdate input and initial grid generation |
| `/yourplane/` | `GET / POST` | 3x3 Life plane analysis dashboard |
| `/marriage_score/` | `GET / POST` | Partner compatibility calculation engine |
| `/generate_pdf/` | `GET` | Generates & streams dynamic numerology PDF report |
| `/login/` | `GET / POST` | Mobile & OTP based user authentication |

---

## ☁️ Deployment

### Deploying to Render
1. Connect your GitHub repository `satishjadav01/cosmic-insight` to https://cosmic-insight-e72j.onrender.com/
2. Select **Web Service** using `render.yaml` or set build command:
   ```bash
   ./build.sh
   ```
3. Set start command:
   ```bash
   gunicorn pro17.wsgi:application
   ```

### Deploying to AWS Elastic Beanstalk
```bash
eb init -p python-3.11 cosmic-insight-app
eb create cosmic-insight-env
eb open
```

---

## 👤 Author

**Satish Jadav**
* GitHub: [@satishjadav01](https://github.com/satishjadav01)

---

<div align="center">
  <sub>Built with ❤️ and 🔮 by Satish Jadav. If you find this project helpful, please give it a ⭐️ on GitHub!</sub>
</div>
