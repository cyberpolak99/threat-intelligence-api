# 🤝 CONTRIBUTING — Threat Intelligence API

---

## **CO ZNACZY CONTRIBUTING?**

Contributing to oznacza:

- 🐛 Zgłaszanie błędy
- ✨ Proposing new features
- 📝 Poprawa dokumentacji
- 🔧 Pull requests (PRs)
- 💬 Q&A w issues

---

## **HOW TO CONTRIBUTE**

### **STEP 1: FORK & CLONE**

1. Fork this repo z: https://github.com/cyberpolak99/threat-intelligence-api
2. Clone lokalnie:
```bash
git clone https://github.com/cyber-polak/threat-intelligence-api.git
cd threat_intelligence_api
```

### **STEP 2: SETUP VIRTUAL ENVIRONMENT**

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### **STEP 3: RUN LOCALLY**

```bash
# Run API
python threat_api.py

# Test endpoints
curl http://localhost:10000/api/threats?limit=10
```

---

## **GUIDELINES**

### **CODING STYLE**

- Follow PEP 8
- Use type hints gdzie possible
- Dodaj docstrings dla funkcji
- Keep functions small (<50 lines)
- Add comments dla complex logic

### **COMMIT MESSAGES**

Format: `[TYPE]: MESSAGE`

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test additions
- `chore:` Maintenance

Examples:
```
feat: add country filtering endpoint
fix: empty database error handling
docs: improved API reference
refactor: simplify threat_fetcher logic
```

### **BRANCHING**

- `main` — production-ready code
- `develop` — development branch
- `feature/xxx` — new feature
- `bugfix/xxx` — bug fix

Workflow:
```
git checkout develop
git checkout -b feature/your-feature-name
# Work...
git commit -m "feat: add feature"
git push origin feature/your-feature-name
# Create PR od develop
```

---

## **BUG REPORTS**

### **Template**

```markdown
## Bug Description
Co się dzieje?

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
Co powinno się wydarzyć?

## Actual Behavior
Co się rzeczywisto zdarzy?

## Environment
- OS: [Windows/Linux/Mac]
- Python version: [3.10+]
- API version: [1.0]

## Screenshots (if applicable)
Screenshots
```

---

## **FEATURE REQUESTS**

### **Template**

```markdown
## Feature Request
Co chciałbyś dodać?

## Use Case
Dlaczego jest to potrzebne?

## Proposed Solution
Jak to zrealizować?

## Alternatives
Alternatywne rozwiązania?

## Additional Context
Dodatkowe informacje
```

---

## **PULL REQUESTS**

### **Przed PR:**

1. ✅ Run tests lokalnie
2. ✅ Update documentation
3. ✅ Update CHANGELOG
4. ✅ Sync z develop branch

### **PR Template**

```markdown
## Type
[ ] Feature
[ ] Bug fix
[ ] Documentation
[ ] Refactoring

## Changes
Opisz zmiany

## Tests
[ ] Tested lokalnie
[ ] All tests passed

## Checklist
- [ ] Code compiles
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] No linting errors
```

---

## **TESTING**

### **Run tests:**

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_api.py
```

### **Writing tests:**

```python
import requests

def test_threats_endpoint():
    """Test /api/threats"""
    response = requests.get("http://localhost:10000/api/threats?limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'count' in data
    assert 'data' in data
```

---

## **DOCUMENTATION**

### **Documentation Updates:**

- Add new endpoints do `API_REFERENCE.md`
- Add examples do `EXAMPLES.md`
- Update `README.md` dla breaking changes

---

## **CODE REVIEW**

### **During review:**

- Respond do wszystkich comments
- Fix all issues
- Add additional tests if required
- Keep PR focused (single feature/fix)

---

## **QUESTIONS?**

- Otwórz issue z label: `question`
- Tag @cyberpolak99
- Użyj template:

```markdown
## Question
Co chcesz wiedzieć?

## Context
Dodatkowe informacje
```

---

## **LICENSJA**

Contributing oznacza, że agree z [MIT License](LICENSE)

---

**Dzięki za contributing!** 🎉

---
