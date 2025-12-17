# Traffic Light Efficiency Simulation and Analysis

## Project Title
Traffic Light Efficiency Simulation and Analysis

## Team Members
- Hazem Abo-Donia (habodoni@stevens.edu)
- Kyle Ponte (kponte@stevens.edu)

## Problem Description
Many intersections run with suboptimal signal timing, which causes delay, queue growth, and fuel waste. This project uses real traffic volume data from Victoria, Australia to evaluate current timing and simulate simple timing changes. The goal is to compare baseline timing to an adjusted plan and report changes in average delay and throughput.

## Data Source
Traffic Signal Volume Data from the State of Victoria (Australia) Open Data Portal:
https://discover.data.vic.gov.au/dataset/traffic-signal-volume-data

The data provides 15-minute vehicle counts by signalized location and approach.

## Program Structure

### Main Components
- `traffic_analysis.ipynb` - Main Jupyter notebook for analysis
- `intersection_data.py` - IntersectionData class for storing traffic data
- `signal_analyzer.py` - SignalTimingAnalyzer class for timing analysis
- `timing_functions.py` - Functions for delay calculations and timing plan generation
- `data_processor.py` - Data I/O and processing utilities
- `timing_plan.py` - TimingPlan class with operator overloading
- `tests/` - Pytest test files

### How to Use the Program

1. **Setup:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Data:**
   - Visit the Victoria Open Data Portal
   - Download traffic signal volume CSV files
   - Place files in `data/` directory
   - **Note:** If no data file is available, the notebook will generate sample data for demonstration

3. **Run Analysis:**
   ```bash
   jupyter notebook
   ```
   - Open `traffic_analysis.ipynb`
   - Run all cells sequentially

4. **Run Tests:**
   ```bash
   pytest tests/ -v
   ```

### Outputs
- `outputs/delay_analysis.png` - Visualization plots showing delay vs time of day and before/after comparisons
- `outputs/summary_report.csv` - Summary statistics for all intersections
- `outputs/timing_comparison_results.csv` - Detailed comparison results between baseline and alternative timing plans

## Main Contributions

### Hazem Abo-Donia
- IntersectionData class implementation with __str__ method
- Data I/O module with CSV processing and generator functions
- Timing functions with advanced Python features (zip, lambda, list comprehensions)
- Visualization module with matplotlib
- Main notebook structure and integration
- Delay calculation tests

### Kyle Ponte
- SignalTimingAnalyzer class with composition relationship
- TimingPlan class with operator overloading
- Comprehensive exception handling throughout codebase
- Data handling and exception scenario tests
- Final notebook integration and documentation

## Requirements Met

### Part 1 Requirements
- ✅ Two classes with relationship (IntersectionData + SignalTimingAnalyzer with composition)
- ✅ Two functions (compute_average_delay, generate_timing_plan)
- ✅ Two advanced libraries (pandas, matplotlib)
- ✅ Two exception approaches (FileNotFoundError, ZeroDivisionError)
- ✅ Two pytest tests
- ✅ Data I/O (CSV read/write)
- ✅ Control flow (for, while, if)
- ✅ Docstrings and comments
- ✅ README file

### Part 2 Requirements (4+ features)
- ✅ Special functions: zip, lambda
- ✅ List comprehension
- ✅ Built-in module: itertools
- ✅ Mutable/immutable objects
- ✅ Operator overloading (__add__)
- ✅ Generator function
- ✅ __name__ guard
- ✅ __str__ method

## Python Version
Python 3.12 or 3.13

## License
This project is for educational purposes only.
