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

# ----------------- PROFESSIONAL DEEP TEAL FINTECH CSS & CONTAINER STYLING -----------------
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
                data = json.load(f)
                if "fixed_liabilities" not in data:
                    data["fixed_liabilities"] = {
                        "housing_status": "No", "rent_amount": 0.0, "maintenance_amount": 0.0,
                        "emi_status": "No", "loan_type": "", "emi_amount": 0.0,
                        "utility_status": "No", "utility_amount": 0.0,
                        "medical_status": "No", "medical_amount": 0.0,
                        "pet_status": "No", "pet_amount": 0.0
                    }
                return data
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
        "target_months": 6,
        "fixed_liabilities": {
            "housing_status": "No", "rent_amount": 0.0, "maintenance_amount": 0.0,
            "emi_status": "No", "loan_type": "", "emi_amount": 0.0,
            "utility_status": "No", "utility_amount": 0.0,
            "medical_status": "No", "medical_amount": 0.0,
            "pet_status": "No", "pet_amount": 0.0
        }
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

pages = ["Home", "Financial Profile", "Purchase Coach", "Financial Health", "Goal Planner", "Money Lens", "Help & Guide"]

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

    st.write("Enter your core financial details and structured commitments inside the clean profile container below.")

    fl = data.get("fixed_liabilities", {})

    # ---------------------------------------------------------
    # BACKWARD-COMPATIBILITY HELPERS
    # ---------------------------------------------------------
    # Calculate old fixed commitments so existing saved profiles
    # can be used to pre-fill the new Flexible Spending field.

    old_fixed_total = (
        float(fl.get("rent_amount", 0.0))
        + float(fl.get("maintenance_amount", 0.0))
        + float(fl.get("emi_amount", 0.0))
        + float(fl.get("utility_amount", 0.0))
        + float(fl.get("medical_amount", 0.0))
    )

    old_expenses = float(data.get("expenses", 0.0))

    # If an older profile exists, estimate flexible spending from
    # old total expenses minus old fixed commitments.
    estimated_flexible_default = max(0.0, old_expenses - old_fixed_total)

    # Single Unified Compact Container Box for the entire profile

    with st.container(border=True):

        # =====================================================
        # 1. CORE INFORMATION
        # =====================================================

        st.subheader("📋 Core Information")

        name = st.text_input(
            "Your Name",
            value=data.get("name", "")
        )

        occupation = st.text_input(
            "Occupation / Status",
            value=data.get("occupation", ""),
            placeholder="e.g., Student / Professional"
        )

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0.0,
            value=float(data.get("income", 0.0))
        )

        current_savings = st.number_input(
            "Current Total Savings (₹)",
            min_value=0.0,
            value=float(data.get("current_savings", 0.0))
        )

        financial_goal = st.text_input(
            "Primary Financial Goal",
            value=data.get("financial_goal", ""),
            placeholder="e.g., Emergency Fund or Asset"
        )

        st.markdown("")

        # =====================================================
        # 2. FIXED COMMITMENTS
        # =====================================================

        st.subheader("🔒 Fixed Commitments")

        # -----------------------------------------------------
        # Housing
        # -----------------------------------------------------

        housing_default = (
            0 if fl.get("housing_status", "No") == "Yes" else 1
        )

        housing_status = st.radio(
            "Fixed Housing Payment",
            ["Yes", "No"],
            index=housing_default,
            key="rad_housing"
        )

        housing_amount = 0.0

        if housing_status == "Yes":

            housing_amount = st.number_input(
                "Monthly Housing Payment (₹)",
                min_value=0.0,
                value=float(
                    fl.get(
                        "housing_amount",
                        fl.get("rent_amount", 0.0)
                        + fl.get("maintenance_amount", 0.0)
                    )
                ),
                key="input_housing"
            )

        # -----------------------------------------------------
        # EMI / Loan
        # -----------------------------------------------------

        emi_default = (
            0 if fl.get("emi_status", "No") == "Yes" else 1
        )

        emi_status = st.radio(
            "Other EMI / Loan Payment",
            ["Yes", "No"],
            index=emi_default,
            key="rad_emi"
        )

        emi_amount = 0.0

        if emi_status == "Yes":

            emi_amount = st.number_input(
                "Monthly EMI / Loan Payment (₹)",
                min_value=0.0,
                value=float(fl.get("emi_amount", 0.0)),
                key="input_emiamt"
            )

        # -----------------------------------------------------
        # Essential Fixed Bills
        # -----------------------------------------------------

        utility_default = (
            0 if fl.get("utility_status", "No") == "Yes" else 1
        )

        utility_status = st.radio(
            "Essential Fixed Bills",
            ["Yes", "No"],
            index=utility_default,
            key="rad_utility"
        )

        utility_amount = 0.0

        if utility_status == "Yes":

            utility_amount = st.number_input(
                "Average Monthly Essential Bills (₹)",
                min_value=0.0,
                value=float(fl.get("utility_amount", 0.0)),
                key="input_utilamt"
            )

        # -----------------------------------------------------
        # Regular Medical / Medication
        # -----------------------------------------------------

        med_default = (
            0 if fl.get("medical_status", "No") == "Yes" else 1
        )

        medical_status = st.radio(
            "Regular Medical / Medication Expense",
            ["Yes", "No"],
            index=med_default,
            key="rad_med"
        )

        medical_amount = 0.0

        if medical_status == "Yes":

            medical_amount = st.number_input(
                "Monthly Medical / Medication Cost (₹)",
                min_value=0.0,
                value=float(fl.get("medical_amount", 0.0)),
                key="input_medamt"
            )

        # =====================================================
        # 3. FLEXIBLE SPENDING
        # =====================================================

        st.markdown("")

        st.subheader("🔄 Flexible Spending")

        st.caption(
            "Include spending that can usually be reduced, postponed, "
            "or controlled when necessary — such as dining, entertainment, "
            "shopping, clothing, and other discretionary expenses."
        )

        flexible_spending = st.number_input(
            "Estimated Monthly Flexible Spending (₹)",
            min_value=0.0,
            value=float(
                data.get(
                    "flexible_spending",
                    estimated_flexible_default
                )
            ),
            key="input_flexible_spending"
        )

        # =====================================================
        # AUTOMATIC CALCULATIONS
        # =====================================================

        total_fixed_commitments = (
            housing_amount
            + emi_amount
            + utility_amount
            + medical_amount
        )

        total_monthly_expenses = (
            total_fixed_commitments
            + flexible_spending
        )

        # Small preview so the user can understand what the app
        # has calculated without entering another expense field.

        st.markdown("")

        col_calc1, col_calc2 = st.columns(2)

        with col_calc1:
            st.metric(
                "🔒 Total Fixed Commitments",
                f"₹{total_fixed_commitments:,.0f}"
            )

        with col_calc2:
            st.metric(
                "💰 Estimated Monthly Expenses",
                f"₹{total_monthly_expenses:,.0f}"
            )

        # =====================================================
        # SAVE PROFILE
        # =====================================================

        st.markdown("")

        if st.button("💾 Save Full Profile & Commitments"):

            if not name or not occupation or income <= 0:

                st.warning(
                    "⚠️ Please fill in your Name, Occupation, "
                    "and a valid Monthly Income."
                )

            else:

                # -------------------------------------------------
                # CORE DATA
                # -------------------------------------------------

                data["name"] = name
                data["occupation"] = occupation
                data["income"] = income
                data["current_savings"] = current_savings
                data["financial_goal"] = financial_goal

                # -------------------------------------------------
                # NEW FINANCIAL STRUCTURE
                # -------------------------------------------------

                data["flexible_spending"] = flexible_spending

                # IMPORTANT:
                # "expenses" is now calculated automatically.
                # There is no separate Monthly Expenses input.
                data["expenses"] = total_monthly_expenses

                # -------------------------------------------------
                # FIXED COMMITMENTS
                # -------------------------------------------------

                data["fixed_liabilities"] = {

                    # NEW STRUCTURE
                    "housing_status": housing_status,
                    "housing_amount": housing_amount,

                    "emi_status": emi_status,
                    "emi_amount": emi_amount,

                    "utility_status": utility_status,
                    "utility_amount": utility_amount,

                    "medical_status": medical_status,
                    "medical_amount": medical_amount,

                    # AUTOMATIC TOTAL
                    "total_fixed_commitments": total_fixed_commitments,

                    # -------------------------------------------------
                    # OLD KEYS RETAINED FOR BACKWARD COMPATIBILITY
                    # -------------------------------------------------

                    "rent_amount": housing_amount,
                    "maintenance_amount": 0.0,

                    # Keep loan_type so any existing Purchase Coach
                    # logic that reads it does not break.
                    "loan_type": str(
                        fl.get("loan_type", "")
                    ),

                    # Pet/dependent fields are retained in storage
                    # only so old data structures do not break.
                    # They are no longer displayed in the Profile UI.
                    "pet_status": fl.get("pet_status", "No"),
                    "pet_amount": float(
                        fl.get("pet_amount", 0.0)
                    )
                }

                # -------------------------------------------------
                # MONTHLY TREND
                # -------------------------------------------------

                if not data.get("monthly_trend"):

                    data["monthly_trend"].append(
                        {
                            "Month": "Month 1",
                            "Savings": current_savings
                        }
                    )

                # -------------------------------------------------
                # SAVE
                # -------------------------------------------------

                save_data(data)

                st.success(
                    "✅ Financial Profile and Commitments saved successfully!"
                )

    # =========================================================
    # NAVIGATION
    # =========================================================

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
                fl = data.get("fixed_liabilities", {})
                total_fixed = (fl.get("rent_amount", 0.0) if fl.get("housing_status") == "Yes" else 0.0) + \
                              (fl.get("maintenance_amount", 0.0) if fl.get("housing_status") == "Yes" else 0.0) + \
                              (fl.get("emi_amount", 0.0) if fl.get("emi_status") == "Yes" else 0.0) + \
                              (fl.get("utility_amount", 0.0) if fl.get("utility_status") == "Yes" else 0.0) + \
                              (fl.get("medical_amount", 0.0) if fl.get("medical_status") == "Yes" else 0.0) + \
                              (fl.get("pet_amount", 0.0) if fl.get("pet_status") == "Yes" else 0.0)
                
                true_disposable = data["income"] - data["expenses"] - total_fixed
                
                prompt = f"""
Act as a concise, professional, supportive AI Financial Coach. Analyze this purchase for {data['name']}:
- Occupation: {data['occupation']}
- Income: ₹{data['income']}
- General Expenses: ₹{data['expenses']}
- Total Fixed Commitments (Housing, EMIs, Utilities, Med, Pets): ₹{total_fixed}
- True Disposable Income: ₹{true_disposable}
- Current Savings: ₹{data['current_savings']}
- Item: {item_name} costing ₹{item_price}
- Reason: {purchase_reason}

Provide a short dashboard-style response using bullet points only. Avoid long paragraphs, unnecessary motivation, or judgmental language.

Use a supportive, professional, non-judgmental financial coaching tone.
Be financially responsible and firm when the numbers indicate risk, but do not shame the user.

Do not use overly harsh language such as:
"REJECT", "you must not", "financial failure", "cash bleed", or similar judgmental expressions.

Do not automatically classify comfort-related purchases as luxuries. Consider the user's stated reason and financial situation.

For the final recommendation, use one of these three verdicts:
🟢 Recommended
🟡 Consider with Caution
🔴 Not Recommended Right Now

Base the verdict on:
- Monthly cash flow
- True Disposable Income
- Current Savings
- Emergency-fund impact
- Purchase cost
- Ongoing costs, if applicable
- Whether the purchase creates additional financial pressure

If the purchase is not recommended, explain the financial reason clearly and provide a practical alternative or a condition under which the purchase could become reasonable.

Format strictly into:

1. Need or Want?
- Clearly identify whether the purchase is a Need, Want, or Comfort/Practical purchase, with a brief reason.

2. Budget & Savings Impact
- Use exact numbers.
- Explain the impact on True Disposable Income and Current Savings.
- Mention any ongoing cost if relevant.
- Clearly state whether the purchase creates financial pressure.

3. Pros & Cons
Pros:
- 2 concise bullet points

Cons:
- 2 concise bullet points

4. Final Verdict & Alternative
- Start with one of the three verdicts:
  🟢 Recommended
  🟡 Consider with Caution
  🔴 Not Recommended Right Now
- Give a short, practical explanation based on the user's numbers.
- If appropriate, suggest a realistic alternative or a condition for making the purchase later.
"""
                with st.spinner("Analyzing your purchase..."):
                    try:
                        response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
                        data["last_purchase_analysis"] = response.text
                        
                        if "purchase_history" not in data:
                            data["purchase_history"] = []
                        
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
        # =========================================================
        # 1. CALCULATE FIXED COMMITMENTS
        # =========================================================
        fl = data.get("fixed_liabilities", {})

        total_fixed = (
            (fl.get("rent_amount", 0.0)
             if fl.get("housing_status") == "Yes" else 0.0)

            + (fl.get("maintenance_amount", 0.0)
               if fl.get("housing_status") == "Yes" else 0.0)

            + (fl.get("emi_amount", 0.0)
               if fl.get("emi_status") == "Yes" else 0.0)

            + (fl.get("utility_amount", 0.0)
               if fl.get("utility_status") == "Yes" else 0.0)

            + (fl.get("medical_amount", 0.0)
               if fl.get("medical_status") == "Yes" else 0.0)

            + (fl.get("pet_amount", 0.0)
               if fl.get("pet_status") == "Yes" else 0.0)
        )

        # =========================================================
        # 2. CORE FINANCIAL CALCULATIONS
        # =========================================================

        monthly_income = float(
            data.get("income", 0.0)
        )

        monthly_spending = float(
            data.get("expenses", 0.0)
        )

        current_savings = float(
            data.get("current_savings", 0.0)
        )

        # ---------------------------------------------------------
        # Monthly Cash Flow
        # ---------------------------------------------------------
        # IMPORTANT:
        # Do NOT force negative surplus to zero.
        # A deficit must remain visible because it is an important
        # financial health signal.

        monthly_surplus = (
            monthly_income
            - monthly_spending
            - total_fixed
        )

        # Total monthly financial need used for emergency coverage
        monthly_safety_need = (
            monthly_spending
            + total_fixed
        )

        # ---------------------------------------------------------
        # Emergency Coverage
        # ---------------------------------------------------------

        if monthly_safety_need > 0:
            emergency_coverage = (
                current_savings / monthly_safety_need
            )
        else:
            emergency_coverage = 0.0

        # ---------------------------------------------------------
        # Surplus Rate
        # ---------------------------------------------------------

        if monthly_income > 0:
            savings_rate = (
                monthly_surplus
                / monthly_income
            ) * 100
        else:
            savings_rate = 0.0

        # =========================================================
        # 3. TOP KPI CARDS
        # =========================================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Monthly Income",
            f"₹{monthly_income:,.0f}"
        )

        col2.metric(
            "🏦 Current Savings",
            f"₹{current_savings:,.0f}"
        )

        col3.metric(
            "💸 Monthly Spending",
            f"₹{monthly_spending:,.0f}"
        )

        col4.metric(
            "🛡️ Emergency Coverage",
            f"{emergency_coverage:.1f} months"
        )

        # =========================================================
        # 4. MONTHLY CASH FLOW
        # =========================================================

        st.markdown("### 💵 Monthly Cash Flow")

        surplus_col1, surplus_col2, surplus_col3 = st.columns(3)

        surplus_col1.metric(
            "Monthly Surplus",
            f"₹{monthly_surplus:,.0f}"
        )

        surplus_col2.metric(
            "Fixed Commitments",
            f"₹{total_fixed:,.0f}"
        )

        surplus_col3.metric(
            "Surplus Rate",
            f"{savings_rate:.1f}%"
        )

        # =========================================================
        # 5. INCOME ALLOCATION & EXPENSE RATIO
        # =========================================================

        st.markdown("### 📉 Income Allocation & Expense Ratio")

        # Flexible spending = General expenses
        flexible_spending = monthly_spending

        # ---------------------------------------------------------
        # IMPORTANT:
        # Plotly pie charts cannot use negative values.
        # If cash flow is negative, show the deficit separately
        # instead of passing a negative number to the pie chart.
        # ---------------------------------------------------------

        if monthly_surplus >= 0:

            pie_data = {
                "Category": [
                    "Fixed Commitments",
                    "Flexible Spending",
                    "Monthly Surplus"
                ],
                "Amount": [
                    total_fixed,
                    flexible_spending,
                    monthly_surplus
                ]
            }

        else:

            pie_data = {
                "Category": [
                    "Fixed Commitments",
                    "Flexible Spending",
                    "Cash Flow Deficit"
                ],
                "Amount": [
                    total_fixed,
                    flexible_spending,
                    abs(monthly_surplus)
                ]
            }

        fig = px.pie(
            pie_data,
            names="Category",
            values="Amount",
            hole=0.4,
            color_discrete_sequence=[
                "#154247",
                "#2E6A71",
                "#88D2D6"
            ]
        )

        fig.update_layout(
            margin=dict(
                t=20,
                b=20,
                l=20,
                r=20
            ),
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =========================================================
        # 6. FINANCIAL SAFETY SUMMARY
        # =========================================================

        st.markdown("### 🛡️ Financial Safety")

        safety_col1, safety_col2 = st.columns(2)

        with safety_col1:
            st.metric(
                "Emergency Fund",
                f"₹{current_savings:,.0f}"
            )

        with safety_col2:
            st.metric(
                "Coverage",
                f"{emergency_coverage:.1f} months"
            )

        # ---------------------------------------------------------
        # Emergency Coverage Interpretation
        # ---------------------------------------------------------

        if emergency_coverage >= 6:

            st.success(
                "🟢 Strong emergency coverage — your current reserve "
                "covers approximately 6 or more months of monthly "
                "financial needs."
            )

        elif emergency_coverage >= 3:

            st.warning(
                "🟡 Moderate emergency coverage — your current reserve "
                f"covers approximately {emergency_coverage:.1f} months. "
                "Gradually building toward 6 months can strengthen "
                "your financial safety buffer."
            )

        else:

            st.error(
                "🔴 Low emergency coverage — your current reserve "
                f"covers approximately {emergency_coverage:.1f} months. "
                "Strengthening your financial safety buffer should "
                "be a priority."
            )

        # =========================================================
        # 7. AI HEALTH REPORT
        # =========================================================

        if st.button("🔍 Generate Health Report"):

            if not client:
                st.error("API Key not found.")

            else:
                prompt = f"""
Act as a practical, concise, and supportive AI Financial Coach.

Analyze the user's financial health using ONLY the financial numbers
provided below.

Name: {data['name']}
Occupation: {data['occupation']}

Financial Metrics:
- Monthly Income: ₹{monthly_income:,.0f}
- Monthly Spending: ₹{monthly_spending:,.0f}
- Fixed Commitments: ₹{total_fixed:,.0f}
- Monthly Surplus: ₹{monthly_surplus:,.0f}
- Current Protected Savings: ₹{current_savings:,.0f}
- Emergency Coverage: {emergency_coverage:.1f} months
- Surplus Rate: {savings_rate:.1f}%

IMPORTANT CALCULATION CONTEXT:

Monthly Surplus is already calculated as:

Monthly Income - Monthly Spending - Fixed Commitments

Do not calculate or describe the same expense twice.

Current Protected Savings is a separate financial reserve.
It is NOT monthly income, NOT monthly surplus, and NOT available
for normal spending, purchases, or goal contributions.

Do not recommend using the protected reserve to solve a recurring
monthly deficit.

The Emergency Coverage figure represents approximately how many
months the protected reserve could cover the user's calculated
monthly financial needs.

TONE AND STYLE:

- Simple and user-friendly
- Professional but conversational
- Concise
- Practical
- Non-judgmental
- Easy for a beginner to understand

Do not use complicated financial terminology unless necessary.

Avoid:
- Generic motivational statements
- Long explanations
- Repeating the same point
- Fear-based language
- Judgmental language
- "Failure", "financially irresponsible", "cash bleed",
  "financially stagnant", or similar wording
- "Must" unless absolutely necessary

Do not make assumptions that are not supported by the numbers.

For example:
- Do not call the income "strong" simply because the occupation
  sounds professional.
- Do not call the savings "healthy" without considering the
  emergency coverage and cash flow together.

Instead, explain what the numbers actually show.

IMPORTANT PRIORITY:

If Monthly Surplus is negative:
1. Identify the monthly deficit as the main issue.
2. Explain that restoring positive cash flow should come before
   increasing goal contributions or aggressive investing.
3. Keep the protected reserve separate.

If Monthly Surplus is positive:
1. Acknowledge the available surplus.
2. Consider whether the emergency coverage is adequate.
3. Then mention goal saving or investing as appropriate.

For Emergency Coverage:
- Below 3 months → Low coverage
- 3 to below 6 months → Moderate coverage
- 6 months or more → Stronger coverage

Do not present these categories as absolute financial rules.
Use them as practical indicators.

OUTPUT FORMAT:

### 1. Health Status
Give ONE short sentence describing the overall financial position.

Use a balanced label such as:
- Healthy
- Stable
- Needs Attention
- Needs Improvement

Choose the label based on the actual numbers.

### 2. Key Strengths
Give exactly 2 short bullets.

Mention genuine strengths supported by the numbers, such as:
- Existing protected savings
- Positive income
- Positive surplus
- Reasonable emergency coverage

Do not force a strength if the numbers do not support it.

### 3. Areas of Improvement
Give exactly 2 short bullets.

Focus only on the most important financial issues.

Each bullet should explain:
- What the issue is
- Why it matters

Keep each bullet to 1-2 sentences maximum.

### 4. Actionable Steps
Give exactly 3 short bullets.

Prioritize the most useful actions based on the user's actual situation.

If the surplus is negative, prioritize:
- Reducing flexible spending where realistic
- Reviewing fixed commitments where possible
- Restoring positive monthly cash flow

Do not suggest using the protected reserve to cover a recurring deficit.

If the surplus is positive, recommendations may include:
- Strengthening the emergency reserve
- Goal contributions
- Long-term investing, if appropriate

### 5. Emergency Fund Assessment
Give ONE short bullet.

State:
- Current emergency coverage in months
- Whether it is low, moderate, or strong
- A practical next step if coverage is below 6 months

Do not repeat the entire Financial Safety section.

IMPORTANT:
Do not repeat values unnecessarily.
Do not restate the same financial problem in every section.
Keep the complete report concise enough to read comfortably in under one minute.
"""

                with st.spinner("Analyzing financial health..."):

                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=prompt
                        )

                        data["last_health_report"] = response.text
                        save_data(data)

                    except Exception as e:
                        st.error(f"Error: {e}")

        # =========================================================
        # 8. PERSISTENT HEALTH REPORT
        # =========================================================

        if data.get("last_health_report"):

            st.markdown("### 📋 Health Report Summary")

            st.markdown(
                data["last_health_report"]
            )

        # =========================================================
        # NAVIGATION
        # =========================================================

        st.markdown("---")

        col_spacer, col1, col2 = st.columns(
            [0.7, 1.4, 1.3]
        )

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
    st.title("🎯 Goal Planner & Progress Dashboard")

    if not data["name"] or data["income"] == 0:
        st.warning(
            "⚠️ Please complete and save your 'Financial Profile' first!"
        )

    else:

        # =========================================================
        # 1. GOAL SETUP
        # =========================================================

        st.markdown("### ⚙️ Goal Setup")

        goal_col1, goal_col2 = st.columns(2)

        with goal_col1:
            target_amount = st.number_input(
                "Target Goal Amount (₹)",
                min_value=0.0,
                value=float(
                    st.session_state.get(
                        "temp_target_amount",
                        data.get("target_amount", 0.0)
                    )
                ),
                step=1000.0
            )

        with goal_col2:
            target_months = st.number_input(
                "Target Timeline (in Months)",
                min_value=1,
                value=int(
                    st.session_state.get(
                        "temp_target_months",
                        data.get("target_months", 6)
                    )
                ),
                step=1
            )

        goal_type = st.selectbox(
            "Goal Type",
            [
                "General Savings Goal",
                "Education",
                "Vehicle",
                "Home / Property",
                "Major Purchase",
                "Travel",
                "Other"
            ],
            index=[
                "General Savings Goal",
                "Education",
                "Vehicle",
                "Home / Property",
                "Major Purchase",
                "Travel",
                "Other"
            ].index(
                data.get("goal_type", "General Savings Goal")
            )
            if data.get("goal_type", "General Savings Goal")
            in [
                "General Savings Goal",
                "Education",
                "Vehicle",
                "Home / Property",
                "Major Purchase",
                "Travel",
                "Other"
            ]
            else 0
        )

        current_goal_fund = st.number_input(
            "Current Goal Fund (₹)",
            min_value=0.0,
            value=float(
                st.session_state.get(
                    "temp_goal_fund",
                    data.get("goal_fund", 0.0)
                )
            ),
            step=1000.0,
            help="Money already set aside specifically for this goal."
        )

        # Temporary session values
        st.session_state["temp_target_amount"] = target_amount
        st.session_state["temp_target_months"] = target_months
        st.session_state["temp_goal_fund"] = current_goal_fund

        # Current data values
        data["target_amount"] = target_amount
        data["target_months"] = target_months
        data["goal_fund"] = current_goal_fund
        data["goal_type"] = goal_type

        if st.button("💾 Save Goal Setup"):

            data["target_amount"] = target_amount
            data["target_months"] = target_months
            data["goal_fund"] = current_goal_fund
            data["goal_type"] = goal_type

            save_data(data)

            st.success("Goal setup saved successfully.")

        # =========================================================
        # 1A. PROTECTED FINANCIAL RESERVE
        # =========================================================

        protected_savings = float(
            data.get("current_savings", 0.0)
        )

        st.caption(
            "Your current savings are kept separate from the Goal Fund. "
            "Whether they should remain untouched depends on the nature "
            "and scale of the goal."
        )

        st.metric(
            "🛡️ Current Savings Reserve",
            f"₹{protected_savings:,.0f}"
        )

        # =========================================================
        # 2. FINANCIAL DATA
        # =========================================================

        monthly_income = float(
            data.get("income", 0.0)
        )

        monthly_expenses = float(
            data.get("expenses", 0.0)
        )

        fl = data.get("fixed_liabilities", {})

        total_fixed = (
            (
                fl.get("rent_amount", 0.0)
                if fl.get("housing_status") == "Yes"
                else 0.0
            )

            + (
                fl.get("maintenance_amount", 0.0)
                if fl.get("housing_status") == "Yes"
                else 0.0
            )

            + (
                fl.get("emi_amount", 0.0)
                if fl.get("emi_status") == "Yes"
                else 0.0
            )

            + (
                fl.get("utility_amount", 0.0)
                if fl.get("utility_status") == "Yes"
                else 0.0
            )

            + (
                fl.get("medical_amount", 0.0)
                if fl.get("medical_status") == "Yes"
                else 0.0
            )

            + (
                fl.get("pet_amount", 0.0)
                if fl.get("pet_status") == "Yes"
                else 0.0
            )
        )

        # IMPORTANT:
        # Keep the actual surplus, including negative values.
        monthly_surplus = (
            monthly_income
            - monthly_expenses
            - total_fixed
        )

        # =========================================================
        # 3. GOAL CALCULATIONS
        # =========================================================

        if target_amount > 0:

            remaining_amount = max(
                0.0,
                target_amount - current_goal_fund
            )

            required_monthly_saving = (
                remaining_amount / target_months
            )

            goal_progress = min(
                1.0,
                current_goal_fund / target_amount
            )

            progress_percentage = goal_progress * 100

            # -----------------------------------------------------
            # GOAL STATUS
            # -----------------------------------------------------

            if remaining_amount <= 0:

                goal_status = "🟢 Goal Already Reached"

                goal_status_message = (
                    "Your current Goal Fund already meets or exceeds "
                    "the target."
                )

            elif monthly_surplus <= 0:

                goal_status = "🔴 Not Currently Feasible"

                goal_status_message = (
                    "Your current monthly cash flow is negative. "
                    "Improving cash flow should come before increasing "
                    "regular goal contributions."
                )

            elif monthly_surplus >= required_monthly_saving:

                goal_status = "🟢 On Track"

                goal_status_message = (
                    "Your current monthly surplus can support the "
                    "required goal contribution within the timeline."
                )

            else:

                goal_status = "🟡 Needs Adjustment"

                goal_status_message = (
                    "Your current monthly surplus is below the amount "
                    "required to reach this goal within the timeline."
                )

        else:

            remaining_amount = 0.0
            required_monthly_saving = 0.0
            goal_progress = 0.0
            progress_percentage = 0.0

            goal_status = "⚪ Goal Not Set"

            goal_status_message = (
                "Enter a target amount to start planning your goal."
            )

        # =========================================================
        # 4. GOAL SNAPSHOT
        # =========================================================

        if target_amount > 0:

            st.markdown("### 📊 Goal Snapshot")

            snap1, snap2, snap3, snap4 = st.columns(4)

            snap1.metric(
                "🎯 Goal Target",
                f"₹{target_amount:,.0f}"
            )

            snap2.metric(
                "💰 Goal Fund",
                f"₹{current_goal_fund:,.0f}"
            )

            snap3.metric(
                "📌 Remaining Goal",
                f"₹{remaining_amount:,.0f}"
            )

            snap4.metric(
                "💵 Required Monthly Saving",
                f"₹{required_monthly_saving:,.0f}"
            )

            # =====================================================
            # 5. GOAL PROGRESS
            # =====================================================

            st.markdown("### 🏁 Goal Progress")

            st.progress(goal_progress)

            st.caption(
                f"₹{current_goal_fund:,.0f} / "
                f"₹{target_amount:,.0f} "
                f"({progress_percentage:.0f}% complete)"
            )

            # =====================================================
            # 6. GOAL FEASIBILITY
            # =====================================================

            st.markdown("### 🧭 Goal Feasibility")

            status_col1, status_col2 = st.columns(2)

            with status_col1:

                st.markdown(
                    f"## {goal_status}"
                )

                st.write(
                    goal_status_message
                )

            with status_col2:

                st.metric(
                    "Monthly Surplus",
                    f"₹{monthly_surplus:,.0f}"
                )

                if remaining_amount > 0:

                    st.caption(
                        f"Required Goal Saving: "
                        f"₹{required_monthly_saving:,.0f}/month"
                    )

            # =====================================================
            # 7. GOAL PROGRESS TRACKER
            # =====================================================

            st.markdown("### 📈 Goal Progress Tracker")

            st.caption(
                "Required = planned path. Actual = recorded Goal Fund."
            )

            chart_months = list(
                range(0, target_months + 1)
            )

            required_path = []

            for month in chart_months:

                required_value = min(
                    target_amount,
                    current_goal_fund
                    + (
                        required_monthly_saving
                        * month
                    )
                )

                required_path.append(
                    required_value
                )

            # -----------------------------------------------------
            # Actual Goal Fund History
            # -----------------------------------------------------

            goal_trend_data = data.get(
                "goal_monthly_trend",
                []
            )

            actual_month_numbers = [0]
            actual_values = [current_goal_fund]

            valid_goal_history = []

            for item in goal_trend_data:

                try:

                    month_text = str(
                        item.get(
                            "Month",
                            "Month 0"
                        )
                    )

                    month_number = int(
                        month_text.split()[-1]
                    )

                    goal_value = float(
                        item.get(
                            "GoalFund",
                            current_goal_fund
                        )
                    )

                    if 1 <= month_number <= target_months:

                        valid_goal_history.append(
                            (
                                month_number,
                                goal_value
                            )
                        )

                except (ValueError, TypeError):

                    continue

            valid_goal_history.sort(
                key=lambda x: x[0]
            )

            for month_number, goal_value in valid_goal_history:

                actual_month_numbers.append(
                    month_number
                )

                actual_values.append(
                    goal_value
                )

            # -----------------------------------------------------
            # Plotly Chart
            # -----------------------------------------------------

            import plotly.graph_objects as go

            required_labels = [
                f"Month {m}"
                for m in chart_months
            ]

            actual_labels = [
                f"Month {m}"
                for m in actual_month_numbers
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=required_labels,
                    y=required_path,
                    mode="lines+markers",
                    name="Required",
                    line=dict(width=3),
                    marker=dict(size=8),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Required: ₹%{y:,.0f}"
                        "<extra></extra>"
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=actual_labels,
                    y=actual_values,
                    mode="lines+markers",
                    name="Actual",
                    line=dict(width=3),
                    marker=dict(size=9),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Actual: ₹%{y:,.0f}"
                        "<extra></extra>"
                    )
                )
            )

            fig.update_layout(
                xaxis_title="Goal Timeline",
                yaxis_title="Goal Fund (₹)",
                height=450,
                margin=dict(
                    t=40,
                    b=40,
                    l=20,
                    r=20
                ),
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.caption(
                "The Required line shows the planned savings path. "
                "The Actual line shows your recorded Goal Fund."
            )

        # =========================================================
        # 8. UPDATE GOAL PROGRESS
        # =========================================================

        st.markdown("### 📝 Update Goal Progress")

        st.caption(
            "Record the total amount accumulated specifically for "
            "this goal by the end of the selected month."
        )

        update_col1, update_col2 = st.columns(2)

        with update_col1:

            selected_month_label = st.selectbox(
                "Select Month",
                [
                    f"Month {i}"
                    for i in range(1, target_months + 1)
                ]
            )

        goal_trend_data = data.get(
            "goal_monthly_trend",
            []
        )

        existing_entry = next(
            (
                item
                for item in goal_trend_data
                if item.get("Month") == selected_month_label
            ),
            None
        )

        if existing_entry:

            default_goal_fund = float(
                existing_entry.get(
                    "GoalFund",
                    current_goal_fund
                )
            )

        elif goal_trend_data:

            valid_previous_values = []

            for item in goal_trend_data:

                try:

                    month_number = int(
                        str(
                            item.get(
                                "Month",
                                "Month 0"
                            )
                        ).split()[-1]
                    )

                    goal_value = float(
                        item.get(
                            "GoalFund",
                            current_goal_fund
                        )
                    )

                    valid_previous_values.append(
                        (
                            month_number,
                            goal_value
                        )
                    )

                except (ValueError, TypeError):

                    continue

            if valid_previous_values:

                valid_previous_values.sort(
                    key=lambda x: x[0]
                )

                default_goal_fund = valid_previous_values[-1][1]

            else:

                default_goal_fund = current_goal_fund

        else:

            default_goal_fund = current_goal_fund

        minimum_goal_fund = max(
            current_goal_fund,
            default_goal_fund
        )

        with update_col2:

            new_goal_fund = st.number_input(
                "Total Goal Fund at Month End (₹)",
                min_value=minimum_goal_fund,
                value=minimum_goal_fund,
                step=1000.0,
                help=(
                    "Enter the total amount accumulated specifically "
                    "for this goal by the end of the selected month."
                )
            )

        if st.button("💾 Save Goal Progress"):

            if "goal_monthly_trend" not in data:
                data["goal_monthly_trend"] = []

            existing_entry = next(
                (
                    item
                    for item in data["goal_monthly_trend"]
                    if item.get("Month") == selected_month_label
                ),
                None
            )

            if new_goal_fund < current_goal_fund:

                st.warning(
                    "⚠️ Goal Fund cannot be lower than your current "
                    "Goal Fund."
                )

            else:

                if existing_entry:

                    existing_entry["GoalFund"] = new_goal_fund

                    st.success(
                        f"Updated {selected_month_label} successfully!"
                    )

                else:

                    data["goal_monthly_trend"].append(
                        {
                            "Month": selected_month_label,
                            "GoalFund": new_goal_fund
                        }
                    )

                    st.success(
                        f"Added {selected_month_label} successfully!"
                    )

                save_data(data)

                st.rerun()

        # =========================================================
        # 9. CALCULATED GOAL RECOMMENDATION
        # =========================================================

        st.markdown("### 💡 Goal Recommendation")

        if target_amount <= 0:

            st.info(
                "Set a target amount above to start planning your goal."
            )

        elif remaining_amount <= 0:

            st.success(
                "🎉 Your current Goal Fund already meets your target."
            )

        elif monthly_surplus <= 0:

            st.warning(
                "Your current monthly cash flow is negative. "
                "Improving cash flow should come before increasing "
                "regular contributions toward this goal."
            )

        elif monthly_surplus >= required_monthly_saving:

            st.success(
                f"Your goal appears achievable. Allocating around "
                f"₹{required_monthly_saving:,.0f} per month would "
                f"support the target within {target_months} months."
            )

        else:

            monthly_gap = (
                required_monthly_saving
                - monthly_surplus
            )

            st.warning(
                f"Your current surplus is about ₹{monthly_gap:,.0f} "
                f"below the monthly amount needed for this timeline."
            )

        # =========================================================
        # 10. AI GOAL ACTION PLAN
        # =========================================================

        if st.button("🚀 Generate Detailed Goal Action Plan"):

            if not client:
                st.error("API Key not found.")

            elif target_amount <= 0:
                st.warning("Please enter a valid target amount.")

            else:
                prompt = f"""
Act as a practical, personalized financial planning assistant.

Analyze the user's specific financial goal using ONLY the financial information provided below.

USER:
- Name: {data['name']}
- Occupation: {data.get('occupation', 'Not provided')}

GOAL:
- Goal Amount: ₹{target_amount:,.0f}
- Timeline: {target_months} months
- Current Goal Fund: ₹{current_goal_fund:,.0f}
- Remaining Goal Amount: ₹{remaining_amount:,.0f}
- Required Monthly Saving: ₹{required_monthly_saving:,.0f}

CURRENT FINANCIAL POSITION:
- Monthly Income: ₹{monthly_income:,.0f}
- Monthly Expenses: ₹{monthly_expenses:,.0f}
- Fixed Commitments: ₹{total_fixed:,.0f}
- Monthly Surplus: ₹{monthly_surplus:,.0f}
- Protected Savings / Current Total Savings: ₹{protected_savings:,.0f}
- Emergency Coverage: {protected_savings / (monthly_expenses + total_fixed) if (monthly_expenses + total_fixed) > 0 else 0:.1f} months

CURRENT GOAL STATUS:
{goal_status}

IMPORTANT DECISION RULES:

1. Personalize the advice completely to the user's actual numbers.
   Do not assume that all users have a similar income, savings,
   expenses, or financial situation.

2. Never use or assume any fixed savings amount, income level,
   expense level, or financial threshold that is not provided above.

3. Do not automatically treat Protected Savings as either:
   - available money for the goal, OR
   - completely untouchable money.

   Instead, assess whether it should remain protected, whether a
   portion could reasonably be considered for this goal, or whether
   it should not be used at all.

4. When making that decision, consider the complete situation:
   - size of the goal
   - timeline
   - current Goal Fund
   - remaining amount
   - monthly surplus or deficit
   - current savings
   - emergency coverage
   - fixed commitments
   - ability to continue meeting regular expenses

5. For a normal or relatively small goal, prefer using the Goal Fund
   and future monthly surplus rather than unnecessarily reducing
   financial reserves.

6. For a major or high-value goal, do not automatically reject
   the use of existing savings. Consider whether using some savings
   could be reasonable while still maintaining an appropriate
   financial safety buffer.

7. If the user's monthly cash flow is negative, identify this as a
   major constraint and prioritize restoring positive cash flow.

8. If the goal is not realistic within the current timeline, explain
   whether the user should reduce the target, extend the timeline,
   increase saving capacity, or reconsider the goal.

9. Do not recommend aggressive investing or risky financial actions
   simply to achieve the goal.

10. Do not make decisions based on generic rules alone. Use the user's
    actual financial context and explain the reasoning briefly.

OUTPUT STYLE:

Keep the response concise, clear, and easy for a beginner to understand.

Do not repeat all dashboard numbers unnecessarily.
Use the numbers only when they help explain a decision.

Do not use complicated financial terminology.
Do not use long paragraphs.
Do not use generic motivational statements.
Do not use fear-based or judgmental language.

Avoid words such as:
"failure", "irresponsible", "impossible", "must", "financially reckless".

Use simple language such as:
"consider", "prioritize", "it may be better to", or
"based on your current situation".

Provide exactly these sections:

### 1. Goal Assessment
- 1-2 short bullets explaining whether the goal is currently
  realistic and why.

### 2. Funding Approach
- Explain the most suitable funding approach for this user.
- Clearly state whether the goal should mainly be funded through
  monthly surplus, the existing Goal Fund, existing savings,
  or a combination.
- If existing savings should remain protected, explain why briefly.
- If using a portion of existing savings could be reasonable,
  explain the conditions briefly.

### 3. Main Constraint
- Identify the single biggest issue affecting this goal.
- Add one short supporting point if needed.

### 4. Practical Next Steps
- Give 2-3 specific actions the user can realistically take.

### 5. Timeline Assessment
- State whether the current timeline should be kept, extended,
  shortened, or reconsidered.
- Give a brief reason.

### 6. Savings Safety
- Briefly explain how the user's current savings and emergency
  coverage affect the decision.
- Do not give a generic recommendation.
- Base the advice on the user's actual financial position.

Keep the final response useful enough to help the user make a decision,
but short enough that it does not feel like a long financial report.
"""

                with st.spinner("Building your personalized goal plan..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=prompt
                        )

                        data["last_goal_plan"] = (
                            "### 📋 Detailed Goal Roadmap\n\n"
                            + response.text
                        )

                        save_data(data)

                    except Exception as e:
                        st.error(f"Error: {e}")

        # =========================================================
        # 11. PERSISTENT GOAL PLAN
        # =========================================================

        if data.get("last_goal_plan"):

            st.markdown(
                data["last_goal_plan"]
            )

        # =========================================================
        # NAVIGATION
        # =========================================================

        st.markdown("---")

        col_spacer, col1, col2 = st.columns(
            [0.7, 1.4, 1.2]
        )

        with col1:

            if st.button("⬅️ Back: Financial Health"):

                st.session_state.page = "Financial Health"
                st.rerun()

        with col2:

            if st.button("Next: Money Lens ➡️"):

                st.session_state.page = "Money Lens"
                st.rerun()


# ----------------- 6. MONEY LENS PAGE -----------------
elif page == "Money Lens":
    st.title("🔍 Money Lens")
    st.write(
        "See your financial situation from a different angle — "
        "without repeating the analysis from other sections."
    )

    if st.button("✨ Show My Insight"):

        if not client:
            st.error("API Key not found.")

        else:
            name_text = data["name"] if data["name"] else "there"

            # =====================================================
            # 1. FINANCIAL DATA
            # =====================================================

            monthly_income = float(
                data.get("income", 0.0)
            )

            monthly_expenses = float(
                data.get("expenses", 0.0)
            )

            current_savings = float(
                data.get("current_savings", 0.0)
            )

            goal_fund = float(
                data.get("goal_fund", 0.0)
            )

            target_amount = float(
                data.get("target_amount", 0.0)
            )

            target_months = int(
                data.get("target_months", 0)
            )

            # =====================================================
            # 2. FIXED COMMITMENTS
            # =====================================================

            fl = data.get("fixed_liabilities", {})

            total_fixed = (
                (fl.get("rent_amount", 0.0)
                 if fl.get("housing_status") == "Yes" else 0.0)

                + (fl.get("maintenance_amount", 0.0)
                   if fl.get("housing_status") == "Yes" else 0.0)

                + (fl.get("emi_amount", 0.0)
                   if fl.get("emi_status") == "Yes" else 0.0)

                + (fl.get("utility_amount", 0.0)
                   if fl.get("utility_status") == "Yes" else 0.0)

                + (fl.get("medical_amount", 0.0)
                   if fl.get("medical_status") == "Yes" else 0.0)

                + (fl.get("pet_amount", 0.0)
                   if fl.get("pet_status") == "Yes" else 0.0)
            )

            # =====================================================
            # 3. MONTHLY CASH FLOW
            # =====================================================

            monthly_surplus = (
                monthly_income
                - monthly_expenses
                - total_fixed
            )

            # =====================================================
            # 4. EMERGENCY COVERAGE
            # =====================================================

            monthly_safety_need = (
                monthly_expenses
                + total_fixed
            )

            if monthly_safety_need > 0:
                emergency_coverage = (
                    current_savings / monthly_safety_need
                )
            else:
                emergency_coverage = 0.0

            # =====================================================
            # 5. GOAL INFORMATION
            # =====================================================

            if target_amount > 0:

                remaining_goal = max(
                    0.0,
                    target_amount - goal_fund
                )

                goal_progress = min(
                    100.0,
                    (goal_fund / target_amount) * 100
                )

            else:

                remaining_goal = 0.0
                goal_progress = 0.0

            # =====================================================
            # 6. AVAILABLE MONEY LENSES
            # =====================================================

            money_lenses = [
                "🔍 Blind Spot",
                "⚖️ Trade-off",
                "💡 Smart Move",
                "🛡️ Safety Check",
                "🎯 Goal Focus",
                "📊 Number Behind the Number",
                "🌱 Small Win",
                "🚦 Watch Out",
                "🔄 What If?"
            ]

            lens_list = ", ".join(money_lenses)

            # =====================================================
            # 7. AI PROMPT
            # =====================================================

            prompt = f"""
Act as an intelligent, calm, and practical AI Financial Coach.

Your task is to give ONE fresh financial perspective that helps
the user understand their money situation better.

The insight should add something new to the application rather than
repeating the detailed analysis already shown in Financial Health,
Purchase Coach, or Goal Planner.

User:
- Name: {name_text}

Financial Context:
- Monthly Income: ₹{monthly_income:,.0f}
- Monthly Spending: ₹{monthly_expenses:,.0f}
- Fixed Commitments: ₹{total_fixed:,.0f}
- Monthly Surplus / Deficit: ₹{monthly_surplus:,.0f}
- Current Total Savings: ₹{current_savings:,.0f}
- Emergency Coverage: {emergency_coverage:.1f} months
- Dedicated Goal Fund: ₹{goal_fund:,.0f}
- Goal Target: ₹{target_amount:,.0f}
- Goal Progress: {goal_progress:.0f}%
- Remaining Goal Amount: ₹{remaining_goal:,.0f}
- Goal Timeline: {target_months} months

IMPORTANT:

1. Personalize the insight using the user's actual financial data.

2. Do not assume that every user has the same level of income,
   savings, expenses, or financial obligations.

3. Do not use any fixed financial amount or hard-coded threshold
   that is not provided in the user's data.

4. Treat Current Total Savings as part of the user's overall
   financial resources, but do not automatically assume that it
   should either be used or never used.

5. When discussing savings, consider:
   - monthly cash flow
   - emergency coverage
   - size and purpose of the goal
   - existing Goal Fund
   - fixed commitments
   - the user's ability to continue meeting regular expenses

6. If the user appears financially secure, the insight may focus on
   a useful opportunity, trade-off, or smarter allocation.

7. If the user has financial pressure, the insight should help the
   user understand the practical risk or trade-off without creating
   unnecessary fear.

8. Do not make a final purchase or goal decision that belongs to
   another section of the application.

9. Do not simply repeat dashboard numbers. Use numbers only when
   they help explain the insight.

10. Do not give investment recommendations unless they are directly
    relevant to the insight.

Choose ONE lens from the following:

{lens_list}

IMPORTANT:

- Choose only ONE lens.
- Make the observation genuinely useful and personalized.
- Look for a relationship, trade-off, blind spot, behaviour pattern,
  opportunity, or "what if" scenario.
- Do NOT repeat the detailed Financial Health report.
- Do NOT repeat the Purchase Coach verdict.
- Do NOT repeat the Goal Planner calculation or recommendation.
- Do NOT simply restate the user's financial numbers.
- Do NOT create a generic motivational quote.
- Do NOT give a long financial lecture.
- Do not make the user feel judged or guilty.

Avoid harsh or overly technical language such as:
"failure", "irresponsible", "must", "reject", "impossible",
"financially reckless", or similar expressions.

Use simple, beginner-friendly language.

OUTPUT FORMAT:

[Selected Lens]

One short paragraph of 2-3 sentences explaining the insight
in simple and direct language.

💡 Takeaway:
One practical sentence the user can remember or act on.

Keep the entire response concise, specific, personalized,
and easy to read.
"""

            # =====================================================
            # 8. GENERATE INSIGHT
            # =====================================================

            with st.spinner("Finding a fresh perspective..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=prompt
                    )

                    st.markdown(response.text)

                except Exception as e:

                    st.error(f"Error: {e}")

    # =============================================================
    # NAVIGATION
    # =============================================================

    st.markdown("---")

    col_spacer, col1, col2 = st.columns(
        [1.8, 1.4, 1.4]
    )

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
    st.write(
        "Everything you need to know about using your AI Personal Finance Coach effectively."
    )

    st.markdown("""
    ### ℹ️ Overview of Features

    * **Financial Profile:** Store your core financial information including
      monthly income, monthly spending, current savings, and structured
      **Fixed Commitments (Housing, EMI, Utilities, Medical, Pets)** locally.

    * **Purchase Coach / Wishlist:** Evaluate a potential purchase using your
      financial position, including income, spending, fixed commitments,
      monthly cash flow, and the potential impact of the purchase.
      Important purchase ideas can also be saved to your Wishlist.

    * **Financial Health Dashboard:** Understand your financial position through
      key indicators such as **Monthly Income, Monthly Spending, Current
      Savings, Emergency Coverage, Monthly Surplus, and Surplus Rate**, along
      with your income allocation and financial health assessment.

    * **Goal Planner & Progress:** Create a financial goal by setting a target
      amount and timeline. Track a separate **Goal Fund** and compare your
      actual progress with the required savings path.

    * **Financial Decision Support:** The app does not assume that your
      existing savings should always be used or always be left untouched.
      For larger or important financial goals, the app considers your
      savings, cash flow, emergency coverage, goal size, and timeline together
      before providing guidance.

    * **Money Lens:** Get one short, personalized financial insight based on
      your overall situation. It focuses on a useful relationship, trade-off,
      blind spot, or scenario that may not be obvious from the other sections.
    """)

    st.markdown("""
    ### 🎯 Understanding Your Goal Planner

    * **Goal Target:** The total amount you want to accumulate for a specific
      financial goal.

    * **Goal Fund:** Money specifically set aside for that particular goal.

    * **Current Savings:** Your total savings entered in the Financial Profile.
      This is considered separately from the dedicated Goal Fund.

    * **Remaining Goal:** The amount still required to reach your target after
      accounting for your current Goal Fund.

    * **Required Monthly Saving:** The approximate amount that needs to be
      allocated toward the goal each month to reach the remaining target within
      your selected timeline.

    * **Goal Progress:** Shows how much of the target has already been
      accumulated in the dedicated Goal Fund.

    * **Goal Feasibility:** Compares the required monthly goal contribution
      with your current Monthly Surplus to assess whether the timeline is
      currently realistic.

    * **Goal Progress Tracker:** Compares the required Goal Fund growth path
      with your actual recorded Goal Fund progress over time.

    * **AI Goal Action Plan:** Provides personalized guidance based on your
      actual goal and complete financial situation. It considers factors such
      as your income, expenses, fixed commitments, current savings, emergency
      coverage, Goal Fund, goal size, and timeline.
    """)

    st.markdown("""
    ### 🛡️ Understanding Your Savings

    * **Current Savings:** The total savings amount you enter in your
      Financial Profile.

    * **Emergency Coverage:** Shows approximately how many months your current
      savings could cover your regular monthly financial needs.

    * **Goal Fund:** Money specifically tracked for a particular goal and
      separated from Current Savings.

    * **Savings Decision:** Current Savings are not automatically treated as
      either available for every goal or completely untouchable. The appropriate
      approach depends on the goal and your overall financial position.

    * **Major Goals:** For a significant goal, the AI can consider whether
      using part of your existing savings may be reasonable while maintaining
      an appropriate financial safety buffer.

    * **Regular Goals:** For smaller or routine goals, using the dedicated
      Goal Fund and future monthly surplus will generally be considered first
      when appropriate.

    * **Important:** The app provides financial guidance based on the
      information you provide. It does not guarantee that a particular
      financial decision will be suitable in every situation.
    """)

    st.markdown("""
    ### 🛠️ Data Management & Security

    * **Local Persistence:** Your financial inputs, goal information, wishlist
      records, and saved reports are stored locally in the application's
      `finance_data.json` file on your machine.

    * **Separate Goal Tracking:** Goal Fund records are maintained separately
      from Current Savings. The app does not automatically transfer or use
      Current Savings for a goal.

    * **Interactive Wishlist:** Saved wishlist items can be marked as
      **Bought** using the available checklist controls or removed when no
      longer needed.

    * **State Management:** Moving between pages or reviewing saved information
      does not automatically erase your profile, goal history, wishlist
      records, or saved AI reports.
    """)

    st.markdown("""
    ### 💡 How to Use the App

    1. Complete and save your **Financial Profile** first.
    2. Use **Purchase Coach** when you need help evaluating a purchase
       before making a financial decision.
    3. Check **Financial Health** to understand your current financial
       position, monthly cash flow, and emergency coverage.
    4. Use **Goal Planner** when you have a specific future financial target.
    5. Keep track of your **Goal Fund** separately from your Current Savings.
    6. For major financial goals, review the AI's guidance on whether your
       existing savings should be considered alongside your future cash flow.
    7. Use **Money Lens** when you want a short, fresh financial perspective
       that is different from the detailed analysis in the other sections.
    """)

    st.markdown("---")

    col_spacer, col1 = st.columns([1.8, 1.4])

    with col1:
        if st.button("⬅️ Back: Money Lens"):
            st.session_state.page = "Money Lens"
            st.rerun()