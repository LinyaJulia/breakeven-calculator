import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and instruction
st.title('Breakeven Calculator')

# New section for breakeven calculation
st.header('Breakeven Point Calculator')

# Input Fixed Costs, Selling Price per Unit, and Variable Cost per Unit
fixed_costs = st.number_input('Enter Fixed Costs', min_value=0.0, step=0.01)
selling_price_per_unit = st.number_input('Enter Selling Price per Unit', min_value=0.0, step=0.01)
variable_cost_per_unit = st.number_input('Enter Variable Cost per Unit', min_value=0.0, step=0.01)

if st.button('Calculate Breakeven Point'):
    # Calculate breakeven point in units
    if selling_price_per_unit > variable_cost_per_unit:
        breakeven_units = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
        breakeven_revenue = breakeven_units * selling_price_per_unit
        
        st.metric(label="Breakeven Point (Units)", value=f"{breakeven_units:.2f} units")
        st.metric(label="Breakeven Point (Revenue)", value=f"${breakeven_revenue:.2f}")
    else:
        st.error("Selling Price per Unit must be greater than Variable Cost per Unit to achieve a breakeven point.")

st.divider()

st.header('Breakeven Graph Creator')

# Input Initial Investment and Yearly Cash Flows
initial_investment = st.number_input('Enter Initial Investment', min_value=0.0, step=0.01)
years = st.slider('Select Number of Years', min_value=1, max_value=20, value=5)

# Create input fields for each year's cash flow
cash_flows = []
for year in range(1, years + 1):
    cash_flow = st.number_input(f'Enter Cash Flow for Year {year}', min_value=0.0, step=0.01)
    cash_flows.append(cash_flow)

# Prepare the data for the DataFrame
data = {
    'Year': list(range(1, years + 1)),
    'Cash Flow': cash_flows,
    'Initial Investment': [initial_investment] + [None] * (years - 1)
}

# Create a DataFrame from the input data
df = pd.DataFrame(data)

# Function to plot the chart
def plot_chart(df):
    initial_investment = df['Initial Investment'][0]  # Assumes the first row contains initial investment
    years = df['Year'].tolist()
    cash_flows = df['Cash Flow'].tolist()

    # Calculating cumulative cash flow
    cumulative_cash_flow = []
    cumulative = 0
    for cash in cash_flows:
        cumulative += cash
        cumulative_cash_flow.append(cumulative)

    # Find the break-even point with decimal precision
    break_even_year = None
    for i in range(1, len(cumulative_cash_flow)):
        if cumulative_cash_flow[i-1] < initial_investment <= cumulative_cash_flow[i]:
            # Linear interpolation
            break_even_year = years[i-1] + (initial_investment - cumulative_cash_flow[i-1]) / (cumulative_cash_flow[i] - cumulative_cash_flow[i-1])
            break

    # Display the break-even point
    if break_even_year:
        st.metric(label="Break-Even Year", value=f"Year {break_even_year:.2f}", delta=None, delta_color="inverse")
    else:
        st.metric(label="Break-Even Year", value="No break-even within the given years", delta=None, delta_color="off")

    # Creating the plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, cumulative_cash_flow, marker='o', label='Cumulative Cash Flow')
    plt.axhline(y=initial_investment, color='r', linestyle='--', label='Initial Investment')
    plt.title('Investment Payback Period')
    plt.xlabel('Year')
    plt.ylabel('Cumulative Cash Flow')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Display the editable DataFrame with default data
st.header('Editable DataFrame')
edited_df = st.data_editor(df, use_container_width=True)

if st.button('Update Chart'):
    st.divider()
    plot_chart(edited_df)
