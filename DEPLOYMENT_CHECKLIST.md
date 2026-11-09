# Deployment Checklist

Use this checklist to ensure your QueryQuest deployment is ready for production or CTF use.

## Pre-Deployment

### Code Preparation
- [ ] All code is committed to git
- [ ] `.env` file is NOT committed (should be in `.gitignore`)
- [ ] `.env.example` exists with template values
- [ ] `requirements.txt` is up to date
- [ ] `README.md` is complete and accurate

### Configuration
- [ ] Generate a strong `SECRET_KEY`
  ```bash
  python3 -c 'import secrets; print(secrets.token_hex(32))'
  ```
- [ ] Set a unique `CTF_FLAG` value
- [ ] Set `COOKIE_SECURE=1` for HTTPS deployments
- [ ] Review `render.yaml` or deployment config

### Repository
- [ ] Code pushed to GitHub/GitLab
- [ ] Repository is public or accessible to Render
- [ ] Branch is set to `main` or `master`

## Render Deployment

### Initial Setup
- [ ] Render account created and verified
- [ ] GitHub account connected to Render
- [ ] Payment method added (if using paid tier)

### Service Configuration
- [ ] New Web Service created
- [ ] Repository connected
- [ ] `render.yaml` detected automatically
- [ ] Environment variables configured:
  - [ ] `SECRET_KEY` (auto-generated or custom)
  - [ ] `CTF_FLAG` (your unique flag)
  - [ ] `COOKIE_SECURE=1`
  - [ ] `PYTHON_VERSION=3.11`

### Persistent Storage (Optional)
- [ ] Disk created: `queryquest-data`
- [ ] Mount path: `/opt/render/project/src/instance`
- [ ] Size: 1 GB minimum

### Build & Deploy
- [ ] Build command verified: `pip install -r requirements.txt && python init_db.py`
- [ ] Start command verified: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 30 --access-logfile - --error-logfile - 'app:create_app()'`
- [ ] Service deployed successfully
- [ ] Build logs reviewed for errors
- [ ] Service status shows "Live"

## Post-Deployment Testing

### Basic Functionality
- [ ] Application URL accessible
- [ ] HTTPS certificate valid (no warnings)
- [ ] Login page loads correctly
- [ ] CSS and static assets load
- [ ] No console errors in browser

### Authentication
- [ ] Login with `trainee` / `trainee123` works
- [ ] Dashboard displays after login
- [ ] Logout works correctly
- [ ] Session persists across page loads

### Core Features
- [ ] Records page lists ordinary records
- [ ] Individual record details display
- [ ] Search functionality works
- [ ] Vulnerable search endpoint accessible

### Security
- [ ] SQL injection vulnerability present (for CTF)
- [ ] No unintended vulnerabilities exposed
- [ ] No sensitive data in logs
- [ ] Error pages don't leak information

### Database
- [ ] Database initialized with sample data
- [ ] Hidden records exist (for CTF solution)
- [ ] Data persists across restarts (if using disk)

## CTF Platform Integration

### Challenge Setup
- [ ] Challenge added to CTF platform (CTFd, etc.)
- [ ] Challenge name: "QueryQuest - The Forgotten Records"
- [ ] Category: Web Exploitation
- [ ] Points value assigned (suggested: 300-350)
- [ ] Description added from `PARTICIPANT_CHALLENGE.md`
- [ ] Connection info: Render URL
- [ ] Flag matches deployment `CTF_FLAG`

### Hints (Optional)
- [ ] Hint 1: Search functionality hint
- [ ] Hint 2: SQL injection keyword hint
- [ ] Hint 3: Database exploration hint

### Testing
- [ ] Solve the challenge from scratch
- [ ] Verify flag submission works
- [ ] Test from participant perspective
- [ ] Check hints are helpful but not too revealing

## Monitoring & Maintenance

### Initial Monitoring
- [ ] Check logs for errors
- [ ] Monitor CPU and memory usage
- [ ] Verify no crashes or restarts
- [ ] Test from different networks/locations

### During CTF Event
- [ ] Monitor service health
- [ ] Watch for abuse or DOS attempts
- [ ] Keep backup of database
- [ ] Have rollback plan ready

### Documentation
- [ ] Participant instructions clear
- [ ] Admin/organizer notes prepared
- [ ] Support contact information available
- [ ] Known issues documented

## Performance Optimization (Optional)

- [ ] Enable caching headers for static assets
- [ ] Optimize database queries
- [ ] Add rate limiting if needed
- [ ] Upgrade to paid tier if free tier insufficient

## Cleanup (After Event)

- [ ] Archive database/logs
- [ ] Document any issues encountered
- [ ] Gather feedback from participants
- [ ] Delete or suspend Render service
- [ ] Remove from CTF platform

## Troubleshooting Reference

### Common Issues
- **503 errors:** Service spinning up (free tier) - wait 30-60 seconds
- **Database not found:** Check build logs, ensure init_db.py ran
- **Login fails:** Verify database initialized correctly
- **Static files 404:** Check static file paths and Flask configuration
- **Environment variables not loaded:** Verify Render dashboard settings

### Support Resources
- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- Project Issues: Check GitHub repository

---

**Status:** 
- [ ] Pre-deployment complete
- [ ] Deployment successful
- [ ] Testing passed
- [ ] CTF integration done
- [ ] Ready for participants

**Deployment Date:** ___________  
**Deployed By:** ___________  
**Render URL:** ___________  
**CTF Platform:** ___________
