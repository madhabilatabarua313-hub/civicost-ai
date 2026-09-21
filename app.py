import io
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
st.set_page_config(page_title="CiviCost AI - Structural Estimator", layout="wide", page_icon="🏗️")

def generate_pdf_report(title, engineer_name, total_cost, summary_items):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title & Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, title)
    p.setFont("Helvetica", 10)
    p.drawString(
        50, height - 65, "--------------------------------------------------"
    )

    # Engineer Name
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, height - 85, f"Prepared By (Engineer): {engineer_name}")
    p.setFont("Helvetica", 10)
    p.drawString(
        50, height - 95, "--------------------------------------------------"
    )

    # Details
    y = height - 125
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Details:")
    y -= 20

    p.setFont("Helvetica", 10)
    for line in summary_items:
        p.drawString(60, y, f"• {line}")
        y -= 18

    # Total Cost
    y -= 10
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total Estimated Cost: BDT {total_cost:,.2f}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
# ---------------------------------------------------------
# INITIALIZE SESSION STATES (Avoids KeyError)
# ---------------------------------------------------------
default_keys = [
    "excavation_summary", "soling_summary", "concrete_summary", 
    "rebar_summary", "brickwork_summary", "plaster_summary", "formwork_summary", "user_ratings"
]
for key in default_keys:
    if key not in st.session_state:
        if key == "user_ratings":
            st.session_state[key] = []
        else:
            st.session_state[key] = 0.0

if "calc_type" not in st.session_state:
    st.session_state["calc_type"] = "🏠 Project Control Center (Home)"

# Helper function for text/report rendering
def get_download_report(title, details_dict, total_cost):
    report_text = f"=========================================\n"
    report_text += f" CIVICOST AI - {title.upper()}\n"
    report_text += f"=========================================\n\n"
    for k, v in details_dict.items():
        report_text += f"{k}: {v}\n"
        report_text += "-" * 41 + "\n"
    report_text += f"\nTOTAL ESTIMATED COST: BDT {total_cost:,.2f}\n"
    report_text += f"=========================================\n"
    return report_text

# Navigation Callback
def set_nav(page_name):
    st.session_state["calc_type"] = page_name

# ---------------------------------------------------------
# SIDEBAR: NAVIGATION & MARKET RATES
# ---------------------------------------------------------
st.sidebar.title("📌 Navigation")
st.sidebar.subheader("📌 Project Details")
engineer_name = st.sidebar.text_input("Engineer Name", value="Engr. Madhabilata Barua")
nav_options = [
    "🏠 Project Control Center (Home)",
    "⛏️ Excavation & Soling",
    "🧱 Concrete Volume (Beam, Column, Slab, Stair)",
    "🔩 Rebar (Steel)",
    "🧱 Brickwork Estimator",
    "🎨 Plastering Estimator",
    "🪵 Formwork & Shuttering",
    "📊 Master Summary & PDF Report",
    "⭐ User Rating & Feedback"
]

calc_type = st.sidebar.radio(
    "Choose Calculation Type:",
    nav_options,
    index=nav_options.index(st.session_state["calc_type"]) if st.session_state["calc_type"] in nav_options else 0,
    key="nav_radio"
)
st.session_state["calc_type"] = calc_type

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Local Market Rates (BDT)")

excavation_rate = st.sidebar.number_input("Earth Excavation (BDT / CFT)", value=8.0)
backfill_rate = st.sidebar.number_input("Earth Backfilling (BDT / CFT)", value=4.0)
brick_price = st.sidebar.number_input("First Class Brick (BDT / Pc)", value=12.5)
cement_price = st.sidebar.number_input("Cement Bag (BDT / Bag)", value=550.0)
sand_price = st.sidebar.number_input("FM 1.5 Sand (BDT / CFT)", value=38.0)
brick_chip_price = st.sidebar.number_input("Brick Chips / Stone (BDT / CFT)", value=115.0)
rod_price = st.sidebar.number_input("60-Grade Rebar (BDT / Kg)", value=95.0)

# ---------------------------------------------------------
# 1. HOME / CONTROL CENTER (Quick Link Cards)
# ---------------------------------------------------------
if st.session_state["calc_type"] == "🏠 Project Control Center (Home)":
    st.title("🏗️ CiviCost AI - Structural Estimator Dashboard")
    st.markdown("Select a module below or use the sidebar menu to quickly jump to any estimation tool.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### ⛏️ Sub-Structure")
        st.write("Excavation, Sand Cushion & Soling")
        if st.button("Open Excavation Calculator", key="btn_ex"):
            set_nav("⛏️ Excavation & Soling")
            st.rerun()

        st.info("### 🔩 Steel Reinforcement")
        st.write("Structural Rebar & Binding Wire")
        if st.button("Open Rebar Calculator", key="btn_st"):
            set_nav("🔩 Rebar (Steel)")
            st.rerun()

    with col2:
        st.success("### 🧱 Concrete Works")
        st.write("Beams, Columns, Slabs & Stairs")
        if st.button("Open Concrete Calculator", key="btn_cn"):
            set_nav("🧱 Concrete Volume (Beam, Column, Slab, Stair)")
            st.rerun()

        st.success("### 🎨 Plastering")
        st.write("Internal & External Surface Plaster")
        if st.button("Open Plaster Calculator", key="btn_pl"):
            set_nav("🎨 Plastering Estimator")
            st.rerun()

    with col3:
        st.warning("### 🧱 Brick Masonry")
        st.write("5\"/10\" Walls & Opening Deductions")
        if st.button("Open Brickwork Calculator", key="btn_bw"):
            set_nav("🧱 Brickwork Estimator")
            st.rerun()

        st.warning("### 🪵 Formwork & Shuttering")
        st.write("Plywood, Props & Shuttering Area")
        if st.button("Open Formwork Calculator", key="btn_fw"):
            set_nav("🪵 Formwork & Shuttering")
            st.rerun()

    st.markdown("---")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        if st.button("📊 Go to Master Summary", use_container_width=True):
            set_nav("📊 Master Summary & PDF Report")
            st.rerun()
    with m_col2:
        if st.button("⭐ Rate & Review App", use_container_width=True):
            set_nav("⭐ User Rating & Feedback")
            st.rerun()

# ---------------------------------------------------------
# 2. EXCAVATION & SOLING ESTIMATOR
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "⛏️ Excavation & Soling":
    st.header("⛏️ Excavation, Soling & Sand Filling Estimator")

    ex_col1, ex_col2 = st.columns(2)
    with ex_col1:
        footing_count = st.number_input("Number of Footings / Trenches", min_value=1, value=5)
        ex_len = st.number_input("Trench Length (ft)", min_value=0.0, value=6.0, key="ex_l")
        ex_wid = st.number_input("Trench Width (ft)", min_value=0.0, value=6.0, key="ex_w")
        ex_dep = st.number_input("Excavation Depth (ft)", min_value=0.0, value=5.0, key="ex_d")
    with ex_col2:
        sand_thick = st.number_input("Sand Cushion Thickness (inch)", min_value=0.0, value=3.0, step=0.5)
        soling_type = st.selectbox("Soling Type", ["Brick Flat Soling (BFS)", "Herringbone Bond Soling (HBB)"], index=0)
        backfill_pct = st.slider("Backfilling Volume (% of excavation)", min_value=0, max_value=80, value=40)

    excavation_vol_cft = (ex_len * ex_wid * ex_dep) * footing_count
    soling_area_sqft = (ex_len * ex_wid) * footing_count
    sand_vol_cft = soling_area_sqft * (sand_thick / 12.0)
    backfill_vol_cft = excavation_vol_cft * (backfill_pct / 100.0)

    bricks_per_sqft = 3.00 if "Flat" in soling_type else 3.75
    total_soling_bricks = soling_area_sqft * bricks_per_sqft

    cost_excavation = excavation_vol_cft * excavation_rate
    cost_backfill = backfill_vol_cft * backfill_rate
    cost_sand = sand_vol_cft * sand_price
    cost_soling_bricks = total_soling_bricks * brick_price
    total_ex_soling_cost = cost_excavation + cost_backfill + cost_sand + cost_soling_bricks
    
    st.session_state["excavation_summary"] = cost_excavation + cost_backfill
    st.session_state["soling_summary"] = cost_sand + cost_soling_bricks

    st.markdown("---")
    st.subheader("📊 Sub-Structure Results")
    r_c1, r_c2, r_c3, r_c4 = st.columns(4)
    with r_c1: st.metric("Excavation Vol", f"{excavation_vol_cft:,.2f} CFT", f"BDT {cost_excavation:,.2f}")
    with r_c2: st.metric("Backfilling Vol", f"{backfill_vol_cft:,.2f} CFT", f"BDT {cost_backfill:,.2f}")
    with r_c3: st.metric("Sand Cushion", f"{sand_vol_cft:,.2f} CFT", f"BDT {cost_sand:,.2f}")
    with r_c4: st.metric("Soling Bricks", f"{total_soling_bricks:,.0f} Pcs", f"BDT {cost_soling_bricks:,.2f}")

    # PDF Breakdown Summary Items
ex_summary_items = [
    f"Total Footings/Trenches: {footing_count}",
    (
        "Excavation Volume:"
        f" {excavation_vol_cft:.2f} CFT (BDT {cost_excavation:,.2f})"
    ),
    (
        "Backfilling Volume:"
        f" {backfill_vol_cft:.2f} CFT (BDT {cost_backfill:,.2f})"
    ),
    f"Sand Cushion Volume: {sand_vol_cft:.2f} CFT (BDT {cost_sand:,.2f})",
    (
        "Soling Bricks:"
        f" {total_soling_bricks:.0f} Pcs (BDT {cost_soling_bricks:,.2f})"
    ),
]

# PDF Generation
ex_pdf = generate_pdf_report(
    title="Excavation & Soling Estimate",
    engineer_name=engineer_name,
    total_cost=total_ex_soling_cost,
    summary_items=ex_summary_items,
)

# PDF Download Button
    st.download_button("Download Section Report (.pdf)", ex_pdf, "Excavation_Report.pdf", "application/pdf")

# 3. ADVANCED CONCRETE VOLUME (Beam, Column, Slab, Stair)
# --------------------------------------------------
elif st.session_state["calc_type"] == "🧱 Concrete Volume (Beam, Column, Slab, Stair)":
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        elem_count = st.number_input("Number of Items/Count", min_value=1, value=1)
        if struct_type in ["Slab / Footing", "Beam"]:
            c_len = st.number_input("Length (ft)", min_value=0.0, value=20.0)
            c_wid = st.number_input("Width / Beam Depth (in ft)", min_value=0.0, value=10.0)
            c_dep = st.number_input("Thickness / Depth (ft)", min_value=0.0, value=0.5)
        elif struct_type == "Column":
            c_len = st.number_input("Column Width (inch)", min_value=0.0, value=12.0) / 12.0
            c_wid = st.number_input("Column Depth (inch)", min_value=0.0, value=15.0) / 12.0
            c_dep = st.number_input("Column Height (ft)", min_value=0.0, value=10.0)
        elif struct_type == "Staircase":
            steps_cnt = st.number_input("Number of Steps", min_value=1, value=10)
            tread_in = st.number_input("Tread Width (inch)", value=10.0) / 12.0
            riser_in = st.number_input("Riser Height (inch)", value=6.0) / 12.0
            stair_width = st.number_input("Stair Flight Width (ft)", value=3.5)
            waist_slab = st.number_input("Waist Slab Thickness (inch)", value=6.0) / 12.0

    with c_col2:
        mix_ratio = st.selectbox("Mix Ratio (Cement : Sand : Aggregate)", 
                                 ["1:1.5:3 (M20 - Standard RCC)", "1:2:4 (M15 - General RCC)", "1:3:6 (M10 - Plain Concrete)"], index=0)
        dry_vol_factor = st.number_input("Dry Volume Factor", min_value=1.3, max_value=1.6, value=1.54, step=0.01)
        c_wastage = st.number_input("Wastage (%)", min_value=0.0, max_value=10.0, value=2.0)

    # Volume Calculations
    if struct_type != "Staircase":
        wet_vol = (c_len * c_wid * c_dep) * elem_count
    else:
        step_vol = 0.5 * tread_in * riser_in * stair_width * steps_cnt
        waist_len = ((steps_cnt * tread_in)**2 + (steps_cnt * riser_in)**2)**0.5
        waist_vol = waist_len * stair_width * waist_slab
        wet_vol = (step_vol + waist_vol) * elem_count

    wet_vol_total = wet_vol * (1 + c_wastage / 100.0)
    dry_vol = wet_vol_total * dry_vol_factor

    r_c, r_s, r_a = (1.0, 1.5, 3.0) if "1:1.5:3" in mix_ratio else ((1.0, 2.0, 4.0) if "1:2:4" in mix_ratio else (1.0, 3.0, 6.0))
    sum_ratio = r_c + r_s + r_a

    cement_bags = (((r_c / sum_ratio) * dry_vol) / 1.25)
    sand_cft = (r_s / sum_ratio) * dry_vol
    agg_cft = (r_a / sum_ratio) * dry_vol

    cost_cement = cement_bags * cement_price
    cost_sand = sand_cft * sand_price
    cost_agg = agg_cft * brick_chip_price
    total_concrete_cost = cost_cement + cost_sand + cost_agg

    st.session_state["concrete_summary"] = total_concrete_cost

    st.markdown("---")
    st.subheader(f"📊 Concrete Estimation Results ({struct_type})")
    st.info(f"📐 Total Wet Volume: **{wet_vol:,.2f} CFT** | Dry Volume: **{dry_vol:,.2f} CFT**")

    res_c1, res_c2, res_c3 = st.columns(3)
    with res_c1: st.metric("Cement Required", f"{cement_bags:,.2f} Bags", f"BDT {cost_cement:,.2f}")
    with res_c2: st.metric("Sand Required", f"{sand_cft:,.2f} CFT", f"BDT {cost_sand:,.2f}")
    with res_c3: st.metric("Aggregate Required", f"{agg_cft:,.2f} CFT", f"BDT {cost_agg:,.2f}")

    st.success(f"💰 Total Concrete Cost: BDT {total_concrete_cost:,.2f}")

  # Concrete PDF Summary Items
conc_summary_items = [
    f"Element Type: {struct_type}",
    f"Total Count: {elem_count}",
    f"Wet Volume: {wet_vol:.2f} CFT",
    f"Dry Volume: {dry_vol:.2f} CFT",
    f"Cement Requirement: {cement_bags:.2f} Bags (BDT {cost_cement:,.2f})",
    f"Sand Requirement: {sand_cft:.2f} CFT (BDT {cost_sand:,.2f})",
    f"Aggregate Requirement: {agg_cft:.2f} CFT (BDT {cost_agg:,.2f})",
]

# Concrete PDF Generation
conc_pdf = generate_pdf_report(
    title=f"Concrete Estimate ({struct_type})",
    engineer_name=engineer_name,
    total_cost=total_concrete_cost,
    summary_items=conc_summary_items,
)

# PDF Download Button
st.download_button(
    label="📄 Download Section Report (.pdf)",
    data=conc_pdf,
    file_name=f"Concrete_Report_{struct_type}.pdf",
    mime="application/pdf",
)

# ---------------------------------------------------------
# 4. REINFORCEMENT STEEL (REBAR)
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "🔩 Rebar (Steel)":
    st.header("🔩 Reinforcement Steel (Rebar) Estimator")

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        total_conc_vol = st.number_input("Total Concrete Volume for Steel (CFT)", min_value=0.0, value=200.0)
        steel_ratio = st.slider("Steel Ratio (%)", min_value=0.5, max_value=4.0, value=1.5, step=0.1)
    with r_col2:
        binding_wire_rate = st.number_input("Binding Wire (Kg per Ton Rebar)", min_value=0.0, value=7.0)

    conc_vol_cum = total_conc_vol * 0.0283168
    steel_weight_kg = (conc_vol_cum * (steel_ratio / 100.0)) * 7850.0
    steel_weight_ton = steel_weight_kg / 1000.0
    binding_wire_kg = steel_weight_ton * binding_wire_rate
    steel_cost = steel_weight_kg * rod_price
    
    st.session_state["rebar_summary"] = steel_cost

    st.markdown("---")
    st.subheader("📊 Rebar Estimation Results")
    st_c1, st_c2, st_c3 = st.columns(3)
    with st_c1: st.metric("Total Rebar Weight", f"{steel_weight_kg:,.2f} Kg", f"{steel_weight_ton:,.3f} Ton")
    with st_c2: st.metric("Binding Wire Needed", f"{binding_wire_kg:,.2f} Kg", "18-20 Gauge Wire")
    with st_c3: st.metric("Total Rebar Cost", f"BDT {steel_cost:,.2f}", f"@ {rod_price} BDT/Kg")

    st.success(f"💰 Total Steel Cost: BDT {steel_cost:,.2f}")

   # Rebar/Steel PDF Summary Items
steel_summary_items = [
    (
        f"Rebar Weight: {steel_weight_kg:,.2f} Kg"
        f" ({steel_weight_ton:,.3f} Ton)"
    ),
    f"Binding Wire: {binding_wire_kg:,.2f} Kg",
    f"Unit Rate: BDT {rod_price}/Kg",
]

# Rebar PDF Generation
steel_pdf = generate_pdf_report(
    title="Steel Rebar Estimate",
    engineer_name=engineer_name,
    total_cost=steel_cost,
    summary_items=steel_summary_items,
)

# PDF Download Button
st.download_button(
    label="📄 Download Section Report (.pdf)",
    data=steel_pdf,
    file_name="Rebar_Report.pdf",
    mime="application/pdf",
)

# ---------------------------------------------------------
# 5. BRICKWORK ESTIMATOR WITH OPENING DEDUCTIONS
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "🧱 Brickwork Estimator":
    st.header("🧱 Brickwork & Wall Estimator")

    b_col1, b_col2 = st.columns(2)
    with b_col1:
        wall_count = st.number_input("Number of Identical Walls", min_value=1, value=1)
        w_len = st.number_input("Wall Length (ft)", min_value=0.0, value=20.0)
        w_height = st.number_input("Wall Height (ft)", min_value=0.0, value=10.0)
        w_thick = st.selectbox("Wall Thickness", ["5 inch (Single Brick)", "10 inch (Double Brick)"], index=0)
    with b_col2:
        st.subheader("🚪 Openings Deduction")
        door_cnt = st.number_input("Number of Doors", min_value=0, value=1)
        door_size = st.number_input("Door Area (Sq.Ft per door)", value=21.0)
        win_cnt = st.number_input("Number of Windows", min_value=0, value=2)
        win_size = st.number_input("Window Area (Sq.Ft per window)", value=12.0)
        b_ratio = st.selectbox("Mortar Mix Ratio", ["1:4 (Rich)", "1:5 (Standard)", "1:6 (General)"], index=1)

    gross_area = (w_len * w_height) * wall_count
    total_deduction = (door_cnt * door_size) + (win_cnt * win_size)
    net_wall_area = max(0.0, gross_area - total_deduction)

    bricks_per_sqft = 5.0 if "5 inch" in w_thick else 10.0
    total_bricks = net_wall_area * bricks_per_sqft

    wall_vol_cft = net_wall_area * (0.4167 if "5 inch" in w_thick else 0.8333)
    mortar_dry_vol = (wall_vol_cft * 0.30) * 1.54

    mc, ms = (1.0, 4.0) if "1:4" in b_ratio else ((1.0, 5.0) if "1:5" in b_ratio else (1.0, 6.0))
    b_cement_bags = ((mc / (mc + ms)) * mortar_dry_vol) / 1.25
    b_sand_cft = (ms / (mc + ms)) * mortar_dry_vol

    cost_b = total_bricks * brick_price
    cost_c = b_cement_bags * cement_price
    cost_s = b_sand_cft * sand_price
    total_bw_cost = cost_b + cost_c + cost_s

    st.session_state["brickwork_summary"] = total_bw_cost

    st.markdown("---")
    st.subheader("📊 Brickwork Estimation Breakdown")
    st.info(f"📐 Gross Area: **{gross_area:,.2f} Sq.Ft** | Deductions: **{total_deduction:,.2f} Sq.Ft** | Net Wall Area: **{net_wall_area:,.2f} Sq.Ft**")

    bw_c1, bw_c2, bw_c3 = st.columns(3)
    with bw_c1: st.metric("Number of Bricks", f"{total_bricks:,.0f} Pcs", f"BDT {cost_b:,.2f}")
    with bw_c2: st.metric("Mortar Cement", f"{b_cement_bags:,.2f} Bags", f"BDT {cost_c:,.2f}")
    with bw_c3: st.metric("Mortar Sand", f"{b_sand_cft:,.2f} CFT", f"BDT {cost_s:,.2f}")

    st.success(f"💰 Total Brickwork Cost: BDT {total_bw_cost:,.2f}")

   # Brickwork PDF Summary Items
bw_summary_items = [
    f"Net Wall Area: {net_wall_area:,.2f} Sq. Ft",
    f"Total Bricks: {total_bricks:,.0f} Pcs (BDT {cost_b:,.2f})",
    f"Mortar Cement: {b_cement_bags:,.2f} Bags (BDT {cost_c:,.2f})",
    f"Mortar Sand: {b_sand_cft:,.2f} CFT (BDT {cost_s:,.2f})",
]

# Brickwork PDF Generation
bw_pdf = generate_pdf_report(
    title="Brickwork Estimate",
    engineer_name=engineer_name,
    total_cost=total_bw_cost,
    summary_items=bw_summary_items,
)

# PDF Download Button
st.download_button(
    label="📄 Download Section Report (.pdf)",
    data=bw_pdf,
    file_name="Brickwork_Report.pdf",
    mime="application/pdf",
)

# ---------------------------------------------------------
# 6. PLASTERING ESTIMATOR
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "🎨 Plastering Estimator":
    st.header("🎨 Plastering Estimator")

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        p_area = st.number_input("Surface Area to Plaster (Sq. Ft)", min_value=0.0, value=300.0)
        both_sides = st.checkbox("Plaster Both Sides of Wall", value=False)
        p_thick = st.selectbox("Plaster Thickness (mm)", [6, 12, 18, 20], index=1)
    with p_col2:
        p_mix = st.selectbox("Plaster Mortar Ratio", ["1:3 (Rich)", "1:4 (Standard)", "1:6 (Rough)"], index=1)

    effective_area = p_area * 2 if both_sides else p_area
    p_dry_vol = (effective_area * ((p_thick / 25.4) / 12.0)) * 1.35

    pc, ps = (1.0, 3.0) if "1:3" in p_mix else ((1.0, 4.0) if "1:4" in p_mix else (1.0, 6.0))
    p_cement_bags = ((pc / (pc + ps)) * p_dry_vol) / 1.25
    p_sand_cft = (ps / (pc + ps)) * p_dry_vol

    p_cost_c = p_cement_bags * cement_price
    p_cost_s = p_sand_cft * sand_price
    total_plaster_cost = p_cost_c + p_cost_s

    st.session_state["plaster_summary"] = total_plaster_cost

    st.markdown("---")
    st.subheader("📊 Plaster Estimation Breakdown")
    pl_c1, pl_c2, pl_c3 = st.columns(3)
    with pl_c1: st.metric("Effective Plaster Area", f"{effective_area:,.2f} Sq.Ft", f"Thickness: {p_thick} mm")
    with pl_c2: st.metric("Cement Required", f"{p_cement_bags:,.2f} Bags", f"BDT {p_cost_c:,.2f}")
    with pl_c3: st.metric("Sand Required", f"{p_sand_cft:,.2f} CFT", f"BDT {p_cost_s:,.2f}")

    st.success(f"💰 Total Plastering Cost: BDT {total_plaster_cost:,.2f}")

 # Plastering PDF Summary Items
plaster_summary_items = [
    f"Effective Area: {effective_area:,.2f} Sq. Ft",
    f"Plaster Thickness: {p_thick} mm",
    f"Plaster Cement: {p_cement_bags:,.2f} Bags (BDT {p_cost_c:,.2f})",
    f"Plaster Sand: {p_sand_cft:,.2f} CFT (BDT {p_cost_s:,.2f})",
]

# Plastering PDF Generation
plaster_pdf = generate_pdf_report(
    title="Plastering Estimate",
    engineer_name=engineer_name,
    total_cost=total_plaster_cost,
    summary_items=plaster_summary_items,
)

# PDF Download Button
st.download_button(
    label="📄 Download Section Report (.pdf)",
    data=plaster_pdf,
    file_name="Plastering_Report.pdf",
    mime="application/pdf",
)

# ---------------------------------------------------------
# 7. FORMWORK & SHUTTERING ESTIMATOR
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "🪵 Formwork & Shuttering":
    st.header("🪵 Formwork & Shuttering Estimator")

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        shutter_area = st.number_input("Shuttering Contact Area (Sq. Ft)", min_value=0.0, value=250.0)
    with s_col2:
        reusability = st.number_input("Estimated Re-uses per Sheet", min_value=1, max_value=20, value=5)
        shutter_rate_sqft = st.number_input("Shuttering Rate (BDT / Sq. Ft)", min_value=0.0, value=45.0)

    plywood_sheets = (shutter_area / 32.0) / reusability
    formwork_cost = shutter_area * shutter_rate_sqft

    st.session_state["formwork_summary"] = formwork_cost

    st.markdown("---")
    st.subheader("📊 Formwork & Shuttering Breakdown")
    sh_c1, sh_c2 = st.columns(2)
    with sh_c1: st.metric("Plywood Sheets Equivalent", f"{plywood_sheets:,.1f} Sheets", f"Based on {reusability} re-uses")
    with sh_c2: st.metric("Total Shuttering Cost", f"BDT {formwork_cost:,.2f}", f"@ {shutter_rate_sqft} BDT/Sq.Ft")

    st.success(f"💰 Total Formwork Cost: BDT {formwork_cost:,.2f}")

  # Formwork PDF Summary Items
fw_summary_items = [
    f"Shuttering Area: {shutter_area:,.2f} Sq. Ft",
    f"Plywood Sheets Equivalent: {plywood_sheets:,.1f} Sheets",
    f"Unit Rate: BDT {shutter_rate_sqft}/Sq. Ft",
]

# Formwork PDF Generation
fw_pdf = generate_pdf_report(
    title="Formwork & Shuttering Estimate",
    engineer_name=engineer_name,
    total_cost=formwork_cost,
    summary_items=fw_summary_items,
)

# PDF Download Button
st.download_button(
    label="📄 Download Section Report (.pdf)",
    data=fw_pdf,
    file_name="Formwork_Report.pdf",
    mime="application/pdf",
)

# ---------------------------------------------------------
# 8. MASTER SUMMARY & PDF REPORT
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "📊 Master Summary & PDF Report":
    st.header("📊 Master Summary & Cost Consolidation")

    summary_data = {
        "Work Category": [
            "Earth Excavation & Backfilling",
            "Sand Filling & Brick Soling",
            "Concrete Works (RCC/PCC)",
            "Steel Reinforcement (Rebar)",
            "Brickwork & Masonry",
            "Plastering Finishing",
            "Formwork & Shuttering"
        ],
        "Estimated Cost (BDT)": [
            st.session_state.get("excavation_summary", 0.0),
            st.session_state.get("soling_summary", 0.0),
            st.session_state.get("concrete_summary", 0.0),
            st.session_state.get("rebar_summary", 0.0),
            st.session_state.get("brickwork_summary", 0.0),
            st.session_state.get("plaster_summary", 0.0),
            st.session_state.get("formwork_summary", 0.0)
        ]
    }

    df_summary = pd.DataFrame(summary_data)
    total_project_cost = df_summary["Estimated Cost (BDT)"].sum()

    st.table(df_summary)
    st.markdown(f"### **Total Estimated Project Cost: BDT {total_project_cost:,.2f}**")

  # Master PDF Summary Items Creation
master_summary_items = [
    f"{row['Work Category']}: BDT {row['Estimated Cost (BDT)']:,.2f}"
    for _, row in df_summary.iterrows()
]

# Master PDF Generation
master_pdf = generate_pdf_report(
    title="Master Cost Consolidation Report",
    engineer_name=engineer_name,
    total_cost=total_project_cost,
    summary_items=master_summary_items,
)

# PDF Download Button
st.download_button(
    label="📄 Download Master Summary Report (.pdf)",
    data=master_pdf,
    file_name="Master_Project_Report.pdf",
    mime="application/pdf",
)

# ---------------------------------------------------------
# 9. USER RATING & FEEDBACK SYSTEM
# ---------------------------------------------------------
elif st.session_state["calc_type"] == "⭐ User Rating & Feedback":
    st.header("⭐ User Rating & Feedback System")
    st.markdown("We value your feedback! Please rate your experience using CiviCost AI.")

    u_name = st.text_input("Your Name / Organization")
    rating = st.slider("Rating (1 = Poor, 5 = Excellent)", min_value=1, max_value=5, value=5)
    feedback_text = st.text_area("Write your feedback or feature requests:")

    if st.button("Submit Feedback", type="primary"):
        if u_name.strip() != "":
            st.session_state["user_ratings"].append({"Name": u_name, "Rating": f"{'⭐'*rating}", "Feedback": feedback_text})
            st.success("Thank you for your rating and feedback!")
        else:
            st.warning("Please enter your name before submitting.")

    st.markdown("---")
    st.subheader("💬 Recent User Feedback")
    if len(st.session_state["user_ratings"]) > 0:
        for fb in reversed(st.session_state["user_ratings"]):
            st.markdown(f"**{fb['Name']}** ({fb['Rating']})")
            st.write(f"_{fb['Feedback']}_")
            st.markdown("---")
    else:
        st.write("No ratings submitted yet. Be the first to leave feedback!")
