
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Task Dashboard", layout="wide")

st.title("📋 Task Tracking Dashboard")

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar for adding a new task
st.sidebar.header("➕ Add New Task")
with st.sidebar.form("task_form"):
    name = st.text_input("Task Name")
    due_date = st.date_input("Due Date", value=datetime.today())
    status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    progress = st.slider("Progress (%)", 0, 100, 0)
    submitted = st.form_submit_button("Add Task")

    if submitted and name:
        st.session_state.tasks.append({
            "Task Name": name,
            "Due Date": due_date.strftime("%Y-%m-%d"),
            "Status": status,
            "Priority": priority,
            "Progress": progress
        })
        st.success("Task added successfully!")

# Display tasks
st.subheader("📌 Current Tasks")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    for i, row in df.iterrows():
        with st.expander(f"{row['Task Name']}"):
            st.write(f"**Due Date:** {row['Due Date']}")
            st.write(f"**Status:** {row['Status']}")
            st.write(f"**Priority:** {row['Priority']}")
            st.progress(row['Progress'])

            col1, col2 = st.columns(2)
            if col1.button("Edit", key=f"edit_{i}"):
                with st.form(f"edit_form_{i}"):
                    new_name = st.text_input("Task Name", value=row['Task Name'])
                    new_due_date = st.date_input("Due Date", value=datetime.strptime(row['Due Date'], "%Y-%m-%d"))
                    new_status = st.selectbox("Status", ["To Do", "In Progress", "Done"], index=["To Do", "In Progress", "Done"].index(row['Status']))
                    new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(row['Priority']))
                    new_progress = st.slider("Progress (%)", 0, 100, value=row['Progress'])
                    update = st.form_submit_button("Update Task")

                    if update:
                        st.session_state.tasks[i] = {
                            "Task Name": new_name,
                            "Due Date": new_due_date.strftime("%Y-%m-%d"),
                            "Status": new_status,
                            "Priority": new_priority,
                            "Progress": new_progress
                        }
                        st.success("Task updated successfully!")
                        st.experimental_rerun()

            if col2.button("Delete", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.success("Task deleted successfully!")
                st.experimental_rerun()
else:
    st.info("No tasks added yet. Use the sidebar to add a new task.")
