# Traffic Light Efficiency Simulation and Analysis

## Project Overview
This project analyzes traffic signal timing efficiency using real traffic volume data from Victoria, Australia.

## Team Members
- Hazem Abo-Donia (habodoni@stevens.edu)
- Kyle Ponte (kponte@stevens.edu)

## Setup Instructions

### Prerequisites
- Python 3.12 or 3.13
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CPE551-Project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download traffic data:
   - Visit: https://discover.data.vic.gov.au/dataset/traffic-signal-volume-data
   - Download CSV files and place in `data/` directory

### Running the Project
1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Open `traffic_analysis.ipynb`

3. Run all cells to execute the analysis

## Project Structure
- `traffic_analysis.ipynb` - Main analysis notebook
- `intersection_data.py` - IntersectionData class
- `signal_analyzer.py` - SignalTimingAnalyzer class
- `timing_functions.py` - Timing calculation functions
- `data_processor.py` - Data I/O utilities
- `tests/` - Pytest test files
