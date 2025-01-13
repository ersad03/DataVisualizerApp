# Data Visualizer: Interactive Data Analysis and Visualization Tool

## Introduction
This web application was initially designed at the request of a PhD student to support and document her research. It provides powerful tools for converting and visualizing data, offering two main functionalities:

1. **XLSX to CSV Converter:**
   - Preview and edit the converted CSV file before downloading.
   - Based on the work of Dilshod Temirkhodjaev.

2. **CSV Data Visualization:**
   - Upload CSV files up to 10GB in size, with support for various file types using the "Universal Encoding Detector" library.
   - Dynamic filtering and data editing within the application.
   - Create relationships using 14 different chart types with intuitive axis selection based on data type (categorical or numerical).
   - Maintain a history of generated charts for comparison and analysis, with options to delete unnecessary charts.
   - Download charts as PNG, view them in full-screen mode, and interact with data dynamically using the Plotly Express library.

The application guides users in selecting data for axes, ensuring informed decisions through visual cues about the data type. Features like dynamic filters and chart history make data exploration and analysis seamless.

## Features

### Conversion and Editing
- Convert XLSX files to CSV format with a preview and editing option.
- Download finalized CSV files.

### Data Upload and Management
- Upload CSV files up to 10GB, with automatic encoding detection.
- Edit data directly within the app.
- Select a percentage of rows to display.
- Dynamic filtering with column/feature deselection.

### Charting and Visualization
- Supports 14 chart types:
  - **Numeric Data Charts:** Histogram, Box Plot, Bubble Chart, Density Plot, Violin Plot, 3D Scatter Plot, Boxen Plot, Bar Plot.
  - **Categorical Data Charts:** Bar Chart, Pie Chart, Sunburst, Dot Plot, Heatmap, Treemap.
- Axis selection dynamically adjusts based on data type.
- Chart history for easy comparison.
- Download charts as PNG.
- Full-screen preview and interactive capabilities for each chart.

## Installation

Follow these steps to set up and run the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/ersad03/DataVisualizerApp.git
   ```

2. Navigate to the project directory:
   ```bash
   cd DataVisualizerApp/
   ```

3. Install dependencies:
   ```bash
   sudo apt install python3-pip
   pip install -r requirements.txt
   ```

4. Update your `~/.bashrc` file:
   ```bash
   echo 'export PATH=$PATH:/home/$USER/.local/' >> ~/.bashrc
   source ~/.bashrc
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Launch the web application by following the installation steps above or by visiting the live app at [datavisualizerpp.streamlit.app](https://datavisualizerpp.streamlit.app).
2. Use the **XLSX to CSV Converter** to preview, edit, and download converted files.
3. Upload a CSV file to the **Data Visualization** page.
4. Explore the data through dynamic filters, table editing, and interactive charts.
5. Generate charts, compare using history, and download as needed.

## Contribution
Contributions are welcome, and any feedback or suggestions for improvement are greatly appreciated.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For more information or to access the live application, visit: [datavisualizerpp.streamlit.app](https://datavisualizerpp.streamlit.app).

