import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gym Dashboard", layout="wide")

params = st.query_params
selected_tab = params.get("tab", "email")  # default to "email"
customer_name = params.get("customer", "")

if "action" in params:
    action = params["action"][0]
    customer = params.get("customer", [""])[0]
    st.title(f"{action.title()} Template for {customer}")
    st.markdown(f"Here you can show templates or forms for sending a {action.upper()} to {customer}.")
    st.stop()


def show_dashboard():
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

    # Sidebar
    st.sidebar.markdown("### Dashboard Navigation")

    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "Dashboard"

    # Tabs
    tabs = ["Dashboard", "Customers", "Risk Management"]

    for tab in tabs:
        button_style = "tab-button"
        if st.session_state.current_tab == tab:
            button_style += " tab-active"
        if st.sidebar.button(f"{tab}", key=tab):
            st.session_state.current_tab = tab

    page = st.session_state.current_tab

    if page == "Dashboard":
        st.markdown("<h1 style='font-size: 40px; font-weight: 700;'>Welcome, Gold's Gym!</h1>", unsafe_allow_html=True)

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

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div style='{card_style}'><h4>Total Members</h4><h2>124</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='{card_style}'><h4>At-Risk Members</h4><h2>19</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='{card_style}'><h4>Avg. CLV</h4><h2>$320</h2></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div style='{card_style}'><h4>Monthly Retention</h4><h2>87%</h2></div>", unsafe_allow_html=True)

        st.subheader("📊 Member Distribution by Package")
        st.info("Here's a breakdown of active members by membership type.")

        membership_counts = {
            "Basic": 30,
            "Premium": 70,
            "Starter": 25
        }

        df_chart = pd.DataFrame({
            "Membership Type": list(membership_counts.keys()),
            "Members": list(membership_counts.values())
        })

        df_chart.set_index("Membership Type", inplace=True)
        st.bar_chart(df_chart)

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

        col1, col2, col3 = st.columns(3)
        with col1:
            selected_membership = st.selectbox("Filter by Membership", ["All"] + sorted(df_customers["Membership"].unique()))
        with col2:
            selected_gender = st.selectbox("Filter by Gender", ["All"] + sorted(df_customers["Gender"].unique()))
        with col3:
            name_search = st.text_input("Search by Name")

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
            "Email": ["jane@gym.com"] * 10,
            "Last Visit": ["March 12 2025"] * 10,
            "Membership": ["Premium", "Premium", "Premium", "Premium", "Starter", "Starter", "Pro", "Pro", "Pro", "Starter"],
            "Reason why at Risk": ["x days inactive"] * 10
        }
        df = pd.DataFrame(data)

        col1, col2 = st.columns(2)
        with col1:
            selected_membership = st.selectbox("Filter by Membership Type", ["All"] + sorted(df["Membership"].unique()))
        with col2:
            search_name = st.text_input("Search by Name")

        if selected_membership != "All":
            df = df[df["Membership"] == selected_membership]
        if search_name:
            df = df[df["Name"].str.contains(search_name, case=False)]

        if "selected_email_row" not in st.session_state:
            st.session_state.selected_email_row = None

        header_cols = st.columns([1.8, 2.5, 2, 2, 1.5, 2])
        header_cols[0].markdown("**Name**")
        header_cols[1].markdown("**Email**")
        header_cols[2].markdown("**Last Visit**")
        header_cols[3].markdown("**Membership**")
        header_cols[4].markdown("**Action**")
        header_cols[5].markdown("**Reason why at Risk**")

        for index, row in df.iterrows():
            cols = st.columns([1.8, 2.5, 2, 2, 1.5, 2])
            cols[0].write(row["Name"])
            cols[1].markdown(f"[{row['Email']}](mailto:{row['Email']})")
            cols[2].write(row["Last Visit"])
            cols[3].write(row["Membership"])

            if cols[4].button("Send Email", key=f"email_btn_{index}"):
                st.session_state.selected_email_row = index
                st.rerun()

            cols[5].write(row["Reason why at Risk"])

            if st.session_state.selected_email_row == index:
                st.markdown("##### ✉️ Compose Email")
                subject = st.text_input("Subject", key=f"subject_{index}")
                message = st.text_area("Message", key=f"message_{index}")
                send_col, cancel_col = st.columns([0.15, 0.1])
                if send_col.button("Send", key=f"send_{index}"):
                    st.success(f"Email sent to {row['Name']} (simulated)")
                    st.session_state.selected_email_row = None
                    st.rerun()
                if cancel_col.button("Cancel", key=f"cancel_{index}"):
                    st.session_state.selected_email_row = None
                    st.rerun()


# Show the dashboard directly
show_dashboard()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Open your browser and visit: http://localhost:8501")
    print("="*60 + "\n")
