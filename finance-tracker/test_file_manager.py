"""This file tests the file_manager file for the finance tracker"""

import pytest
import os
from file_manager import FileManager
from transaction import Income, Expense
from budget import Budget


class TestFileManager:
    """Test cases for the filemanager class"""
    
    @pytest.fixture
    def file_manager(self, tmp_path):
        """This method creates a filemanager with temporery files"""
        trans_file = tmp_path / "test_transactions.json"
        budget_file = tmp_path / "test_budget.json"
        return FileManager(str(trans_file), str(budget_file))
    
    @pytest.fixture
    def sample_transactions(self):
        """This method creates a sample transactions for testing"""
        return [
            Income("2024-11-01", 2000.00, "salary", "Monthly paycheck"),
            Expense("2024-11-02", 150.00, "groceries", "Weekly shopping"),
            Expense("2024-11-03", 50.00, "entertainment", "Movie tickets"),
        ]
    
    @pytest.fixture
    def sample_budget(self):
        """This method creates a sample budget for testing"""
        budget = Budget()
        budget.set_limit("groceries", 500.00)
        budget.add_expense("groceries", 150.00)
        return budget
    
    def test_save_and_load_transactions(self, file_manager, sample_transactions):
        """This tests if the program can save and load transactions properly"""
        result = file_manager.save_transactions(sample_transactions)
        assert result is True
        assert os.path.exists(file_manager.transactions_file)
        loaded = file_manager.load_transactions()
        assert len(loaded) == 3
        assert isinstance(loaded[0], Income)
        assert loaded[0].amount == 2000.00
    
    def test_save_and_load_budget(self, file_manager, sample_budget):
        """This tests if the program can save and load budgets properly"""
        result = file_manager.save_budget(sample_budget)
        assert result is True
        loaded = file_manager.load_budget()
        assert loaded.limits['groceries'] == 500.00
        assert loaded.spent['groceries'] == 150.00
    
    def test_load_nonexistent_files(self, file_manager):
        """This tests loading when files don't exist"""
        transactions = file_manager.load_transactions()
        budget = file_manager.load_budget()
        assert transactions == []
        assert isinstance(budget, Budget)
        assert budget.limits == {}
    
    def test_export_to_csv(self, file_manager, sample_transactions, tmp_path):
        """This tests if the program can export data to a CSV file properly"""
        csv_file = tmp_path / "export.csv"
        result = file_manager.export_to_csv(sample_transactions, str(csv_file))
        assert result is True
        assert os.path.exists(csv_file)
    
    def test_import_from_csv(self, file_manager, sample_transactions, tmp_path):
        """This tests if the program can import data from a CSV file properly"""
        csv_file = tmp_path / "import.csv"
        file_manager.export_to_csv(sample_transactions, str(csv_file))
        loaded = file_manager.import_from_csv(str(csv_file))
        assert len(loaded) == 3
        assert isinstance(loaded[0], Income)
        assert loaded[0].amount == 2000.00