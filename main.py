import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime, timedelta


# ------------------------------
# Initialization and Sample Data
# ------------------------------

def init_session_state():
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("user_role", "employee")
    st.session_state.setdefault("checkins", [])
    st.session_state.setdefault("resources", [
        {"title": "Mindfulness Meditation Techniques", "category": "Mindfulness"},
        {"title": "Stress Management Strategies", "category": "Stress"},
        {"title": "Work-Life Balance Tips", "category": "Balance"},
        {"title": "Healthy Eating for Energy", "category": "Nutrition"},
        {"title": "Quick Breathing Exercises", "category": "Relaxation"}
    ])
    st.session_state.setdefault("coaches", [
        {"name": "Alice Johnson", "specialty": "Stress Management"},
        {"name": "Bob Smith", "specialty": "Mindfulness"},
        {"name": "Carol Lee", "specialty": "Work-Life Balance"}
    ])


init_session_state()


# ------------------------------
# Helper Functions
# ------------------------------

def save_checkin(mood, stress, comment):
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood,
        "stress": stress,
        "comment": comment
    }
    st.session_state["checkins"].append(new_entry)


def get_checkin_dataframe():
    if st.session_state["checkins"]:
        return pd.DataFrame(st.session_state["checkins"])
    else:
        return pd.DataFrame(columns=["date", "mood", "stress", "comment"])


def simulate_ai_recommendation(mood, stress):
    # Basic simulation: if mood is low or stress is high, recommend a resource
    if mood < 4 or stress > 7:
        return "We recommend checking out our Stress Management Strategies and scheduling a coaching session."
    elif mood < 6:
        return "Consider exploring mindfulness exercises to boost your mood."
    else:
        return "Great job! Keep up the good work and remember to take short breaks."


# ------------------------------
# Login Page
# ------------------------------

def login_page():
    st.title("WellBeing360 Login")
    st.write("Please enter your credentials to continue.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            # Simplified authentication logic
            st.session_state["logged_in"] = True
            # For demonstration, assume role based on username keyword
            if "hr" in username.lower():
                st.session_state["user_role"] = "hr_manager"
            else:
                st.session_state["user_role"] = "employee"
            st.experimental_rerun()
        else:
            st.error("Please enter both username and password.")


# ------------------------------
# Employee Dashboard
# ------------------------------

def employee_dashboard():
    st.title("Employee Dashboard - WellBeing360")
    st.write("Welcome to your personal wellness dashboard.")

    st.sidebar.markdown("### Navigation")
    view_option = st.sidebar.radio("Choose a section", ["Check-In", "Resources", "Coaching", "History"])

    if view_option == "Check-In":
        st.subheader("Wellness Check-In")
        mood = st.slider("How is your mood today?", 1, 10, 5, help="1 = Very Low, 10 = Excellent")
        stress = st.slider("How stressed are you today?", 1, 10, 5, help="1 = Not stressed, 10 = Extremely stressed")
        comment = st.text_area("Additional Comments (optional)")

        if st.button("Submit Check-In"):
            save_checkin(mood, stress, comment)
            recommendation = simulate_ai_recommendation(mood, stress)
            st.success("Your check-in has been submitted!")
            st.info(recommendation)

    elif view_option == "Resources":
        st.subheader("Resource Hub")
        category = st.selectbox("Filter by Category",
                                options=["All", "Mindfulness", "Stress", "Balance", "Nutrition", "Relaxation"])
        filtered_resources = [r for r in st.session_state["resources"] if
                              category == "All" or r["category"] == category]
        for resource in filtered_resources:
            st.markdown(f"- **{resource['title']}** ({resource['category']})")

    elif view_option == "Coaching":
        st.subheader("Mentorship & Coaching")
        st.write("Request a coaching session:")
        selected_coach = st.selectbox("Choose a Coach", [c["name"] for c in st.session_state["coaches"]])
        session_date = st.date_input("Select Session Date", datetime.now() + timedelta(days=1))
        session_time = st.time_input("Select Session Time", datetime.now().time())
        if st.button("Request Coaching Session"):
            st.success(
                f"Your coaching session with {selected_coach} is scheduled for {session_date} at {session_time}.")

    elif view_option == "History":
        st.subheader("Wellness Check-In History")
        df = get_checkin_dataframe()
        if not df.empty:
            st.dataframe(df)
            # Plot a simple line chart of mood over time
            df['date'] = pd.to_datetime(df['date'])
            chart = alt.Chart(df).mark_line(point=True).encode(
                x='date:T',
                y='mood:Q'
            ).properties(
                title="Mood Trend Over Time"
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No check-in data available yet.")


# ------------------------------
# HR Manager Dashboard
# ------------------------------

def hr_manager_dashboard():
    st.title("HR Manager Dashboard - WellBeing360")
    st.write("Overview of employee wellness across your organization.")

    # Simulated aggregated wellness metrics per department
    departments = {
        "Sales": {"avg_mood": 6.2, "avg_stress": 5.8, "num_entries": 25},
        "Engineering": {"avg_mood": 7.1, "avg_stress": 4.3, "num_entries": 30},
        "Marketing": {"avg_mood": 5.5, "avg_stress": 6.2, "num_entries": 20},
        "HR": {"avg_mood": 8.0, "avg_stress": 3.7, "num_entries": 15}
    }

    st.sidebar.markdown("### Navigation")
    view_option = st.sidebar.radio("Choose a section", ["Overview", "Detailed Reports"])

    if view_option == "Overview":
        st.subheader("Aggregated Wellness Metrics")
        data = []
        for dept, metrics in departments.items():
            data.append(
                {"Department": dept, "Average Mood": metrics["avg_mood"], "Average Stress": metrics["avg_stress"]})
        df_dept = pd.DataFrame(data)
        st.table(df_dept)

        st.subheader("Mood by Department")
        mood_chart = alt.Chart(df_dept).mark_bar().encode(
            x=alt.X("Department:N", sort=None),
            y="Average Mood:Q",
            color="Department:N"
        ).properties(
            width=600,
            height=300
        )
        st.altair_chart(mood_chart, use_container_width=True)

        st.subheader("Stress by Department")
        stress_chart = alt.Chart(df_dept).mark_bar().encode(
            x=alt.X("Department:N", sort=None),
            y="Average Stress:Q",
            color="Department:N"
        ).properties(
            width=600,
            height=300
        )
        st.altair_chart(stress_chart, use_container_width=True)

        st.write("Automated Alert: No departments with critical wellness issues at this time.")

    elif view_option == "Detailed Reports":
        st.subheader("Detailed Employee Wellness Report")
        df = get_checkin_dataframe()
        if not df.empty:
            st.write("Overall Check-In Data:")
            st.dataframe(df)
            st.subheader("Wellness Trends")
            chart = alt.Chart(df).mark_line(point=True).encode(
                x='date:T',
                y='mood:Q',
                color=alt.value('blue'),
                tooltip=['date:T', 'mood:Q', 'stress:Q']
            ).properties(
                title="Mood Trend Over Time"
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No check-in data available for detailed reports.")


# ------------------------------
# Main Function and Navigation
# ------------------------------

def main():
    if not st.session_state["logged_in"]:
        login_page()
    else:
        st.sidebar.title("WellBeing360")
        role = st.sidebar.radio("Select Role", ("Employee", "HR Manager"))
        st.session_state["user_role"] = role.lower().replace(" ", "_")
        if st.session_state["user_role"] == "employee":
            employee_dashboard()
        elif st.session_state["user_role"] == "hr_manager":
            hr_manager_dashboard()


if __name__ == '__main__':
    main()
