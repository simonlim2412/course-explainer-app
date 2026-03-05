# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based web application that displays course information. The application uses a simple MVC-style architecture with Flask handling routing, view functions rendering templates, and a Course model managing course data.

## Development Environment

### Setup

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/Mac
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Dependencies (`requirements.txt`):
- `Flask==3.1.2` — web framework
- `gunicorn==20.1.0` — WSGI server for production
- `python-dotenv==0.21.0` — loads `.env` configuration

### Running the Application

```bash
python src/app.py
```

The application will be available at `http://127.0.0.1:5000`

### Running Tests

```bash
# Run all tests
python -m unittest discover -s tests

# Run a specific test file
python -m unittest tests.test_app

# Run a specific test case
python -m unittest tests.test_app.AppTestCase.test_index
```

## Repository Structure

```
course-explainer-app/
├── .claude/                          # Claude Code configuration
│   ├── agents/
│   │   ├── ui-testing-agent.md       # Agent for UI verification
│   │   └── ux-design-planner.md      # Agent for UX planning
│   ├── commands/
│   │   ├── implement_ui_user_story.md
│   │   └── explain_this_file.md
│   ├── skills/
│   │   └── ui-designer/              # UI/UX design skill
│   └── settings.local.json
├── .github/workflows/
│   ├── claude.yml                    # Claude Code GitHub Actions integration
│   └── claude-code-review.yml        # Automated code review
├── src/                              # Main application source
│   ├── app.py                        # Flask app entry point and route registration
│   ├── views.py                      # View functions (HTTP handlers)
│   ├── models.py                     # Course data model and in-memory data
│   ├── templates/
│   │   ├── layout.html               # Base template (header, nav, footer)
│   │   ├── index.html                # Home page (hero + course grid)
│   │   ├── course.html               # Course detail page
│   │   └── contact.html              # Contact form + social links
│   └── static/css/
│       └── styles.css                # All CSS (542 lines, CSS variables)
├── tests/
│   └── test_app.py                   # Unit tests (11 test cases)
├── CLAUDE.md                         # This file
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
└── .gitignore                        # Excludes venv/, .env, __pycache__, etc.
```

## Architecture

### Application Structure

The application follows a modular Flask design:

- **src/app.py**: Application entry point and Flask configuration. Routes are registered using `add_url_rule()` rather than decorators, which allows views to remain decoupled from Flask.
- **src/views.py**: View functions that handle HTTP requests and return rendered templates. Views are pure functions that don't depend on Flask decorators.
- **src/models.py**: Data models (currently in-memory Course objects stored in a list). No database backend — all course data is hardcoded.
- **src/templates/**: Jinja2 HTML templates with inheritance structure (`layout.html` as base).
- **src/static/css/**: CSS stylesheets for the application.

### Routes

Registered in `app.py` via `add_url_rule()`:

| Method | Path | View | Description |
|--------|------|------|-------------|
| GET | `/` | `index` | Home page with course listing |
| GET | `/course/<course_id>` | `course` | Course detail (1-based ID) |
| GET, POST | `/contact` | `contact` | Contact form |

### View Functions (`src/views.py`)

- **`index()`**: Fetches the `courses` list from `models.py` and renders `index.html`.
- **`course(course_id)`**: Looks up a course by 1-based index. Returns 404 if `course_id` is out of range.
- **`contact()`**: Handles GET (render form) and POST (validate + process). Server-side validation:
  - Name: required (non-empty)
  - Email: must match regex `r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'`
  - Address: minimum 10 characters
  - On success: prints form data to stdout and re-renders with `success=True`
  - On failure: re-renders form with an `errors` dict

### Data Model (`src/models.py`)

```python
class Course:
    def __init__(self, title, description, instructor, duration, topics=None):
        ...
```

Current courses (hardcoded, in-memory):

1. "Introduction to Python" — John Doe — 4 weeks
2. "Web Development with Flask" — Jane Smith — 6 weeks
3. "Data Science Fundamentals" — Alice Johnson — 8 weeks
4. "Go Programming Essentials" — Robert Chen — 5 weeks

To add a course, edit the `courses` list in `models.py`.

### Key Design Patterns

1. **Separation of concerns**: Routes (`app.py`), view logic (`views.py`), and data (`models.py`) are separated into distinct modules.
2. **Template inheritance**: Templates use Jinja2's `extends`/`block` pattern with `layout.html` as the base template.
3. **Manual route registration**: Routes are registered with `add_url_rule()` instead of `@app.route()` decorators, allowing view functions to be imported and tested independently.
4. **Loose coupling**: `views.py` imports only `render_template` and `request` from Flask — not `app` or any decorators.

### Templates

- **`layout.html`**: Base template. Defines `<header>`, `<main class="container">`, and `<footer>`. Navigation links: Home, Course Details, Contact.
- **`index.html`**: Hero section + CSS grid of course cards. Each card shows title, description, instructor, duration, topic count, and links to `/course/{{ loop.index }}`.
- **`course.html`**: Displays a single course — title, description, instructor, duration, and topics list.
- **`contact.html`**: Contact form (name, email, address with server-side validation + error display) and social media links section (Twitter, LinkedIn, GitHub, Facebook with inline SVG icons).

### CSS Design System (`src/static/css/styles.css`)

CSS custom properties (variables):

```css
--primary: #2563eb
--primary-dark: #1e40af
--primary-light: #dbeafe
--text-primary: #1e293b
--text-secondary: #64748b
--border: #e2e8f0
--success: #10b981
--error: #ef4444
```

Responsive breakpoints:
- `max-width: 1024px` — adjust font sizes, grid columns
- `max-width: 768px` — stack contact form columns, single course column
- `max-width: 480px` — mobile optimizations (16px min for form inputs)

Layout approach: CSS Grid for course cards (`repeat(auto-fit, minmax(300px, 1fr))`), Flexbox for header and contact layout.

## Test Structure (`tests/test_app.py`)

Uses Python's `unittest` framework. 11 test cases in `AppTestCase`:

| Test | Description |
|------|-------------|
| `test_index` | GET `/` returns 200, all course titles present |
| `test_course` | GET `/course/1` returns 200 |
| `test_golang_course` | GET `/course/4` returns Go course and instructor name |
| `test_contact_page_loads` | GET `/contact` shows form and social section |
| `test_contact_form_valid_submission` | POST with valid data shows success message |
| `test_contact_form_missing_name` | POST without name shows name error |
| `test_contact_form_missing_email` | POST without email shows email error |
| `test_contact_form_invalid_email` | POST with bad email format shows error |
| `test_contact_form_missing_address` | POST without address shows address error |
| `test_contact_form_short_address` | POST with <10 char address shows error |
| `test_contact_form_all_empty_fields` | POST all empty shows all error messages |

**Test patterns**:
- `self.app.get(path)` / `self.app.post(path, data={...})`
- Assertions: `self.assertEqual(response.status_code, 200)` and `self.assertIn(b'string', response.data)`

## Known Issues / Caveats

1. **`course.html` template order**: The file has `<!DOCTYPE html>` before `{% extends 'layout.html' %}`. The `{% extends %}` tag should be the first thing in the file for correct Jinja2 template inheritance.
2. **Contact form success**: On success, form data is only printed to stdout. There is no email sending or persistence.
3. **No database**: All course data is hardcoded. There is no ORM, migration system, or database backend.
4. **`.env` not committed**: The `.env` file (containing `FLASK_APP` and `FLASK_ENV`) is gitignored. Create it locally as needed.

## Naming Conventions

- Python functions and variables: `snake_case`
- CSS classes: `kebab-case` (e.g., `course-card`, `course-meta`)
- Template blocks: `snake_case` (e.g., `{% block content %}`)

## Development Workflow

### Add Unit Tests

Whenever you add any changes, add unit tests and run them to make sure they pass before committing.

### Verify Changes with Playwright (MANDATORY)

**After implementing any new feature, you MUST:**

1. Start the Flask application (if not already running — `python src/app.py`)
2. Use the Playwright MCP tool to connect to the application at `http://127.0.0.1:5000`
3. Navigate to and interact with the new feature to verify it works correctly
4. Take a screenshot of the working feature
5. Save the screenshot in the `test-output/` folder with a descriptive filename (e.g., `feature-name-verification-YYYY-MM-DD.png`)

This step ensures that all features are visually verified and provides documentation of the working state of the application.

## Important Notes

- The `views.py` module imports only `render_template` and `request` from Flask, maintaining loose coupling.
- Course IDs in URLs are 1-based (matching Jinja2's `loop.index`) and are used to index into the `courses` list.
- The virtual environment (`venv/`) must not be committed to version control.
- GitHub Actions workflows (`.github/workflows/`) integrate Claude Code for automated code review and issue handling.
