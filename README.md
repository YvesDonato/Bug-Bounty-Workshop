# Halftone Image Processor

A Django web application that converts uploaded images into halftone (dot-pattern) versions.

---

## Bug Bounty Workshop

This codebase has **10 bugs** hidden across the application. Your goal is to find and fix as many as possible in **30 minutes**.

### Rules

- You may use **any tools** — Claude Code, grep, reading code, running the app, whatever works.
- Bugs span the full stack: signals, middleware, views, models, algorithms, templates.
- Some bugs crash the app. Some produce wrong output. Some are silent. Two are visual.
- Each bug is in a **different file**. No file has more than 2 bugs.
- **All files are fair game** — comments in the code are not hints about which files to focus on.

### Scoring

| Criteria | Points |
|---|---|
| Identify the bug (name the file + describe the issue) | 1 |
| Explain the root cause (why does it happen?) | 2 |
| Working proof of concept (show how to trigger it) | 3 |
| Correct fix (code change that resolves it) | 2 |
| **Max per bug** | **8** |
| **Max total (10 bugs)** | **80** |

### How to Participate

> **Before you do anything else — fork this repo.**
> Do not clone `Intuit-Toronto/django-box` directly. You need your own fork so you can push your branch and open a PR. If you skip this step, you won't be able to submit.

#### 1. Fork this repo

Click **Fork** on GitHub (top-right of this page), then clone **your fork**:

```bash
git clone https://github.com/<your-username>/django-box.git
cd django-box
```

#### 2. Set up the project

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ and try using the app. You'll notice things break.

#### 3. Find and fix bugs

Start by using the app — register, log in, upload images, browse the gallery, try presets, batch upload. Read the code. Use Claude Code. Some hints:

- **Try the basic flow first.** Can you register and log in?
- **Upload different images.** Do the results look correct?
- **Try edge cases.** What happens with unusual input values?
- **Check the gallery.** Does pagination work correctly?
- **Look at batch processing.** Does the status update properly?

#### 4. Submit your fixes

```bash
git checkout -b fix/bug-bounty-$(whoami)
git add -A
git commit -m "fix: bug bounty submissions"
git push -u origin fix/bug-bounty-$(whoami)
```

Open a **Pull Request** from your fork to `Intuit-Toronto/django-box` targeting `main`.

#### 5. CI checks your work

Automated tests run on your PR. Each bug has tests that **fail when the bug exists** and **pass when you fix it correctly**. Check the PR status to see which bugs you've fixed.

---

## About

Halftone is a printing technique that simulates continuous tone imagery through the use of dots of varying size. This app recreates that effect digitally — users upload an image, and the app returns a black-and-white halftone version using a grid-sampling algorithm powered by Pillow.

### Features

- **User authentication** — Register and login with username and password.
- **User profiles** — Configure default halftone preferences (dot spacing, style).
- **Image upload** — Upload any common image format (PNG, JPG, etc.).
- **Halftone processing** — Three styles: classic (dots), diamond, and line.
- **Image gallery** — Browse past uploads with pagination.
- **Sharing** — Mark images as public and share via token-based URLs.
- **Presets** — Save and import named combinations of halftone parameters as JSON.
- **Batch processing** — Upload multiple images at once with status tracking.
- **Rate limiting** — Upload rate limiting to prevent abuse.
- **Activity logging** — Middleware tracks user activity.

## Prerequisites

| Tool | Download |
|------|----------|
| **Git** | [git-scm.com/downloads](https://git-scm.com/downloads) |
| **Python 3.10+** | [python.org/downloads](https://www.python.org/downloads/) |
| **VS Code** (recommended) | [code.visualstudio.com](https://code.visualstudio.com/) |

> **Windows users**: check "Add Python to PATH" during Python install, and use `python` instead of `python3` for all commands below.

## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd django-box
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv            # macOS / Linux
   python -m venv venv             # Windows
   ```

   Then activate it:

   ```bash
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Seed sample data** (optional)

   ```bash
   python manage.py seed_workshop
   ```

   This creates test users (`alice`, `bob`, `charlie` — password: `workshop2024`) with sample images and presets.

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

7. **Open the app** at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure

```
django-box/
├── halftone_project/      # Django project settings, URLs, middleware
├── accounts/              # Auth app (register, login, logout, profile, signals)
├── processor/             # Image processing app
│   ├── halftone.py        # Standalone halftone algorithm (3 styles)
│   ├── batch.py           # Batch processing logic
│   ├── utils.py           # Preset validation
│   ├── models.py          # ImageUpload, Preset, BatchJob, ActivityLog
│   └── views.py           # Upload, gallery, presets, batch, sharing views
├── templates/             # Shared base template + app templates
├── static/css/            # Stylesheet
├── media/                 # Uploaded and processed images (created at runtime)
├── requirements.txt
└── manage.py
```

## CI / Automated Testing

A GitHub Actions workflow (`.github/workflows/test.yml`) runs tests on every push and pull request to `main`. Tests are pulled from a private repository during CI, so they are not visible in participant forks.
