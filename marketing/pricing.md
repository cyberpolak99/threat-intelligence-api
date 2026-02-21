# 💰 PRYCING — Threat Intelligence API

---

## **DOKŁADNY PRICING NA RAPIDAPI**

---

## **TIER 1: FREE (DARMOWY)**

### **Specyfikacja:**

| Feature | Szczegóły |
|---------|-----------|
| **Requests** | 10 per day |
| **Endpointy** | /api/threats, /api/threats/stats, /api/health |
| **Rate Limit** | 10/day |
| **Auth** | None required |
| **Support** | Community (GitHub issues) |
| **SLA** | Best effort |
| **Data Retention** | Real-time (no backup) |
| **Features** | • Pobieraj threat data<br>• Stats endpoint<br>• Health check<br>• Documentation<br>• Examples |

**Dla kogo:** Developers learning, hobbyist projects, small-scale testing

**Limitations:**
- Nie dla production
- Brak priority support
- 10 requests/day może nie być wystarczający dla heavy users

---

## **TIER 2: BASIC ($9.99/MONTH)**

### **Specyfikacja:**

| Feature | Szczegóły |
|---------|-----------|
| **Requests** | 1,000 per month |
| **Endpointy** | Wszystkie (3 endpoints) |
| **Rate Limit** | 33/day (average) |
| **Auth** | Basic auth (API key) |
| **Support** | Email within 24 hours |
| **SLA** | 99% uptime |
| **Data Retention** | 30 days |
| **Features** | • Wszystkie free features<br>• API key authentication<br>• Rate limiting<br>• Priority support<br>• Usage analytics<br>• Webhook<br>• Email alerts<br>• Custom filtering<br>• Bulk export (CSV/JSON) |

**Dla kogo:** Hobbyist developers, small projects, research projects

**Zalety:**
- Wystarczający dla wiele use cases
- Email support
- 30-day data retention
- Webhook capability

**Limitations:**
- Nie dla production enterprise
- Niski request limit (1k/month)
- Brak advanced features

---

## **TIER 3: PRO ($49.99/MONTH)**

### **Specyfikacja:**

| Feature | Szczegóły |
|---------|-----------|
| **Requests** | 10,000 per month |
| **Endpointy** | Wszystkie + future endpoints |
| **Rate Limit** | 333/day (average) |
| **Auth** | API key + OAuth2 (planowane) |
| **Support** | Email + Slack 30 minutes |
| **SLA** | 99.5% uptime (guaranteed) |
| **Data Retention** | 90 days |
| **Features** | • Wszystkie Basic features<br>• OAuth2 support (planowane)<br>• Real-time WebSocket (planowane)<br>• Advanced filtering<br>• Custom integrations<br>• Dedicated support<br>• API analytics dashboard<br>• Whitelist IP range<br>• Custom headers<br>• Bulk operations (1000+ requests) |

**Dla kogo:** Production deployments, medium-sized companies, SaaS projects

**Zalety:**
- High request volume (10k/month)
- Dedicated support
- Real-time future features
- 90-day data retention
- Custom integration support

**Limitations:**
- Nie dla enterprise (>1M requests/month)
- Brak on-prem deployment
- Nie dla multi-tenant system

---

## **FUTURE TIERS (PLANOWANE)**

### **TIER 4: ENTERPRISE (Custom Pricing)**

### **Specyfikacja:**

| Feature | Szczegóły |
|---------|-----------|
| **Requests** | Custom (1M+ per month) |
| **Endpointy** | Wszystkie + custom endpoints |
| **Rate Limit** | Custom |
| **Auth** | OAuth2 + SSO |
| **Support** | Dedicated account manager |
| **SLA** | 99.9% uptime (guaranteed) |
| **Data Retention** | Unlimited |
| **Features** | • Wszystko z Pro<br>• On-prem deployment<br>• Custom endpoints<br>• Multi-tenant support<br>• Enterprise support<br>• Dedicated account manager<br>• Custom integration service<br>• Security audit<br>• Training<br>• Priority roadmap influence |

**Dla kogo:** Large enterprises, government, managed security service providers (MSSPs)

**Cena:** Custom (contact sales@threatintelligence.com)

---

## **COMPARISON TABLE**

| Feature | Free | Basic | Pro | Enterprise |
|---------|------|-------|-----|-----------|
| Requests | 10/dzień | 1,000/miesiąc | 10,000/miesiąc | Custom |
| Auth | None | Basic | Basic + OAuth2 | OAuth2 + SSO |
| Support | Community | Email (24h) | Email + Slack (30m) | Account Manager |
| SLA | Best Effort | 99% | 99.5% | 99.9% |
| Data Retention | Real-time | 30 days | 90 days | Unlimited |
| Webhook | ❌ | ✅ | ✅ | ✅ |
| Custom Filters | ❌ | ✅ | ✅ | ✅ |
| Bulk Export | ❌ | ✅ | ✅ | ✅ |
| WebSocket | ❌ | ❌ | ✅ (planowane) | ✅ |
| On-Prem | ❌ | ❌ | ❌ | ✅ |

---

## **HOW TO UPGRADE**

### **FROM FREE TO BASIC:**

1. **Otwórz RapidAPI dashboard**
2. **Zaloguj się** do konto Basic
3. **Uzyskaj API key**
4. **Add API key do headers:**
```python
headers = {
    "X-RapidAPI-Key": "your_api_key_here"
}
response = requests.get("https://api.threatintelligence.com/api/threats", headers=headers)
```

### **FROM BASIC TO PRO:**

Same like Free→Basic, just use Pro API key

---

## **PAYMENT OPTIONS**

### **SUPPORTED PAYMENT METHODS:**
- Credit card (Visa, Mastercard, American Express)
- PayPal
- Bitcoin (planowane)
- Invoice dla enterprise (Net 30)

### **BILLING CYCLE:**
- **Monthly** (billing every month)
- **Annual** ( discounts:
  - 2 months free na annual subscription
  - Procent: 16.7% discount)

---

## **REFUND POLICY**

### **FREE TIER:**
- N/A (darmowe)

### **BASIC/PRO:**
- 7-day refund window
- Poniżej request limit (np., użyłeś <10% requests within 7 days)
- Refund przez:
  1. Contact RapidAPI support
  2. Provide reason
  3. Refund w 5-7 dni

### **ENTERPRISE:**
- Custom refund policy
- Wskazuje w contract

---

## **FAQ PRICING**

### **Q: Can I test before paying?**
**A:** Tak — Free tier dla testing (10 requests/day)

### **Q: What happens if I exceed limit?**
**A:** You'll receive 429 Too Many Requests error. Upgrade tier or wait until next billing cycle.

### **Q: Can I cancel anytime?**
**A:** Tak — prorated refund pending. Cancellation prorated do następny billing cycle.

### **Q: Do you offer education/nonprofit discounts?**
**A:** Tak — contact sales@threatintelligence.com dla special pricing

### **Q: Can I negotiate pricing?**
**A:** Tak — dla enterprise (1M+ requests/month), we offer custom pricing

### **Q: What's included in "support"?**
**A:** 
- **Free:** Community (GitHub issues, Stack Overflow)
- **Basic:** Email support (24 hours response time)
- **Pro:** Email + Slack (30 minutes response time)
- **Enterprise:** Dedicated account manager

### **Q: Do you provide onboarding?**
**A:** Dla Pro+ tier: 30-min onboarding call (setup integration questions)

---

## **SPECIAL OFFERS**

### **LAUNCH PROMO:**
- **Pro tier:** $39.99/month (za pierwsze 3 months)
- **Enterprise:** Setup cost waived (value: $500)

### **BUNDLE OFFER:**
- **Pro + Enterprise support:** $59.99/month (dla 3 months trial)

### **REFERRAL BONUS:**
- **$10 credit** za każdym referral kto subskrybuje Basic+
- **Referral limit:** Unlimited

---

## **COST PER REQUEST**

| Tier | Cost per Request | Break-even Points |
|------|------------------|-------------------|
| Free | $0 | N/A |
| Basic | $0.01 | 1,000 requests = $9.99 |
| Pro | $0.005 | 10,000 requests = $49.99 |
| Enterprise | $0.001 | 100,000 requests = $100 (example) |

---

## **ROI CALCULATOR**

### **BASIC TIER:**
- **Monthly cost:** $9.99
- **Value:** Automated threat intel saves ~2 hours/month ($40/hour)
- **ROI:** 800% return in первый месяц

### **PRO TIER:**
- **Monthly cost:** $49.99
- **Value:** Saves ~8 hours/month (security engineer at $80/hour)
- **ROI:** 1,280% return w pierwszy miesiąc

---

## **CONTACT SALES**

### **FOR ENTERPRISE:**
- **Email:** sales@threatintelligence.com
- **Phone:** +48-XXX-XXX-XXX (planowane)
- **Location:** Poland / Worldwide

### **FOR SUPPORT:**
- **Documentation:** See README.md, API_REFERENCE.md
- **GitHub:** https://github.com/cyberpolak99/threat-intelligence-api/issues
- **Email:** support@threatintelligence.com (Basic+)

---

**Pricing Guide** | Version: 1.0 | Update: 2026-02-21

---
