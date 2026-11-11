import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Focus OS — Smart To-Do",
    page_icon="⚡",
    layout="centered"
)

# Custom Clean Styling
st.markdown("""
    <style>
        .block-container { max-width: 680px; padding-top: 2rem; }
        .stCheckbox { margin-bottom: -10px; }
        .badge {
            background-color: #f1f5f9;
            color: #475569;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Draft the Q3 Product Proposal", "category": "highlight", "est": 90, "completed": False},
        {"id": 2, "title": "Refactor Auth middleware architecture", "category": "deep", "est": 60, "completed": False},
        {"id": 3, "title": "Send signed NDA back to Sarah", "category": "quick", "est": 2, "completed": True},
        {"id": 4, "title": "Inbox zero & archive stale threads", "category": "shallow", "est": 20, "completed": False},
        {"id": 5, "title": "Design feedback on Figma mocks", "category": "waiting", "est": None, "completed": False}
    ]

# Header & Metrics
today_str = datetime.now().strftime("%A, %B %d").upper()
st.caption(f"🗓️ {today_str}")
st.title("Today's Focus")

total_tasks = len(st.session_state.tasks)
completed_tasks = sum(1 for t in st.session_state.tasks if t["completed"])
progress = completed_tasks / total_tasks if total_tasks > 0 else 0.0

st.progress(progress)
st.caption(f"**{int(progress * 100)}% Completed** ({completed_tasks} of {total_tasks} tasks)")

st.write("---")

# Quick Input Form
with st.form("task_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        title = st.text_input("New Task", placeholder="What needs to get done?", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("Add Task", use_container_width=True)

    col3, col4 = st.columns([2, 1])
    with col3:
        cat_labels = {
            "highlight": "⭐ Must-Win Highlight",
            "deep": "⚡ Deep Work",
            "quick": "🚀 Quick Win (< 5m)",
            "shallow": "☕ Admin / Shallow",
            "waiting": "⏳ Waiting On"
        }
        category = st.selectbox("Category", options=list(cat_labels.keys()), format_func=lambda x: cat_labels[x], label_visibility="collapsed")
    with col4:
        est = st.number_input("Minutes", min_value=0, max_value=480, step=5, placeholder="Est. min", label_visibility="collapsed")

    if submitted and title.strip():
        new_task = {
            "id": int(datetime.now().timestamp() * 1000),
            "title": title.strip(),
            "category": category,
            "est": est if est > 0 else None,
            "completed": False
        }
        st.session_state.tasks.insert(0, new_task)
        st.rerun()

# Categories Renderer
categories = [
    ("⭐ Must-Win Highlight", "highlight"),
    ("⚡ Deep Work", "deep"),
    ("🚀 Quick Wins (< 5m)", "quick"),
    ("☕ Admin / Shallow", "shallow"),
    ("⏳ Waiting On / Blockers", "waiting")
]

for display_name, cat_key in categories:
    cat_tasks = [t for t in st.session_state.tasks if t["category"] == cat_key]
    
    st.markdown(f"##### {display_name}")
    
    if not cat_tasks:
        st.caption("No tasks here.")
    else:
        for t in cat_tasks:
            c1, c2, c3 = st.columns([0.8, 0.12, 0.08])
            
            # 1. Checkbox / Strike-through
            with c1:
                label = f"~~{t['title']}~~" if t["completed"] else t["title"]
                is_checked = st.checkbox(label, value=t["completed"], key=f"chk_{t['id']}")
                if is_checked != t["completed"]:
                    t["completed"] = is_checked
                    st.rerun()

            # 2. Estimate Badge
            with c2:
                if t["est"]:
                    st.markdown(f"<span class='badge'>{t['est']}m</span>", unsafe_allow_html=True)

            # 3. Delete Button
            with c3:
                if st.button("✕", key=f"del_{t['id']}", help="Delete task"):
                    st.session_state.tasks = [task for task in st.session_state.tasks if task["id"] != t["id"]]
                    st.rerun()
                    
    st.write("")