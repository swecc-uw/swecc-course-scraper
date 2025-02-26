# SWECC Course Scraper

### Dev Setup

```bash
python -m venv venv
source venv/bin/activate
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
