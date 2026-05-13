const translations = {
    en: {
        'nav.dashboard': 'Dashboard',
        'nav.expenses': 'Expenses',
        'nav.budget': 'Budget',
        'nav.logout': 'Logout',
        'auth.login_desc': 'Login to manage your expenses',
        'auth.username': 'Username',
        'auth.password': 'Password',
        'auth.login_btn': 'Login',
        'auth.no_account': "Don't have an account?",
        'auth.signup_link': 'Sign up',
        'auth.signup_desc': 'Start managing your expenses smartly',
        'auth.signup_btn': 'Sign Up',
        'auth.has_account': 'Already have an account?',
        'auth.login_link': 'Login',
        'dashboard.ai_insight': 'AI Insight',
        'dashboard.total_spent': 'Total Spent',
        'dashboard.monthly_spent': 'This Month',
        'dashboard.monthly_budget': 'Monthly Budget',
        'dashboard.remaining': 'Remaining',
        'dashboard.trend': 'Spending Trend',
        'dashboard.categories': 'Categories',
        'dashboard.recent': 'Recent Transactions',
        'dashboard.view_all': 'View All',
        'dashboard.no_data': 'No expenses found.',
        'table.date': 'Date',
        'table.title': 'Title',
        'table.category': 'Category',
        'table.amount': 'Amount',
        'table.action': 'Action',
        'expenses.add_new': 'Add New Expense',
        'expenses.payment': 'Payment Type',
        'expenses.notes': 'Notes (Optional)',
        'expenses.add_btn': 'Add Expense',
        'expenses.filter': 'Filter',
        'expenses.no_found': 'No expenses found.',
        'budget.set': 'Set Monthly Budget',
        'budget.month': 'Month',
        'budget.amount': 'Budget Amount (₹)',
        'budget.save': 'Save Budget',
        'budget.history': 'Budget History',
        'budget.no_found': 'No budgets set yet.'
    },
    hi: {
        'nav.dashboard': 'डैशबोर्ड',
        'nav.expenses': 'खर्च',
        'nav.budget': 'बजट',
        'nav.logout': 'लॉग आउट',
        'auth.login_desc': 'अपने खर्चों का प्रबंधन करने के लिए लॉगिन करें',
        'auth.username': 'उपयोगकर्ता नाम',
        'auth.password': 'पासवर्ड',
        'auth.login_btn': 'लॉगिन',
        'auth.no_account': "खाता नहीं है?",
        'auth.signup_link': 'साइन अप करें',
        'auth.signup_desc': 'होशियारी से अपने खर्चों का प्रबंधन शुरू करें',
        'auth.signup_btn': 'साइन अप',
        'auth.has_account': 'क्या आपके पास पहले से एक खाता है?',
        'auth.login_link': 'लॉगिन',
        'dashboard.ai_insight': 'एआई इनसाइट',
        'dashboard.total_spent': 'कुल खर्च',
        'dashboard.monthly_spent': 'इस महीने',
        'dashboard.monthly_budget': 'मासिक बजट',
        'dashboard.remaining': 'शेष',
        'dashboard.trend': 'खर्च की प्रवृत्ति',
        'dashboard.categories': 'श्रेणियाँ',
        'dashboard.recent': 'हाल के लेनदेन',
        'dashboard.view_all': 'सभी देखें',
        'dashboard.no_data': 'कोई खर्च नहीं मिला।',
        'table.date': 'तारीख',
        'table.title': 'शीर्षक',
        'table.category': 'श्रेणी',
        'table.amount': 'राशि',
        'table.action': 'कार्रवाई',
        'expenses.add_new': 'नया खर्च जोड़ें',
        'expenses.payment': 'भुगतान प्रकार',
        'expenses.notes': 'नोट्स (वैकल्पिक)',
        'expenses.add_btn': 'खर्च जोड़ें',
        'expenses.filter': 'फ़िल्टर',
        'expenses.no_found': 'कोई खर्च नहीं मिला।',
        'budget.set': 'मासिक बजट सेट करें',
        'budget.month': 'महीना',
        'budget.amount': 'बजट राशि (₹)',
        'budget.save': 'बजट सहेजें',
        'budget.history': 'बजट इतिहास',
        'budget.no_found': 'अभी तक कोई बजट सेट नहीं किया गया है।'
    },
    te: {
        'nav.dashboard': 'డాష్‌బోర్డ్',
        'nav.expenses': 'ఖర్చులు',
        'nav.budget': 'బడ్జెట్',
        'nav.logout': 'లాగ్ అవుట్',
        'auth.login_desc': 'మీ ఖర్చులను నిర్వహించడానికి లాగిన్ చేయండి',
        'auth.username': 'వినియోగదారు పేరు',
        'auth.password': 'పాస్‌వర్డ్',
        'auth.login_btn': 'లాగిన్',
        'auth.no_account': "ఖాతా లేదా?",
        'auth.signup_link': 'సైన్ అప్ చేయండి',
        'auth.signup_desc': 'మీ ఖర్చులను తెలివిగా నిర్వహించడం ప్రారంభించండి',
        'auth.signup_btn': 'సైన్ అప్',
        'auth.has_account': 'ఇప్పటికే ఖాతా ఉందా?',
        'auth.login_link': 'లాగిన్',
        'dashboard.ai_insight': 'AI అంతర్దృష్టి',
        'dashboard.total_spent': 'మొత్తం ఖర్చు',
        'dashboard.monthly_spent': 'ఈ నెల',
        'dashboard.monthly_budget': 'నెలవారీ బడ్జెట్',
        'dashboard.remaining': 'మిగిలినది',
        'dashboard.trend': 'ఖర్చు ట్రెండ్',
        'dashboard.categories': 'కేటగిరీలు',
        'dashboard.recent': 'ఇటీవలి లావాదేవీలు',
        'dashboard.view_all': 'అన్నింటినీ వీక్షించండి',
        'dashboard.no_data': 'ఎటువంటి ఖర్చులు కనుగొనబడలేదు.',
        'table.date': 'తేదీ',
        'table.title': 'శీర్షిక',
        'table.category': 'వర్గం',
        'table.amount': 'మొత్తం',
        'table.action': 'చర్య',
        'expenses.add_new': 'కొత్త ఖర్చు జోడించండి',
        'expenses.payment': 'చెల్లింపు రకం',
        'expenses.notes': 'గమనికలు (ఐచ్ఛికం)',
        'expenses.add_btn': 'ఖర్చు జోడించండి',
        'expenses.filter': 'ఫిల్టర్',
        'expenses.no_found': 'ఎటువంటి ఖర్చులు కనుగొనబడలేదు.',
        'budget.set': 'నెలవారీ బడ్జెట్ సెట్ చేయండి',
        'budget.month': 'నెల',
        'budget.amount': 'బడ్జెట్ మొత్తం (₹)',
        'budget.save': 'బడ్జెట్ సేవ్ చేయండి',
        'budget.history': 'బడ్జెట్ చరిత్ర',
        'budget.no_found': 'ఇంకా బడ్జెట్‌లు సెట్ చేయబడలేదు.'
    }
};

function applyTranslations(lang) {
    if (!translations[lang]) return;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}

function changeLanguage(lang) {
    fetch('/settings/language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: lang })
    }).then(() => {
        applyTranslations(lang);
        document.documentElement.lang = lang;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const lang = document.documentElement.lang || 'en';
    applyTranslations(lang);
});
