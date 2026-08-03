import os
import json
import streamlit as st
import google.genai as genai
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
client = None
if api_key:
    client = genai.Client(api_key=api_key)

# Page Configuration
st.set_page_config(page_title="AI Personal Finance Coach", page_icon="🛡️", layout="wide")

# ----------------- PROFESSIONAL DEEP TEAL FINTECH CSS & FORCED WHITE FONT -----------------
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F7F6;
    }
    
    h1, h2, h3 {
        color: #154247 !important;
        font-family: 'Inter', sans-serif;
    }

    .stButton > button {
        background-color: #E6F1F2;
        color: #154247;
        border: 1px solid #88D2D6;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #88D2D6;
        border-color: #2E6A71;
        color: #154247;
    }
    
    div[data-testid="stMetricValue"] {
        color: #154247;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background-color: #154247 !important;
    }
    
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stRadio div,
    section[data-testid="stSidebar"] .stRadio label p {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] input:checked + div {
        background-color: #88D2D6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- PERMANENT STORAGE FUNCTIONS (JSON) -----------------
DATA_FILE = "finance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "name": "",
        "occupation": "",
        "income": 0.0,
        "expenses": 0.0,
        "current_savings": 0.0,
        "financial_goal": "",
        "purchase_history": [],
        "monthly_trend": [],
        "last_purchase_analysis": "",
        "last_health_report": "",
        "last_goal_plan": "",
        "target_amount": 0.0,
        "target_months": 6
    }

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

if "app_data" not in st.session_state:
    st.session_state.app_data = load_data()

data = st.session_state.app_data

if "page" not in st.session_state:
    st.session_state.page = "Home"

pages = ["Home", "Financial Profile", "Purchase Coach", "Financial Health", "Goal Planner", "Motivation", "Help & Guide"]

st.sidebar.title("Navigation")
st.session_state.page = st.sidebar.radio("Go to", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
page = st.session_state.page

# ----------------- 1. HOME PAGE -----------------
if page == "Home":
    st.title("🛡️ AI Personal Finance Coach")
    st.markdown("### Welcome to your secure financial dashboard.")
    st.write("Take absolute control of your wealth, analyze purchases instantly with AI, track long-term growth trends, and build a secure financial future.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Smart Purchase Analysis", "Instant", "AI Powered")
    with col2:
        st.metric("Financial Health", "Real-time", "Permanent Storage")
    with col3:
        st.metric("Goal Planning", "Visual Trends", "Line Graph Enabled")
        
    st.info("👈 Use the sidebar navigation or click below to start setting up your profile.")
    
    st.markdown("---")
    col_spacer, col2 = st.columns([2.2, 1])
    with col2:
        if st.button("Next: Financial Profile ➡️"):
            st.session_state.page = "Financial Profile"
            st.rerun()

# ----------------- 2. FINANCIAL PROFILE PAGE -----------------
elif page == "Financial Profile":
    st.title("👤 Financial Profile")
    st.write("Enter your core financial details below. Your data is permanently saved locally and remains secure.")

    with st.form("profile_form"):
        name = st.text_input("Your Name", value=data["name"])
        occupation = st.text_input("Occupation / Status", value=data["occupation"], placeholder="e.g., Student / Professional")
        income = st.number_input("Monthly Income (₹)", min_value=0.0, value=float(data["income"]))
        expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=float(data["expenses"]))
        current_savings = st.number_input("Current Total Savings (₹)", min_value=0.0, value=float(data["current_savings"]))
        financial_goal = st.text_input("Primary Financial Goal", value=data["financial_goal"], placeholder="e.g., Emergency Fund or Asset")

        submitted = st.form_submit_button("Save Profile")
        if submitted:
            if not name or not occupation or income <= 0:
                st.warning("⚠️ Please fill in your Name, Occupation, and a valid Monthly Income.")
            else:
                data["name"] = name
                data["occupation"] = occupation
                data["income"] = income
                data["expenses"] = expenses
                data["current_savings"] = current_savings
                data["financial_goal"] = financial_goal
                
                if not data["monthly_trend"]:
                    data["monthly_trend"].append({"Month": "Month 1", "Savings": current_savings})
                
                save_data(data)
                st.success("✅ Profile saved permanently! Your data is secure.")

    st.markdown("---")
    col_spacer, col1, col2 = st.columns([1, 1.3, 1.4])
    with col1:
        if st.button("⬅️ Back: Home"):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("Next: Purchase Coach ➡️"):
            st.session_state.page = "Purchase Coach"
            st.rerun()

# ----------------- 3. PURCHASE COACH PAGE -----------------
elif page == "Purchase Coach":
    st.title("🛒 Purchase Coach & Wishlist Dashboard")
    st.write("Evaluating a purchase? Let AI objectively review your numbers before you add it to your wishlist.")

    if not data["name"] or data["income"] == 0:
        st.warning("⚠️ Please complete and save your 'Financial Profile' first!")
    else:
        item_name = st.text_input(
            "What do you want to buy?", 
            value=st.session_state.get('temp_item_name', ''), 
            placeholder="e.g., Medicine, AC, Smartwatch"
        )
        st.session_state['temp_item_name'] = item_name

        item_price = st.number_input(
            "Item Price (₹)", 
            min_value=0.0, 
            value=float(st.session_state.get('temp_item_price', 0.0))
        )
        st.session_state['temp_item_price'] = item_price

        purchase_reason = st.text_input(
            "Why do you want to buy this?", 
            value=st.session_state.get('temp_item_reason', ''), 
            placeholder="e.g., Necessity, Comfort, Luxury"
        )
        st.session_state['temp_item_reason'] = purchase_reason

        if st.button("📊 Analyze Purchase Decision"):
            if not client:
                st.error("API Key not found or invalid.")
            elif not item_name or item_price <= 0:
                st.warning("Please enter a valid item name and price.")
            else:
                surplus = data["income"] - data["expenses"]
                prompt = f"""
                Act as a strict, concise, professional AI Financial Coach. Analyze this purchase for {data['name']}:
                - Occupation: {data['occupation']}
                - Income: ₹{data['income']}
                - Expenses: ₹{data['expenses']}
                - Monthly Surplus: ₹{surplus}
                - Current Savings: ₹{data['current_savings']}
                - Item: {item_name} costing ₹{item_price}
                - Reason: {purchase_reason}

                Provide a short dashboard-style response using bullet points only. Avoid long paragraphs and skip any extra motivation. Format strictly into:
                1. Need or Want? (1 line)
                2. Budget & Savings Impact (Short bullet points with exact numbers)
                3. Pros & Cons (2 bullet points each)
                4. Final Verdict & Alternative (Should they buy it? Give a short practical suggestion)
                """
                with st.spinner("Analyzing your purchase..."):
                    try:
                        response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
                        data["last_purchase_analysis"] = response.text
                        
                        if "purchase_history" not in data:
                            data["purchase_history"] = []
                        
                        # Add new item with default purchased status as False
                        data["purchase_history"].insert(0, {
                            "item": item_name,
                            "price": item_price,
                            "reason": purchase_reason,
                            "purchased": False
                        })
                        save_data(data)
                        st.success("✅ Purchase analyzed and saved to Wishlist Log successfully!")
                    except Exception as e:
                        st.error(f"Error generating analysis: {e}")

        # Persistent AI Analysis View
        if data.get("last_purchase_analysis"):
            st.markdown("### 📋 Quick Purchase Insights")
            st.markdown(data["last_purchase_analysis"])

        if data.get("purchase_history"):
            st.markdown("---")
            st.markdown("### 📜 Permanent Wishlist Log")
            st.write("Check the box once you purchase an item, or click Remove to delete it.")
            
            for idx, hist in enumerate(data["purchase_history"][:5]):
                col_check, col_item, col_btn = st.columns([0.8, 5.2, 1.2])
                
                with col_check:
                    is_purchased = st.checkbox("Bought", value=hist.get("purchased", False), key=f"check_bought_{idx}")
                    if is_purchased != hist.get("purchased", False):
                        hist["purchased"] = is_purchased
                        save_data(data)
                
                with col_item:
                    item_display = f"~~{hist['item']}~~ — ₹{hist['price']} *(Reason: {hist['reason']})* [PURCHASED]" if hist.get("purchased") else f"**{hist['item']}** — ₹{hist['price']} *(Reason: {hist['reason']})*"
                    st.markdown(f"{idx+1}. {item_display}")
                
                with col_btn:
                    if st.button("Remove", key=f"del_hist_{idx}"):
                        data["purchase_history"].remove(hist)
                        save_data(data)
                        st.success(f"Removed '{hist['item']}' from wishlist!")
                        st.rerun()

    st.markdown("---")
    col_spacer, col1, col2 = st.columns([0.7, 1.4, 1.4])
    with col1:
        if st.button("⬅️ Back: Financial Profile"):
            st.session_state.page = "Financial Profile"
            st.rerun()
    with col2:
        if st.button("Next: Financial Health ➡️"):
            st.session_state.page = "Financial Health"
            st.rerun()

# ----------------- 4. FINANCIAL HEALTH PAGE -----------------
elif page == "Financial Health":
    st.title("📊 Financial Health Dashboard")
    
    if not data["name"] or data["income"] == 0:
        st.warning("⚠️ Please complete and save your 'Financial Profile' first!")
    else:
        surplus = max(0.0, data["income"] - data["expenses"])
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Income", f"₹{data['income']}")
        col2.metric("Expenses", f"₹{data['expenses']}")
        col3.metric("Monthly Surplus", f"₹{surplus}")
        col4.metric("Savings", f"₹{data['current_savings']}")

        st.markdown("### 📉 Income Allocation & Expense Ratio")
        
        pie_data = {
            "Category": ["Expenses", "Surplus / Savings"],
            "Amount": [data["expenses"], surplus]
        }
        fig = px.pie(pie_data, names="Category", values="Amount", hole=0.4, 
                     color_discrete_sequence=["#154247", "#88D2D6"])
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🔍 Generate Health Report"):
            if not client:
                st.error("API Key not found.")
            else:
                prompt = f"""
                Act as a concise, professional financial advisor. Review financial health for {data['name']} ({data['occupation']}):
                - Income: ₹{data['income']}, Expenses: ₹{data['expenses']}, Surplus: ₹{surplus}, Savings: ₹{data['current_savings']}

                Provide a crisp, short bullet-point response. No long paragraphs, no introductory greetings, and no motivation. Include:
                1. Health Status (1 line summary)
                2. Key Strengths (2 bullet points)
                3. Areas of Improvement (2 bullet points)
                4. Actionable Steps (2-3 short bullets)
                """
                with st.spinner("Analyzing financial health..."):
                    try:
                        response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
                        data["last_health_report"] = response.text
                        save_data(data)
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Persistent Health Report View
        if data.get("last_health_report"):
            st.markdown("### 📋 Health Report Summary")
            st.markdown(data["last_health_report"])

    st.markdown("---")
    col_spacer, col1, col2 = st.columns([0.7, 1.4, 1.3])
    with col1:
        if st.button("⬅️ Back: Purchase Coach"):
            st.session_state.page = "Purchase Coach"
            st.rerun()
    with col2:
        if st.button("Next: Goal Planner ➡️"):
            st.session_state.page = "Goal Planner"
            st.rerun()

# ----------------- 5. GOAL PLANNER PAGE -----------------
elif page == "Goal Planner":
    st.title("🎯 Goal Planner & Trend Dashboard")

    if not data["name"] or data["income"] == 0:
        st.warning("⚠️ Please complete and save your 'Financial Profile' first!")
    else:
        target_amount = st.number_input(
            "Target Goal Amount (₹)", 
            min_value=0.0, 
            value=float(st.session_state.get('temp_target_amount', data.get("target_amount", 0.0)))
        )
        st.session_state['temp_target_amount'] = target_amount
        data["target_amount"] = target_amount
        
        target_months = st.number_input(
            "Target Timeline (in Months)", 
            min_value=1, 
            value=int(st.session_state.get('temp_target_months', data.get("target_months", 6)))
        )
        st.session_state['temp_target_months'] = target_months
        data["target_months"] = target_months

        with st.expander("📈 Update Savings Trend Data"):
            selected_month_label = st.selectbox("Select Month to Record/Update", [f"Month {i}" for i in range(1, 13)])
            new_savings_input = st.number_input("Record Savings for Selected Month (₹)", min_value=0.0, value=float(data["current_savings"]))
            
            if st.button("Save/Update Trend History"):
                existing_entry = next((item for item in data["monthly_trend"] if item["Month"] == selected_month_label), None)
                if existing_entry:
                    existing_entry["Savings"] = new_savings_input
                    st.success(f"Updated {selected_month_label} record successfully!")
                else:
                    data["monthly_trend"].append({"Month": selected_month_label, "Savings": new_savings_input})
                    st.success(f"Added {selected_month_label} record successfully!")
                save_data(data)

        if data["monthly_trend"]:
            st.markdown("### 📈 Long-term Savings Growth Trend")
            chart_source = {item["Month"]: item["Savings"] for item in data["monthly_trend"]}
            st.line_chart(chart_source)

        if st.button("🚀 Generate Action Plan"):
            if not client:
                st.error("API Key not found.")
            elif target_amount <= 0:
                st.warning("Please enter a valid target amount.")
            else:
                monthly_target = target_amount / target_months
                progress_val = min(1.0, data["current_savings"] / target_amount) if target_amount > 0 else 0.0
                st.markdown(f"**Goal Progress Tracking (Current Savings vs Target):**")
                st.progress(progress_val)

                prompt = f"""
                Create a micro action plan for {data['name']} to reach goal of ₹{target_amount} in {target_months} months.
                - Monthly Income: ₹{data['income']}, Surplus: ₹{data['income'] - data['expenses']}
                - Required Monthly Saving: ₹{monthly_target:.2f}
                - Current Savings already available: ₹{data['current_savings']}

                Keep it extremely brief and bulleted. No fluff, no motivation. Include:
                1. Monthly Target Breakdown
                2. Potential Roadblocks (2 bullets)
                3. Quick Execution Steps (2-3 bullets)
                """
                with st.spinner("Building your plan..."):
                    try:
                        response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
                        data["last_goal_plan"] = f"### 📋 Goal Roadmap (Target: ₹{monthly_target:.2f}/month)\n\n" + response.text
                        save_data(data)
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Persistent Goal Plan View
        if data.get("last_goal_plan"):
            st.markdown(data["last_goal_plan"])

    st.markdown("---")
    col_spacer, col1, col2 = st.columns([0.7, 1.4, 1.2])
    with col1:
        if st.button("⬅️ Back: Financial Health"):
            st.session_state.page = "Financial Health"
            st.rerun()
    with col2:
        if st.button("Next: Motivation ➡️"):
            st.session_state.page = "Motivation"
            st.rerun()

# ----------------- 6. MOTIVATION PAGE -----------------
elif page == "Motivation":
    st.title("✨ AI Motivation & Insights")
    st.write("Your dedicated space for sensible financial wisdom and encouragement.")

    if st.button("💡 Get Daily Motivation"):
        if not client:
            st.error("API Key not found.")
        else:
            name_text = data["name"] if data["name"] else "Friend"
            prompt = f"Provide a short, powerful, and practical financial wisdom quote and a 2-line advice specifically for a student/professional named {name_text}."
            with st.spinner("Fetching inspiration..."):
                try:
                    response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    col_spacer, col1, col2 = st.columns([1.8, 1.4, 1.4])
    with col1:
        if st.button("⬅️ Back: Goal Planner"):
            st.session_state.page = "Goal Planner"
            st.rerun()
    with col2:
        if st.button("Next: Help & Guide ➡️"):
            st.session_state.page = "Help & Guide"
            st.rerun()

# ----------------- 7. HELP & GUIDE PAGE (STATIC) -----------------
elif page == "Help & Guide":
    st.title("📖 App Help & User Guide")
    st.write("Everything you need to know about navigating and using your AI Personal Finance Coach effectively.")

    st.markdown("""
    ### ℹ️ Overview of Features
    * **Financial Profile:** Securely store your core income, expenses, and savings locally. This data serves as the foundation for all AI analysis and calculations.
    * **Purchase Coach / Wishlist:** Evaluate major purchases instantly with AI feedback and maintain a permanent wishlist log with interactive checklist features.
    * **Financial Health Dashboard:** View clear expense-to-income allocation ratios and get expert optimization health checks.
    * **Goal Planner & Trend:** Track your long-term savings growth via dynamic charts and roadmap breakdowns.

    ### 🛠️ Data Management & Security
    * **Local Persistence:** All your inputs are securely stored in a local file (`finance_data.json`) on your machine. Your data remains private and secure.
    * **Interactive Wishlist:** You can mark wishlist items as 'Bought' using the checklist checkboxes or remove them entirely without losing your workflow.
    * **State Management:** Navigating back and forth between pages or reviewing insights will not erase your filled profiles, history logs, or AI reports.

    ### ❓ Frequently Asked Questions (FAQ)
    * **Q: Why did my month count change automatically?**
      * *A:* In the updated version, you can manually select which month you want to update or record, completely preventing unintended auto-increments.
    * **Q: Do I need internet access for help or guides?**
      * *A:* No! This Help & Guide page is completely static and hard-coded, meaning it loads instantly without requiring any AI API calls.
    """)

    st.markdown("---")
    col_spacer, col1 = st.columns([1.8, 1.4])
    with col1:
        if st.button("⬅️ Back: Motivation"):
            st.session_state.page = "Motivation"
            st.rerun()