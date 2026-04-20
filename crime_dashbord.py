# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# st.title("Crime Analysis Dashboard - Karnataka")

# df = pd.read_csv("/Users/bhagyasree/data_analytics/Crime_rate_analysis_karnataka/datafile.csv")

# current = 'During the current month'
# prev_month = 'During the previous month'
# prev_year = 'During the corresponding month of previous year'

# # Aggregate
# major = df.groupby('Major Heads')[[current, prev_month, prev_year]].sum()

# major['MoM_change'] = major[current] - major[prev_month]
# major['YoY_change'] = major[current] - major[prev_year]

# # Top crimes
# st.subheader("Top Crime Categories")
# st.bar_chart(major[current].sort_values(ascending=False).head(10))

# # MoM
# st.subheader("Month-over-Month Change")
# st.bar_chart(major['MoM_change'].sort_values(ascending=False).head(10))

# # YoY
# st.subheader("Year-over-Year Change")
# st.bar_chart(major['YoY_change'].sort_values(ascending=False).head(10))

# # Heatmap
# st.subheader("Crime Relationship Heatmap")

# pivot = pd.pivot_table(
#     df,
#     values=current,
#     index='Heads of Crime',
#     columns='Major Heads',
#     aggfunc='sum'
# ).fillna(0)

# fig, ax = plt.subplots(figsize=(10,5))
# sns.heatmap(pivot, ax=ax)
# st.pyplot(fig)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Karnataka Crime Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0d0f1a;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #12152a !important;
    border-right: 1px solid #1e2340;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #a0a8c8 !important;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #1a1e35 0%, #141828 100%);
    border: 1px solid #252a48;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, #4f8ef7, #38d9f5); }
.kpi-card.red::before   { background: linear-gradient(90deg, #f7506e, #f9a26c); }
.kpi-card.green::before { background: linear-gradient(90deg, #38d9a9, #4fb8f7); }
.kpi-card.orange::before{ background: linear-gradient(90deg, #f9c46c, #f7506e); }

.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    margin: 8px 0 4px;
}
.kpi-label {
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7499;
}
.kpi-delta {
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 6px;
}
.up   { color: #f7506e; }
.down { color: #38d9a9; }

/* Section title */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #c8cfe8;
    padding: 6px 0 12px;
    border-bottom: 1px solid #1e2340;
    margin-bottom: 16px;
    letter-spacing: 0.02em;
}

/* Chart containers */
.chart-box {
    background: #12152a;
    border: 1px solid #1e2340;
    border-radius: 16px;
    padding: 20px;
}

/* Divider */
hr { border-color: #1e2340 !important; }

/* Table */
.stDataFrame { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrameResizable"] { background: #12152a !important; }
</style>
""", unsafe_allow_html=True)


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/bhagyasree/data_analytics/Crime_rate_analysis_karnataka/datafile.csv")
    return df

df = load_data()

CURR  = 'During the current month'
PREV  = 'During the previous month'
PREVY = 'During the corresponding month of previous year'

# Aggregate by major heads
major = df.groupby('Major Heads')[[CURR, PREV, PREVY]].sum().reset_index()
major['MoM'] = major[CURR] - major[PREV]
major['YoY'] = major[CURR] - major[PREVY]
major['MoM_pct'] = ((major[CURR] - major[PREV]) / major[PREV].replace(0, np.nan) * 100).round(1)
major['YoY_pct'] = ((major[CURR] - major[PREVY]) / major[PREVY].replace(0, np.nan) * 100).round(1)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Karnataka Crime Analytics")
    st.markdown("---")
    st.markdown("**Filters**")

    all_heads = sorted(df['Major Heads'].dropna().unique().tolist())
    selected_heads = st.multiselect(
        "Crime Categories",
        options=all_heads,
        default=all_heads[:6],
        help="Filter by major crime category"
    )

    top_n = st.slider("Top N for bar charts", min_value=5, max_value=20, value=10)
    st.markdown("---")
    st.markdown("**Color Palette**")
    palette = st.selectbox("Chart theme", ["Crimson", "Ocean", "Forest", "Sunset"])
    palette_map = {
        "Crimson": ["#f7506e", "#f9a26c", "#f9c46c"],
        "Ocean":   ["#4f8ef7", "#38d9f5", "#38d9a9"],
        "Forest":  ["#38d9a9", "#4fb8f7", "#a7f750"],
        "Sunset":  ["#f9c46c", "#f7506e", "#c46cf9"],
    }
    colors = palette_map[palette]
    st.markdown("---")
    st.caption("Data: Karnataka Police Crime Records")


# ── Filter data ───────────────────────────────────────────────────────────────
if selected_heads:
    filtered_major = major[major['Major Heads'].isin(selected_heads)]
    filtered_df    = df[df['Major Heads'].isin(selected_heads)]
else:
    filtered_major = major.copy()
    filtered_df    = df.copy()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='font-family:Syne;font-size:2.4rem;font-weight:800;
           background:linear-gradient(90deg,#f7506e,#f9a26c);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           margin-bottom:4px;'>
    Karnataka Crime Analysis Dashboard
</h1>
<p style='color:#6b7499;font-size:0.95rem;margin-top:0;'>
    Month-over-month &amp; year-over-year crime statistics across Karnataka districts
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_curr  = int(filtered_major[CURR].sum())
total_prev  = int(filtered_major[PREV].sum())
total_prevy = int(filtered_major[PREVY].sum())
mom_delta   = total_curr - total_prev
yoy_delta   = total_curr - total_prevy
cats        = len(filtered_major)

def delta_html(val):
    arrow = "▲" if val > 0 else "▼"
    cls   = "up" if val > 0 else "down"
    return f'<div class="kpi-delta {cls}">{arrow} {abs(val):,}</div>'

c1, c2, c3, c4 = st.columns(4)
kpis = [
    (c1, "blue",   f"{total_curr:,}",  "Current Month Crimes",     delta_html(mom_delta)),
    (c2, "red",    f"{mom_delta:+,}",  "MoM Change",               '<div class="kpi-delta" style="color:#6b7499">vs Previous Month</div>'),
    (c3, "green",  f"{yoy_delta:+,}",  "YoY Change",               '<div class="kpi-delta" style="color:#6b7499">vs Same Month Last Year</div>'),
    (c4, "orange", f"{cats}",          "Crime Categories Tracked",  '<div class="kpi-delta" style="color:#6b7499">Major Heads</div>'),
]
for col, cls, val, label, delta in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            {delta}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Helper: styled horizontal bar chart ───────────────────────────────────────
def styled_bar(ax, series, color_main, color_accent, title, xlabel):
    vals   = series.values
    labels = series.index.tolist()
    y_pos  = np.arange(len(labels))

    # Background bars
    ax.barh(y_pos, [max(abs(v) for v in vals)] * len(vals),
            color="#1e2340", height=0.6, zorder=1)

    bar_colors = [color_main if v >= 0 else color_accent for v in vals]
    bars = ax.barh(y_pos, vals, color=bar_colors, height=0.6, zorder=2,
                   edgecolor="none")

    for bar, val in zip(bars, vals):
        x = bar.get_width()
        ax.text(x + max(abs(v) for v in vals) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:,.0f}", va='center', ha='left', fontsize=8,
                color='#a0a8c8', fontweight='500')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9, color='#c8cfe8')
    ax.set_xlabel(xlabel, fontsize=9, color='#6b7499')
    ax.set_title(title, fontsize=12, fontweight='700', color='#e8eaf0',
                 pad=12, fontfamily='DejaVu Sans')
    ax.set_facecolor('#12152a')
    ax.tick_params(colors='#6b7499')
    ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    ax.xaxis.set_tick_params(labelsize=8, labelcolor='#6b7499')
    ax.axvline(0, color='#252a48', linewidth=1)
    plt.tight_layout()


# ── Row 1: Top Crimes + MoM ───────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="section-title">🔴 Top Crime Categories — Current Month</div>', unsafe_allow_html=True)
    top_crimes = (
        filtered_major.set_index('Major Heads')[CURR]
        .sort_values(ascending=True).tail(top_n)
    )
    fig, ax = plt.subplots(figsize=(7, max(3.5, top_n * 0.42)))
    fig.patch.set_facecolor('#12152a')
    styled_bar(ax, top_crimes, colors[0], colors[1], "", "Incidents")
    st.pyplot(fig)
    plt.close()

with col_b:
    st.markdown('<div class="section-title">📊 Month-over-Month Change</div>', unsafe_allow_html=True)
    mom_data = (
        filtered_major.set_index('Major Heads')['MoM']
        .sort_values(ascending=True).tail(top_n)
    )
    fig, ax = plt.subplots(figsize=(7, max(3.5, top_n * 0.42)))
    fig.patch.set_facecolor('#12152a')
    styled_bar(ax, mom_data, colors[0], colors[2], "", "Δ Incidents")
    st.pyplot(fig)
    plt.close()


# ── Row 2: YoY + Trend comparison ────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.markdown('<div class="section-title">📅 Year-over-Year Change</div>', unsafe_allow_html=True)
    yoy_data = (
        filtered_major.set_index('Major Heads')['YoY']
        .sort_values(ascending=True).tail(top_n)
    )
    fig, ax = plt.subplots(figsize=(7, max(3.5, top_n * 0.42)))
    fig.patch.set_facecolor('#12152a')
    styled_bar(ax, yoy_data, colors[0], colors[2], "", "Δ Incidents")
    st.pyplot(fig)
    plt.close()

with col_d:
    st.markdown('<div class="section-title">📈 Curr vs Prev Month vs Prev Year</div>', unsafe_allow_html=True)
    comp = (
        filtered_major.nlargest(8, CURR)
        .set_index('Major Heads')[[CURR, PREV, PREVY]]
    )
    x   = np.arange(len(comp))
    w   = 0.28
    fig, ax = plt.subplots(figsize=(7, 4.2))
    fig.patch.set_facecolor('#12152a')
    ax.set_facecolor('#12152a')

    ax.bar(x - w, comp[CURR],  w, label='Current',   color=colors[0], alpha=0.95)
    ax.bar(x,     comp[PREV],  w, label='Prev Month', color=colors[1], alpha=0.85)
    ax.bar(x + w, comp[PREVY], w, label='Prev Year',  color=colors[2], alpha=0.75)

    ax.set_xticks(x)
    ax.set_xticklabels(comp.index, rotation=35, ha='right', fontsize=8, color='#c8cfe8')
    ax.tick_params(axis='y', labelcolor='#6b7499', labelsize=8)
    ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.set_ylabel("Incidents", fontsize=9, color='#6b7499')
    legend = ax.legend(fontsize=8, framealpha=0,
                       labelcolor='#c8cfe8', loc='upper right')
    ax.set_title("Top 8 Categories — Three-Period Comparison",
                 fontsize=11, fontweight='700', color='#e8eaf0', pad=10)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ── Heatmap ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">🌡️ Crime Relationship Heatmap — Heads of Crime × Major Categories</div>',
            unsafe_allow_html=True)

pivot = pd.pivot_table(
    filtered_df,
    values=CURR,
    index='Heads of Crime',
    columns='Major Heads',
    aggfunc='sum'
).fillna(0)

# Limit rows for readability
pivot_plot = pivot.loc[pivot.sum(axis=1).nlargest(25).index]

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('#12152a')
ax.set_facecolor('#12152a')

cmap = sns.color_palette("RdYlGn_r", as_cmap=True)
sns.heatmap(
    pivot_plot,
    ax=ax,
    cmap=cmap,
    linewidths=0.3,
    linecolor='#1e2340',
    annot=len(pivot_plot.columns) <= 10,
    fmt='.0f',
    annot_kws={"size": 7, "color": "#e8eaf0"},
    cbar_kws={"shrink": 0.6, "label": "Incidents"},
)
ax.set_xlabel("Major Heads", fontsize=10, color='#6b7499', labelpad=10)
ax.set_ylabel("Heads of Crime", fontsize=10, color='#6b7499', labelpad=10)
ax.set_title("Crime Intensity Map (Top 25 Sub-Categories)",
             fontsize=13, fontweight='700', color='#e8eaf0', pad=14)
ax.tick_params(axis='x', colors='#a0a8c8', labelsize=8, rotation=40)
ax.tick_params(axis='y', colors='#a0a8c8', labelsize=8)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
plt.tight_layout()
st.pyplot(fig)
plt.close()


# ── Data Table ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">📋 Detailed Crime Statistics Table</div>', unsafe_allow_html=True)

display_df = (
    filtered_major[['Major Heads', CURR, PREV, PREVY, 'MoM', 'YoY', 'MoM_pct', 'YoY_pct']]
    .rename(columns={
        'Major Heads': 'Category',
        CURR:          'Current',
        PREV:          'Prev Month',
        PREVY:         'Prev Year',
        'MoM':         'MoM Δ',
        'YoY':         'YoY Δ',
        'MoM_pct':     'MoM %',
        'YoY_pct':     'YoY %',
    })
    .sort_values('Current', ascending=False)
    .reset_index(drop=True)
)

st.dataframe(
    display_df.style
        .background_gradient(subset=['Current'], cmap='Reds')
        .applymap(lambda v: 'color: #f7506e' if isinstance(v, (int, float)) and v > 0
                  else ('color: #38d9a9' if isinstance(v, (int, float)) and v < 0 else ''),
                  subset=['MoM Δ', 'YoY Δ', 'MoM %', 'YoY %'])
        .format({'Current': '{:,.0f}', 'Prev Month': '{:,.0f}', 'Prev Year': '{:,.0f}',
                 'MoM Δ': '{:+,.0f}', 'YoY Δ': '{:+,.0f}',
                 'MoM %': '{:+.1f}%', 'YoY %': '{:+.1f}%'}),
    use_container_width=True,
    height=420,
)
 
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;color:#3a3f60;font-size:0.78rem;padding:32px 0 8px;'>
    Karnataka Crime Analytics Dashboard · Data: Karnataka State Police
</div>
""", unsafe_allow_html=True)