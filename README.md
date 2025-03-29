# SWECC Course Scraper

### Installation (non-contributors)

```bash
pip install swecc-course-scraper
```

### Dev Setup

## for Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Windows (PowerShell)

```bash
python -m venv venv
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # Only needed if script execution is blocked
.venv/Scripts/Activate.ps1
pip install -e ".[dev]"
pre-commit install
```



### Commands

```bash
# lint
ruff check swecc_course_scraper

# format
black swecc_course_scraper

# type check
mypy swecc_course_scraper

# test
pytest
```
