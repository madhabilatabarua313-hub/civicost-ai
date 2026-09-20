import streamlit as st

# Page Configuration
st.set_page_config(
    page_page_title="CiviCost AI",
    page_icon="🏗️",
    layout="wide"
)

# Title & Subtitle
st.title("🏗️ CiviCost AI - Civil Engineering Assistant")
st.write("Calculate construction materials, estimation, and cost projections accurately.")

# Sidebar Navigation
st.sidebar.header("📌 Select Calculator")
calc_type = st.sidebar.selectbox(
    "Choose a calculation:",
    ["Concrete Volume & Cement/Sand/Aggregate", "Brickwork Estimation", "Plastering Estimation"]
)

st.divider()

# 1. Concrete Volume & Materials Calculator
if calc_type == "Concrete Volume & Cement/Sand/Aggregate":
    st.subheader("🧱 Concrete Material Calculator (1 : 2 : 4 Ratio)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Length (ft)", min_value=0.1, value=10.0, step=0.5)
    with col2:
        width = st.number_input("Width (ft)", min_value=0.1, value=10.0, step=0.5)
    with col3:
        thickness = st.number_input("Thickness / Height (inches)", min_value=0.1, value=5.0, step=0.5)
        
    cement_price = st.sidebar.number_input("Cement Price per Bag (BDT)", value=550)
    sand_price = st.sidebar.number_input("Sand Price per Cft (BDT)", value=45)
    brick_chips_price = st.sidebar.number_input("Khoa/Aggregate Price per Cft (BDT)", value=120)

    if st.button("Calculate Concrete Materials", type="primary"):
        # Wet Volume in CFT
        wet_vol = length * width * (thickness / 12.0)
        # Dry Volume (1.54 multiplier)
        dry_vol = wet_vol * 1.54
        
        # Ratio 1:2:4 -> Sum = 7
        total_ratio = 1 + 2 + 4
        cement_cft = (1 / total_ratio) * dry_vol
        cement_bags = cement_cft / 1.25  # 1 bag cement = 1.25 cft
        sand_cft = (2 / total_ratio) * dry_vol
        chips_cft = (4 / total_ratio) * dry_vol
        
        total_cost = (cement_bags * cement_price) + (sand_cft * sand_price) + (chips_cft * brick_chips_price)

        st.success(f"**Total Concrete Volume (Wet):** {wet_vol:.2f} CFT")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cement Required", f"{cement_bags:.2f} Bags")
        m2.metric("Sand Required", f"{sand_cft:.2f} CFT")
        m3.metric("Aggregate/Khoa", f"{chips_cft:.2f} CFT")
        m4.metric("Estimated Material Cost", f"৳ {total_cost:,.2f}")

# 2. Brickwork Calculator
elif calc_type == "Brickwork Estimation":
    st.subheader("🧱 Brickwork & Mortar Estimator")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        wall_length = st.number_input("Wall Length (ft)", min_value=0.1, value=20.0)
    with col2:
        wall_height = st.number_input("Wall Height (ft)", min_value=0.1, value=10.0)
    with col3:
        wall_thickness = st.selectbox("Wall Thickness", ["5 inch", "10 inch"])
        
    brick_unit_price = st.sidebar.number_input("Price per Brick (BDT)", value=12.5)

    if st.button("Calculate Brickwork", type="primary"):
        wall_area = wall_length * wall_height
        
        if wall_thickness == "5 inch":
            total_bricks = wall_area * 5  # Standard approx 5 bricks/sqft for 5" wall
        else:
            total_bricks = wall_area * 10 # Standard approx 10 bricks/sqft for 10" wall
            
        brick_cost = total_bricks * brick_unit_price
        
        st.success(f"**Total Wall Area:** {wall_area:.2f} Sq. Ft.")
        
        c1, c2 = st.columns(2)
        c1.metric("Total Bricks Needed", f"{int(total_bricks)} Pcs")
        c2.metric("Estimated Brick Cost", f"৳ {brick_cost:,.2f}")

# 3. Plastering Estimation
elif calc_type == "Plastering Estimation":
    st.subheader("🖌️ Wall Plaster Material Estimator (1:4 Ratio)")
    
    col1, col2 = st.columns(2)
    with col1:
        plaster_area = st.number_input("Plaster Area (Sq. Ft.)", min_value=1.0, value=500.0)
    with col2:
        plaster_thick = st.selectbox("Plaster Thickness", ["0.5 inch (12 mm)", "0.75 inch (18 mm)"])

    if st.button("Calculate Plaster", type="primary"):
        thick_ft = 0.5 / 12.0 if "0.5" in plaster_thick else 0.75 / 12.0
        wet_vol = plaster_area * thick_ft
        dry_vol = wet_vol * 1.33 # Plaster dry volume factor
        
        # 1:4 ratio sum = 5
        cement_cft = (1 / 5) * dry_vol
        cement_bags = cement_cft / 1.25
        sand_cft = (4 / 5) * dry_vol
        
        st.success(f"**Total Plaster Area:** {plaster_area} Sq. Ft.")
        
        c1, c2 = st.columns(2)
        c1.metric("Cement Needed", f"{cement_bags:.2f} Bags")
        c2.metric("Sand Needed", f"{sand_cft:.2f} CFT")
