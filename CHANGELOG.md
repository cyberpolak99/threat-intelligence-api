# 📋 CHANGELOG — Threat Intelligence API

**All notable changes to this project will be documented in this file.**

---

## [1.0.0] - 2026-02-20

### ADDED
- ✅ Threat Intelligence API (flask-based)
- ✅ Threat Feed Scraper (scrape CERT Polska, AbuseIPDB, CINS)
- ✅ 3 endpoints: /api/threats, /api/threats/stats, /api/health
- ✅ SQLite database integration (incident_reports table)
- ✅ GitHub repozytorium: cyberpolak99/threat-intelligence-api
- ✅ Documentation: README.md, API_REFERENCE.md, QUICK_START.md, EXAMPLES.md

### FEATURES
- Pobierz threat data z multiple sources
- Real-time threat tracking
- JSON/API access
- Support filtering (limit parameter)
- Health check endpoint

### TECHNOLOGY
- Python 3.12
- Flask 3.0
- SQLite
- Requests library

### DEPLOYMENT
- Local testing: python threat_api.py (localhost:10000)
- Ready for RapidAPI deployment

---

## [UNRELEASED] - ZAPLANOWANE

### PLANNED
- [ ] Authentication (API key-based)
- [ ] Rate limiting (per tier)
- [ ] Additional endpoints:
  - [ ] /api/threats/by-country
  - [ ] /api/threats/by-severity
  - [ ] /api/threats/by-type
  - [ ] /api/threats/search
- [ ] Subscription system
- [ ] Webhook notifications
- [ ] Real-time WebSocket support
- [ ] Email alerts integration
- [ ] Dashboard web app
- [ ] ML prediction (risk scoring)

### OPTIMIZATION
- [ ] Caching layer (Redis)
- [ ] Pagination (page/per_page)
- [ ] Sorting options
- [ ] Aggregated stats (by severity, by type, by date)
- [ ] Batch export (CSV/JSON)

---

## [1.0.1] - PLANOWANE (tydzień)

### BUG FIXES
- [ ] Fix empty database issue
- [ ] Optimize query performance
- [ ] Handle HTTP 429 errors (rate limiting)

### IMPROVEMENTS
- [ ] Better error messages
- [ ] Response time <200ms
- [ ] Documentation improvements
- [ ] Add troubleshooting guide

---

## [1.1.0] - PLANOWANE (miesiąc)

### NEW FEATURES
- [ ] Auth system (API keys)
- [ ] Rate limiter
- [ ] Admin panel
- [ ] User management
- [ ] Usage analytics

### ENHANCEMENTS
- [ ] Add subscription tiers
- [ ] Premium features
- [ ] Enterprise plans
- [ ] Custom integrations

---

## [2.0.0] - PLANOWANE (kwartał)

### MAJOR UPDATE
- [ ] ML-powered threat prediction
- [ ] Geolocation data
- [ ] Reputation scoring
- [ ] Correlation analysis
- [ ] Automated incident response

### NEW PLATFORMS
- [ ] Docker image
- [ ] Kubernetes deployment
- [ ] Cloud-native architecture
- [ ] Multi-tenant support

---

## [3.0.0] - PLANOWANE (rok+)

### COMPLETE REWRITE
- [ ] Microservices architecture
- [ ] Event-driven system
- [ ] Real-time stream processing
- [ ] AI-driven analysis
- [ ] Enterprise-grade features

---

## **KONTRYBUCJA**

Do zrobienia changelog:

1. Dodaj nowy section na top (np., [1.1.0] - 2026-03-XX)
2. W [UNRELEASED] zapisz planowane features
3. Gdy release — przenież do nowy section
4. Keep changelog na GitHub

---

**Changelog Template inspired by Keep a Changelog**

---
