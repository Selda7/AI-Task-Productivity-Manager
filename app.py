import streamlit as st
import pandas as pd
import csv
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# ==================================
# Streamlit UI
# ==================================

st.set_page_config(page_title="AI Task Manager", layout="centered")
st.markdown("### AI Task Productivity Manager")
st.title("Manage your tasks, Analyze productivity.")
st.sidebar.title("🧭 Navigation")
menu = st.sidebar.radio(
    "",
    ["Add Task", "View Tasks", "Analytics", "Predict Productivity"]
)

# ==================================
# load CSS
# ==================================

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==================================
# Core Logic Functions
# ==================================

def init_tasks_file():
    if not os.path.exists("tasks.csv"):
        df = pd.DataFrame(columns=["Task Name", "Date", "Type", "Duration", "Status"])
        df.to_csv("tasks.csv", index=False)
init_tasks_file()

def add_task(name, date, task_type, duration):
    with open("tasks.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, date, task_type, duration, "Pending"])


def load_tasks():
    return pd.read_csv("tasks.csv")


def mark_task_done(task_index):
    df = pd.read_csv("tasks.csv")
    df.loc[task_index, "Status"] = "Done"
    df.to_csv("tasks.csv", index=False)


def convert_duration(duration):
    if not isinstance(duration, str):
        return 0
    duration = duration.lower()
    try:
        if "hour" in duration:
            return float(duration.split()[0]) * 60
        elif "minute" in duration:
            return float(duration.split()[0])
        else:
            return 0
    except:
        return 0


def retrain_model():
    df = pd.read_csv("tasks.csv")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    df["Day"] = df["Date"].dt.day_name()
    df["Duration_minutes"] = df["Duration"].apply(convert_duration)
    df["Productive"] = df["Duration_minutes"] >= 60

    le_day = LabelEncoder()
    le_type = LabelEncoder()

    df["Day_encoded"] = le_day.fit_transform(df["Day"])
    df["Type_encoded"] = le_type.fit_transform(df["Type"])

    X = df[["Day_encoded", "Type_encoded"]]
    y = df["Productive"]

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    return model, le_day, le_type

# ==================================
# Add Task
# ==================================

if menu == "Add Task":
    st.markdown("""
    <div class="ai-card">
        <h3>➕ Add New Task</h3>
        <p>Create a task and let AI learn from your productivity</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("📝 Task name")
            task_type = st.text_input("🏷 Task type")

        with col2:
            date = st.date_input("📅 Task date")
            duration = st.text_input("⏱ Duration (e.g. 30 minutes / 2 hours)")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Add Task"):
           if name.strip() == "" or task_type.strip() == "" or duration.strip() == "":
                st.warning("Please fill all fields")
           else:
              add_task(name, str(date), task_type, duration)
              retrain_model()
              st.success("Task added & AI updated ")

# ==================================
# View Tasks
# ==================================

elif menu == "View Tasks":
    st.header("📋 Your Tasks")

    df = load_tasks()
    total_tasks = len(df)
    done_tasks = len(df[df["Status"] == "Done"])
    pending_tasks = len(df[df["Status"] == "Pending"])

    progress = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Total Tasks</h4>
            <h2>{total_tasks}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Completed</h4>
            <h2>{done_tasks}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Pending</h4>
            <h2>{pending_tasks}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <h4>Progress</h4>
            <h2>{progress}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if df.empty:
        st.info("No tasks yet")
    else:
        for idx, row in df.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

                with col1:
                    st.markdown(f"📝 {row['Task Name']}")

                with col2:
                    st.markdown(f"📅 {row['Date']}")

                with col3:
                    st.markdown(f"🏷 {row['Type']}")

                with col4:
                    if row["Status"] == "Done":
                        st.success("Done")
                    else:
                        st.warning("Pending")

                with col5:
                    if row["Status"] == "Pending":
                        if st.button("✔️", key=f"done_{idx}"):
                            mark_task_done(idx)
                            
# ==================================
# Analytics
# ==================================

elif menu == "Analytics":

    st.markdown("""
    <div class="analytics-header">
        <h1>📊 Productivity Analytics</h1>
    <p>
        Understand your work patterns and improve your productivity using data insights.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_tasks()
    if df.empty:
        st.info("No analytics data yet")
    st.subheader("Most Active Days")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Day"] = df["Date"].dt.day_name()

    day_activity = df["Day"].value_counts()
    st.caption("Shows which days you complete the most tasks, helping you identify your peak productivity days.")

    day_activity = df["Day"].value_counts()
    st.bar_chart(day_activity)
    st.subheader("Focus Areas")
    st.caption("Displays how your tasks are distributed across different categories to understand where your time goes.")

    type_focus = df["Type"].value_counts()
    st.bar_chart(type_focus)
    st.subheader("Average Task Duration by Type")
    st.caption("Compares the average time spent on each task type to highlight which activities consume more time.")

    df["Duration_minutes"] = df["Duration"].apply(convert_duration)
    avg_duration = df.groupby("Type")["Duration_minutes"].mean()
    st.bar_chart(avg_duration)

# ==================================
# Predict Productivity
# ==================================

elif menu == "Predict Productivity":
    st.markdown("""
    <div class="predict-card">
        <h3> Productivity Prediction</h3>
        <p>Let AI estimate whether this task will be productive</p>
    </div>
    """, unsafe_allow_html=True)

    model, le_day, le_type = retrain_model()

    col1, col2 = st.columns(2)

    with col1:
        day = st.selectbox("📅 Select Day", le_day.classes_)

    with col2:
        task_type = st.selectbox("🏷 Select Task Type", le_type.classes_)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Predict Productivity"):
        day_encoded = le_day.transform([day])[0]
        type_encoded = le_type.transform([task_type])[0]

        prediction = model.predict([[day_encoded, type_encoded]])

        if prediction[0]:
            st.success("✅ This task is likely to be productive")
        else:
            st.warning("⚠️ This task may be less productive")
