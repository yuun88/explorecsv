import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("CSV Data Analysis")

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)
    for col_name in df.columns: 
        if col_name.lower() == 'email':
            df.pop(col_name)
    
    header_list = df.columns.unique()
    header_selection = st.multiselect('Select columns', header_list, ['user_id'])

    df_selection = df[header_selection]
    
    # Display the DataFrame for editing
    edited_df = st.data_editor(df_selection, num_rows="dynamic")
    
    # Filter out 'user_id' from the columns for the selectbox
    columns_for_selectbox = [col for col in edited_df.columns if col != 'user_id']
    
    # Selectbox for user to choose the X-axis column
    x_axis_column = st.selectbox("Attribute to analyse", columns_for_selectbox)
    
    # Ensure the selected column and 'user_id' columns exist in the DataFrame
    if x_axis_column in edited_df.columns and 'user_id' in edited_df.columns:
        # Aggregate the data if necessary (e.g., count of user_id per selected column)
        aggregated_data = edited_df.groupby(x_axis_column)['user_id'].count().reset_index()
        
        # Rename columns for clarity
        aggregated_data.columns = [x_axis_column, 'user_id_count']
        
        # Create a bar chart using Matplotlib
        fig, ax = plt.subplots()
        ax.bar(aggregated_data[x_axis_column], aggregated_data['user_id_count'])
        ax.set_xlabel(x_axis_column)
        ax.set_ylabel('User ID Count')
        ax.set_title(f'Bar Chart of {x_axis_column} vs User ID Count')
        plt.xticks(rotation=90, ha='right')
        
        # Create tabs for bar chart and unique values
        tab1, tab2 = st.tabs(["Bar Chart", "Unique Users"])
        
        with tab1:
            st.pyplot(fig)
        
        with tab2:
            # Display the unique values and their counts
            unique_values_counts = edited_df[x_axis_column].value_counts(dropna=False).reset_index()
            unique_values_counts.columns = [x_axis_column, 'count']
            st.write(f"Unique values and counts for {x_axis_column}, including NaN:")
            st.write(unique_values_counts)
    else:
        st.write("The file need a 'user_id' column. Then make sure you have selected 'user_id' and a second attribute")
