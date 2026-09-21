import streamlit as st
import pandas as pd
from fpdf import FPDF

# Page Configuration
st.set_page_config(
    page_title="CiviCost AI",
    page_icon="🏗️",
    layout="wide"
)

# Function to generate PDF Reports
# Helper function to sanitize special characters
def clean_text(text):
    if isinstance(text, str):
        return text.replace("৳", "BDT ").replace("—", "-").replace("–", "-").encode('latin-1', 'replace').decode('latin-1')
    return str(text)

# Function to generate PDF Reports
def generate_pdf(project_title, summary_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    
    # Title
    pdf.cell(0, 10, clean_text(project_title), ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Estimation Summary & Cost Breakdown", ln=True)
    pdf.ln(3)
    
    # Table Header
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(70, 8, "Item / Material", border=1, fill=True)
    pdf.cell(60, 8, "Quantity", border=1, fill=True)
    pdf.cell(60, 8, "Estimated Cost (BDT)", border=1, fill=True, ln=True)
    
    # Table Body
    pdf.set_font("Helvetica", "", 10)
    for row in summary_data:
        # Handle both dictionary and list/tuple rows safely
        if isinstance(row, dict):
            item = clean_text(str(row.get("Item", "")))
            qty = clean_text(str(row.get("Quantity", "")))
            cost = clean_text(str(row.get("Cost (BDT)", row.get("Cost", ""))))
        elif isinstance(row, (list, tuple)):
            item = clean_text(str(row[0])) if len(row) > 0 else ""
            qty = clean_text(str(row[1])) if len(row) > 1 else ""
            cost = clean_text(str(row[2])) if len(row) > 2 else ""
        else:
            item, qty, cost = "", "", ""
        
        pdf.cell(70, 8, item, border=1)
        pdf.cell(60, 8, qty, border=1)
        pdf.cell(60, 8, cost, border=1, ln=True)
        
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, "Generated automatically by CiviCost AI Assistant - BNBC 2020 Compliant", ln=True, align="C")
    
    return bytes(pdf.output())


# ==========================================
# 1. Sidebar Navigation & Market Rates
# ==========================================
st.sidebar.title("📌 Navigation")
calc_type = st.sidebar.selectbox(
    "Choose Calculation Type:",
   [
            "Home / Overview",
            "Excavation & Soling Estimator",
            "Concrete Volume & Material Calculator",
            "Rebar (Steel) Calculator",
            "Brickwork Estimator",
            "Plastering Estimator"
        ]
)

st.sidebar.divider()
st.sidebar.subheader("⚙️ Local Market Rates (BDT)")

# Dynamic Material Price Inputs with Default Bangladesh Rates
price_cement = st.sidebar.number_input("Cement Price (per bag - BDT)", value=550.0, step=5.0)
price_sand = st.sidebar.number_input("Sand Price (per CFT - BDT)", value=45.0, step=1.0)
price_aggregate = st.sidebar.number_input("Coarse Aggregate Price (per CFT - BDT)", value=120.0, step=2.0)
price_rebar = st.sidebar.number_input("Steel/Rebar Price (per KG - BDT)", value=98.0, step=1.0)
price_brick = st.sidebar.number_input("Brick Price (per Piece - BDT)", value=12.5, step=0.5)


# ==========================================
# 2. Home / Overview Section
# ==========================================
if calc_type == "Home / Overview":
    st.title("🏗️ Welcome to CiviCost AI")
    st.subheader("Smart Structural Material & Cost Estimation Assistant")
    
    st.markdown("""
    **CiviCost AI** is a specialized civil engineering tool designed for fast and accurate structural material estimation according to **BNBC 2020** guidelines. It helps site engineers, contractors, and home builders calculate material quantities and total estimated costs in BDT.
    """)
    
    st.divider()
    
    # Active Market Price Metrics
    st.markdown("### 💵 Active Market Rates")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Cement", f"BDT {price_cement:.0f}/bag")
    m2.metric("Sand", f"BDT {price_sand:.0f}/cft")
    m3.metric("Aggregate", f"BDT {price_aggregate:.0f}/cft")
    m4.metric("Steel", f"BDT {price_rebar:.0f}/kg")
    m5.metric("Brick", f"BDT {price_brick:.1f}/pc")
    
    st.caption("💡 *You can adjust these material rates anytime using the sidebar on the left.*")
    
    st.divider()
    
  # Feature Overview Cards
    st.markdown("### 🛠️ Available Estimator Modules")
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        #### ⛏️ Excavation & Soling Estimator
        - Earthwork excavation volume & safety allowance.
        - Single & Double Flat Brick Soling (FBS) count.
        - Lean Concrete (CC) breakdown & backfilling volume.
        """)

        st.info("""
        #### 🧱 Concrete Mix Estimator
        - Supports Slabs, Beams, Columns, Footings & Staircases.
        - Includes standard concrete grades (M10, M15, M20, M25).
        - Generates Cement (Bags), Sand (CFT), Aggregate (CFT) & Water (L) breakdowns.
        """)
        
        st.info("""
        #### 🧱 Brickwork & Mortar Estimator
        - Wall thickness selections (5'', 10'', 3'').
        - Door & Window opening deduction options.
        - Mortar mix ratios (1:4, 1:5, 1:6) & wastage allowance.
        """)

    with col2:
        st.success("""
        #### ⚙️ Rebar (Steel) Estimator
        - BSTI standard bar diameters (8mm to 32mm).
        - d²/533 weight calculation in KG and Metric Tons.
        - Standard 12-meter commercial bar count calculator.
        """)
        
        st.success("""
        #### 🖌️ Wall & Ceiling Plaster Estimator
        - Inner wall, outer wall, and ceiling plaster ratios (1:3, 1:4, 1:5, 1:6).
        - Thickness conversion (0.25'', 0.5'', 0.75'') and material cost breakdown.
        """)

    st.caption("👉 *Select a calculator module from the sidebar menu to begin estimation.*")
        
        st.success("""
        #### 🖌️ Wall & Ceiling Plaster Estimator
        - Inner wall, outer wall, and ceiling plaster ratios (1:3, 1:4, 1:5, 1:6).
        - Thickness conversion (0.25'', 0.5'', 0.75'') and material cost breakdown.
        """)

    st.caption("👈 *Select a calculator module from the sidebar menu to begin estimation.*")

# ==========================================
# Excavation & Soling Estimator
# ==========================================
elif calc_type == "Excavation & Soling Estimator":
    st.subheader("⛏️ Excavation, Soling & Backfilling Estimator")
    st.write("Calculate earthwork excavation volume, flat brick soling (FBS), lean CC, and backfilling requirements.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 📐 Pit / Trench Dimensions")
        num_pits = st.number_input("Number of Identical Pits / Footings", min_value=1, value=10, step=1)
        pit_length = st.number_input("Length of Pit (Ft)", min_value=0.1, value=6.0, step=0.5)
        pit_width = st.number_input("Width of Pit (Ft)", min_value=0.1, value=6.0, step=0.5)
        pit_depth = st.number_input("Depth of Excavation (Ft)", min_value=0.1, value=5.0, step=0.5)
        
        st.markdown("##### 📐 Soling & CC Details")
        soling_layers = st.selectbox("Brick Soling Type", ["Single Flat Brick Soling (FBS)", "Double Layer Soling"])
        cc_thickness = st.number_input("Lean Concrete / CC Thickness (Inches)", min_value=0.0, value=3.0, step=0.5)
        cc_ratio = st.selectbox("Lean Concrete Mix Ratio (Cement : Sand : Aggregate)", ["1:3:6", "1:4:8", "1:2:4"])

    with col2:
        st.markdown("##### 🧱 Concrete Footing Volume (For Backfilling Calculation)")
        footing_length = st.number_input("Concrete Footing Length (Ft)", min_value=0.0, value=5.0, step=0.5)
        footing_width = st.number_input("Concrete Footing Width (Ft)", min_value=0.0, value=5.0, step=0.5)
        footing_depth = st.number_input("Concrete Footing Depth/Height (Ft)", min_value=0.0, value=1.5, step=0.25)
        
        st.markdown("##### 🚜 Additional Settings")
        working_space = st.number_input("Extra Working Space / Safety Allowance (%)", min_value=0.0, value=5.0, step=1.0)
        price_soil = st.number_input("Backfilling Soil / Sand Price (per CFT - BDT)", min_value=0.0, value=18.0, step=1.0)

    st.divider()

    if st.button("Calculate Earthwork & Soling"):
        # Safe material rate fetches from sidebar variables or defaults
        p_cement = globals().get("price_cement", 550.0)
        p_sand = globals().get("price_sand", 45.0)
        p_brick = globals().get("price_brick", globals().get("price_bricks", 12.0))
        p_agg = globals().get("price_aggregate", globals().get("price_khoa", 130.0))

        # 1. Total Excavation Calculation
        raw_excavation_cft = pit_length * pit_width * pit_depth * num_pits
        total_excavation_cft = raw_excavation_cft * (1 + working_space / 100)
        
        # 2. Flat Brick Soling Calculation (Standard BNBC: 3.15 bricks per sq.ft for single flat layer)
        pit_area_sqft = pit_length * pit_width * num_pits
        bricks_per_sqft = 3.15 if soling_layers == "Single Flat Brick Soling (FBS)" else 6.30
        total_soling_bricks = pit_area_sqft * bricks_per_sqft
        
        # 3. Lean Concrete (CC) Calculation
        cc_thickness_ft = cc_thickness / 12.0
        cc_wet_volume = pit_area_sqft * cc_thickness_ft
        cc_dry_volume = cc_wet_volume * 1.54 # Dry volume factor
        
        ratio_parts = [float(x) for x in cc_ratio.split(":")]
        sum_ratio = sum(ratio_parts)
        
        c_part, s_part, a_part = ratio_parts[0], ratio_parts[1], ratio_parts[2]
        
        cc_cement_cft = (cc_dry_volume * c_part) / sum_ratio
        cc_cement_bags = cc_cement_cft / 1.25
        cc_sand_cft = (cc_dry_volume * s_part) / sum_ratio
        cc_agg_cft = (cc_dry_volume * a_part) / sum_ratio
        
        # 4. Backfilling Volume Calculation
        footing_concrete_vol = footing_length * footing_width * footing_depth * num_pits
        soling_vol = pit_area_sqft * (0.25 if soling_layers == "Single Flat Brick Soling (FBS)" else 0.5)
        backfilling_cft = total_excavation_cft - (footing_concrete_vol + cc_wet_volume + soling_vol)
        backfilling_cft = max(0.0, backfilling_cft)
        
        # Cost Calculations
        cost_bricks = total_soling_bricks * p_brick
        cost_cc_cement = cc_cement_bags * p_cement
        cost_cc_sand = cc_sand_cft * p_sand
        cost_cc_agg = cc_agg_cft * p_agg
        cost_cc_total = cost_cc_cement + cost_cc_sand + cost_cc_agg
        cost_backfill = backfilling_cft * price_soil
        
        total_estimated_cost = cost_bricks + cost_cc_total + cost_backfill
        
        # --- DISPLAY RESULTS ---
        st.success("✅ Earthwork & Soling Estimation Completed!")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Excavation", f"{total_excavation_cft:,.2f} CFT")
        m2.metric("Soling Bricks", f"{total_soling_bricks:,.0f} Pcs")
        m3.metric("Lean CC Cement", f"{cc_cement_bags:,.2f} Bags")
        m4.metric("Backfill Volume", f"{backfilling_cft:,.2f} CFT")

        st.divider()
        st.markdown("### 📊 Detailed Breakdown & Material Quantities")
        
        summary_df = pd.DataFrame({
            "Item / Material": [
                "Total Excavation Volume (with safety margin)",
                "Flat Brick Soling (FBS)",
                "Lean CC Cement",
                "Lean CC Sand",
                "Lean CC Coarse Aggregate",
                "Backfilling Soil/Sand"
            ],
            "Quantity": [
                f"{total_excavation_cft:,.2f} CFT",
                f"{total_soling_bricks:,.0f} Pcs",
                f"{cc_cement_bags:,.2f} Bags",
                f"{cc_sand_cft:,.2f} CFT",
                f"{cc_agg_cft:,.2f} CFT",
                f"{backfilling_cft:,.2f} CFT"
            ],
            "Cost (BDT)": [
                "N/A (Labor/Machine)",
                f"BDT {cost_bricks:,.2f}",
                f"BDT {cost_cc_cement:,.2f}",
                f"BDT {cost_cc_sand:,.2f}",
                f"BDT {cost_cc_agg:,.2f}",
                f"BDT {cost_backfill:,.2f}"
            ]
        })
        
        st.table(summary_df)
        st.subheader(f"💰 Total Material Cost: BDT {total_estimated_cost:,.2f}")
        
        # PDF Generation Data Preparation
        pdf_report_data = [
            {"Item": row["Item / Material"], "Quantity": row["Quantity"], "Cost (BDT)": row["Cost (BDT)"]}
            for _, row in summary_df.iterrows()
        ]
        
        pdf_bytes = generate_pdf("Excavation & Soling Estimation", pdf_report_data)
        st.download_button(
            label="📄 Download Excavation Report (PDF)",
            data=pdf_bytes,
            file_name="Excavation_Soling_Report.pdf",
            mime="application/pdf"
        )

# 1. Concrete Calculator
if calc_type == "Concrete Volume & Material Calculator":
    st.subheader("🧱 Concrete Mix & Material Estimator")
    
    # Structural Member Selection
    element_type = st.radio(
        "Select Structural Element:",
        ["Slab", "Beam", "Column", "Footing", "Staircase"],
        horizontal=True
    )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        length = st.number_input("Length (ft)", min_value=0.1, value=10.0, step=0.5)
    with col2:
        width = st.number_input("Width (ft)", min_value=0.1, value=10.0, step=0.5)
    with col3:
        thickness = st.number_input("Thickness / Depth (inches)", min_value=0.1, value=5.0, step=0.5)
    with col4:
        num_elements = st.number_input("Number of Elements", min_value=1, value=1, step=1)
        
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        concrete_grade = st.selectbox(
            "Concrete Grade (Mix Ratio)",
            [
                "M10 — 1:3:6 (PCC / Lean Concrete)",
                "M15 — 1:2:4 (General RCC Work)",
                "M20 — 1:1.5:3 (Standard RCC Member)",
                "M25 — 1:1:2 (Heavy Structural RCC)"
            ],
            index=1
        )
    with col_g2:
        wastage_pct = st.slider("Concrete Wastage (%)", min_value=0, max_value=15, value=5)
        
    cement_price = st.sidebar.number_input("Cement Price (per bag - BDT)", value=550)
    sand_price = st.sidebar.number_input("Sand Price (per CFT - BDT)", value=45)
    chips_price = st.sidebar.number_input("Coarse Aggregate Price (per CFT - BDT)", value=120)

    if st.button("Calculate Concrete", type="primary"):
        # Single element wet volume in CFT
        single_wet_vol = length * width * (thickness / 12.0)
        total_wet_vol = single_wet_vol * num_elements
        
        # Dry volume calculation with wastage
        dry_vol = total_wet_vol * 1.54
        dry_vol += dry_vol * (wastage_pct / 100.0)
        
        # Extract ratio numbers from selected string
        ratio_str = concrete_grade.split("—")[1].split("(")[0].strip()
        c_r, s_r, a_r = map(float, ratio_str.split(":"))
        total_ratio = c_r + s_r + a_r
        
        cement_cft = (c_r / total_ratio) * dry_vol
        cement_bags = cement_cft / 1.25
        sand_cft = (s_r / total_ratio) * dry_vol
        chips_cft = (a_r / total_ratio) * dry_vol
        
        # Water calculation (approx 25 liters per bag of cement)
        water_liters = cement_bags * 25
        
        total_cost = (cement_bags * cement_price) + (sand_cft * sand_price) + (chips_cft * chips_price)

        st.success(f"**Total Concrete Volume ({num_elements} {element_type}s):** {total_wet_vol:.2f} CFT (Includes {wastage_pct}% Wastage)")
        
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Cement Required", f"{cement_bags:.2f} Bags")
        m2.metric("Sand Required", f"{sand_cft:.2f} CFT")
        m3.metric("Aggregate Required", f"{chips_cft:.2f} CFT")
        m4.metric("Water Needed", f"{water_liters:.0f} Liters")
        m5.metric("Estimated Cost", f"BDT {total_cost:,.2f}")
        
        # PDF Generation
        report_data = {
            "Element Type": f"{element_type} (Qty: {num_elements})",
            "Concrete Grade": concrete_grade,
            "Total Wet Volume": f"{total_wet_vol:.2f} CFT",
            "Wastage Percentage": f"{wastage_pct}%",
            "Cement Required": f"{cement_bags:.2f} Bags",
            "Sand Required": f"{sand_cft:.2f} CFT",
            "Coarse Aggregate Required": f"{chips_cft:.2f} CFT",
            "Water Required": f"~{water_liters:.0f} Liters",
            "Estimated Total Cost": f"BDT {total_cost:,.2f}"
        }
        pdf_bytes = generate_pdf(f"Concrete Mix Estimation ({element_type})", report_data)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name=f"concrete_{element_type.lower()}_report.pdf",
            mime="application/pdf"
        )

# 2. Rebar (Steel) Calculator
elif calc_type == "Rebar (Steel) Calculator":
    st.subheader("⚙️ Rebar (Steel) Quantity, Weight & BBS Estimator")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        bar_dia = st.selectbox(
            "Bar Diameter (mm)",
            [8, 10, 12, 16, 20, 22, 25, 28, 32],
            index=3,
            help="Select BSTI standard rebar size in mm"
        )
    with col2:
        num_bars = st.number_input("Number of Bars / Pieces", min_value=1, value=10, step=1)
    with col3:
        input_mode = st.radio("Length Unit Mode", ["Custom Length (ft)", "Standard 12m Bars (40 ft)"], horizontal=True)

    if input_mode == "Custom Length (ft)":
        length_per_bar = st.number_input("Length per Bar (ft)", min_value=0.1, value=39.5, step=0.5)
    else:
        length_per_bar = 39.37  # Standard 12 meter length

    steel_price_per_kg = st.sidebar.number_input("Steel Price (per kg - BDT)", value=98.0)
    wastage_pct = st.sidebar.slider("Rebar Cutting Wastage & Lapping (%)", min_value=0, max_value=15, value=5)

    if st.button("Calculate Rebar", type="primary"):
        total_length_ft = length_per_bar * num_bars
        
        # Formula: Weight per foot (kg/ft) = d^2 / 533
        weight_per_ft = (bar_dia ** 2) / 533.0
        
        base_weight_kg = total_length_ft * weight_per_ft
        total_weight_kg = base_weight_kg + (base_weight_kg * wastage_pct / 100.0)
        
        total_weight_ton = total_weight_kg / 1000.0
        total_cost = total_weight_kg * steel_price_per_kg
        
        # Calculate full 12m length rod count equivalent
        full_rods_equivalent = (total_length_ft * (1 + wastage_pct/100.0)) / 39.37

        st.success(f"**Total Rebar Length:** {total_length_ft:.2f} ft (Includes {wastage_pct}% Wastage/Lapping)")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Weight (KG)", f"{total_weight_kg:.2f} Kg")
        c2.metric("Total Weight (Tons)", f"{total_weight_ton:.3f} Ton")
        c3.metric("Standard 12m Rods", f"~{int(round(full_rods_equivalent))} Nos")
        c4.metric("Estimated Steel Cost", f"BDT {total_cost:,.2f}")
        
        # PDF Generation
        report_data = {
            "Bar Diameter": f"{bar_dia} mm",
            "Number of Pieces": f"{num_bars} Nos",
            "Length per Bar": f"{length_per_bar:.2f} ft",
            "Total Length": f"{total_length_ft:.2f} ft",
            "Wastage Allowed": f"{wastage_pct}%",
            "Total Weight (Kg)": f"{total_weight_kg:.2f} Kg",
            "Total Weight (Tons)": f"{total_weight_ton:.3f} Ton",
            "Equivalent 12m Rods": f"~{int(round(full_rods_equivalent))} Nos",
            "Estimated Total Cost": f"BDT {total_cost:,.2f}"
        }
        pdf_bytes = generate_pdf("Rebar (Steel) Quantity Estimation", report_data)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="rebar_estimation_report.pdf",
            mime="application/pdf"
        )
# 3. Brickwork Calculator
elif calc_type == "Brickwork Estimator":
    st.subheader("🧱 Brickwork & Mortar Estimator")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        wall_length = st.number_input("Wall Length (ft)", min_value=0.1, value=20.0, step=0.5)
    with col2:
        wall_height = st.number_input("Wall Height (ft)", min_value=0.1, value=10.0, step=0.5)
    with col3:
        wall_thick = st.selectbox("Wall Thickness", ["5 inch (Single Brick)", "10 inch (Double / Outer Wall)", "3 inch (Partition Wall)"])

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        mortar_ratio = st.selectbox("Mortar Mix Ratio (Cement : Sand)", ["1:4 (Rich Mix)", "1:5 (Standard)", "1:6 (Lean Mix)"], index=1)
    with col_b:
        openings_area = st.number_input("Deduct Openings (Doors/Windows Sq. Ft.)", min_value=0.0, value=0.0, step=5.0)
    with col_c:
        wastage_pct = st.slider("Brick Wastage (%)", min_value=0, max_value=15, value=5)

    brick_price = st.sidebar.number_input("Price per Brick (BDT)", value=12.5)
    cement_price = st.sidebar.number_input("Cement Price (per bag - BDT)", value=550)
    sand_price = st.sidebar.number_input("Sand Price (per CFT - BDT)", value=45)

    if st.button("Calculate Brickwork", type="primary"):
        # Wall Area Calculation
        gross_area = wall_length * wall_height
        net_area = max(0.0, gross_area - openings_area)
        
        # Wall Thickness in feet
        if "5 inch" in wall_thick:
            thick_ft = 5.0 / 12.0
            bricks_per_sqft = 5.0  # Standard BD estimate for 5" wall
        elif "10 inch" in wall_thick:
            thick_ft = 10.0 / 12.0
            bricks_per_sqft = 10.0 # Standard BD estimate for 10" wall
        else:
            thick_ft = 3.0 / 12.0
            bricks_per_sqft = 3.5

        # Total Bricks calculation with wastage
        base_bricks = net_area * bricks_per_sqft
        total_bricks = int(base_bricks + (base_bricks * wastage_pct / 100.0))

        # Mortar Dry Volume calculation (Approx 30% of total wall volume)
        wall_volume = net_area * thick_ft
        wet_mortar_vol = wall_volume * 0.30
        dry_mortar_vol = wet_mortar_vol * 1.33

        # Mortar Mix Ratio split
        ratio_parts = mortar_ratio.split("(")[0].strip().split(":")
        c_part = float(ratio_parts[0])
        s_part = float(ratio_parts[1])
        total_parts = c_part + s_part

        cement_cft = (c_part / total_parts) * dry_mortar_vol
        cement_bags = cement_cft / 1.25
        sand_cft = (s_part / total_parts) * dry_mortar_vol

        # Costing
        cost_bricks = total_bricks * brick_price
        cost_cement = cement_bags * cement_price
        cost_sand = sand_cft * sand_price
        total_cost = cost_bricks + cost_cement + cost_sand

        st.success(f"**Net Wall Area:** {net_area:.2f} Sq. Ft. (Gross: {gross_area:.2f} sq.ft, Deducted: {openings_area} sq.ft)")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Bricks Needed", f"{total_bricks:,} Nos")
        c2.metric("Cement Required", f"{cement_bags:.2f} Bags")
        c3.metric("Sand Required", f"{sand_cft:.2f} CFT")
        c4.metric("Estimated Cost", f"BDT {total_cost:,.2f}")

        # PDF Generation
        report_data = {
            "Gross Wall Area": f"{gross_area:.2f} Sq. Ft.",
            "Openings Deducted": f"{openings_area:.2f} Sq. Ft.",
            "Net Wall Area": f"{net_area:.2f} Sq. Ft.",
            "Wall Thickness": wall_thick,
            "Mortar Ratio": mortar_ratio,
            "Wastage Allowed": f"{wastage_pct}%",
            "Bricks Required": f"{total_bricks:,} Nos",
            "Cement Required": f"{cement_bags:.2f} Bags",
            "Sand Required": f"{sand_cft:.2f} CFT",
            "Estimated Total Cost": f"BDT {total_cost:,.2f}"
        }
        pdf_bytes = generate_pdf("Brickwork Estimation", report_data)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="brickwork_report.pdf",
            mime="application/pdf"
        )
# 4. Plastering Calculator
elif calc_type == "Plastering Estimator":
    st.subheader("🖌️ Wall & Ceiling Plastering Estimator")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        plaster_area = st.number_input("Plaster Area (Sq. Ft.)", min_value=1.0, value=500.0)
    with col2:
        plaster_thick = st.selectbox("Plaster Thickness", ["0.5 inch (12 mm)", "0.75 inch (18 mm)", "0.25 inch (6 mm)"])
    with col3:
        mix_ratio = st.selectbox("Mix Ratio (Cement : Sand)", ["1:3 (Ceiling)", "1:4 (Outer Wall)", "1:5 (Inner Wall)", "1:6 (Inner Wall)"])
        
    cement_price = st.sidebar.number_input("Cement Price (per bag - BDT)", value=550)
    sand_price = st.sidebar.number_input("Sand Price (per CFT - BDT)", value=45)
    wastage_pct = st.sidebar.slider("Plaster Wastage (%)", min_value=0, max_value=15, value=5)

    if st.button("Calculate Plaster", type="primary"):
        # Thickness conversion
        if "0.25" in plaster_thick:
            thick_ft = 0.25 / 12.0
        elif "0.5" in plaster_thick:
            thick_ft = 0.5 / 12.0
        else:
            thick_ft = 0.75 / 12.0
            
        wet_vol = plaster_area * thick_ft
        dry_vol = wet_vol * 1.33  # Dry volume multiplier
        
        # Add wastage
        dry_vol += dry_vol * (wastage_pct / 100.0)
        
        # Ratio Calculation
        ratio_parts = mix_ratio.split("(")[0].strip().split(":")
        c_part = float(ratio_parts[0])
        s_part = float(ratio_parts[1])
        total_parts = c_part + s_part
        
        cement_cft = (c_part / total_parts) * dry_vol
        cement_bags = cement_cft / 1.25
        sand_cft = (s_part / total_parts) * dry_vol
        
        total_cost = (cement_bags * cement_price) + (sand_cft * sand_price)
        
        st.success(f"**Total Plaster Area:** {plaster_area} Sq. Ft. (Wastage Included: {wastage_pct}%)")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Cement Required", f"{cement_bags:.2f} Bags")
        c2.metric("Sand Required", f"{sand_cft:.2f} CFT")
        c3.metric("Estimated Material Cost", f"BDT {total_cost:,.2f}")
        
        # PDF Generation
        report_data = {
            "Plaster Area": f"{plaster_area} Sq. Ft.",
            "Thickness": plaster_thick,
            "Mix Ratio": mix_ratio,
            "Wastage Allowance": f"{wastage_pct}%",
            "Cement Required": f"{cement_bags:.2f} Bags",
            "Sand Required": f"{sand_cft:.2f} CFT",
            "Estimated Total Cost": f"BDT {total_cost:,.2f}"
        }
        pdf_bytes = generate_pdf("Plastering Estimation", report_data)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="plastering_report.pdf",
            mime="application/pdf"
        )
