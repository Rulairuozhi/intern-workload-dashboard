"""
Intern Weekly Workload Dashboard
A lightweight web app for monitoring departmental intern workload analytics.
Built with Streamlit + Pandas + Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Intern Workload Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Visual theme
ACCENT = "#7B61FF"
ACCENT_DARK = "#5B43D6"
ACCENT_SOFT = "#EEEAFE"
BLUE = "#3B82F6"
BLUE_DARK = "#1D4ED8"
BLUE_SOFT = "#DBEAFE"
BG = "#FAF9FF"
TEXT = "#20212A"
MUTED = "#6B6F80"
BORDER = "#ECEAF5"
DANGER = "#E5484D"
DANGER_DARK = "#B4232A"
DANGER_SOFT = "#FFE8EC"
SUCCESS = "#2DBE9F"
SUCCESS_SOFT = "#DDF7F1"
AMBER = "#F5B84B"
AMBER_DARK = "#D97706"

# Custom CSS for a clean dashboard UI
st.markdown("""
    <style>
    :root {
        --accent: #7B61FF;
        --accent-soft: #EEEAFE;
        --bg: #FAF9FF;
        --text: #20212A;
        --muted: #6B6F80;
        --border: #ECEAF5;
    }

    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(123, 97, 255, 0.08), transparent 34rem),
            linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2.8rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.92);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: var(--text);
        letter-spacing: 0;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(236, 234, 245, 0.95);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.94);
        box-shadow: 0 18px 42px rgba(35, 31, 64, 0.07);
        padding: 1.05rem 1.1rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid rgba(236, 234, 245, 0.95);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        box-shadow: 0 14px 32px rgba(35, 31, 64, 0.06);
    }

    div[data-testid="stMetricLabel"] p {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text);
        font-weight: 800;
        overflow: visible;
        text-overflow: clip;
        white-space: nowrap;
        font-size: clamp(1.35rem, 2vw, 2rem);
    }

    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid rgba(236, 234, 245, 0.95);
        border-radius: 18px;
        box-shadow: 0 18px 42px rgba(35, 31, 64, 0.07);
        padding: 0.65rem 0.75rem 0.25rem 0.75rem;
        overflow: hidden !important;
    }

    div[data-testid="stPlotlyChart"] > div,
    div[data-testid="stPlotlyChart"] iframe,
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container {
        overflow: hidden !important;
        scrollbar-width: none;
    }

    div[data-testid="stPlotlyChart"] > div::-webkit-scrollbar,
    div[data-testid="stPlotlyChart"] iframe::-webkit-scrollbar,
    div[data-testid="stPlotlyChart"] .js-plotly-plot::-webkit-scrollbar,
    div[data-testid="stPlotlyChart"] .plot-container::-webkit-scrollbar {
        display: none;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.45rem;
        background: #F3F1FA;
        border-radius: 999px;
        padding: 0.28rem;
        width: fit-content;
    }

    .stTabs [data-baseweb="tab"] {
        height: 2.25rem;
        border-radius: 999px;
        padding: 0 1rem;
        color: var(--muted);
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent);
        color: white;
    }

    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: var(--accent);
        box-shadow: 0 0 0 5px rgba(123, 97, 255, 0.13);
    }

    .stSlider [data-testid="stTickBar"] {
        display: none;
    }

    .section-gap {
        height: 1.1rem;
    }

    .header-title {
        display: block;
        color: var(--text);
        font-size: 2.65rem;
        line-height: 1.22;
        font-weight: 800;
        letter-spacing: 0;
        margin-bottom: 0.35rem;
        padding-top: 0.2rem;
        padding-bottom: 0.15rem;
        min-height: 3.4rem;
        overflow: visible;
    }

    .header-subtitle {
        color: var(--muted);
        font-size: 1.02rem;
        margin-bottom: 1.3rem;
    }

    h2, h3 {
        color: var(--text);
        letter-spacing: 0;
    }

    hr {
        border-color: transparent;
        margin: 0.6rem 0 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

@st.cache_data
def process_excel_data(uploaded_file):
    """
    Process Excel file from wide to long format and add Status field.
    """
    try:
        file_name = getattr(uploaded_file, "name", "").lower()
        if file_name.endswith(".xls"):
            engines = ["calamine", "xlrd", "openpyxl"]
        else:
            engines = ["calamine", "openpyxl", "xlrd"]
        read_errors = []
        raw_df = None

        for engine in engines:
            try:
                uploaded_file.seek(0)
                raw_df = pd.read_excel(uploaded_file, engine=engine)
                break
            except Exception as read_error:
                read_errors.append(f"{engine}: {read_error}")

        if raw_df is None:
            raise ValueError(
                "Could not read this Excel file. "
                "Please save it again as .xlsx and upload it. "
                f"Reader errors: {' | '.join(read_errors)}"
            )

        raw_df.columns = [str(col).strip() for col in raw_df.columns]
        
        # Validate required columns
        required_cols = ['Week', 'Date']
        if not all(col in raw_df.columns for col in required_cols):
            available_cols = ", ".join(raw_df.columns.astype(str))
            raise ValueError(
                f"Excel must contain columns: {required_cols}. "
                f"Found columns: {available_cols}"
            )
        
        # Define department columns
        dept_cols = ['PPM1', 'DP', 'PPM2', 'STA', 'PEH', 'IP1', 'IP2']
        available_depts = [col for col in dept_cols if col in raw_df.columns]
        
        if not available_depts:
            available_depts = [
                col for col in raw_df.columns
                if col not in required_cols and not col.startswith("Unnamed")
            ]

        if not available_depts:
            raise ValueError("Excel must contain at least one department column")
        
        # Convert wide to long format
        df_long = raw_df.melt(
            id_vars=['Week', 'Date'],
            value_vars=available_depts,
            var_name='Department',
            value_name='Hours'
        )
        
        # Convert Hours to numeric
        df_long['Hours'] = pd.to_numeric(df_long['Hours'], errors='coerce')
        
        # Add Status column
        df_long['Status'] = df_long['Hours'].apply(
            lambda x: 'Busy' if x > 32 else 'Normal' if pd.notna(x) else 'N/A'
        )
        
        # Remove NaN hours
        df_long = df_long.dropna(subset=['Hours'])
        df_long['Week'] = pd.to_numeric(df_long['Week'], errors='ignore')
        
        return df_long.reset_index(drop=True)
        
    except Exception as e:
        raise ValueError(f"Error processing Excel file: {str(e)}")


def calculate_kpi_metrics(df):
    """Calculate KPI metrics."""
    total_hours = df['Hours'].sum()
    avg_hours = df['Hours'].mean()
    busy_count = len(df[df['Status'] == 'Busy'])
    peak_week = df.groupby('Week')['Hours'].sum().idxmax() if len(df) > 0 else 'N/A'
    
    return {
        'total_hours': round(total_hours, 1),
        'avg_hours': round(avg_hours, 1),
        'busy_count': busy_count,
        'peak_week': peak_week
    }


def generate_insights(df):
    """Generate automatic insights."""
    insights = {}
    
    dept_avg = df.groupby('Department')['Hours'].mean()
    insights['busiest_dept'] = dept_avg.idxmax()
    insights['busiest_avg'] = round(dept_avg.max(), 1)
    
    dept_std = df.groupby('Department')['Hours'].std().dropna()
    if dept_std.empty:
        insights['most_volatile'] = 'N/A'
        insights['volatility_std'] = 0
    else:
        insights['most_volatile'] = dept_std.idxmax()
        insights['volatility_std'] = round(dept_std.max(), 1)
    
    week_total = df.groupby('Week')['Hours'].sum()
    insights['busiest_week'] = week_total.idxmax()
    insights['busiest_week_hours'] = round(week_total.max(), 1)
    
    total_records = len(df)
    busy_records = len(df[df['Status'] == 'Busy'])
    insights['busy_percentage'] = round((busy_records / total_records * 100) if total_records > 0 else 0, 1)
    
    return insights


def style_chart(fig, height, show_legend=None, top_margin=58, bottom_margin=38):
    """Apply the shared lightweight dashboard chart style."""
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, Segoe UI, Arial, sans-serif', color=TEXT, size=12),
        title=dict(font=dict(size=16, color=TEXT, family='Inter, Segoe UI, Arial, sans-serif')),
        margin=dict(l=18, r=18, t=top_margin, b=bottom_margin),
        hoverlabel=dict(bgcolor='white', bordercolor=BORDER, font=dict(color=TEXT)),
    )
    fig.update_xaxes(
        gridcolor='#F0EEF8',
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
        zeroline=False
    )
    fig.update_yaxes(
        gridcolor='#F0EEF8',
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
        zeroline=False
    )
    if show_legend is not None:
        fig.update_layout(showlegend=show_legend)
    return fig


def format_week(value):
    """Render week values compactly for metric cards and labels."""
    if isinstance(value, (int, np.integer)):
        return str(value)
    if isinstance(value, (float, np.floating)) and value.is_integer():
        return str(int(value))
    return str(value)


# ============================================================================
# MAIN APP
# ============================================================================

st.markdown('<div class="header-title">Intern Workload Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">A compact view of weekly workload, pressure points, and department-level capacity.</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("Settings")
    
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=['xlsx', 'xls'],
        help="Upload your Excel file with Week, Date, and department columns"
    )
    
    if uploaded_file:
        try:
            df = process_excel_data(uploaded_file)
            st.success("File processed successfully")
            
            st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
            all_departments = sorted(df['Department'].unique())
            selected_depts = st.multiselect(
                "Select Departments",
                all_departments,
                default=[],
                placeholder="All departments"
            )
            if not selected_depts:
                selected_depts = all_departments
            
            all_weeks = sorted(df['Week'].unique())
            selected_weeks = st.multiselect(
                "Select Weeks",
                all_weeks,
                default=[],
                format_func=lambda week: f"Week {format_week(week)}",
                placeholder="All weeks"
            )
            if not selected_weeks:
                selected_weeks = all_weeks
            
            df_filtered = df[
                (df['Department'].isin(selected_depts)) & 
                (df['Week'].isin(selected_weeks))
            ].copy()
            
            st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download filtered data",
                data=csv,
                file_name=f"workload_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
            st.info(f"Showing {len(df_filtered)} records from {len(selected_depts)} departments and {len(selected_weeks)} weeks.")
            
        except ValueError as e:
            st.error(f"Error: {str(e)}")
            st.stop()
    else:
        st.warning("Please upload an Excel file to begin analysis.")
        st.info("""
        **Required format**
        - Column 1: Week (numeric)
        - Column 2: Date (date range as text)
        - Columns 3+: Department names (PPM1, DP, PPM2, STA, PEH, IP1, IP2, etc.)
        - Cell values: Total hours for that department in that week
        """)
        st.stop()

# KPI METRICS
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("No data matches the current filters. Please select at least one department and one week.")
    st.stop()

metrics = calculate_kpi_metrics(df_filtered)
insights = generate_insights(df_filtered)

line_data = df_filtered.groupby(['Week', 'Department'])['Hours'].sum().reset_index()
week_values = sorted(line_data['Week'].unique())
tick_step = max(1, int(np.ceil(len(week_values) / 12)))
week_ticks = week_values[::tick_step]
weekly_all = df_filtered.groupby('Week')['Hours'].sum().reset_index()
dept_summary = df_filtered.groupby('Department').agg(
    Total_Hours=('Hours', 'sum'),
    Avg_Hours=('Hours', 'mean'),
    Busy_Entries=('Status', lambda s: (s == 'Busy').sum()),
    Records=('Hours', 'count')
).reset_index()
dept_summary['Busy_Rate'] = dept_summary['Busy_Entries'] / dept_summary['Records'] * 100
dept_summary = dept_summary.sort_values('Total_Hours', ascending=False)
status_counts = df_filtered['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

st.subheader("Executive Summary")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Hours", f"{metrics['total_hours']:,.0f}")

with col2:
    st.metric("Avg Hours/Entry", f"{metrics['avg_hours']:.1f}")

with col3:
    st.metric("Busy Entries", metrics['busy_count'])

with col4:
    st.metric("Busy Rate", f"{insights['busy_percentage']:.1f}%")

with col5:
    st.metric("Peak Week", f"W{format_week(metrics['peak_week'])}")

# DASHBOARD OVERVIEW
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.subheader("Dashboard Overview")

default_week_range = (week_values[0], week_values[-1])
if len(week_values) > 1:
    trend_week_range = st.session_state.get("trend_week_range", default_week_range)
    if (
        not isinstance(trend_week_range, tuple) or
        len(trend_week_range) != 2 or
        trend_week_range[0] < week_values[0] or
        trend_week_range[1] > week_values[-1]
    ):
        trend_week_range = default_week_range
        st.session_state["trend_week_range"] = default_week_range
else:
    trend_week_range = default_week_range

trend_data = line_data[
    (line_data['Week'] >= trend_week_range[0]) &
    (line_data['Week'] <= trend_week_range[1])
].copy()
trend_week_values = sorted(trend_data['Week'].unique())
trend_tick_step = max(1, int(np.ceil(len(trend_week_values) / 12)))
trend_week_ticks = trend_week_values[::trend_tick_step]
weekly_total = trend_data.groupby('Week')['Hours'].sum().reset_index()
avg_weekly_hours = weekly_total['Hours'].mean()
peak_row = weekly_total.loc[weekly_total['Hours'].idxmax()]

overview_col, health_col = st.columns([2.2, 1])

with overview_col:
    st.markdown("**Workload Trend**")
    overall_tab, focus_tab = st.tabs(["Overall Trend", "Department Focus"])

    with overall_tab:
        fig_line = go.Figure()
        fig_line.add_trace(
            go.Scatter(
                x=weekly_total['Week'],
                y=weekly_total['Hours'],
                mode='lines',
                name='Total Hours',
                line=dict(color=ACCENT, width=3.4, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(123, 97, 255, 0.14)',
                hovertemplate='Week %{x}<br>Total Hours: %{y:.1f}<extra></extra>'
            )
        )
        fig_line.add_trace(
            go.Scatter(
                x=[peak_row['Week']],
                y=[peak_row['Hours']],
                mode='markers+text',
                name='Peak Week',
                marker=dict(color=ACCENT_DARK, size=12, line=dict(color='white', width=2)),
                text=[f"Peak: W{format_week(peak_row['Week'])}"],
                textposition='top center',
                hovertemplate='Peak Week %{x}<br>Total Hours: %{y:.1f}<extra></extra>'
            )
        )
        fig_line.add_hline(
            y=avg_weekly_hours,
            line_dash="dash",
            line_color="#9A94B8",
            annotation_text=f"Average ({avg_weekly_hours:.1f}h)",
            annotation_position="right"
        )
        fig_line.update_layout(
            title="Total Weekly Workload Trend",
            height=420,
            hovermode='x unified',
            xaxis_title='Week Number',
            yaxis_title='Total Hours',
            showlegend=False,
        )
        style_chart(fig_line, height=420, show_legend=False, top_margin=62, bottom_margin=38)
        fig_line.update_xaxes(tickmode='array', tickvals=trend_week_ticks, showgrid=True)
        fig_line.update_yaxes(showgrid=True, rangemode='tozero')
        st.plotly_chart(fig_line, use_container_width=True)

    with focus_tab:
        dept_totals_for_focus = trend_data.groupby('Department')['Hours'].sum().sort_values(ascending=False)
        default_focus_depts = dept_totals_for_focus.head(min(3, len(dept_totals_for_focus))).index.tolist()
        selected_focus_depts = st.multiselect(
            "Departments to compare",
            dept_totals_for_focus.index.tolist(),
            default=default_focus_depts,
            key="trend_focus_departments"
        )
        if len(selected_focus_depts) > 4:
            st.info("Showing the first 4 selected departments to keep the trend readable.")
            selected_focus_depts = selected_focus_depts[:4]

        if selected_focus_depts:
            focus_data = trend_data[trend_data['Department'].isin(selected_focus_depts)].copy()
            fig_focus = px.line(
                focus_data,
                x='Week',
                y='Hours',
                color='Department',
                markers=True,
                title="Focused Department Trend",
                labels={'Week': 'Week Number', 'Hours': 'Total Hours'},
                template='plotly_white',
                color_discrete_sequence=[ACCENT, "#4FA8FF", SUCCESS, AMBER]
            )
            fig_focus.update_traces(line=dict(width=3, shape='spline'), marker=dict(size=7), opacity=0.95)
            fig_focus.add_hline(
                y=32,
                line_dash="dash",
                line_color=DANGER,
                annotation_text="Busy Threshold (32h)",
                annotation_position="right"
            )
            fig_focus.update_layout(
                height=420,
                hovermode='x unified',
                legend=dict(
                    title_text='',
                    orientation='h',
                    yanchor='top',
                    y=-0.2,
                    xanchor='center',
                    x=0.5
                ),
                margin=dict(l=20, r=20, t=70, b=105),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter, Segoe UI, Arial, sans-serif', color=TEXT, size=12)
            )
            style_chart(fig_focus, height=420, top_margin=62, bottom_margin=105)
            fig_focus.update_xaxes(tickmode='array', tickvals=trend_week_ticks, showgrid=True)
            fig_focus.update_yaxes(showgrid=True, rangemode='tozero')
            st.plotly_chart(fig_focus, use_container_width=True)
        else:
            st.info("Select at least one department to show the focused trend.")

    if len(week_values) > 1:
        st.slider(
            "Trend week range",
            min_value=week_values[0],
            max_value=week_values[-1],
            value=trend_week_range,
            key="trend_week_range"
        )

with health_col:
    st.markdown("**Peak Week Breakdown**")
    peak_week_data = trend_data[trend_data['Week'] == peak_row['Week']].sort_values('Hours', ascending=True)
    fig_peak = px.bar(
        peak_week_data,
        x='Hours',
        y='Department',
        orientation='h',
        title=f"Department Load in W{format_week(peak_row['Week'])}",
        labels={'Hours': 'Hours', 'Department': 'Department'},
        color='Hours',
        color_continuous_scale=[
            [0, '#FFF3D6'],
            [0.55, AMBER],
            [1, AMBER_DARK]
        ],
        template='plotly_white'
    )
    fig_peak.update_traces(marker_line_color='rgba(217, 119, 6, 0.22)', marker_line_width=1)
    fig_peak.update_layout(coloraxis_showscale=False, bargap=0.36)
    style_chart(fig_peak, height=285, top_margin=62, bottom_margin=36)
    fig_peak.update_xaxes(rangemode='tozero')
    st.plotly_chart(fig_peak, use_container_width=True)

    fig_status = px.pie(
        status_counts,
        names='Status',
        values='Count',
        hole=0.62,
        title='Status Mix',
        color='Status',
        color_discrete_map={'Normal': SUCCESS, 'Busy': DANGER, 'N/A': '#B8B2CC'},
        template='plotly_white'
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    fig_status.update_traces(marker=dict(line=dict(color='white', width=3)))
    style_chart(fig_status, height=205, show_legend=False, top_margin=48, bottom_margin=8)
    st.plotly_chart(fig_status, use_container_width=True)

# DEPARTMENT ANALYTICS
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.subheader("Department Comparison")

dept_col1, dept_col2 = st.columns([1.35, 1])

with dept_col1:
    fig_bar = px.bar(
        dept_summary,
        x='Department',
        y='Total_Hours',
        color='Total_Hours',
        title="Total Workload by Department",
        labels={'Department': 'Department', 'Total_Hours': 'Total Hours'},
        color_continuous_scale=[
            [0, BLUE_SOFT],
            [0.55, BLUE],
            [1, BLUE_DARK]
        ],
        template='plotly_white'
    )
    fig_bar.update_traces(marker_line_color='rgba(59, 130, 246, 0.22)', marker_line_width=1)
    fig_bar.update_layout(coloraxis_showscale=False, bargap=0.28)
    style_chart(fig_bar, height=390, top_margin=62, bottom_margin=42)
    fig_bar.update_yaxes(rangemode='tozero')
    st.plotly_chart(fig_bar, use_container_width=True)

with dept_col2:
    busy_rate_data = dept_summary.sort_values('Busy_Rate', ascending=True)
    fig_busy_rate = px.bar(
        busy_rate_data,
        x='Busy_Rate',
        y='Department',
        orientation='h',
        title='Busy Rate by Department',
        labels={'Busy_Rate': 'Busy Rate (%)', 'Department': 'Department'},
        color='Busy_Rate',
        color_continuous_scale=[
            [0, '#FFE8EC'],
            [0.55, DANGER],
            [1, DANGER_DARK]
        ],
        template='plotly_white'
    )
    fig_busy_rate.update_layout(coloraxis_showscale=False, bargap=0.36)
    style_chart(fig_busy_rate, height=390, top_margin=62, bottom_margin=42)
    fig_busy_rate.update_xaxes(range=[0, 100], ticksuffix='%')
    st.plotly_chart(fig_busy_rate, use_container_width=True)

# PATTERNS AND DISTRIBUTION
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.subheader("Patterns & Distribution")

pattern_col1, pattern_col2 = st.columns([1, 1])

with pattern_col1:
    top_weeks = weekly_all.sort_values('Hours', ascending=False).head(6).sort_values('Hours')
    top_weeks = top_weeks.assign(Week_Label=top_weeks['Week'].apply(lambda week: f"Week {week}"))
    fig_top_weeks = px.bar(
        top_weeks,
        x='Hours',
        y='Week_Label',
        orientation='h',
        title='Top Workload Weeks',
        labels={'Hours': 'Total Hours', 'Week_Label': 'Week'},
        color='Hours',
        color_continuous_scale=[
            [0, '#FFF3D6'],
            [0.55, AMBER],
            [1, AMBER_DARK]
        ],
        template='plotly_white'
    )
    fig_top_weeks.update_layout(coloraxis_showscale=False, bargap=0.36)
    style_chart(fig_top_weeks, height=360, top_margin=62, bottom_margin=42)
    fig_top_weeks.update_xaxes(rangemode='tozero')
    st.plotly_chart(fig_top_weeks, use_container_width=True)

with pattern_col2:
    fig_box = px.box(
        df_filtered,
        x='Department',
        y='Hours',
        color='Department',
        title='Workload Distribution by Department',
        labels={'Department': 'Department', 'Hours': 'Hours'},
        points='outliers',
        color_discrete_sequence=[ACCENT, BLUE, SUCCESS, AMBER, "#FF8A9A", "#8B5CF6"],
        template='plotly_white'
    )
    fig_box.add_hline(
        y=32,
        line_dash='dash',
        line_color=DANGER,
        annotation_text='Busy Threshold (32h)',
        annotation_position='right'
    )
    style_chart(fig_box, height=360, show_legend=False, top_margin=62, bottom_margin=42)
    fig_box.update_yaxes(rangemode='tozero')
    st.plotly_chart(fig_box, use_container_width=True)

# HEATMAP
st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
st.subheader("Department × Week Heatmap")

heatmap_data = df_filtered.pivot_table(
    index='Department',
    columns='Week',
    values='Hours',
    aggfunc='sum'
)

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=[
            [0, '#F8FAFC'],
            [0.2, '#DBEAFE'],
            [0.4, '#FDE68A'],
            [0.62, '#FB923C'],
            [0.82, '#EF4444'],
            [1, DANGER_DARK]
        ],
        colorbar=dict(title='Hours', thickness=16, xpad=14),
        hovertemplate='Dept: %{y}<br>Week: %{x}<br>Hours: %{z:.1f}<extra></extra>'
    )
)

fig_heatmap.update_layout(
    title='Workload Intensity Heatmap',
    xaxis_title='Week Number',
    yaxis_title='Department',
    height=420,
    template='plotly_white'
)
style_chart(fig_heatmap, height=420, top_margin=62, bottom_margin=42)
fig_heatmap.update_layout(margin=dict(l=18, r=82, t=62, b=42))
fig_heatmap.update_xaxes(tickmode='array', tickvals=week_ticks if week_ticks else heatmap_data.columns)

st.plotly_chart(fig_heatmap, use_container_width=True)
