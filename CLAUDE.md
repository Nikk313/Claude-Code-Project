# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Spendly is a personal expense tracking web application built with Flask. It allows users to log expenses, categorize spending, and understand their financial patterns.

## Commands

```bash
# Run the application
python app.py

# Run tests (pytest is configured but no tests exist yet)
pytest
```

The app runs on `http://localhost:5001` in debug mode.

## Architecture

- **Backend**: Flask (single `app.py` with route definitions)
- **Database**: SQLite (placeholder in `database/db.py` - students implement this)
- **Frontend**: Jinja2 templates with vanilla JavaScript
- **Styling**: Custom CSS with CSS variables (no framework)

## Project Structure

```
├── app.py                 # Flask application with routes
├── database/
│   └── db.py              # Database utilities (get_db, init_db, seed_db)
├── static/
│   ├── css/style.css      # All application styles
│   └── js/main.js         # Client-side JavaScript (video modal)
├── templates/
│   ├── base.html          # Base template with navbar/footer
│   ├── landing.html       # Landing page with hero and features
│   ├── login.html         # User login
│   ├── register.html      # User registration
│   ├── terms.html         # Terms and conditions
│   └── privacy.html       # Privacy policy
└── requirements.txt
```

## Key Patterns

- **Base template** (`base.html`) defines navbar, footer, and Google Fonts (DM Serif Display, DM Sans)
- **Auth pages** use `.auth-section` styling with centered card layout
- **Legal pages** use `.legal-page` styling with sectioned content
- **Video modal** in landing page loads YouTube embed on click (autoplay enabled)

## Development Status

This is a student project in progress. Currently implemented:
- Landing page with hero section and features
- Login/register UI (no backend logic)
- Terms and privacy pages
- Database placeholder (to be implemented)

Routes marked as "coming in Step X" are placeholders for future implementation:
- `/logout` (Step 3)
- `/profile` (Step 4)
- `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` (Steps 7-9)

## Tech constraints
- Flask only — no FastAPI, no Django, no other web frameworks
- SQLite only — no PostgreSQL, no SQLAlchemy ORM, no external DB
- Vanilla JS only — no React, no jQuery, no npm packages
- No new pip packages — work within requirements.txt as-is unless explicitly told otherwise
- Python 3.10+ assumed — f-strings and match statements are fine

## Subagent Policy
- Always use a builtin explore subagent for codebase exploration before implementing any new feature
- Always use a subagent to verify test results after any implementation
- When asked to plan, delegate codebase research to a subagent before presenting the plan
- always use a builtin plan subagent in plan mode

## Warnings and things to avoid
- Never use raw string returns for stub routes once a step is implemented — always render a template
- Never hardcode URLs in templates — always use url_for()
- Never put DB logic in route functions — it belongs in database/db.py
- Never install new packages mid-feature without flagging it — keep requirements.txt in sync
- Never use JS frameworks — the frontend is intentionally vanilla
- database/db.py is currently empty — do not assume helpers exist until the step that implements them
- FK enforcement is manual — SQLite foreign keys are off by default; get_db() must run PRAGMA foreign_keys = ON on every connection
- The app runs on port 5001, not the Flask default 5000 — don't change this