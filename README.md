# QueryQuest - SQL Injection CTF Challenge

A deliberately vulnerable web application designed for Capture The Flag (CTF) competitions and SQL injection training.

## 🎯 Challenge Overview

QueryQuest is a fictional business records management system with an intentional SQL injection vulnerability. Participants must discover and exploit the vulnerability to find hidden records containing the flag.

## 🚀 Quick Start

### Local Development

1. **Clone and setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY and CTF_FLAG
   ```

3. **Initialize and run:**
   ```bash
   python init_db.py
   flask run
   ```

4. **Access the application:**
   - Open http://localhost:5000
   - Login with `trainee` / `trainee123`

### Deploy to Render

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Push to GitHub
2. Connect to Render
3. Render auto-detects `render.yaml`
4. Deploy! 🚀

### Docker Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production Docker deployment with docker-compose.

```bash
cp .env.example .env
# Edit .env with your secrets
docker-compose up -d --build
```

## 📋 Features

- **Authentication System** - Login/logout functionality
- **Records Browser** - View business records
- **Search Interface** - Find records by name
- **Vulnerable Endpoint** - SQL injection opportunity
- **Hidden Data** - Secret records with flag

## 🔐 Default Credentials

| Username | Password   |
|----------|------------|
| trainee  | trainee123 |

## 🏗️ Tech Stack

- **Backend:** Python 3.11, Flask 3.0
- **Database:** SQLite3
- **Server:** Gunicorn
- **Frontend:** HTML, CSS, Jinja2 templates

## 📁 Project Structure

```
sqli/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Safe routes
│   ├── vulnerable_search.py # Vulnerable search endpoint
│   ├── models.py            # Database models
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── instance/data/           # SQLite database (created on init)
├── config.py                # Configuration
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment config
└── README.md               # This file
```

## ⚠️ Security Warning

**This application is intentionally vulnerable!**

- Contains SQL injection vulnerabilities
- For educational purposes only
- Never use with real data
- Deploy in isolated environments only
- Not for production use

## 🎓 Learning Objectives

Participants will learn:
- SQL injection identification
- SQL query manipulation
- UNION-based injection attacks
- Database schema enumeration
- Data extraction techniques

## 📝 Challenge Hints

<details>
<summary>Hint 1 (Click to reveal)</summary>
The search functionality might not properly sanitize input...
</details>

<details>
<summary>Hint 2 (Click to reveal)</summary>
Try using SQL keywords in your search queries
</details>

<details>
<summary>Hint 3 (Click to reveal)</summary>
There might be other tables in the database...
</details>

## 🛠️ Development

### Running Tests
```bash
source venv/bin/activate
python -m pytest
```

### Database Reset
```bash
rm -rf instance/data/
python init_db.py
```

## 📚 Documentation

- [Render Deployment Guide](RENDER_DEPLOYMENT.md) - Deploy to Render
- [Docker Deployment Guide](DEPLOYMENT.md) - Production Docker setup
- [Participant Challenge](PARTICIPANT_CHALLENGE.md) - Challenge description

## 🤝 Contributing

This is a CTF challenge application. If you find security issues beyond the intentional vulnerability, please report them responsibly.

## 📄 License

This project is intended for educational use in authorized CTF competitions.

## 🎖️ Credits

Created for CTF competitions and SQL injection training workshops.

---

**Remember:** Only use this application in authorized educational environments. Never deploy to public internet without proper isolation and monitoring.
