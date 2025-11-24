
# BMI Calculator - Smart Health Tracking

A comprehensive Python-based BMI calculator with beautiful GUI, data persistence, and advanced analytics. Track your health journey with interactive charts and multi-user support.

## Features

- **Accurate BMI Calculation** - Precise weight/(height²) formula
- **Health Classification** - Underweight, Normal, Overweight, Obese
- **Data Persistence** - SQLite database with timestamps
- **Interactive Charts** - BMI & weight trends with matplotlib
- **Multi-User Support** - Track multiple users individually
- **Dual Interface** - GUI & Command-line versions
- **Input Validation** - Comprehensive error handling

## Quick Start

### Installation
```bash
pip install matplotlib
```

### Run GUI Version
```bash
python bmi_calculator.py
```

### Run CLI Version
```bash
python bmi_calculator.py --cli
```

## How to Use

### GUI Application
1. **Calculator Tab** - Enter username, weight (kg), height (m)
2. **History Tab** - View past records and user history  
3. **Statistics Tab** - Generate interactive trend charts

### Command Line
- Simple text-based interface
- Follow prompts for weight and height
- Instant BMI results and category

## BMI Categories

| Category | BMI Range |
|----------|-----------|
| Underweight | < 18.5 |
| Normal weight | 18.5 - 24.9 |
| Overweight | 25 - 29.9 |
| Obese | ≥ 30 |

## Tech Stack

- **Python 3.11.9** - Core programming language
- **Tkinter** - GUI framework
- **Matplotlib** - Data visualization
- **SQLite3** - Database management
- **DateTime** - Timestamp handling

## Key Highlights

- **Professional GUI** with tabbed interface
- **Real-time data validation** and error handling
- **Historical tracking** with timestamps
- **Beautiful charts** with trend analysis
- **Multi-platform compatibility** (Windows, Mac, Linux)

## Code Architecture

```python
BMICalculator()          # Core logic & database
BMICalculatorGUI()       # GUI interface  
command_line_bmi()       # CLI interface
```

## Sample Output

```
Username: John
Weight: 75 kg
Height: 1.75 m
BMI: 24.49
Category: Normal weight
Data saved: Yes
```
