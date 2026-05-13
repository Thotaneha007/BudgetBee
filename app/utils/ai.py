import os
import google.generativeai as genai
from flask import current_app

def generate_financial_insights(expenses, budget, total_spent, total_income, current_month):
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        return fallback_insights(expenses, budget, total_spent, total_income)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepare context for AI
        context = f"Analyze these financial metrics for {current_month}:\n"
        context += f"Total Income: {total_income}\n"
        context += f"Total Spent: {total_spent}\n"
        context += f"Savings: {total_income - total_spent}\n"
        context += f"Monthly Budget: {budget}\n\n"
        context += "Expenses List:\n"
        
        for exp in expenses:
            context += f"- {exp['title']}: {exp['amount']} ({exp['category']})\n"
            
        prompt = f"""
        {context}
        
        You are an AI financial advisor. Based on the user's expenses and budget, provide exactly 2 short, distinct, and actionable insights.
        Focus on:
        - Overspending trends
        - Savings recommendations
        - Category analysis
        Keep each insight under 15 words. Do not use markdown, just return two lines of text separated by a newline.
        """
        
        response = model.generate_content(prompt)
        insights = [line.strip() for line in response.text.split('\n') if line.strip()]
        return insights[:3] if insights else fallback_insights(expenses, budget, total_spent, total_income)
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return fallback_insights(expenses, budget, total_spent, total_income)

def fallback_insights(expenses, budget, spent, income):
    insights = []
    savings = income - spent
    
    if income > 0:
        savings_rate = (savings / income) * 100
        if savings_rate > 20:
            insights.append(f"Great job! You've saved {savings_rate:.1f}% of your income.")
        elif savings_rate < 0:
            insights.append("Warning: You are spending more than you earn.")
    if budget > 0:
        if spent > budget:
            insights.append(f"Warning: Budget exceeded by ₹{spent - budget:.2f}.")
        elif spent > budget * 0.8:
            insights.append(f"Alert: You have used {spent/budget*100:.1f}% of your budget.")
            
    if expenses:
        categories = {}
        for exp in expenses:
            categories[exp['category']] = categories.get(exp['category'], 0) + exp['amount']
        
        highest_cat = max(categories.items(), key=lambda x: x[1])
        insights.append(f"Highest spending category: {highest_cat[0]} (₹{highest_cat[1]:.2f})")
        
    if not insights:
        insights.append("Looking good! Keep tracking your expenses.")
        
    return insights
