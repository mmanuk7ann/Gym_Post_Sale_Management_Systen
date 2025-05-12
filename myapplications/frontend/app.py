import streamlit as st
import pandas as pd


st.set_page_config(page_title="Gym Dashboard", layout="wide")

import requests


API_BASE_URL = "http://api:8000"
GYM_ID = 3# You can make this dynamic later if needed


def fetch_total_members():
   try:
       res = requests.get(f"{API_BASE_URL}/gyms/gym/members-count?gym_id={GYM_ID}")
       return res.json().get("total_members", 0) if res.status_code == 200 else 0
   except:
       return 0
   
def fetch_last_week_visits():
    try:
        res = requests.get(f"{API_BASE_URL}/gyms/gym/last_week_visits?gym_id={GYM_ID}")
        return res.json() if res.status_code == 200 else 0
    except:
        return 0



def fetch_risk_members():
   try:
       res = requests.get(f"{API_BASE_URL}/gyms/gym/risk-count?gym_id={GYM_ID}")
       return res.json() if res.status_code == 200 else 0
   except:
       return 0


def fetch_average_clv():
   try:
       res = requests.get(f"{API_BASE_URL}/gyms/gym/average-clv?gym_id={GYM_ID}")
       return res.json().get("average_clv", 0) if res.status_code == 200 else 0
   except:
       return 0


# def fetch_retention_rate():
#    try:
#        res = requests.get(f"{API_BASE_URL}/gyms/gym/retention-rate?gym_id={GYM_ID}")
#        return f"{res.json()}%" if res.status_code == 200 else "N/A"
#    except:
#        return "N/A"
  
def fetch_customers_by_package():
    try:
        res = requests.get(f"{API_BASE_URL}/gyms/gym/customers-by-package?gym_id={GYM_ID}")
        if res.status_code == 200:
            return res.json()  # <-- just return res.json(), no .get() anymore
        else:
            st.error(f"Failed to fetch package data. Status code: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"API error: {e}")
        return []

  
def fetch_customers():
   try:
       res = requests.get(f"{API_BASE_URL}/customers/customer/all?gym_id={GYM_ID}")
       if res.status_code == 200:
           return res.json()  # List of customers
       else:
           st.error(f"Failed to fetch customers. Status code: {res.status_code}")
           return []
   except Exception as e:
       st.error(f"API error: {e}")
       return []

#email button endpoint
def send_customer_email(to_email, subject_text, message_text):
    payload = {
        "email": to_email,
        "subject_text": subject_text,
        "text": message_text
    }
    try:
        res = requests.post(f"{API_BASE_URL}/email/send", json=payload)
        if res.status_code == 200:
            return True
        else:
            st.error(f"Failed to send email. Status code: {res.status_code}")
            return False
    except Exception as e:
        st.error(f"API error: {e}")
        return False

  
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
       total_members = fetch_total_members()
       at_risk_members = fetch_risk_members()
       avg_clv = fetch_average_clv()
       last_week_visits = fetch_last_week_visits()
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
           st.markdown(f"<div style='{card_style}'><h4>Total Members</h4><h2>{total_members}</h2></div>", unsafe_allow_html=True)
       with col2:
           st.markdown(f"<div style='{card_style}'><h4>At-Risk Members</h4><h2>{at_risk_members}</h2></div>", unsafe_allow_html=True)
       with col3:
           st.markdown(f"<div style='{card_style}'><h4>Avg. CLV</h4><h2>${avg_clv}</h2></div>", unsafe_allow_html=True)
       with col4:
           st.markdown(f"<div style='{card_style}'><h4>Last Week Visits</h4><h2>{last_week_visits}</h2></div>", unsafe_allow_html=True)


       st.subheader("📊 Member Distribution by Package")
       st.info("Here's a breakdown of active members by membership type.")


       # Fetch real data
       packages_data = fetch_customers_by_package()


       # Prepare data for bar chart
       if packages_data:
           membership_counts = {pkg["package_name"]: pkg["customer_count"] for pkg in packages_data}


           df_chart = pd.DataFrame({
               "Membership Type": list(membership_counts.keys()),
               "Members": list(membership_counts.values())
           })


           df_chart.set_index("Membership Type", inplace=True)
           st.bar_chart(df_chart)
       else:
           st.warning("No membership data available.")



#CUSTOMERS PAGE

   elif page == "Customers":
       st.title("👥 Customers")


       customers = fetch_customers()

       if customers:
           # Prepare the DataFrame
           df_customers = pd.DataFrame(customers)


           # Rename columns to match your UI
           df_customers.rename(columns={
               "name": "Name",
               "email": "Email",
               "phone": "Phone",
               "membership": "Membership",
               "gender": "Gender"
           }, inplace=True)


           col1, col2, col3 = st.columns(3)
           with col1:
               selected_membership = st.selectbox("Filter by Membership", ["All"] + sorted(df_customers["Membership"].dropna().unique()))
           with col2:
               selected_gender = st.selectbox("Filter by Gender", ["All"] + sorted(df_customers["Gender"].dropna().unique()))
           with col3:
               name_search = st.text_input("Search by Name")


           if selected_membership != "All":
               df_customers = df_customers[df_customers["Membership"] == selected_membership]
           if selected_gender != "All":
               df_customers = df_customers[df_customers["Gender"] == selected_gender]
           if name_search:
               df_customers = df_customers[df_customers["Name"].str.contains(name_search, case=False)]

           df_customers.index = df_customers.index + 1
           
           st.dataframe(df_customers, use_container_width=True)
       else:
           st.warning("No customers to display.")


       #
##RISK MANAGEMENT
   #
   elif page == "Risk Management":
    st.title("📉 At-Risk Customers")

    # Fetch real data from API
    def fetch_risk_customers():
        try:
            res = requests.get(f"{API_BASE_URL}/customers/customer/risk?gym_id={GYM_ID}")
            if res.status_code == 200:
                return res.json()
            else:
                st.error(f"Failed to fetch risk customers. Status code: {res.status_code}")
                return []
        except Exception as e:
            st.error(f"API error: {e}")
            return []


    risk_customers = fetch_risk_customers()

    if risk_customers:
        # Prepare the DataFrame
        df = pd.DataFrame([
            {
                "Name": customer["name"],
                "Email": customer["email"],
                "Last Visit": pd.to_datetime(customer["last_visit"]).strftime("%B %d %Y"),  # format nicely
                "Membership": customer["membership"],
                # "Reason why at Risk": customer["reason"]
                "Reason why at Risk": f"{customer['inactive_days']} days inactive"

            }
            for customer in risk_customers
        ])

        col1, col2 = st.columns(2)
        with col1:
            selected_membership = st.selectbox("Filter by Membership Type", ["All"] + sorted(df["Membership"].dropna().unique()))
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
                    success = send_customer_email(
                        to_email=row['Email'],
                        subject_text=subject,
                        message_text=message
                    )
                    if success:
                        st.success(f"Email sent to {row['Name']}")
                        st.session_state.selected_email_row = None
                        st.rerun()

                if cancel_col.button("Cancel", key=f"cancel_{index}"):
                    st.session_state.selected_email_row = None
                    st.rerun()

    else:
        st.warning("No at-risk customers to display.")



# Show the dashboard directly
show_dashboard()


if __name__ == "__main__":
   print("\n" + "="*60)
   print("Open your browser and visit: http://localhost:8501")
   print("="*60 + "\n")
