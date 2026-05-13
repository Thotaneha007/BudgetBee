// Mobile Sidebar Toggle
const mobileToggle = document.getElementById('mobileToggle');
const sidebar = document.getElementById('sidebar');

if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768) {
        if (sidebar && !sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme') || 'light';

if (currentTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        let theme = document.documentElement.getAttribute('data-theme');
        if (theme === 'dark') {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        }
        
        // Update charts if they exist
        if (window.trendChartInstance) {
            window.trendChartInstance.update();
        }
        if (window.categoryChartInstance) {
            window.categoryChartInstance.update();
        }
        if (window.yearlyChartInstance) {
            window.yearlyChartInstance.update();
        }
        if (window.trueYearlyChartInstance) {
            window.trueYearlyChartInstance.update();
        }
        if (window.savingsGrowthChartInstance) {
            window.savingsGrowthChartInstance.update();
        }
    });
}

// Chart.js Default Config for Theme Support
Chart.defaults.color = () => {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? '#9CA3AF' : '#6B7280';
};
Chart.defaults.font.family = "'Inter', sans-serif";

function initCharts(data) {
    const trendCtx = document.getElementById('trendChart');
    const catCtx = document.getElementById('categoryChart');
    
    if (trendCtx && data.trend) {
        const labels = data.trend.months;
        
        window.trendChartInstance = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Income',
                        data: data.trend.income,
                        borderColor: '#14B8A6',
                        backgroundColor: 'rgba(20, 184, 166, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Expenses',
                        data: data.trend.expenses,
                        borderColor: '#F59E0B',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', align: 'end' }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
    
    if (catCtx && data.categories) {
        const labels = Object.keys(data.categories);
        const values = Object.values(data.categories);
        
        const colors = [
            '#F59E0B', '#14B8A6', '#6366F1', '#EF4444', 
            '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16', '#64748B'
        ];
        
        window.categoryChartInstance = new Chart(catCtx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right' }
                },
                cutout: '70%'
            }
        });
    }
    
    // Yearly Chart (Last 12 Months)
    const yearlyCtx = document.getElementById('yearlyChart');
    if (yearlyCtx && data.yearly) {
        window.yearlyChartInstance = new Chart(yearlyCtx, {
            type: 'bar',
            data: {
                labels: data.yearly.months,
                datasets: [
                    {
                        label: 'Income',
                        data: data.yearly.income,
                        backgroundColor: '#14B8A6',
                        borderRadius: 4
                    },
                    {
                        label: 'Expenses',
                        data: data.yearly.expenses,
                        backgroundColor: '#F59E0B',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', align: 'end' }
                }
            }
        });
    }

    // True Yearly Chart (All Years)
    const trueYearlyCtx = document.getElementById('trueYearlyChart');
    if (trueYearlyCtx && data.true_yearly) {
        window.trueYearlyChartInstance = new Chart(trueYearlyCtx, {
            type: 'bar',
            data: {
                labels: data.true_yearly.years,
                datasets: [
                    {
                        label: 'Income',
                        data: data.true_yearly.income,
                        backgroundColor: 'rgba(20, 184, 166, 0.8)',
                        borderRadius: 4
                    },
                    {
                        label: 'Expenses',
                        data: data.true_yearly.expenses,
                        backgroundColor: 'rgba(245, 158, 11, 0.8)',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });
    }

    // Savings Growth Chart
    const savingsCtx = document.getElementById('savingsGrowthChart');
    if (savingsCtx && data.true_yearly) {
        window.savingsGrowthChartInstance = new Chart(savingsCtx, {
            type: 'line',
            data: {
                labels: data.true_yearly.years,
                datasets: [{
                    label: 'Savings',
                    data: data.true_yearly.savings,
                    borderColor: '#6366F1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });
    }

    // Peak Stats
    const peakContainer = document.getElementById('yearlyPeakStats');
    if (peakContainer && data.peak_month) {
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const monthIdx = parseInt(data.peak_month) - 1;
        peakContainer.innerHTML = `
            <div class="category-badge" style="background: rgba(239, 68, 68, 0.1); color: var(--danger); border-color: var(--danger);">
                <i class="ph ph-warning"></i> Peak Spend: ${monthNames[monthIdx]} (₹${data.peak_amount.toFixed(0)})
            </div>
        `;
    }
}

// Voice Input Feature (SpeechRecognition API)
const voiceBtn = document.getElementById('voiceBtn');
if (voiceBtn) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        // Set language based on current selection
        recognition.lang = document.documentElement.lang === 'hi' ? 'hi-IN' : 
                           document.documentElement.lang === 'te' ? 'te-IN' : 'en-US';
                           
        voiceBtn.addEventListener('click', () => {
            voiceBtn.style.color = 'var(--danger)';
            voiceBtn.style.animation = 'pulse 1s infinite';
            recognition.start();
        });
        
        recognition.onresult = (event) => {
            const result = event.results[0][0].transcript.toLowerCase();
            console.log("Voice input:", result);
            
            // Simple parsing: "food 200" or "200 for food"
            // This is a basic rule-based parser.
            let amount = result.match(/\d+(\.\d+)?/);
            let category = "Others";
            
            if (result.includes('food') || result.includes('khana') || result.includes('bhojanam')) category = "Food";
            if (result.includes('travel') || result.includes('yatra') || result.includes('prayanam')) category = "Travel";
            if (result.includes('shop') || result.includes('kharidari')) category = "Shopping";
            
            // If on expenses page, auto-fill form
            const titleInput = document.getElementById('expenseTitle');
            const amountInput = document.getElementById('expenseAmount');
            if (titleInput && amountInput) {
                titleInput.value = "Voice: " + result;
                if (amount) amountInput.value = amount[0];
                
                const catSelect = document.querySelector('select[name="category"]');
                if (catSelect) catSelect.value = category;
                
                alert(`Voice parsed. Title: ${result}, Amount: ${amount ? amount[0] : 'not found'}`);
            } else {
                alert(`Voice Input: "${result}". Go to Expenses page to add.`);
            }
        };
        
        recognition.onspeechend = () => {
            recognition.stop();
            resetVoiceBtn();
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            resetVoiceBtn();
            alert('Error with voice recognition: ' + event.error);
        };
        
        function resetVoiceBtn() {
            voiceBtn.style.color = '';
            voiceBtn.style.animation = '';
        }
        
    } else {
        voiceBtn.addEventListener('click', () => {
            alert("Speech Recognition API not supported in this browser.");
        });
    }
}

// Add simple CSS animation for pulse
const style = document.createElement('style');
style.innerHTML = `
@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
`;
document.head.appendChild(style);

// Auto-dismiss Alerts
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'toastSlideOut 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// FAB Toggle
const fabMain = document.getElementById('fabMain');
const fabMenu = document.getElementById('fabMenu');
if (fabMain && fabMenu) {
    fabMain.addEventListener('click', (e) => {
        e.stopPropagation();
        fabMenu.classList.toggle('active');
        fabMain.querySelector('i').classList.toggle('ph-plus');
        fabMain.querySelector('i').classList.toggle('ph-x');
    });

    document.addEventListener('click', () => {
        fabMenu.classList.remove('active');
        fabMain.querySelector('i').classList.add('ph-plus');
        fabMain.querySelector('i').classList.remove('ph-x');
    });
}
