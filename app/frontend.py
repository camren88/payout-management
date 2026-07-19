import streamlit as st  # type: ignore[import]
import requests  # type: ignore[import]

st.set_page_config(
    page_title="Payout Management System",
    page_icon="💰",
    layout="wide"
)

st.title("💰 User Payout Management System")
st.write("Frontend for FastAPI Backend")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Dashboard",
        "Create User",
        "Create Sale",
        "Advance Payout",
        "Create Withdrawal",
        "Post Reconciliation"
    ]
)

if menu == "Create User":

    st.header("Create User")

    name = st.text_input("Username")

    email = st.text_input("Email")

    if st.button("Create"):

        try:
           with st.spinner("Creating user..."):

              response = requests.post(
                 "http://127.0.0.1:8000/users/",
                 json={
                   "username": name,
                   "email": email
              }
              )
              
              response.raise_for_status()

           st.success(response.json())

        except requests.exceptions.RequestException as e:
            st.error(str(e))


if menu == "Create Sale":

    st.header("Create Sale")

    user_id = st.number_input("User ID", step=1)
    
    brand =st.text_input("Brand Name")

    earning = st.number_input("Sale Amount")

    if st.button("Create Sale"):

        try:

            with st.spinner("Creating Sale..."):

               response = requests.post(
                   "http://127.0.0.1:8000/sales/",
                   json={
                       "user_id": int(user_id),
                       "brand": brand,
                       "earning": float(earning)
                  }
               )

               #response.raise_for_status() 
            if response.status_code != 200:
                st.error(response.json())   # <-- shows FastAPI's detailed error
            else:
                st.success(response.json())
 

            st.success(response.json())
        except requests.exceptions.RequestException as e:
            st.error(str(e))



if menu == "Dashboard":
    st.header("Dashboard")

    users = requests.get("http://127.0.0.1:8000/users/").json()
    sales = requests.get("http://127.0.0.1:8000/sales/").json()
    payouts = requests.get("http://127.0.0.1:8000/payouts/").json()
    withdrawals = requests.get("http://127.0.0.1:8000/withdrawals/").json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Users", len(users))
    col2.metric("Sales", len(sales))
    col3.metric("Payouts", len(payouts))
    col4.metric("Withdrawals", len(withdrawals))

    st.divider()

    st.subheader("Recent Users")
    st.dataframe(users)

    st.subheader("Recent Sales")
    st.dataframe(sales)


if menu == "Create Withdrawal":
    st.header("Create Withdrawal")
    

    user_id = st.number_input("User ID", step=1, key="withdraw_user")
    amount = st.number_input("Withdrawal Amount", min_value=0.0, key="withdraw_amount")

    if st.button("Create Withdrawal"):
        try:
            with st.spinner("Creating Withdrawal..."):
                response = requests.post(
                    "http://127.0.0.1:8000/withdrawals/",
                    json={
                        "user_id": user_id,
                        "amount": amount
                    }
                )
                response.raise_for_status()  
            st.success(response.json())
        except requests.exceptions.RequestException as e:
            # If a 422 or 500 error happens, this will catch it and print the details
            if response is not None and response.status_code != 200:
                st.error(f"Error {response.status_code}: {response.text}")
            else:
                st.error(str(e))

if menu == "Process Advances":
    st.header("Process Advance Payouts")
    st.info("This will automatically calculate a 10% advance for all eligible pending sales.")
    
    adv_user_id = st.text_input("User ID", key="adv_user")
    
    if st.button("Run Advance Job"):
        try:
            with st.spinner("Processing..."):
                # Hit the new endpoint we just made
                response = requests.post(f"http://127.0.0.1:8000/advances/process/{adv_user_id}")
                response.raise_for_status()
                
            data = response.json()
            st.success(data["message"])
            st.metric("Total Advance Processed", f"₹{data['total_advance']}")
            
        except requests.exceptions.RequestException as e:
            if response is not None and response.status_code != 200:
                st.error(f"Error {response.status_code}: {response.text}")
            else:
                st.error(str(e))  