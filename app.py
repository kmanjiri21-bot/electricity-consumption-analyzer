
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Electricity Consumption Analyzer",
    page_icon="⚡",
    layout="wide"
)

if "usage" not in st.session_state:
    st.session_state.usage = []

if "appliances" not in st.session_state:
    st.session_state.appliances = []

st.title("⚡ Electricity Consumption Analyzer")
st.write("Monitor electricity usage, detect unusual consumption and save energy.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Appliance Tracker",
    "Waste Detector",
    "Saving Challenge"
])

# DASHBOARD
with tab1:
    st.header("Electricity Usage Dashboard")

    with st.form("usage_form"):
        date = st.date_input("Select date")
        units = st.number_input(
            "Electricity consumed (kWh)",
            min_value=0.0,
            step=0.5
        )
        submitted = st.form_submit_button("Add Usage")

    if submitted:
        st.session_state.usage.append({
            "Date": str(date),
            "Units": units
        })
        st.success("Electricity usage added!")

    if st.session_state.usage:
        df = pd.DataFrame(st.session_state.usage)
        df["Date"] = pd.to_datetime(df["Date"])

        total = df["Units"].sum()
        average = df["Units"].mean()

        c1, c2 = st.columns(2)
        c1.metric("Total Consumption", f"{total:.2f} kWh")
        c2.metric("Average Usage", f"{average:.2f} kWh")

        st.subheader("Daily Consumption")
        st.line_chart(df.set_index("Date")["Units"])

        df["Month"] = df["Date"].dt.strftime("%Y-%m")
        monthly = df.groupby("Month")["Units"].sum()

        st.subheader("Monthly Consumption")
        st.bar_chart(monthly)

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Usage Report",
            df.to_csv(index=False),
            "electricity_usage.csv",
            "text/csv"
        )
    else:
        st.info("Add your daily electricity usage to see the dashboard.")

# APPLIANCE TRACKER
with tab2:
    st.header("Appliance-wise Electricity Tracker")

    with st.form("appliance_form"):
        name = st.text_input("Appliance name")
        watts = st.number_input(
            "Power rating (Watts)",
            min_value=1,
            value=100
        )
        hours = st.number_input(
            "Hours used per day",
            min_value=0.0,
            max_value=24.0,
            value=2.0
        )
        added = st.form_submit_button("Add Appliance")

    if added:
        if name.strip():
            energy = watts * hours / 1000
            st.session_state.appliances.append({
                "Appliance": name,
                "Power (W)": watts,
                "Hours/day": hours,
                "Daily Energy (kWh)": energy
            })
            st.success("Appliance added!")
        else:
            st.warning("Please enter an appliance name.")

    if st.session_state.appliances:
        adf = pd.DataFrame(st.session_state.appliances)
        st.dataframe(adf, use_container_width=True)

        total_appliance = adf["Daily Energy (kWh)"].sum()
        st.metric("Estimated Daily Appliance Usage",
                  f"{total_appliance:.2f} kWh")

        st.bar_chart(adf.set_index("Appliance")["Daily Energy (kWh)"])

        st.download_button(
            "Download Appliance Report",
            adf.to_csv(index=False),
            "appliance_report.csv",
            "text/csv"
        )
    else:
        st.info("Add appliances to calculate their electricity usage.")

# WASTE DETECTOR
with tab3:
    st.header("Electricity Waste Detector")
    st.write("Find appliances with unusually high daily usage.")

    if st.session_state.appliances:
        adf = pd.DataFrame(st.session_state.appliances)

        limit = st.slider(
            "Daily usage alert limit (kWh)",
            min_value=0.5,
            max_value=20.0,
            value=3.0
        )

        for _, item in adf.iterrows():
            if item["Daily Energy (kWh)"] > limit:
                st.warning(
                    f"{item['Appliance']}: High usage of "
                    f"{item['Daily Energy (kWh)']:.2f} kWh/day. "
                    "Consider checking its usage."
                )
            else:
                st.success(
                    f"{item['Appliance']}: Usage is within the selected limit."
                )
    else:
        st.info("Add appliances in the Appliance Tracker first.")

# SAVING CHALLENGE
with tab4:
    st.header("Electricity Saving Challenge")
    st.write("Set a daily saving target and monitor your progress.")

    baseline = st.number_input(
        "Your usual daily consumption (kWh)",
        min_value=0.0,
        value=10.0
    )

    target = st.slider(
        "Target percentage reduction",
        min_value=5,
        max_value=50,
        value=10
    )

    goal = baseline * (1 - target / 100)

    st.metric("Your Daily Consumption Goal", f"{goal:.2f} kWh")

    actual = st.number_input(
        "Enter today's actual consumption (kWh)",
        min_value=0.0,
        value=0.0
    )

    if st.button("Check My Challenge"):
        saved = baseline - actual
        if baseline > 0 and actual <= goal:
            st.success(
                f"Congratulations! You reached your saving goal. "
                f"You saved {saved:.2f} kWh."
            )
        elif baseline > 0:
            st.warning(
                f"Keep trying! Your usage is {actual:.2f} kWh. "
                f"Your target is {goal:.2f} kWh."
            )
        else:
            st.info("Enter a usual daily consumption greater than zero.")

st.divider()
st.caption("Electricity Consumption Analyzer | Mini Project")

