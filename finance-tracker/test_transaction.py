"""This file tests the transaction file for the finance tracker."""

import pytest
from transaction import Transaction, Income, Expense


class TestTransaction:
    """Test cases for the transaction classes"""
    
    def test_valid_income(self):
        """This tests if the program creates a valid income correctly""" 
        income = Income("2024-11-01", 1500.00, "Salary", "Monthly paycheck")
        assert income.date == "2024-11-01"
        assert income.amount == 1500.00
        assert income.category == "salary"
        assert income.description == "Monthly paycheck"
    
    def test_valid_expense(self):
        """This tests if the program creates a valid expense correctly"""
        expense = Expense("2024-11-02", 45.50, "Groceries", "Weekly shopping")
        assert expense.date == "2024-11-02"
        assert expense.amount == 45.50
        assert expense.category == "groceries"
        assert expense.description == "Weekly shopping"
    
    def test_invalid_date_format(self):
        """This tests if invalid date formats raise errors"""
        with pytest.raises(ValueError):
            Income("11/01/2024", 1500, "Salary", "Test")
        with pytest.raises(ValueError):
            Expense("2024-13-01", 100, "Food", "Test")
    
    def test_invalid_amount_negative(self):
        """This tests if negative amounts raise errors"""
        with pytest.raises(ValueError):
            Income("2024-11-01", -100, "Salary", "Test")
    
    def test_invalid_amount_zero(self):
        """This tests if a 0 amount raise errors"""
        with pytest.raises(ValueError):
            Expense("2024-11-01", 0, "Food", "Test")
    
    def test_category_lowercase_conversion(self):
        """This tests if the categories are converted to lowercase correctly"""
        income = Income("2024-11-01", 100, "SALARY", "Test")
        assert income.category == "salary"
    
    def test_inheritance(self):
        """This tests if the income and expense inherit from transaction"""
        income = Income("2024-11-01", 1500, "Salary", "Test")
        expense = Expense("2024-11-01", 100, "Food", "Test")
        assert isinstance(income, Transaction)
        assert isinstance(expense, Transaction)
    
    def test_to_dict(self):
        """This tests if the program can converge to dictionary correctly"""
        income = Income("2024-11-01", 1500.00, "Salary", "Paycheck")
        income_dict = income.to_dict()
        assert income_dict['date'] == "2024-11-01"
        assert income_dict['amount'] == 1500.00
        assert income_dict['type'] == "Income"
