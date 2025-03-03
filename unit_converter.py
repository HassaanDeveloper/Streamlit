import streamlit as st

# Set page configuration
st.set_page_config(page_title="Universal Unit Converter", page_icon="📏", layout="wide")

# Custom CSS for dark mode and styling
st.markdown("""
    <style>
        body { background-color: #121212; color: white; }
        .stTextInput, .stSelectbox, .stNumberInput { border-radius: 10px; }
        .stButton>button { border-radius: 10px; background-color: #00cc99; color: white; }
        .stButton>button:hover { background-color: #009977; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📏 Universal Unit Converter")

# Conversion factors
conversion_factors = {
    "Length": {
        "Meters": 1, 
        "Kilometers": 1000, 
        "Centimeters": 0.01, 
        "Millimeters": 0.001,
        "Miles": 1609.34, 
        "Yards": 0.9144, 
        "Feet": 0.3048, 
        "Inches": 0.0254
    },
    "Weight": {
        "Kilograms": 1, 
        "Grams": 0.001, 
        "Milligrams": 0.000001, 
        "Pounds": 0.453592, 
        "Ounces": 0.0283495
    },
    "Temperature": {
        "Celsius": 1, 
        "Fahrenheit": 1, 
        "Kelvin": 1
    },
    "Volume": {
        "Liters": 1, 
        "Milliliters": 0.001, 
        "Cubic Meters": 1000, 
        "Gallons (US)": 3.78541,
        "Quarts (US)": 0.946353, 
        "Pints (US)": 0.473176, 
        "Cups (US)": 0.236588, 
        "Fluid Ounces (US)": 0.0295735
    },
    "Time": {
        "Seconds": 1, 
        "Minutes": 60, 
        "Hours": 3600, 
        "Days": 86400, 
        "Weeks": 604800,
        "Months": 2629746, 
        "Years": 31556952
    }
}

# Sidebar for category selection
category = st.sidebar.selectbox("📂 Select Category", list(conversion_factors.keys()))

# Main layout
col1, col2, col3 = st.columns([1, 1, 0.3])

with col1:
    value = st.number_input("🔢 Enter Value", min_value=0.0, value=1.0)
    from_unit = st.selectbox("🔄 From Unit", list(conversion_factors[category].keys()))

with col2:
    to_unit = st.selectbox("🎯 To Unit", list(conversion_factors[category].keys()))

with col3:
    if st.button("🔀 Swap Units"):
        from_unit, to_unit = to_unit, from_unit

# Conversion Logic
def convert_units(value, from_unit, to_unit, category):
    # Check if the conversion category is Temperature
    if category == "Temperature":
        
        # Converting from Celsius
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return (value * 9/5) + 32  # Celsius to Fahrenheit formula
            elif to_unit == "Kelvin":
                return value + 273.15  # Celsius to Kelvin formula
            else:
                return value  # If converting to the same unit, return the value as is

        # Converting from Fahrenheit
        if from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9  # Fahrenheit to Celsius formula
            elif to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15  # Fahrenheit to Kelvin formula
            else:
                return value  # If converting to the same unit, return the value as is

        # Converting from Kelvin
        if from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15  # Kelvin to Celsius formula
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32  # Kelvin to Fahrenheit formula
            else:
                return value  # If converting to the same unit, return the value as is
    else:
        base_value = value * conversion_factors[category][from_unit]
        return base_value / conversion_factors[category][to_unit]

# Perform conversion dynamically
result = convert_units(value, from_unit, to_unit, category)

# Display result
st.success(f"**Result:** {value:.2f} {from_unit} = {result:.2f} {to_unit}")

# Store conversion history
if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append(f"{value:.2f} {from_unit} ➝ {result:.2f} {to_unit}")

# Show conversion history
st.markdown("### 📜 Conversion History")
st.write(st.session_state.history[-5:])  # Show last 5 conversions

# Footer
st.markdown("---")
st.markdown("🎉 **Made by Hassaan using Streamlit**")
