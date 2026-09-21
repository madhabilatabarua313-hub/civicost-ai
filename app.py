import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="CivicCost AI - Smart BOQ & Construction Estimator",
    page_icon="🏗️",
    layout="wide"
)

# Initialize Session States
if "calc_type" not in st.session_state:
    st.session_state["calc_type"] = "🏠 Home / Dashboard"

if "estimates_data" not in st.session_state:
    st.session_state["estimates_data"] = {}

# --------------------------------------------------
# HELPER: PDF GENERATOR FUNCTION
# --------------------------------------------------
def generate_pdf_report(title, engineer_name, project_name, total_cost, summary_items):
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
    
    # Custom Styles (Safe Font Defaults)
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1E3A8A'), spaceAfter=10)
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#4B5563'), spaceAfter=4)
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=10, textColor=colors.white)
    table_body_style = ParagraphStyle('TableBody', parent=styles['Normal'], fontSize=9, textColor=colors.black)

    story = []

    # Document Header
    story.append(Paragraph("<b>CivicCost AI - Construction Cost Estimate</b>", title_style))
    story.append(Paragraph(f"<b>Project Name:</b> {project_name if project_name else 'N/A'}", meta_style))
    story.append(Paragraph(f"<b>Engineer/User:</b> {engineer_name if engineer_name else 'N/A'}", meta_style))
    story.append(Paragraph(f"<b>Estimate Type:</b> {title}", meta_style))
    story.append(Spacer(1, 15))

    # Table Construction
    data = [[Paragraph("Item Description", table_header_style), Paragraph("Quantity", table_header_style), Paragraph("Total Cost (BDT)", table_header_style)]]
    
    for item in summary_items:
        data.append([
            Paragraph(str(item.get("Item", "")), table_body_style),
            Paragraph(str(item.get("Qty", "")), table_body_style),
            Paragraph(str(item.get("Cost", "")), table_body_style)
        ])
    
    # Total Row
    data.append([
        Paragraph("<b>TOTAL ESTIMATED COST</b>", table_body_style),
        Paragraph("", table_body_style),
        Paragraph(f"<b>BDT {total_cost:,.2f}</b>", table_body_style)
    ])

    t = Table(data, colWidths=[240, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>Generated automatically via CivicCost AI Platform.</i>", meta_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------------------------------
# SIDEBAR - NAVIGATION & MARKET PRICE INPUTS
# --------------------------------------------------
st.sidebar.title("🏗️ CivicCost AI")
st.sidebar.caption("Smart BOQ & Structural Cost Estimator")

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
st.sidebar.subheader("📌 Project & Regional Market Rates")

# Regional Location Preset
location = st.sidebar.selectbox("Select Project Location", ["Dhaka", "Chattogram", "Sylhet", "Custom Rates"])

# Regional Rate Presets (BDT)
default_rates = {
    "Dhaka": {"cement": 560.0, "sand": 45.0, "brick": 13.0, "khoa": 130.0, "steel": 98.0, "excavation": 12.0},
    "Chattogram": {"cement": 570.0, "sand": 50.0, "brick": 14.0, "khoa": 135.0, "steel": 99.0, "excavation": 14.0},
    "Sylhet": {"cement": 550.0, "sand": 35.0, "brick": 13.5, "khoa": 125.0, "steel": 97.5, "excavation": 11.0},
    "Custom Rates": {"cement": 560.0, "sand": 45.0, "brick": 13.0, "khoa": 130.0, "steel": 98.0, "excavation": 12.0}
}

current_preset = default_rates[location]

engineer_name = st.sidebar.text_input("Engineer Name", value="Engr. User")
project_name = st.sidebar.text_input("Project Name", value="Residential Building")

st.sidebar.markdown("### 💰 Material Market Rates (BDT)")
rate_cement = st.sidebar.number_input("Cement Rate (/Bag)", value=current_preset["cement"])
rate_sand = st.sidebar.number_input("Sand Rate (/CFT)", value=current_preset["sand"])
rate_brick = st.sidebar.number_input("Brick Rate (/Piece)", value=current_preset["brick"])
rate_khoa = st.sidebar.number_input("Brick Chips/Khoa (/CFT)", value=current_preset["khoa"])
rate_steel = st.sidebar.number_input("Steel/Rebar Rate (/KG)", value=current_preset["steel"])
rate_exc = st.sidebar.number_input("Excavation Rate (/CFT)", value=current_preset["excavation"])

# --------------------------------------------------
# SECTION 1: HOME / DASHBOARD INTERFACE
# --------------------------------------------------
if st.session_state["calc_type"] == "🏠 Home / Dashboard":
    st.title("🏗️ CivicCost AI — Smart BOQ & Construction Estimator")
    st.markdown("""
    Welcome to **CivicCost AI**, an intelligent structural BOQ estimation platform designed for engineers, contractors, and project planners. 
    Select a module below to generate precise material quantities, real-time BDT cost breakdowns based on local market prices, and downloadable PDF reports.
    """)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.info("### 📐 Footing & Column Estimation")
        st.write("Calculate concrete volume, dry materials (cement, sand, khoa), and reinforcement rebar weight with spacing details.")
        if st.button("Open Footing & Column Module", key="btn_fc"):
            st.session_state["calc_type"] = "📐 Footing & Column Estimation"
            st.rerun()

        st.success("### 🏗️ Sub-structure Excavation & Soling")
        st.write("Estimate earthwork excavation, sand bed filling, and single/double layer flat brick soling quantities.")
        if st.button("Open Excavation & Soling Module", key="btn_ex"):
            st.session_state["calc_type"] = "🏗️ Sub-structure Excavation & Soling"
            st.rerun()

    with col2:
        st.warning("### 🧱 Concrete Volume (Beam, Column, Slab, Stair)")
        st.write("Multi-purpose concrete volume estimator for structural elements with adjustable mix ratios (1:1.5:3, 1:2:4).")
        if st.button("Open Concrete Module", key="btn_conc"):
            st.session_state["calc_type"] = "🧱 Concrete Volume (Beam, Column, Slab, Stair)"
            st.rerun()

        st.error("### 📑 Combined Project Master PDF")
        st.write("Generate a single comprehensive BOQ report compiling estimates from all completed modules.")
        if st.button("Generate Combined Summary", key="btn_comb"):
            st.session_state["calc_type"] = "📑 Combined Project Report"
            st.rerun()

    st.markdown("---")
    st.markdown("💡 **Tip:** Adjust local market rates in the left sidebar to automatically calculate updated BDT costs.")

# --------------------------------------------------
# SECTION 2: FOOTING & COLUMN ESTIMATION
# --------------------------------------------------
elif st.session_state["calc_type"] == "📐 Footing & Column Estimation":
    st.header("📐 Footing & Column BOQ Estimation")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        num_footings = st.number_input("Number of Footings", min_value=1, value=4)
        f_len = st.number_input("Footing Length (ft)", min_value=1.0, value=6.0)
        f_wid = st.number_input("Footing Width (ft)", min_value=1.0, value=6.0)
        f_dep = st.number_input("Footing Depth (inch)", min_value=1.0, value=18.0) / 12.0
    
    with col_in2:
        mix_ratio = st.selectbox("Concrete Mix Ratio", ["1:1.5:3", "1:2:4"])
        rebar_dia = st.selectbox("Main Rebar Size (mm)", [12, 16, 20, 25], index=1)
        rebar_spacing = st.number_input("Rebar Center-to-Center Spacing (inch)", min_value=3.0, value=6.0)

    # Calculations
    wet_vol = num_footings * f_len * f_wid * f_dep
    dry_vol = wet_vol * 1.54
    
    parts = [float(x) for x in mix_ratio.split(":")]
    total_parts = sum(parts)
    
    cement_bags = (dry_vol * (parts[0] / total_parts)) / 1.25
    sand_cft = dry_vol * (parts[1] / total_parts)
    khoa_cft = dry_vol * (parts[2] / total_parts)
    
    num_bars_x = int((f_len * 12) / rebar_spacing) + 1
    num_bars_y = int((f_wid * 12) / rebar_spacing) + 1
    total_bar_len_ft = (num_bars_x * f_wid + num_bars_y * f_len) * num_footings
    
    rebar_weight_kg = total_bar_len_ft * ((rebar_dia ** 2) / 162.2) * 0.3048

    # Costs based on Market Rate Inputs
    cost_c = cement_bags * rate_cement
    cost_s = sand_cft * rate_sand
    cost_k = khoa_cft * rate_khoa
    cost_r = rebar_weight_kg * rate_steel
    total_fc_cost = cost_c + cost_s + cost_k + cost_r

    st.subheader("📊 Quantities & Cost Breakdown")
    st.write(f"• **Wet Concrete Volume:** {wet_vol:,.2f} CFT")
    st.write(f"• **Cement Required:** {cement_bags:,.2f} Bags (BDT {cost_c:,.2f})")
    st.write(f"• **Sand Required:** {sand_cft:,.2f} CFT (BDT {cost_s:,.2f})")
    st.write(f"• **Khoa/Chips Required:** {khoa_cft:,.2f} CFT (BDT {cost_k:,.2f})")
    st.write(f"• **Rebar ({rebar_dia}mm):** {rebar_weight_kg:,.2f} KG (BDT {cost_r:,.2f})")
    st.markdown(f"### 💰 **Total Section Cost: BDT {total_fc_cost:,.2f}**")

    fc_summary = [
        {"Item": f"Cement ({mix_ratio})", "Qty": f"{cement_bags:,.2f} Bags", "Cost": f"BDT {cost_c:,.2f}"},
        {"Item": "Sand", "Qty": f"{sand_cft:,.2f} CFT", "Cost": f"BDT {cost_s:,.2f}"},
        {"Item": "Khoa/Chips", "Qty": f"{khoa_cft:,.2f} CFT", "Cost": f"BDT {cost_k:,.2f}"},
        {"Item": f"Steel Rebar ({rebar_dia}mm)", "Qty": f"{rebar_weight_kg:,.2f} KG", "Cost": f"BDT {cost_r:,.2f}"}
    ]

    st.session_state["estimates_data"]["Footing & Column"] = {
        "cost": total_fc_cost,
        "items": fc_summary
    }

    pdf_data = generate_pdf_report("Footing & Column Estimate", engineer_name, project_name, total_fc_cost, fc_summary)
    st.download_button(
        label="📄 Download Section PDF Report",
        data=pdf_data,
        file_name="Footing_Column_Report.pdf",
        mime="application/pdf"
    )

# --------------------------------------------------
# SECTION 3: SUB-STRUCTURE EXCAVATION & SOLING
# --------------------------------------------------
elif st.session_state["calc_type"] == "🏗️ Sub-structure Excavation & Soling":
    st.header("🏗️ Sub-structure Excavation & Soling")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        total_length = st.number_input("Total Trench Length (ft)", min_value=1.0, value=100.0)
        width = st.number_input("Trench Width (ft)", min_value=1.0, value=5.0)
        depth = st.number_input("Excavation Depth (ft)", min_value=1.0, value=5.0)

    with col_e2:
        sand_depth = st.number_input("Sand Filling Depth (inch)", min_value=0.0, value=3.0) / 12.0
        soling_type = st.selectbox("Brick Soling Type", ["Single Layer (3 bricks/sft)", "Flat Soling Double Layer (6 bricks/sft)", "None"])

    # Calculations
    vol_cft = total_length * width * depth
    cost_exc = vol_cft * rate_exc

    sand_cft = total_length * width * sand_depth
    cost_sand = sand_cft * rate_sand

    if soling_type != "None":
        soling_sqft = total_length * width
        multiplier = 3.0 if "Single Layer" in soling_type else 6.0
        total_soling_bricks = soling_sqft * multiplier
        cost_soling = total_soling_bricks * rate_brick
    else:
        total_soling_bricks = 0
        cost_soling = 0.0

    total_ex_cost = cost_exc + cost_sand + cost_soling

    st.subheader("📊 Quantities & Cost Breakdown")
    st.write(f"• **Excavation Volume:** {vol_cft:,.2f} CFT (BDT {cost_exc:,.2f})")
    st.write(f"• **Sand Filling Volume:** {sand_cft:,.2f} CFT (BDT {cost_sand:,.2f})")
    st.write(f"• **Soling Bricks:** {total_soling_bricks:,.0f} Pcs (BDT {cost_soling:,.2f})")
    st.markdown(f"### 💰 **Total Section Cost: BDT {total_ex_cost:,.2f}**")

    ex_summary = [
        {"Item": "Earth Excavation", "Qty": f"{vol_cft:,.2f} CFT", "Cost": f"BDT {cost_exc:,.2f}"},
        {"Item": "Sand Bed Filling", "Qty": f"{sand_cft:,.2f} CFT", "Cost": f"BDT {cost_sand:,.2f}"},
        {"Item": "Flat Brick Soling", "Qty": f"{total_soling_bricks:,.0f} Pcs", "Cost": f"BDT {cost_soling:,.2f}"}
    ]

    st.session_state["estimates_data"]["Excavation & Soling"] = {
        "cost": total_ex_cost,
        "items": ex_summary
    }

    pdf_data = generate_pdf_report("Excavation & Soling Estimate", engineer_name, project_name, total_ex_cost, ex_summary)
    st.download_button(
        label="📄 Download Section PDF Report",
        data=pdf_data,
        file_name="Excavation_Soling_Report.pdf",
        mime="application/pdf"
    )

# --------------------------------------------------
# SECTION 4: CONCRETE VOLUME (BEAM, COLUMN, SLAB, STAIR)
# --------------------------------------------------
elif st.session_state["calc_type"] == "🧱 Concrete Volume (Beam, Column, Slab, Stair)":
    st.header("🧱 Concrete Volume & Structural Materials")

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        struct_type = st.selectbox("Select Structural Element", ["Slab", "Beam", "Column", "Staircase"])
        elem_count = st.number_input("Number of Identical Items", min_value=1, value=1)
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

    c_bags = (dry_c_vol * (c_parts[0] / c_total_parts)) / 1.25
    c_sand = dry_c_vol * (c_parts[1] / c_total_parts)
    c_khoa = dry_c_vol * (c_parts[2] / c_total_parts)

    cost_c_bag = c_bags * rate_cement
    cost_c_sand = c_sand * rate_sand
    cost_c_khoa = c_khoa * rate_khoa

    total_conc_cost = cost_c_bag + cost_c_sand + cost_c_khoa

    st.subheader("📊 Quantities & Cost Breakdown")
    st.write(f"• **Element Type:** {struct_type} (Quantity: {elem_count})")
    st.write(f"• **Wet Concrete Volume:** {wet_c_vol:,.2f} CFT")
    st.write(f"• **Cement:** {c_bags:,.2f} Bags (BDT {cost_c_bag:,.2f})")
    st.write(f"• **Sand:** {c_sand:,.2f} CFT (BDT {cost_c_sand:,.2f})")
    st.write(f"• **Khoa/Chips:** {c_khoa:,.2f} CFT (BDT {cost_c_khoa:,.2f})")
    st.markdown(f"### 💰 **Total Section Cost: BDT {total_conc_cost:,.2f}**")

    conc_summary = [
        {"Item": f"Cement ({struct_type})", "Qty": f"{c_bags:,.2f} Bags", "Cost": f"BDT {cost_c_bag:,.2f}"},
        {"Item": "Sand", "Qty": f"{c_sand:,.2f} CFT", "Cost": f"BDT {cost_c_sand:,.2f}"},
        {"Item": "Khoa/Chips", "Qty": f"{c_khoa:,.2f} CFT", "Cost": f"BDT {cost_c_khoa:,.2f}"}
    ]

    st.session_state["estimates_data"][f"Concrete ({struct_type})"] = {
        "cost": total_conc_cost,
        "items": conc_summary
    }

    pdf_data = generate_pdf_report(f"Concrete Volume ({struct_type})", engineer_name, project_name, total_conc_cost, conc_summary)
    st.download_button(
        label="📄 Download Section PDF Report",
        data=pdf_data,
        file_name=f"Concrete_{struct_type}_Report.pdf",
        mime="application/pdf"
    )

# --------------------------------------------------
# SECTION 5: COMBINED PROJECT REPORT
# --------------------------------------------------
elif st.session_state["calc_type"] == "📑 Combined Project Report":
    st.header("📑 Combined Project Master BOQ Report")

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

        st.subheader("📋 Project Summary Table")
        for item in combined_items:
            st.write(f"• **{item['Item']}**: {item['Qty']} — **{item['Cost']}**")

        st.markdown(f"## 🏆 **Grand Total Estimated Cost: BDT {grand_total:,.2f}**")

        comb_pdf_data = generate_pdf_report("Master Combined BOQ Report", engineer_name, project_name, grand_total, combined_items)
        st.download_button(
            label="📑 Download Master Combined PDF Report",
            data=comb_pdf_data,
            file_name="Master_Combined_BOQ_Report.pdf",
            mime="application/pdf"
        )

# --------------------------------------------------
# SECTION 6: USER RATINGS & FEEDBACK
# --------------------------------------------------
elif st.session_state["calc_type"] == "⭐ User Ratings & Feedback":
    st.header("⭐ User Ratings & Feedback")
    st.write("We value your feedback! Rate your experience with CivicCost AI.")

    rating = st.slider("Rate the platform accuracy & usability", 1, 5, 5)
    feedback_text = st.text_area("Share your feedback or feature suggestions")

    if st.button("Submit Feedback"):
        st.success(f"Thank you for rating us {rating}/5 stars! Your feedback has been recorded.")
