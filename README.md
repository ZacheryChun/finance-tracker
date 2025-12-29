# Personal Finance Tracker

A Python command-line application for tracking income, expenses, and budgets with real-time overspending alerts.

## Features

- Track income and expense transactions with categories
- Set monthly budget limits for different spending categories
- Real-time budget alerts when approaching or exceeding limits
- View all transactions sorted by date
- View transactions grouped by category
- Generate comprehensive financial summary reports
- Export data to CSV format
- Automatic data persistence using JSON
- Comprehensive test suite with pytest

## Technologies Used

- **Python 3.7+**
- **pytest** for testing
- **JSON** for data storage
- **CSV** for data export
- **Regular Expressions** for input validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ZacheryChun/personal-finance-tracker.git
cd personal-finance-tracker
```

2. Install required packages:
```bash
pip install pytest
```

## Usage

Run the program:
```bash
python finance_tracker.py
```

### Main Menu Options:
1. Add Transaction (Income or Expense)
2. View All Transactions
3. View Transactions by Category
4. Set Budget
5. View Budget Status
6. Generate Summary Report
7. Export to CSV
8. Backup Data
9. Exit

## Running Tests

Run all tests:
```bash
pytest -v
```

Run specific test file:
```bash
pytest test_transaction.py -v
```

## Project Structure
```
finance-tracker/
├── transaction.py          # Transaction classes (Income, Expense)
├── budget.py              # Budget management
├── file_manager.py        # File I/O operations
├── finance_tracker.py     # Main application
├── test_transaction.py    # Transaction tests
├── test_budget.py         # Budget tests
├── test_file_manager.py   # File manager tests
└── README.md             # This file
```

## Course Modules Demonstrated

- **Modules 1-2**: Python fundamentals, file I/O
- **Module 3**: Testing with pytest
- **Module 4**: Basic object-oriented programming
- **Modules 5-6**: Container data types (lists, dictionaries, sets)
- **Module 7**: Advanced OOP (inheritance, polymorphism)
- **Module 8**: Regular expressions
- **Module 9**: Modular programming

## Example Usage
```
Welcome to your Personal Finance Tracker!

1. Add income: $2000 (Salary)
2. Set budget: Groceries - $500
3. Add expense: $150 (Groceries) - Alert: $350 remaining
4. View budget status - See formatted summary
5. Generate report - Complete financial overview
```

## Author

Zachery Chun

## License

This project was created as a final project for a Python programming course.
