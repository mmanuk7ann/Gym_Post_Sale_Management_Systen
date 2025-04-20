# # app.py


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gym Dashboard", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

params = st.query_params
selected_tab = params.get("tab", "email")  # default to "email"
customer_name = params.get("customer", "")

if "action" in params:
    action = params["action"][0]
    customer = params.get("customer", [""])[0]
    st.title(f"{action.title()} Template for {customer}")
    st.markdown(f"Here you can show templates or forms for sending a {action.upper()} to {customer}.")
    st.stop()



def show_login():
    st.markdown("<h1 style='font-size: 40px; font-weight: 600;'>Login</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Log In")

    if login_btn:
        if email == "admin@gym.com" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
  # This line makes it instantly move to the dashboard
        else:
            st.error("Email or Password is incorrect.")

def show_dashboard():
    import pandas as pd

    # Custom CSS
    st.sidebar.markdown("""
        <style>
            div[data-testid="stSidebar"] {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100vh;
            }
            .tab-button {
                border: none;
                background: none;
                color: #262730;
                font-size: 16px;
                text-align: left;
                padding: 0.5rem 1rem;
                margin: 0.2rem 0;
                border-radius: 5px;
            }
            .tab-button:hover {
                background-color: #eeeeee;
                cursor: pointer;
            }
            .tab-active {
                background-color: #dddddd !important;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar layout
    st.sidebar.markdown("### Dashboard Navigation")

    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Dashboard"

    # Tab list
    tabs = ["Dashboard", "Customers", "Risk Management", "Templates"]

    # Display as styled buttons
    for tab in tabs:
        button_style = "tab-button"
        if st.session_state.current_tab == tab:
            button_style += " tab-active"

        if st.sidebar.button(f"{tab}", key=tab):
            st.session_state.current_tab = tab

    # Logout button at bottom
    with st.sidebar:
        st.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    # Page logic
    page = st.session_state.current_tab

    if page == "Dashboard":

        st.markdown("<h1 style='font-size: 40px; font-weight: 700;'>Welcome, Gold's Gym!</h1>", unsafe_allow_html=True)

        # Card styles
        card_style = """
            background-color: #f9f9f9;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.07);
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        """


        # Create 4 cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"<div style='{card_style}'><h4>Total Members</h4><h2>124</h2></div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div style='{card_style}'><h4>At-Risk Members</h4><h2>19</h2></div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div style='{card_style}'><h4>Avg. CLV</h4><h2>$320</h2></div>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"<div style='{card_style}'><h4>Monthly Retention</h4><h2>87%</h2></div>", unsafe_allow_html=True)


        st.subheader("🔔 Alerts")
        st.warning("Churn rate has increased by 15% in the last 30 days.")
        st.line_chart({"Churn Rate (%)": [10, 12, 13, 14, 15]})

    elif page == "Customers":
        st.title("👥 Customers")

        customer_data = {
            "Name": ["Jane Smith", "John Doe", "Emma Brown", "Mark Lee", "Sara White"],
            "Email": ["jane@gym.com", "john@gym.com", "emma@gym.com", "mark@gym.com", "sara@gym.com"],
            "Phone": ["+1234567890", "+1987654321", "+1122334455", "+1098765432", "+1223344556"],
            "Membership": ["Premium", "Basic", "Premium", "Basic", "Premium"],
            "Gender": ["Female", "Male", "Female", "Male", "Female"]
        }

        df_customers = pd.DataFrame(customer_data)
        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_membership = st.selectbox("Filter by Membership", options=["All"] + sorted(df_customers["Membership"].unique()))
        with col2:
            selected_gender = st.selectbox("Filter by Gender", options=["All"] + sorted(df_customers["Gender"].unique()))
        with col3:
            name_search = st.text_input("Search by Name")

        # Apply filters
        if selected_membership != "All":
            df_customers = df_customers[df_customers["Membership"] == selected_membership]

        if selected_gender != "All":
            df_customers = df_customers[df_customers["Gender"] == selected_gender]

        if name_search:
            df_customers = df_customers[df_customers["Name"].str.contains(name_search, case=False)]


        st.dataframe(df_customers, use_container_width=True)

    elif page == "Risk Management":
        st.title("📉 At-Risk Customers")

        data = {
            "Name": ["Jane Smith"] * 10,
            "Last Visit": ["March 12 2025"] * 10,
            "Membership": ["Premium", "Premium", "Premium", "Premium", "Starter", "Starter", "Pro", "Pro", "Pro", "Starter"] ,
            "Risk": ["High"] * 10,
            "Action": ["Send Email", "Send Email", "Send Email", "Send SMS", "Push Notification", "Send Email", "Send Email", "Send Email", "Send Email", "Send Email" ],
            "Reason why at Risk": ["x days inactive"] * 10
        }

        df = pd.DataFrame(data)

    # Filters section
        col1, col2 = st.columns(2)
        with col1:
            selected_membership = st.selectbox("Filter by Membership Type", options=["All"] + sorted(df["Membership"].unique()))
        with col2:
            search_name = st.text_input("Search by Name")

        # Apply filters
        if selected_membership != "All":
            df = df[df["Membership"] == selected_membership]

        if search_name:
            df = df[df["Name"].str.contains(search_name, case=False)]
        if selected_membership != "All":
            df = df[df["Membership"] == selected_membership]

        #CHANGES MADE FROM HERE

        # Render custom table with action buttons
        st.write("###")
                # Header row
        with st.container():
            st.markdown("<div style='max-height: 500px; overflow-y: auto;'>", unsafe_allow_html=True)
        header_cols = st.columns([2, 2, 2, 1.5, 2, 2])
        header_cols[0].markdown("**Name**")
        header_cols[1].markdown("**Last Visit**")
        header_cols[2].markdown("**Membership**")
        header_cols[3].markdown("**Risk**")
        header_cols[4].markdown("**Action**")
        header_cols[5].markdown("**Reason why at Risk**")
        # st.markdown("---")

        for index, row in df.iterrows():
            cols = st.columns([2, 2, 2, 1.5, 2, 2])
            cols[0].write(row["Name"])
            cols[1].write(row["Last Visit"])
            cols[2].write(row["Membership"])
            cols[3].write(row["Risk"])

            if row["Action"] == "Send Email":
                if cols[4].button("Send Email", key=f"email_{index}"):
                    st.session_state.current_tab = "Templates"
                    st.session_state.selected_action = "Send Email"
                    st.session_state.selected_customer = row["Name"]
                    # st.experimental_rerun()
                    st.rerun()

            elif row["Action"] == "Send SMS":
                if cols[4].button("Send SMS", key=f"email_{index}"):
                    st.session_state.current_tab = "Templates"
                    st.session_state.selected_action = "Send Email"
                    st.session_state.selected_customer = row["Name"]
                    st.rerun()

                    # st.experimental_rerun()
            elif row["Action"] == "Push Notification":
                if cols[4].button("Push Notification", key=f"email_{index}"):
                    st.session_state.current_tab = "Templates"
                    st.session_state.selected_action = "Send Email"
                    st.session_state.selected_customer = row["Name"]
                    st.rerun()

                    # st.experimental_rerun()


            cols[5].write(row["Reason why at Risk"])
            #UP TO HERE

        st.markdown("</div>", unsafe_allow_html=True)
    elif page == "Templates":
        st.title("📨 Communication Templates")


        tabs = st.tabs(["Email Templates", "SMS Templates", "Push Notification Templates"])

        with tabs[0]:
            st.subheader("Email Templates")
            st.markdown("**Option 1:**")
            st.code("""Subject: We miss you at the gym, {{name}}!

        Hi {{name}},

        We noticed you haven't visited in a while. We'd love to have you back!
        Here's a special offer just for you.

        See you soon,
        Gold's Gym Team
        """)

            st.markdown("**Option 2:**")
            st.code("""Subject: Your fitness journey isn't over!

        Hi {{name}},

        Don't stop now! We believe in you.
        Check out our new programs starting this month.

        - Gold's Gym Team
        """)

        with tabs[1]:
            st.subheader("SMS Templates")
            st.markdown("**Option 1:**")
            st.code("Hey {{name}}, we miss you at Gold’s Gym! Come back this week for a special offer 💪")

            st.markdown("**Option 2:**")
            st.code("Your fitness goals are waiting, {{name}}. We’ve got something exciting just for you!")

        with tabs[2]:
            st.subheader("Push Notification Templates")
            st.markdown("**Option 1:**")
            st.code("🏋️‍♂️ Don’t forget your workout today, {{name}}!")

            st.markdown("**Option 2:**")
            st.code("🔥 {{name}}, it’s time to crush your goals at Gold’s Gym!")


        st.markdown("---")
        st.button("Back to Risk Management", on_click=lambda: st.session_state.update({"current_tab": "Risk Management"}))




# Control flow
if st.session_state.logged_in:
    show_dashboard()
else:
    show_login()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📢  Open your browser and visit: http://localhost:8501")
    print("="*60 + "\n")

