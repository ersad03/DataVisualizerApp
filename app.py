import streamlit as st
import pandas as pd
import chardet
from io import StringIO
from xlsx2csv import Xlsx2csv
import plotly.express as px
import plotly.graph_objects as go

# Function to detect encoding using chardet
def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

# Initialize session state to store plots if not already initialized
if 'plots' not in st.session_state:
    st.session_state.plots = []

# Function to generate numeric plots based on user's selections
def generate_numeric_plot(df, x_axis, y_axis, plot_type, size_var=None, color_var=None, z_axis=None):
    if plot_type == "Histogram":
        fig = px.histogram(df, x=x_axis, color=x_axis)

    elif plot_type == "Box Plot":
        if x_axis:
            fig = px.box(df, x=x_axis, y=y_axis)
        else:
            fig = px.box(df, y=y_axis)

    elif plot_type == "Boxen Plot":
        if x_axis:
            fig = px.box(df, x=x_axis, y=y_axis, boxmode='overlay', points="all")  # Use boxmode for Boxen-like display
        else:
            fig = px.box(df, y=y_axis, boxmode='overlay', points="all")

    elif plot_type == "Heatmap":
        fig = px.density_heatmap(df, x=x_axis, y=y_axis)

    elif plot_type == "Bubble Chart":
        fig = px.scatter(df, x=x_axis, y=y_axis, size=size_var, color=color_var)

    elif plot_type == "Density Plot":
        if y_axis:
            fig = px.density_contour(df, x=x_axis, y=y_axis, marginal_x="histogram", marginal_y="histogram")
        else:
            fig = px.density_contour(df, x=x_axis, marginal_x="histogram")

    elif plot_type == "Violin Plot":
        if x_axis:
            fig = px.violin(df, x=x_axis, y=y_axis, box=True, points="all")
        else:
            fig = px.violin(df, y=y_axis, box=True, points="all")

    elif plot_type == "3D Scatter Plot":
        fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=color_var, size=size_var)

    elif plot_type == "Bar Plot":
        fig = px.bar(df, x=x_axis, y=y_axis, barmode='group')  # Default to grouped bars

    # Update layout for Plotly-based charts
    fig.update_layout(title=f"{plot_type} with {x_axis} vs {y_axis}" if y_axis else f"{plot_type} with {x_axis}")
    return fig

# Function to generate categorical plot based on user's selections (existing behavior)
def generate_categorical_plot(df, x_axis, y_axes, plot_type):
    if plot_type == "Bar Chart":
        fig = go.Figure()
        for y_axis in y_axes:
            fig.add_trace(go.Bar(x=df[x_axis], y=df[y_axis], name=y_axis))
        fig.update_layout(barmode='group')

    elif plot_type == "Pie Chart":
        fig = px.pie(df, names=x_axis)

    elif plot_type == "Sunburst":
        fig = px.sunburst(df, path=[x_axis] + y_axes)

    elif plot_type == "Dot Plot":
        fig = go.Figure()
        for y_axis in y_axes:
            fig.add_trace(go.Scatter(x=df[x_axis], y=df[y_axis], mode='markers', name=y_axis))

    elif plot_type == "Heatmap":
        heatmap_data = pd.crosstab(df[x_axis], df[y_axes[0]])
        fig = px.imshow(heatmap_data, text_auto=True)

    elif plot_type == "Treemap":  # Treemap replacing Mosaic Plot
        fig = px.treemap(df, path=[x_axis] + y_axes)

    # Update layout for Plotly-based charts
    if plot_type != "Treemap":
        fig.update_layout(title=f"{plot_type} with {x_axis} vs {', '.join(y_axes)}" if y_axes else f"{plot_type} with {x_axis}")
    return fig

# Delete plot based on index
def delete_plot(index):
    if 0 <= index < len(st.session_state.plots):
        st.session_state.plots.pop(index)

# Set the page configuration
st.set_page_config(page_title="Data Visualizer & Converter", layout="wide", page_icon="📊", initial_sidebar_state='expanded')

# Sidebar to select between pages
page = st.sidebar.selectbox("Select Page", ["Data Visualizer", "XLSX to CSV Converter"])

if page == "Data Visualizer":
    st.title("📊 Data Visualizer")

    # File upload section (in sidebar)
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        # Detect file encoding using chardet
        file_encoding = detect_encoding(uploaded_file)
        uploaded_file.seek(0)

        try:
            df = pd.read_csv(uploaded_file, encoding=file_encoding)
            st.success(f"File successfully uploaded with encoding '{file_encoding}'!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            df = None

        if df is not None:
            st.subheader("Adjust Dataset Size by Percentage")
            percentage_rows = st.slider("Select percentage of rows to display and edit", min_value=10, max_value=100, value=100, step=10)
            num_rows = int((percentage_rows / 100) * len(df))
            edited_df = st.data_editor(df.head(num_rows), num_rows="dynamic", use_container_width=True)

            df = edited_df.copy()

            # Initialize filtered_df to be the same as df by default
            filtered_df = df.copy()

            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

            if not categorical_columns:
                st.warning("No categorical columns detected. Some plots may not be available.")

            # ----- Dynamic Deselect Filtering Section -----
            if categorical_columns:
                st.sidebar.subheader("Dynamic Filters")

                # Cascading dynamic deselect filters
                for col in categorical_columns:
                    unique_values = filtered_df[col].unique().tolist()

                    # Multiselect for deselecting options with updated placeholder
                    deselected_values = st.sidebar.multiselect(
                        f"Deselect options from {col}",  # Title of the selectbox
                        options=unique_values, 
                        default=[],  # No deselection by default
                        help="Deselect options to exclude them. Leaving blank selects all.",
                        placeholder="Choose an option to remove"  # Placeholder text when no option is selected
                    )

                    # Filter logic: if nothing is deselected, keep all; otherwise, filter
                    if len(deselected_values) == 0:
                        selected_values = unique_values
                    else:
                        selected_values = [item for item in unique_values if item not in deselected_values]

                    # Filter the dataframe based on deselected values
                    filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

                st.write(f"Filtered dataset contains {len(filtered_df)} rows.")
            else:
                st.sidebar.info("No categorical columns available for filtering.")

            # Define chart type options with a divider ("---")
            chart_options = [
                "Bar Chart", "Pie Chart", "Sunburst", "Dot Plot", "Heatmap", "Treemap",
                "---",  # Divider between groups
                "Histogram", "Box Plot", "Bubble Chart", "Density Plot", "Violin Plot", "3D Scatter Plot", "Boxen Plot", "Bar Plot"
            ]

            st.subheader("Select Chart Type")
            chart_type = st.selectbox("Choose plot type", chart_options)

            # Ensure divider ("---") is not selectable
            if chart_type == "---":
                st.warning("Please select a valid chart type.")

            if chart_type in ["Histogram", "Box Plot", "Boxen Plot", "Heatmap", "Bubble Chart", "Density Plot", "Violin Plot", "3D Scatter Plot", "Bar Plot"]:
                # Numeric data configurations
                x_axis = st.selectbox("Select the X-axis", options=numeric_columns if chart_type in ["Density Plot", "Boxen Plot", "Violin Plot", "3D Scatter Plot", "Bar Plot"] else categorical_columns)
                y_axis = None
                size_var = None
                color_var = None
                z_axis = None

                if chart_type != "Histogram" and chart_type != "Density Plot":
                    y_axis = st.selectbox("Select the Y-axis (numeric)", options=numeric_columns)

                if chart_type == "Bubble Chart" or chart_type == "3D Scatter Plot":
                    size_var = st.selectbox("Select the variable for bubble size", options=numeric_columns)
                    color_var = st.selectbox("Select the variable for bubble color", options=[None] + df.columns.tolist())

                if chart_type == "3D Scatter Plot":
                    z_axis = st.selectbox("Select the Z-axis (numeric)", options=numeric_columns)

                fig = generate_numeric_plot(filtered_df, x_axis, y_axis, chart_type, size_var=size_var, color_var=color_var, z_axis=z_axis)

            else:
                # Categorical data configurations (existing behavior)
                if chart_type == "Bar Chart":
                    x_axis = st.selectbox("Select the X-axis (categorical)", options=categorical_columns)
                    if numeric_columns:
                        y_axes = st.multiselect("Select Y-axes (numeric)", options=numeric_columns, default=numeric_columns)
                    else:
                        st.warning("No numeric columns detected. Displaying all categorical columns for Y-axis.")
                        y_axes = st.multiselect("Select Y-axes (categorical)", options=categorical_columns)

                elif chart_type == "Pie Chart":
                    st.info("For pie charts, select a categorical column for proportions.")
                    if categorical_columns:
                        x_axis = st.selectbox("Select a categorical column for Pie Chart", options=categorical_columns)
                        y_axes = None
                    else:
                        st.error("Pie Chart requires at least one categorical column.")

                elif chart_type == "Sunburst":
                    st.info("For Sunburst charts, select hierarchical categorical columns.")
                    x_axis = st.selectbox("Select the root categorical column", options=categorical_columns)
                    y_axes = st.multiselect("Select additional categorical columns for hierarchy", options=[col for col in categorical_columns if col != x_axis])

                elif chart_type == "Dot Plot":
                    x_axis = st.selectbox("Select the X-axis (categorical)", options=categorical_columns)
                    if numeric_columns:
                        y_axes = st.multiselect("Select Y-axes (numeric)", options=numeric_columns)
                    else:
                        st.warning("No numeric columns detected. Displaying all categorical columns for Y-axis.")
                        y_axes = st.multiselect("Select Y-axes (categorical)", options=categorical_columns)

                elif chart_type == "Heatmap":
                    st.info("For heatmaps, select two categorical columns.")
                    x_axis = st.selectbox("Select the X-axis (categorical)", options=categorical_columns)
                    y_axes = st.multiselect("Select the Y-axis (categorical)", options=[col for col in categorical_columns if col != x_axis], max_selections=1)

                elif chart_type == "Treemap":
                    st.info("For Treemaps, select hierarchical categorical columns.")
                    x_axis = st.selectbox("Select the root categorical column", options=categorical_columns)
                    y_axes = st.multiselect("Select additional categorical columns for hierarchy", options=[col for col in categorical_columns if col != x_axis])

            # Generate plot button
            if st.button("Generate Plot"):
                if chart_type == "Pie Chart" and not x_axis:
                    st.error("Please select a categorical column for Pie Chart.")
                elif chart_type in ["Histogram", "Box Plot", "Boxen Plot", "Heatmap", "Bubble Chart", "Density Plot", "Violin Plot", "3D Scatter Plot", "Bar Plot"]:
                    if not x_axis or (chart_type != "Histogram" and chart_type != "Density Plot" and not y_axis):
                        st.error("Please select valid X and Y axes for the chart.")
                    else:
                        st.session_state.plots.append({"plot": fig, "plot_type": chart_type, "x_axis": x_axis, "y_axis": y_axis})

                elif chart_type != "Pie Chart" and (not x_axis or not y_axes):
                    st.error("Please select valid X and Y axes for the chart.")
                else:
                    fig = generate_categorical_plot(filtered_df, x_axis, y_axes, chart_type)
                    if fig is not None or chart_type == "Treemap":
                        st.session_state.plots.append({"plot": fig, "plot_type": chart_type, "x_axis": x_axis, "y_axes": y_axes})

            # Display all generated plots with delete buttons
            for i, plot_data in enumerate(st.session_state.plots):
                with st.container():
                    st.plotly_chart(plot_data["plot"], use_container_width=True)
                    # Simplified delete button to only show "Delete the plot [type]"
                    st.button(f"Delete the plot {plot_data['plot_type']}",
                              key=f"delete_{i}",
                              on_click=delete_plot,
                              args=(i,))

    else:
        st.info("Please upload a dataset to begin.")

elif page == "XLSX to CSV Converter":
    st.title("XLSX to CSV Converter")
    uploaded_file = st.file_uploader("Choose an XLSX file", type=["xlsx"])

    if uploaded_file is not None:
        st.write("File uploaded successfully. Processing...")

        xlsx2csv = Xlsx2csv(uploaded_file, delimiter=',', outputencoding='utf-8')
        workbook = xlsx2csv.workbook
        sheet_names = [sheet['name'] for sheet in workbook.sheets]

        sheet_name = st.selectbox("Select sheet to convert:", sheet_names)

        if sheet_name:
            sheet_id = xlsx2csv.getSheetIdByName(sheet_name)
            output_csv = StringIO()
            xlsx2csv.convert(output_csv, sheetid=sheet_id)
            output_csv.seek(0)

            st.write("### Editable CSV Output")
            csv_content = output_csv.getvalue()
            edited_csv = st.text_area("Edit the CSV content below:", value=csv_content, height=300)

            st.download_button(label="Download Edited CSV", data=edited_csv, file_name=f"{uploaded_file.name.split('.')[0]}_{sheet_name}_converted.csv", mime="text/csv")
