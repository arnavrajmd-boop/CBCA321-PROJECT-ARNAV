import streamlit as st
import plotly.express as px
import pandas as pd

from core.git_analyzer import (
    analyze_repository,
    filter_by_developer,
    get_developer_list,
    get_developer_stats,
)

st.set_page_config(
    page_title="Developer Contribution Visualizer",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Developer Contribution Visualizer")
st.caption("CBCA321 Project #6 • Assessment 3: Developer Contribution Analysis & Filtering")

# Sidebar: Repository path input and configuration
with st.sidebar:
    st.header("⚙️ Repository Settings")
    repo_path_input = st.text_input(
        "Local Git repository path",
        value=st.session_state.get("analyzed_path", ""),
        placeholder="e.g. D:\\CLOUD PRO\\CBCA321-PROJECT-ARNAV",
        help="Enter the path of any readable local Git repository on your system.",
    )
    col_analyze, col_reset = st.columns([2, 1])
    with col_analyze:
        analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)
    with col_reset:
        reset_clicked = st.button("Reset", use_container_width=True)

if reset_clicked:
    st.session_state.pop("result", None)
    st.session_state.pop("analyzed_path", None)
    st.session_state.pop("analysis_error", None)
    st.rerun()

if analyze_clicked:
    if not repo_path_input or not repo_path_input.strip():
        st.session_state["analysis_error"] = "Please enter a valid Git repository directory path."
        st.session_state.pop("result", None)
    else:
        try:
            analyzed = analyze_repository(repo_path_input.strip())
            st.session_state["result"] = analyzed
            st.session_state["analyzed_path"] = repo_path_input.strip()
            st.session_state.pop("analysis_error", None)
        except ValueError as exc:
            st.session_state["analysis_error"] = str(exc)
            st.session_state.pop("result", None)
        except Exception as exc:
            st.session_state["analysis_error"] = f"An unexpected error occurred: {exc}"
            st.session_state.pop("result", None)

# Display error if any occurred during analysis
if st.session_state.get("analysis_error"):
    st.error(f"❌ {st.session_state['analysis_error']}")

raw_result = st.session_state.get("result")

if raw_result is None:
    st.info("ℹ️ Enter a local Git repository path in the sidebar and click **Analyze**.")
    st.markdown(
        """
        ### What this dashboard provides:
        - **Repository Validation**: Verifies local Git folders and inspects commit history.
        - **Aggregated Contributions**: Commits, changed files, insertions, and deletions across all authors.
        - **Developer Filtering**: Isolate any individual contributor to review their specific impact, activity timeline, and commits.
        - **Interactive Visualizations**: High-contrast charts for commit distribution and chronological project velocity.
        """
    )
    st.stop()

if raw_result.commits.empty:
    st.warning("⚠️ The repository is valid, but contains no commits to analyze.")
    st.stop()

# Contributor Filter in Sidebar
developer_names = get_developer_list(raw_result)
filter_options = ["All developers"] + developer_names

with st.sidebar:
    st.markdown("---")
    st.header("👤 Contributor Filter")
    selected_developer = st.selectbox(
        "Select Contributor",
        options=filter_options,
        index=0,
        help="Choose a specific contributor to filter all metrics, charts, and tables.",
    )
    st.markdown("---")
    st.markdown(f"**Repository:** `{st.session_state.get('analyzed_path', '')}`")
    st.markdown(f"**Total Contributors:** `{len(developer_names)}`")
    st.markdown(f"**Total Commits:** `{len(raw_result.commits):,}`")

# Apply filtering
is_filtered = (selected_developer != "All developers")
filtered_result = filter_by_developer(raw_result, selected_developer)
stats = get_developer_stats(raw_result, selected_developer)
total_repo_commits = len(raw_result.commits)

# Filter Status Banner
if is_filtered:
    share_pct = (stats["commits"] / total_repo_commits * 100) if total_repo_commits > 0 else 0
    st.success(
        f"🎯 **Filtered Contributor:** **{selected_developer}** | "
        f"**{stats['commits']}** of **{total_repo_commits}** commits ({share_pct:.1f}% share) | "
        f"Active Days: **{stats['active_days']}** | "
        f"Period: **{stats['first_commit_date']}** to **{stats['last_commit_date']}**"
    )
else:
    st.info(f"📊 Showing overall repository metrics across all **{len(developer_names)}** contributors.")

# KPI Metric Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    label="Total Commits",
    value=f"{stats['commits']:,}",
    delta=f"{stats['commits']/total_repo_commits*100:.1f}% of repo" if is_filtered else f"{len(developer_names)} authors",
)
c2.metric(
    label="Lines Added",
    value=f"+{stats['additions']:,}",
    delta=f"Net: {stats['net_lines']:+,} lines" if is_filtered else None,
)
c3.metric(
    label="Lines Deleted",
    value=f"-{stats['deletions']:,}",
    delta="- deletions" if is_filtered else None,
    delta_color="inverse",
)
c4.metric(
    label="Files Changed",
    value=f"{stats['files_changed']:,}",
    delta=f"{stats['active_days']} active day(s)" if is_filtered else None,
)

st.markdown("---")

# Charts Section
col_chart_left, col_chart_right = st.columns(2)

with col_chart_left:
    if is_filtered:
        st.subheader(f"Code Impact: {selected_developer}")
        df_impact = pd.DataFrame({
            "Metric": ["Lines Added", "Lines Deleted"],
            "Lines": [stats["additions"], stats["deletions"]],
        })
        fig_impact = px.bar(
            df_impact,
            x="Metric",
            y="Lines",
            text="Lines",
            color="Metric",
            color_discrete_map={"Lines Added": "#10b981", "Lines Deleted": "#ef4444"},
        )
        fig_impact.update_traces(textposition="outside")
        fig_impact.update_layout(showlegend=False, yaxis_title="Line Count", height=380)
        st.plotly_chart(fig_impact, use_container_width=True)
    else:
        st.subheader("Commits by Developer")
        fig_devs = px.bar(
            raw_result.developer_summary,
            x="author",
            y="commits",
            text="commits",
            labels={"author": "Contributor", "commits": "Commits"},
            color="commits",
            color_continuous_scale="Blues",
        )
        fig_devs.update_traces(textposition="outside")
        fig_devs.update_layout(
            xaxis_tickangle=-35,
            xaxis_title="Contributor",
            yaxis_title="Commits",
            height=380,
            showlegend=False,
        )
        st.plotly_chart(fig_devs, use_container_width=True)

with col_chart_right:
    st.subheader(f"Activity Over Time {'— ' + selected_developer if is_filtered else ''}")
    if filtered_result.activity.empty:
        st.info("No activity recorded for the selected timeline.")
    else:
        fig_activity = px.line(
            filtered_result.activity,
            x="date",
            y=["commits", "additions", "deletions"],
            markers=True,
            labels={"value": "Count", "variable": "Metric", "date": "Date"},
            color_discrete_map={
                "commits": "#3b82f6",
                "additions": "#10b981",
                "deletions": "#ef4444",
            },
        )
        fig_activity.update_layout(
            height=380,
            yaxis_title="Count",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_activity, use_container_width=True)

st.markdown("---")

# Data Tables Section
st.subheader(f"📋 Contribution Summary Table {'— ' + selected_developer if is_filtered else ''}")
df_display_summary = filtered_result.developer_summary.copy()
df_display_summary.columns = ["Contributor", "Commits", "Files Changed", "Lines Added", "Lines Deleted"]
st.dataframe(df_display_summary, use_container_width=True, hide_index=True)

st.subheader(f"📝 Commit Details Table {'— ' + selected_developer if is_filtered else ''}")
st.caption(f"Showing {len(filtered_result.commits)} commit(s)")

df_display_commits = filtered_result.commits.copy().sort_values("date", ascending=False)
if pd.api.types.is_datetime64_any_dtype(df_display_commits["date"]):
    df_display_commits["date"] = df_display_commits["date"].dt.strftime("%Y-%m-%d")

df_display_commits.columns = [
    "Commit SHA",
    "Author",
    "Date",
    "Commit Message",
    "Files Changed",
    "Lines Added",
    "Lines Deleted",
]
st.dataframe(df_display_commits, use_container_width=True, hide_index=True)
