import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="CivicCost AI - BNBC Compliant BOQ Estimator",
    page_icon="🏗️",
    layout="wide"
)

# --------------------------------------------------
# HIDE GITHUB / FORK TOOLBAR & STREAMLIT FOOTER
# --------------------------------------------------
st.markdown("""
    <style>
    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }

[data-testid="stAppDeployButton"] {
        display: none !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "calc_type" not in st.session_state:
    st.session_state["calc_type"] = "🏠 Home / Dashboard"

if "estimates_data" not in st.session_state:
    st.session_state["estimates_data"] = {}

# Custom Styling for Punchy Modern UI
st.markdown("""
    <style>
    .main-title {
        font-size: 2.3rem;
        color: #1E3A8A;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 15px;
    }
    .feature-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .highlight-box {
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPER: REPORTLAB PDF GENERATOR (ENGINEER BRANDED)
# --------------------------------------------------
def generate_pdf_report(title, engineer_name, project_name, location, wastage_pct, total_cost, summary_items):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1E3A8A'), spaceAfter=6)
    sub_title_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#64748B'), spaceAfter=12)
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#334155'), spaceAfter=3)
    table_header_style = ParagraphStyle('THeader', parent=styles['Normal'], fontSize=9, textColor=colors.white, fontName="Helvetica-Bold")
    table_body_style = ParagraphStyle('TBody', parent=styles['Normal'], fontSize=8.5, textColor=colors.black)

    story = []

    # Document Header
    story.append(Paragraph("<b>CivicCost AI — Structural BOQ Engineering Estimate</b>", title_style))
    story.append(Paragraph("<i>BNBC Standard Compliant Construction Costing Report</i>", sub_title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=10))

    # Project Metadata Section
    story.append(Paragraph(f"<b>Project Title:</b> {project_name if project_name else 'N/A'}", meta_style))
    story.append(Paragraph(f"<b>Prepared By (Engineer):</b> {engineer_name if engineer_name else 'Engr. User'}", meta_style))
    story.append(Paragraph(f"<b>Project Location:</b> {location} | <b>Applied Wastage & Lap Allowance:</b> {wastage_pct}%", meta_style))
    story.append(Paragraph(f"<b>Module Name:</b> {title}", meta_style))
    story.append(Spacer(1, 12))

    # Items Table
    data = [[
        Paragraph("Item Description", table_header_style), 
        Paragraph("Quantity", table_header_style), 
        Paragraph("Estimated Cost (BDT)", table_header_style)
    ]]
    
    for item in summary_items:
        data.append([
            Paragraph(str(item.get("Item", "")), table_body_style),
            Paragraph(str(item.get("Qty", "")), table_body_style),
            Paragraph(str(item.get("Cost", "")), table_body_style)
        ])
    
    # Grand Total Row
    data.append([
        Paragraph("<b>GRAND TOTAL ESTIMATED COST</b>", table_body_style),
        Paragraph("", table_body_style),
        Paragraph(f"<b>BDT {total_cost:,.2f}</b>", table_body_style)
    ])

    t = Table(data, colWidths=[250, 140, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<i>Report generated automatically via CivicCost AI | Prepared by {engineer_name}</i>", sub_title_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------------------------------
# SIDEBAR - REGIONAL RATES, METADATA & WASTAGE
# --------------------------------------------------
st.sidebar.title("🏗️ CivicCost AI")
st.sidebar.caption("BNBC Compliant Estimator Engine")

# Navigation Menu
nav_options = [
    "🏠 Home / Dashboard",
    "📐 Footing & Column Estimation",
    "🏗️ Sub-structure Excavation & Soling",
    "🧱 Concrete Volume (Beam, Column, Slab, Stair)",
    "📑 Combined Project Report",
    "⭐ User Ratings & Feedback"
]

selected_nav = st.sidebar.radio("Select Navigation", nav_options, index=nav_options.index(st.session_state["calc_type"]))
st.session_state["calc_type"] = selected_nav

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Engineer & Project Meta")
engineer_name = st.sidebar.text_input("Engineer Name", value="Engr. Madhabilata Barua")
project_name = st.sidebar.text_input("Project Name", value="3-Storey Residential Building")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Wastage & Lap Allowance")
wastage_percent = st.sidebar.slider("Wastage & Lap Factor (%)", min_value=0, max_value=15, value=5, step=1, help="Applies margin for rebar cutting, overlaps, and site material wastage.")
wastage_factor = 1.0 + (wastage_percent / 100.0)

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Regional Market Price (BDT)")

location = st.sidebar.selectbox("Select Location Preset", ["Dhaka", "Chattogram", "Sylhet", "Rajshahi", "Khulna", "Custom Rates"])

default_rates = {
    "Dhaka": {"cement": 560.0, "sand": 45.0, "brick": 13.0, "khoa": 130.0, "steel": 98.0, "excavation": 12.0, "water": 0.20},
    "Chattogram": {"cement": 570.0, "sand": 50.0, "brick": 14.0, "khoa": 135.0, "steel": 99.0, "excavation": 14.0, "water": 0.25},
    "Sylhet": {"cement": 550.0, "sand": 35.0, "brick": 13.5, "khoa": 125.0, "steel": 97.5, "excavation": 11.0, "water": 0.18},
    "Rajshahi": {"cement": 540.0, "sand": 40.0, "brick": 12.5, "khoa": 120.0, "steel": 96.5, "excavation": 10.0, "water": 0.20},
    "Khulna": {"cement": 550.0, "sand": 42.0, "brick": 13.0, "khoa": 125.0, "steel": 97.0, "excavation": 11.5, "water": 0.22},
    "Custom Rates": {"cement": 560.0, "sand": 45.0, "brick": 13.0, "khoa": 130.0, "steel": 98.0, "excavation": 12.0, "water": 0.20}
}

current_preset = default_rates[location]

rate_cement = st.sidebar.number_input("Cement Rate (/Bag BDT)", value=current_preset["cement"])
rate_sand = st.sidebar.number_input("Sand Rate (/CFT BDT)", value=current_preset["sand"])
rate_brick = st.sidebar.number_input("Brick Rate (/Piece BDT)", value=current_preset["brick"])
rate_khoa = st.sidebar.number_input("Brick Chips/Khoa (/CFT BDT)", value=current_preset["khoa"])
rate_steel = st.sidebar.number_input("Steel/Rebar Rate (/KG BDT)", value=current_preset["steel"])
rate_exc = st.sidebar.number_input("Excavation Rate (/CFT BDT)", value=current_preset["excavation"])
rate_water = st.sidebar.number_input("Water Rate (/Liter BDT)", value=current_preset["water"])

# --------------------------------------------------
# SECTION 1: HOME / DASHBOARD INTERFACE
# --------------------------------------------------
if st.session_state["calc_type"] == "🏠 Home / Dashboard":
    st.markdown('<div class="main-title">CivicCost AI — Smart Structural BOQ Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Precision Construction Estimation Engine Compliant with BNBC Standards & Regional Bangladesh Material Rates</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight-box">
    💡 <b>Welcome!</b> CivicCost AI bridges structural engineering formulas with current Bangladesh market pricing (BDT). Select an estimation module below, adjust material unit prices and wastage allowance in the left sidebar, and download engineer-branded PDF reports.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("📐 Footing & Column Estimation")
        st.write("Calculates total concrete volume, rebar weight (KG), cement bags, sand, khoa & mixing water requirements with adjustable wastage factor.")
        if st.button("Open Footing & Column Module", key="btn_fc"):
            st.session_state["calc_type"] = "📐 Footing & Column Estimation"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🏗️ Sub-structure Excavation & Soling")
        st.write("Estimate earthwork trench excavation, sand bed cushions, and single/double flat brick soling count as per BNBC specifications.")
        if st.button("Open Excavation & Soling Module", key="btn_ex"):
            st.session_state["calc_type"] = "🏗️ Sub-structure Excavation & Soling"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🧱 Concrete Volume (Beam, Column, Slab, Stair)")
        st.write("Multi-purpose structural concrete estimator for beams, slabs, columns, and stairs including water requirement and mix ratios.")
        if st.button("Open Concrete Module", key="btn_conc"):
            st.session_state["calc_type"] = "🧱 Concrete Volume (Beam, Column, Slab, Stair)"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("📑 Combined Master PDF Report")
        st.write("Compiles all completed estimations into a single master engineering Bill of Quantities (BOQ) PDF stamped with engineer metadata.")
        if st.button("Generate Combined Master Report", key="btn_comb"):
            st.session_state["calc_type"] = "📑 Combined Project Report"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 2: FOOTING & COLUMN ESTIMATION
# --------------------------------------------------
elif st.session_state["calc_type"] == "📐 Footing & Column Estimation":
    st.header("📐 Footing & Column BOQ Estimation")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        num_footings = st.number_input("Number of Identical Footings", min_value=1, value=4)
        f_len = st.number_input("Footing Length (ft)", min_value=1.0, value=6.0)
        f_wid = st.number_input("Footing Width (ft)", min_value=1.0, value=6.0)
        f_dep = st.number_input("Footing Thickness/Depth (inch)", min_value=1.0, value=18.0) / 12.0
    
    with col_in2:
        mix_ratio = st.selectbox("Concrete Mix Ratio (BNBC)", ["1:1.5:3", "1:2:4", "1:1.5:3 (Grade M20)"])
        rebar_dia = st.selectbox("Main Rebar Diameter (mm)", [10, 12, 16, 20, 25], index=2)
        rebar_spacing = st.number_input("Rebar Center-to-Center Spacing (inch)", min_value=3.0, value=6.0)
    st.markdown("---")
    st.markdown("##### 📏 Column Specifications")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        num_cols = st.number_input("Number of Columns", min_value=1, value=4)
        col_len = st.number_input("Column Length/Dia (ft)", min_value=0.5, value=1.0, step=0.25)
    with col_c2:
        col_wid = st.number_input("Column Width (ft) [if square/rect]", min_value=0.5, value=1.0, step=0.25)
        col_height = st.number_input("Column Height (ft)", min_value=1.0, value=10.0, step=0.5)
    with col_c3:
        tie_spacing = st.number_input("Tie/Stirrup Spacing (inch)", min_value=3.0, value=6.0, step=1.0)
    
   # Engineering Calculations
    clean_mix = mix_ratio.split(" ")[0]
    footing_wet_vol = num_footings * f_len * f_wid * f_dep
    column_wet_vol = num_cols * col_len * col_wid * col_height
    wet_vol = footing_wet_vol + column_wet_vol
    dry_vol = wet_vol * 1.54

    parts = [float(x) for x in clean_mix.split(":")]
    total_parts = sum(parts)
    
    # Quantities with Wastage Factor
    cement_bags = ((dry_vol * (parts[0] / total_parts)) / 1.25) * wastage_factor
    sand_cft = (dry_vol * (parts[1] / total_parts)) * wastage_factor
    khoa_cft = (dry_vol * (parts[2] / total_parts)) * wastage_factor
    
    # Water Calculation (BNBC Standard W/C ratio = 0.45; 1 Bag Cement = 50 kg -> 22.5 L Water)
    water_liters = cement_bags * 22.5

    num_bars_x = int((f_len * 12) / rebar_spacing) + 1
    num_bars_y = int((f_wid * 12) / rebar_spacing) + 1
    # Column main steel length & ties calculation
    col_main_bar_ft = num_cols * col_height * 4  
    num_ties_per_col = (col_height * 12) / tie_spacing
    tie_perimeter = 2 * (col_len + col_wid)
    total_ties_ft = num_cols * num_ties_per_col * (tie_perimeter + 1)
    
    # Total Bar Length including Footings and Columns
    footing_bar_len = (num_bars_x * f_wid + num_bars_y * f_len) * num_footings
    total_bar_len_ft = footing_bar_len + col_main_bar_ft + total_ties_ft
    
    # Rebar Weight Formula
    rebar_weight_kg = (total_bar_len_ft * ((rebar_dia ** 2) / 162.2) * 0.3048) * wastage_factor

    # Costs
    cost_c = cement_bags * rate_cement
    cost_s = sand_cft * rate_sand
    cost_k = khoa_cft * rate_khoa
    cost_w = water_liters * rate_water
    cost_r = rebar_weight_kg * rate_steel
    total_fc_cost = cost_c + cost_s + cost_k + cost_w + cost_r

    st.markdown("---")
    st.subheader("📊 Quantities & Cost Breakdown")
    st.caption(f"*Note: Material quantities include a {wastage_percent}% wastage & lap margin.*")

    st.info(f"🧱 **Total Concrete Required:** **{wet_vol:,.2f} CFT** (Wet Volume) | **{dry_vol:,.2f} CFT** (Dry Volume)")

    q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns(5)
    q_col1.metric("Cement Required", f"{cement_bags:,.1f} Bags", f"BDT {cost_c:,.0f}")
    q_col2.metric("Sand Required", f"{sand_cft:,.1f} CFT", f"BDT {cost_s:,.0f}")
    q_col3.metric("Khoa/Chips Required", f"{khoa_cft:,.1f} CFT", f"BDT {cost_k:,.0f}")
    q_col4.metric("Water Required", f"{water_liters:,.0f} Liters", f"BDT {cost_w:,.0f}")
    q_col5.metric(f"Rebar ({rebar_dia}mm)", f"{rebar_weight_kg:,.1f} KG", f"BDT {cost_r:,.0f}")

    st.markdown(f"### 💰 **Total Footing & Column Section Cost: BDT {total_fc_cost:,.2f}**")

# Formula & Sample Calculation Expander
with st.expander("📐 View Engineering Formula & Sample Calculation"):
    st.markdown("""
    **1. Concrete Volume Calculation:**
    * **Total Concrete Volume** = (Footings Volume + Columns Volume)
    * **Dry Volume** = Wet Volume $\times 1.54$ (Standard Practice Factor for dry mix conversion)

    **2. Material Calculation (Mix Ratio):**
    * **Cement Bags** = $\\frac{\\text{Dry Volume} \\times \\text{Cement Proportion}}{\\text{Total Proportion}} \\div 1.25 \\text{ CFT/bag} \\times \\text{Wastage Factor}$
    * **Sand Volume** = $\\text{Dry Volume} \\times \\frac{\\text{Sand Proportion}}{\\text{Total Proportion}} \\times \\text{Wastage Factor}$
    * **Khoa/Chips Volume** = $\\text{Dry Volume} \\times \\frac{\\text{Khoa Proportion}}{\\text{Total Proportion}} \\times \\text{Wastage Factor}$
    * **Mixing Water ($W/C = 0.45$):** Cement Bags $\\times 22.5 \\text{ Liters/bag}$

    **3. Rebar Weight Formula:**
    * **Unit Weight (kg/m)** = $\\frac{d^2}{162.2}$ (where $d$ is bar diameter in mm)
    * **Total Steel Weight** = Total Length $\\times$ Unit Weight $\\times$ Wastage Factor
    """)

   # Only create this summary if the Footing & Column page is currently selected
if st.session_state.get("calc_type") == "Footing & Column Estimation":
    fc_summary = [
        {"Item": "Total Concrete Volume", "Qty": f"{wet_vol:,.1f} CFT (Wet)", "Cost": "-"},
        {"Item": f"Cement ({clean_mix})", "Qty": f"{cement_bags:,.1f} Bags", "Cost": f"BDT {cost_c:,.2f}"},
        {"Item": "Sand", "Qty": f"{sand_cft:,.1f} CFT", "Cost": f"BDT {cost_s:,.2f}"},
        {"Item": "Khoa/Chips", "Qty": f"{khoa_cft:,.1f} CFT", "Cost": f"BDT {cost_k:,.2f}"},
        {"Item": "Mixing Water", "Qty": f"{water_liters:,.0f} Liters", "Cost": f"BDT {cost_w:,.2f}"},
        {"Item": f"Steel Rebar ({rebar_dia}mm)", "Qty": f"{rebar_weight_kg:,.1f} KG", "Cost": f"BDT {cost_r:,.2f}"}
    ]

 st.session_state["estimates_data"]["Footing & Column"] = {
        "cost": total_fc_cost,
        "summary": fc_summary
    }

    pdf_data = generate_pdf_report("Footing & Column Estimate", engineer_name, project_name, location, wastage_percent, total_fc_cost, fc_summary)
    st.download_button(
        label="📥 Download Section PDF Report",
        data=pdf_data,
        file_name=f"Footing_Column_Report_{project_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

# ----------------------------------------------------
# SECTION 3: SUB-STRUCTURE EXCAVATION & SOLING (Clean & Fixed)
# ----------------------------------------------------
if st.session_state["calc_type"] == "Sub-structure Excavation & Soling":
    st.header("Sub-structure Excavation & Flat Brick Soling")

    # Safe variables
    rate_exc = 15.0
    rate_sand = 35.0
    rate_brick = 12.0
    wastage_factor = 1.05

    # 1. INPUT FIELDS (Must be at the top)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        total_length = st.number_input("Total Trench/Pit Length (ft)", min_value=1.0, value=100.0, key="ex_len_v2")
        width = st.number_input("Trench/Pit Width (ft)", min_value=1.0, value=5.0, key="ex_width_v2")
        depth = st.number_input("Excavation Depth (ft)", min_value=1.0, value=5.0, key="ex_depth_v2")

    with col_e2:
        sand_depth = st.number_input("Sand Bed Cushion Depth (inch)", min_value=0.0, value=3.0, key="ex_sand_v2") / 12.0
        soling_type = st.selectbox("Brick Soling Type", ["Single Layer Flat Soling", "Double Layer Flat Soling"], key="ex_soling_v2")

    # 2. CALCULATIONS
    vol_cft = total_length * width * depth
    cost_exc = vol_cft * rate_exc

    sand_cft = (total_length * width * sand_depth) * wastage_factor
    cost_sand = sand_cft * rate_sand

    soling_sqft = total_length * width
    multiplier = 3.0 if "Single Layer" in soling_type else 6.0
    total_soling_bricks = (soling_sqft * multiplier) * wastage_factor
    cost_soling = total_soling_bricks * rate_brick

    total_ex_cost = cost_exc + cost_sand + cost_soling

    # 3. DISPLAY METRICS & RESULTS
    st.markdown("---")
    st.subheader("📊 Quantities & Cost Breakdown")

    e_col1, e_col2, e_col3 = st.columns(3)
    e_col1.metric("Excavation Volume", f"{vol_cft:,.1f} CFT", f"BDT {cost_exc:,.0f}")
    e_col2.metric("Sand Filling Cushion", f"{sand_cft:,.1f} CFT", f"BDT {cost_sand:,.0f}")
    e_col3.metric("Soling Bricks", f"{total_soling_bricks:,.0f} Pcs", f"BDT {cost_soling:,.0f}")

    st.markdown(f"### 💰 **Total Section Cost: BDT {total_ex_cost:,.2f}**")

    # 4. EXPANDER (Must be at the very bottom)
    with st.expander("📐 View Engineering Formula & Sample Calculation"):
        st.markdown(f"""
        **1. Earth Excavation Volume:**
        * Formula = Length $\\times$ Width $\\times$ Depth
        * Calculation = {total_length} ft $\\times$ {width} ft $\\times$ {depth} ft = **{vol_cft:,.1f} CFT**
        """)
        
# --------------------------------------------------
# SECTION 4: CONCRETE VOLUME (BEAM, COLUMN, SLAB, STAIR)
# --------------------------------------------------
elif st.session_state["calc_type"] == "🧱 Concrete Volume (Beam, Column, Slab, Stair)":
    st.header("🧱 Concrete Volume & Structural Materials")

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        struct_type = st.selectbox("Select Structural Element", ["Slab", "Beam", "Column", "Staircase"])
        elem_count = st.number_input("Number of Identical Elements", min_value=1, value=1)
        c_len = st.number_input("Length/Span (ft)", min_value=0.1, value=20.0)
        c_wid = st.number_input("Width (ft)", min_value=0.1, value=15.0)

    with c_col2:
        c_dep = st.number_input("Thickness/Depth (inch)", min_value=1.0, value=6.0) / 12.0
        c_ratio = st.selectbox("Mix Ratio", ["1:1.5:3", "1:2:4"], key="c_mix")

    # Calculations
    wet_c_vol = elem_count * c_len * c_wid * c_dep
    dry_c_vol = wet_c_vol * 1.54

    c_parts = [float(x) for x in c_ratio.split(":")]
    c_total_parts = sum(c_parts)

    c_bags = ((dry_c_vol * (c_parts[0] / c_total_parts)) / 1.25) * wastage_factor
    c_sand = (dry_c_vol * (c_parts[1] / c_total_parts)) * wastage_factor
    c_khoa = (dry_c_vol * (c_parts[2] / c_total_parts)) * wastage_factor
    c_water = c_bags * 22.5

    cost_c_bag = c_bags * rate_cement
    cost_c_sand = c_sand * rate_sand
    cost_c_khoa = c_khoa * rate_khoa
    cost_c_water = c_water * rate_water

    total_conc_cost = cost_c_bag + cost_c_sand + cost_c_khoa + cost_c_water

    st.markdown("---")
    st.subheader("📊 Quantities & Cost Breakdown")
    st.caption(f"*Note: Material quantities include a {wastage_percent}% wastage factor.*")

    st.info(f"🧱 **Total {struct_type} Concrete Required:** **{wet_c_vol:,.2f} CFT** (Wet Volume) | **{dry_c_vol:,.2f} CFT** (Dry Volume)")

    mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)
    mc_col1.metric("Cement Required", f"{c_bags:,.1f} Bags", f"BDT {cost_c_bag:,.0f}")
    mc_col2.metric("Sand Required", f"{c_sand:,.1f} CFT", f"BDT {cost_c_sand:,.0f}")
    mc_col3.metric("Khoa/Chips Required", f"{c_khoa:,.1f} CFT", f"BDT {cost_c_khoa:,.0f}")
    mc_col4.metric("Water Required", f"{c_water:,.0f} Liters", f"BDT {cost_c_water:,.0f}")

    st.markdown(f"### 💰 **Total Section Cost: BDT {total_conc_cost:,.2f}**")

    conc_summary = [
        {"Item": f"Concrete Volume ({struct_type})", "Qty": f"{wet_c_vol:,.1f} CFT (Wet)", "Cost": "-"},
        {"Item": f"Cement ({c_ratio})", "Qty": f"{c_bags:,.1f} Bags", "Cost": f"BDT {cost_c_bag:,.2f}"},
        {"Item": "Sand", "Qty": f"{c_sand:,.1f} CFT", "Cost": f"BDT {cost_c_sand:,.2f}"},
        {"Item": "Khoa/Chips", "Qty": f"{c_khoa:,.1f} CFT", "Cost": f"BDT {cost_c_khoa:,.2f}"},
        {"Item": "Mixing Water", "Qty": f"{c_water:,.0f} Liters", "Cost": f"BDT {cost_c_water:,.2f}"}
    ]

    st.session_state["estimates_data"][f"Concrete ({struct_type})"] = {
        "cost": total_conc_cost,
        "items": conc_summary
    }

    pdf_data = generate_pdf_report(f"Concrete Volume ({struct_type})", engineer_name, project_name, location, wastage_percent, total_conc_cost, conc_summary)
    st.download_button(
        label="📄 Download Section PDF Report",
        data=pdf_data,
        file_name=f"Concrete_{struct_type}_Report_{project_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

# --------------------------------------------------
# SECTION 5: COMBINED PROJECT REPORT
# --------------------------------------------------
elif st.session_state["calc_type"] == "📑 Combined Project Report":
    st.header("📑 Master Combined Project BOQ Report")

    if not st.session_state["estimates_data"]:
        st.warning("⚠️ No estimates calculated yet! Please calculate quantities in above sections first.")
    else:
        combined_items = []
        grand_total = 0.0

        for sec_name, data in st.session_state["estimates_data"].items():
            grand_total += data["cost"]
            for item in data["items"]:
                combined_items.append({
                    "Item": f"[{sec_name}] {item['Item']}",
                    "Qty": item["Qty"],
                    "Cost": item["Cost"]
                })

        st.subheader("📋 Complete Project BOQ Summary Table")
        
        df_master = pd.DataFrame(combined_items)
        st.table(df_master)

        st.markdown(f"## 🏆 **Grand Total Estimated Project Cost: BDT {grand_total:,.2f}**")

        comb_pdf_data = generate_pdf_report("Master Combined BOQ Report", engineer_name, project_name, location, wastage_percent, grand_total, combined_items)
        st.download_button(
            label="📑 Download Master Combined PDF Report",
            data=comb_pdf_data,
            file_name=f"Master_Combined_BOQ_Report_{project_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# --------------------------------------------------
# SECTION 6: USER RATINGS & FEEDBACK (Safe Persistent Version)
# --------------------------------------------------
elif st.session_state["calc_type"] == "⭐ User Ratings & Feedback":
    st.header("⭐ User Ratings & Feedback")
    st.write("We value your feedback! Rate your experience with CivicCost AI.")

    import json
    import os

    FEEDBACK_FILE = "feedback.json"

    # Load existing feedbacks from file if exists, otherwise use default
    def load_feedbacks():
        if os.path.exists(FEEDBACK_FILE):
            try:
                with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return [
            {"Engineer": "Engr. Nazmul", "Rating": "5/5 ⭐", "Feedback": "Extremely helpful for quick BNBC calculations!"},
            {"Engineer": "Engr. Tanvir", "Rating": "4/5 ⭐", "Feedback": "Great layout and regional pricing feature."}
        ]

    # Save feedbacks safely to file
    def save_feedbacks(feedbacks):
        try:
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump(feedbacks, f, ensure_ascii=False, indent=4)
        except Exception:
            # Fallback silently if cloud storage is read-only, preventing any app crash
            pass

    # Initialize session state storage
    if "feedbacks_list" not in st.session_state:
        st.session_state["feedbacks_list"] = load_feedbacks()

    with st.form("feedback_form"):
        rating = st.slider("Rate the platform accuracy & usability", 1, 5, 5)
        feedback_text = st.text_area("Share your feedback or feature suggestions")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            new_feedback = {
                "Engineer": engineer_name if 'engineer_name' in locals() and engineer_name else "Guest Engineer",
                "Rating": f"{rating}/5 ⭐",
                "Feedback": feedback_text if feedback_text else "No comments provided"
            }
            # Insert at the top of the list
            st.session_state["feedbacks_list"].insert(0, new_feedback)
            # Save to file safely
            save_feedbacks(st.session_state["feedbacks_list"])
            st.success("Thank you! Your feedback has been published successfully.")

    st.markdown("---")
    st.subheader("📋 Public User Feedback & Ratings")
    
    # Display all feedbacks on screen
    for idx, fb in enumerate(st.session_state["feedbacks_list"], 1):
        with st.container():
            st.info(f"**# {idx} | Engineer: {fb['Engineer']} | Rating: {fb['Rating']}**\n\n> \"{fb['Feedback']}\"")
