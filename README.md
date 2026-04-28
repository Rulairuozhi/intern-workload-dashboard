# Intern Weekly Workload Dashboard

A lightweight, interactive web application for monitoring and analyzing departmental intern workload patterns.

## Features

- Upload Excel files with weekly workload data
- Interactive filters by department and week
- KPI dashboard tracking total hours, average load, busy weeks
- 5 interactive visualizations with Plotly
- Automatic business insights generation
- CSV data export
- Works on desktop and mobile browsers

## Quick Start (Local)

### Prerequisites

- Python 3.8 or higher
- pip (package manager)

### Installation & Run

1. Clone/download the project:
`
git clone <repository-url>
cd 实习生工作时长可视化
`

2. Install dependencies:
`
pip install -r requirements.txt
`

3. Run the application:
`
streamlit run App.py
`

4. Open browser at http://localhost:8501

## Excel Data Format

Your Excel file should contain:
- Column 1: Week (numbers like 1, 2, 3...)
- Column 2: Date (text like 2024-01-01 to 2024-01-07)
- Columns 3+: Department names (PPM1, DP, PPM2, STA, PEH, IP1, IP2)
- Cell values: Total hours for that department in that week

Example:
| Week | Date | PPM1 | DP | PPM2 | STA | PEH | IP1 | IP2 |
|------|------|------|----|----|-----|-----|-----|-----|
| 1 | 2024-01-01 to 2024-01-07 | 28 | 35 | 25 | 30 | 32 | 40 | 22 |
| 2 | 2024-01-08 to 2024-01-14 | 30 | 28 | 38 | 32 | 25 | 28 | 35 |

## Online Deployment (Streamlit Community Cloud - FREE)

### Recommended for Team Access

1. Push code to GitHub:
`
git add .
git commit -m Add: Intern Workload Dashboard
git push origin main
`

2. Go to https://share.streamlit.io
3. Click New app
4. Sign in with GitHub
5. Fill in:
   - Repository: username/repo-name
   - Branch: main
   - Main file: App.py
6. Click Deploy
7. Get your public URL (https://your-app.streamlit.app)
8. Share URL with team

## Dashboard Guide

### Sidebar
- Upload Excel file
- Select departments to analyze
- Select weeks to analyze
- Download filtered data as CSV

### Top Section (KPI)
- Total Hours: Sum of all hours
- Avg Hours/Entry: Average hours per department-week
- Busy Weeks: Count of >32 hour entries
- Peak Week: Week with highest total hours

### Visualizations

1. **Weekly Trend Line Chart**
   - Shows how workload changes week by week
   - Red dashed line = 32-hour busy threshold
   - Peaks above line = high-pressure weeks

2. **Department Comparison Bar Chart**
   - Compares total workload across departments
   - Use for resource allocation planning

3. **Workload Heatmap**
   - Shows intensity: Department x Week
   - Darker colors = higher workload
   - Quickly spot bottlenecks

4. **Busy Frequency Bar Chart**
   - How often each department exceeds 32 hours
   - Indicates chronic pressure points

5. **Distribution Box Plot**
   - Shows if workload is stable or varies
   - Helps identify unpredictable workloads

### Auto-Generated Insights
- Highest Average Load: Most-loaded department
- Most Volatile: Most unpredictable department
- Busiest Period: Peak workload week

## Requirements

- streamlit>=1.28.0
- pandas>=2.0.0
- numpy>=1.24.0
- plotly>=5.14.0
- openpyxl>=3.1.0

## Project Structure

`
e:\实习生工作时长可视化\
|- App.py                              (Main application)
|- requirements.txt                    (Python dependencies)
|- .gitignore                          (Git ignore rules)
|- .streamlit/
|  |- config.toml                      (Streamlit configuration)
|- Weekly_Summary_Visualisation.xlsx   (Sample data)
|- README.md                           (This file)
`

## Troubleshooting

### ModuleNotFoundError
`
pip install -r requirements.txt --upgrade
`

### Excel file not recognized
- Ensure .xlsx or .xls format
- Check columns: Week, Date, PPM1, DP, etc.
- Verify department columns have numbers (no text)

### Slow performance
- Filter data in Excel before uploading
- Use Week filter for specific periods

## Version History

- v1.0 (2026-04-27): Initial release
  - File upload and data processing
  - 5 interactive visualizations
  - KPI dashboard
  - Automatic insights
  - CSV export
  - Cloud deployment ready

## Support

1. Check Troubleshooting section
2. Review Streamlit docs: https://docs.streamlit.io
3. Contact development team

Made with care for data-driven decision making
