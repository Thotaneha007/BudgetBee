# 🐝 BudgetBee: Smart Spending Made Simple

BudgetBee is a professional-grade, AI-powered personal finance management application designed to help users track, analyze, and optimize their financial health. Built with a focus on modern fintech aesthetics and user experience, it combines traditional tracking with state-of-the-art AI insights.

![Dashboard Preview](https://via.placeholder.com/1200x600?text=BudgetBee+Dashboard+Preview)

## 🚀 Key Features

- **📊 Comprehensive Analytics**: Dynamic dashboards powered by Chart.js showing Income vs. Expenses, category breakdowns, and yearly trends.
- **🤖 AI Financial Assistant**: Personalized financial advice and spending analysis generated using Google's Gemini 1.5 Flash API.
- **📸 OCR Receipt Scanning**: Instantly add expenses by uploading receipt images—powered by Tesseract OCR.
- **🎯 Smart Goals**: Set, track, and visualize your savings targets with interactive progress bars.
- **🔄 Recurring & Subscriptions**: Track fixed costs and service renewals automatically with dedicated identifiers.
- **📂 Professional Exports**: Export your financial data to PDF or Excel for offline reporting.
- **🌐 Multilingual Support**: Fully localized interface supporting English, Hindi, and Telugu.
- **🌓 Dark/Light Mode**: A beautiful, theme-aware UI that adapts to your preferences.
- **🎤 Voice Input**: Hands-free transaction entry using browser-based Speech Recognition.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), JavaScript (ES6+)
- **Charts**: Chart.js
- **AI**: Google Generative AI (Gemini API)
- **OCR**: Pytesseract, Pillow
- **Export**: ReportLab (PDF), Openpyxl (Excel)
- **Icons**: Phosphor Icons

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Tesseract OCR (Optional, for receipt scanning)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/BudgetBee.git
   cd BudgetBee
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.get
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your keys:
   ```env
   SECRET_KEY=your_flask_secret_key
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

5. **Run the application**:
   ```bash
   python run.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

## 📁 Project Structure

```text
BudgetBee/
├── app/
│   ├── routes/          # Flask Blueprints for auth, dashboard, expenses, etc.
│   ├── static/          # CSS, JS, and image assets
│   ├── templates/       # Jinja2 HTML templates
│   ├── utils/           # AI, OCR, and Export helpers
│   └── __init__.py      # App factory and DB initialization
├── config.py            # Configuration settings
├── run.py               # Application entry point
├── schema.sql           # Database schema
└── requirements.txt     # Python dependencies
```

## 📈 Future Enhancements

- [ ] **Bank Integration**: Plaid API integration for automated transaction syncing.
- [ ] **Push Notifications**: Low budget alerts and recurring payment reminders.
- [ ] **Advanced ML**: Predict future spending based on historical data patterns.
- [ ] **Mobile App**: Native iOS/Android version using React Native.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ for better financial freedom.*
