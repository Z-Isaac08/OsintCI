# 🔍 OSINT CI

> Ivoirian Phone Number Intelligence Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Country](https://img.shields.io/badge/Country-Côte%20d'Ivoire-orange)

---

## 📌 Description

**OSINT CI** is an open-source intelligence tool focused on Ivoirian phone numbers (+225).
It allows analysts, researchers, and security professionals to quickly gather publicly
available information about a phone number registered in Côte d'Ivoire.

Built for educational purposes and professional OSINT workflows.

---

## ✨ Features

- ✅ Phone number validation (format + existence)
- ✅ Carrier & line type identification (Orange CI, MTN CI, Moov Africa)
- ✅ Geographic zone detection (Abidjan, Bouaké, San-Pédro...)
- ✅ Spam / fraud risk scoring
- ✅ Local blacklist lookup
- ✅ Social media presence (WhatsApp, Telegram)
- ✅ Google Dorks generation (TikTok, Facebook, Instagram)
- ✅ JSON export
- 🔄 Truecaller lookup (coming soon)

---

## ⚙️ Installation

**Requirements:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/yourusername/osint-ci.git
cd osint-ci

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Full scan

```bash
python main.py scan +2250707777777
```

### Validate a number

```bash
python main.py validate +2250707777777
```

### Carrier lookup

```bash
python main.py carrier +2250707777777
```

### Spam check

```bash
python main.py spam +2250707777777
```

### Social media check

```bash
python main.py social +2250707777777
```

### Export results as JSON

```bash
python main.py scan +2250707777777 --export
```

---

## 📤 Output Example

```json
{
  "number": "+2250707777777",
  "valid": true,
  "carrier": "Orange CI",
  "line_type": "Mobile",
  "region": "National (Mobile)",
  "spam": {
    "is_spam": false,
    "risk_score": 10,
    "risk_level": "Low"
  },
  "social": {
    "whatsapp": {
      "link": "https://wa.me/2250707777777"
    },
    "telegram": {
      "link": "https://t.me/+2250707777777"
    },
    "tiktok": {
      "dork_url": "https://www.google.com/search?q=%220707777777%22+site%3Atiktok.com"
    }
  }
}
```

---

## 📁 Project Structure

```
osint-ci/
├── main.py
├── requirements.txt
├── README.md
├── modules/
│   ├── __init__.py
│   ├── banner.py
│   ├── validator.py
│   ├── carrier.py
│   ├── spam_checker.py
│   └── social_checker.py
├── data/
│   └── spam_numbers.json
└── output/
    └── .gitkeep
```

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational and research purposes only**.
All data used is sourced from **publicly available information**.

- Do **not** use this tool to harass, stalk, or harm individuals
- Do **not** use this tool for illegal surveillance
- The author is **not responsible** for any misuse of this tool
- Usage must comply with **Ivoirian law** (Loi n°2013-450 sur la protection des données personnelles)
- Results may be **inaccurate** — always verify through official channels

By using this tool, you agree to use it **responsibly and legally**.

---

## 👤 Author

**ZC0ok**
Cybersecurity and AI Student

---

## 📄 License

This project is licensed under the **MIT License**.
See [LICENSE](LICENSE) for details.

---

> _"With great power comes great responsibility."_
