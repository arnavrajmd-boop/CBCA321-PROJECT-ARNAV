import streamlit as st
import plotly.express as px

from core.git_analyzer import analyze_repository, filter_by_developer

st.set_page_config(page_title="Developer Contribution Visualizer", page_icon="📊", layout="wide")
st.title("📊 Developer Contribution Visualizer")
st.caption("CBCA321 Project #6 • Git history analysis")

with st.sidebar:
    st.header("Repository")
    repo_path = st.text_input("Local Git repository path")
    analyze = st.button("Analyze Repository", type="primary", use_container_width=True)

if analyze:
    try:
        st.session_state["result"] = analyze_repository(repo_path)
    except ValueError as exc:
        st.error(str(exc))

result = st.session_state.get("result")
if result is None:
    st.info("Enter a local Git repository path and click Analyze Repository.")
    st.stop()

if result.commits.empty:
    st.warning("No commits were found.")
    st.stop()

developers = ["All developers"] + sorted(result.commits["author"].unique().tolist())
selected = st.sidebar.selectbox("Developer filter", developers)
result = filter_by_developer(result, selected)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Commits", f"{len(result.commits):,}")
c2.metric("Lines Added", f"{int(result.commits['additions'].sum()):,}")
c3.metric("Lines Deleted", f"{int(result.commits['deletions'].sum()):,}")
c4.metric("Files Changed", f"{int(result.commits['files_changed'].sum()):,}")

left, right = st.columns(2)

with left:
    st.subheader("Commits by Developer")
    fig = px.bar(result.developer_summary, x="author", y="commits")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Activity Over Time")
    fig = px.line(
        result.activity,
        x="date",
        y=["commits","additions","deletions"],
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Contribution Summary")
st.dataframe(result.developer_summary, use_container_width=True, hide_index=True)

st.subheader("Commit Details")
st.dataframe(
    result.commits.sort_values("date", ascending=False),
    use_container_width=True,
    hide_index=True
)
