# Threat Intelligence Dashboard (Backend v1)

**FastAPI dashboard** dla Cyber Shield AI Threat Intelligence API

---

## 🚀 **Uruchomienie**

### **Lokalne:**
```bash
cd ti-dashboard
pip install -r requirements.txt
python main.py
```

**URL:** http://localhost:8001

---

## 📊 **Features**

### **Dashboard (/)**
- 📈 Summary stats (total threats, by severity, by type)
- 📌 Latest 5 threats
- 🔄 Auto-refresh co 30 sekund

### **Threats (/threats)**
- 📋 Paginated list of threats (50 per page)
- 🔍 Filtr by severity (CRITICAL/HIGH/MEDIUM/LOW)
- 💻 Sortowanie po IP, Type, Detected

### **API Endpoints:**
- `GET /api/stats` — JSON statystyki
- `GET /api/threats` — JSON threats z filtrowaniem
- `GET /api/dashboard/stats` — Dashboard stats + latest threats

---

## 🎨 **UI**

- **Dark theme** (cyber aesthetics)
- **Responsive** (mobile-friendly)
- **Fast loading** (minimal JavaScript)
- **Real-time** (auto-refresh, click refresh button)

---

## 🔧 **Configuration**

**Environment variables:**
```bash
PORT=8001  # Default localhost port (używane przez Render: zmienna środowiskowa)
```

---

## 🚀 **Deploy na Render**

1. **Nowy Web Service** w Render Dashboard
2. **Connect GitHub repo:** `cyberpolak99/threat-intelligence-api`
3. **Root Directory:** `ti-dashboard/`
4. **Build Command:**
```bash
cd ti-dashboard && pip install -r requirements.txt
```
5. **Start Command:**
```bash
cd ti-dashboard && python main.py
```
6. **Click Deploy**

---

## 📊 **Data Source**

Dashboard używa lokalnej listy THREAT_DATA w pamięci. 

**Do integracji z Threat API:**
- Zmodyfikuj main.py do importu z `threat_api.py` lub
- Użyj HTTP requests do Threat API endpoints

---

## 🎯 **Next Steps (Backend v2)**

- [ ] Real-time updates (WebSocket/FastAPI WebSockets)
- [ ] Search by IP, type, date range
- [ ] Export CSV/PDF
- [ ] User authentication (admin panel)
- [ ] Map visualization (geographic threats)

---

**Status:** v1 - Production Ready  
**Tech Stack:** FastAPI 0.104.1 + Jinja2 3.1.2 + Uvicorn 0.24.0  
**Maintainer:** Cyber Shield AI
