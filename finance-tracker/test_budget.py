"""This file tests the budget file for the finance tracker"""

import pytest
from budget import Budget

class TestBudget:
    """Test cases for the budget class"""
    
    def test_budget_initialization(self):
        """This tests if the budget initializes with empty dictionaries"""
        budget = Budget()
        assert budget.limits == {}
        assert budget.spent == {}
    
    def test_valid_budget_limit(self):
        """This tests if we set a valid budget limit"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        assert budget.limits["groceries"] == 500.00
        assert budget.spent["groceries"] == 0.0
    
    def test_negative_limit(self):
        """This tests if a negative limits raises a ValueError"""
        budget = Budget()
        with pytest.raises(ValueError):
            budget.set_limit("groceries", -100)
    
    def test_add_expense(self):
        """This tests if we add an expense to category"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 100.00)
        budget.add_expense("groceries", 50.00)
        assert budget.spent["groceries"] == 150.00
    
    def test_get_remaining_within_budget(self):
        """This tests getting the remaining budget when under the limit"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 200.00)
        remaining = budget.get_remaining("groceries")
        assert remaining == 300.00
    
    def test_get_remaining_over_budget(self):
        """This tests getting the remaining budget when over the limit"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 600.00)
        remaining = budget.get_remaining("groceries")
        assert remaining == -100.00
    
    def test_is_over_budget(self):
        """This tests if the program detects the user to be over budget"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 300.00)
        assert budget.is_over_budget("groceries") is False
        budget.add_expense("groceries", 300.00)
        assert budget.is_over_budget("groceries") is True
    
    def test_get_status(self):
        """This tests if the program displays the status accurately"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 200.00)
        status = budget.get_status("groceries")
        assert status['limit'] == 500.00
        assert status['spent'] == 200.00
        assert status['remaining'] == 300.00
        assert status['over_budget'] is False
    
    def test_to_dict_and_from_dict(self):
        """This tests if the program converts the budget to and from the dictionary"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 200.00)
        data = budget.to_dict()
        new_budget = Budget()
        new_budget.from_dict(data)
        assert new_budget.limits == budget.limits
        assert new_budget.spent == budget.spent
