"""This file handles saving and loading data for the finance tracker."""

import json
import csv
import os
from transaction import Transaction, Income, Expense
from budget import Budget

class FileManager:
    """This class manages saving and loading finance tracker data."""
    
    def __init__(self, transactions_file="transactions.json", budget_file="budget.json"):
        """This method initializes the file manager.
        
        Args:
            transactions_file (str): The filename for the transactions data
            budget_file (str): The filename for budget data
        """
        self.transactions_file = transactions_file
        self.budget_file = budget_file
    
    def save_transactions(self, transactions):
        """This method saves transactions to a JSON file.
        
        Args:
            transactions (list): The list of transaction objects
            
        Returns:
            bool: Returns true if successful and false if otherwise
        """
        try:
            data = []
            for t in transactions:
                if isinstance(t, Income):
                    trans_type = 'Income'
                else:
                    trans_type = 'Expense'
                trans_dict = {
                    'date': t.date,
                    'amount': t.amount,
                    'category': t.category,
                    'description': t.description,
                    'type': trans_type
                }
                data.append(trans_dict)
            
            with open(self.transactions_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Transaction Saved!: {len(transactions)} transactions to {self.transactions_file}")
            return True
            
        except Exception as e:
            print(f"There was an error saving transactions: {e}")
            return False
    
    def load_transactions(self):
        """This method loads the transactions from a JSON file.
        
        Returns:
            list: The list of transaction objects. If the file 
                    does't exist, it will be an empty list
        """
        try:
            if not os.path.exists(self.transactions_file):
                print(f"No file found")
                return []
            
            with open(self.transactions_file, 'r') as f:
                data = json.load(f)
            
            transactions = []
            for item in data:
                if item['type'] == 'Income':
                    t = Income(
                        item['date'],
                        item['amount'],
                        item['category'],
                        item['description']
                    )
                else:
                    t = Expense(
                        item['date'],
                        item['amount'],
                        item['category'],
                        item['description']
                    )
                transactions.append(t)
            
            print(f"Transactions loaded!: {len(transactions)} transactions from {self.transactions_file}")
            return transactions
            
        except json.JSONDecodeError:
            print(f"Error: {self.transactions_file} is corrupted.")
            return []
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    def save_budget(self, budget):
        """This method saves the budget to the JSON file.
        
        Args:
            budget (Budget): The budget that needs to be saved 
            
        Returns:
            bool: Returns true if successful and false if otherwise
        """
        try:
            data = budget.to_dict()
            
            with open(self.budget_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Saved budget to {self.budget_file}")
            return True
            
        except Exception as e:
            print(f"Error saving budget: {e}")
            return False
    
    def load_budget(self):
        """This method loads the budget from a JSON file
        
        Returns:
            Budget: The budget object. If the file doesn't exist 
                    then it will be a new empty budget 
        """
        try:
            if not os.path.exists(self.budget_file):
                print(f"No file found.")
                return Budget()
            
            with open(self.budget_file, 'r') as f:
                data = json.load(f)
            
            budget = Budget()
            budget.from_dict(data)
            
            print(f"Loaded budget from {self.budget_file}")
            return budget
            
        except json.JSONDecodeError:
            print(f"Error: {self.budget_file} is corrupted. Starting fresh.")
            return Budget()
        except Exception as e:
            print(f"Error loading budget: {e}")
            return Budget()
    
    def export_to_csv(self, transactions, filename="transactions_export.csv"):
        """This method exports the transactions to a CSV file.
        
        Args:
            transactions (list): The list of transaction objects
            filename (str): The output CSV filename
            
        Returns:
            bool: Returns true if successful and false if otherwise
        """
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                
                writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])
                
                for t in transactions:
                    if isinstance(t, Income):
                        trans_type = 'Income'
                    else:
                        trans_type = 'Expense'
                        
                    writer.writerow([
                        t.date,
                        trans_type,
                        t.category,
                        t.amount,
                        t.description
                    ])
            
            print(f"Exported {len(transactions)} transactions to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def import_from_csv(self, filename):
        """This method imports the transactions from a CSV file.
        
        Args:
            filename (str): The CSV filename that will be imported
            
        Returns:
            list: The list of transaction objects. It will be an 
                    empty list if there is an error 
        """
        try:
            if not os.path.exists(filename):
                print(f"File not found: {filename}")
                return []
            
            transactions = []
            
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    if row['Type'] == 'Income':
                        t = Income(
                            row['Date'],
                            row['Amount'],
                            row['Category'],
                            row['Description']
                        )
                    else:
                        t = Expense(
                            row['Date'],
                            row['Amount'],
                            row['Category'],
                            row['Description']
                        )
                    transactions.append(t)
            
            print(f"Imported {len(transactions)} transactions from {filename}")
            return transactions
            
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return []
    
    def backup_data(self):
        """This method creates backup copies of data files
        
        Returns:
            bool: Returns true if successful and false if otherwise
        """
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if os.path.exists(self.transactions_file):
                backup_name = f"transactions_backup_{timestamp}.json"
                with open(self.transactions_file, 'r') as src:
                    with open(backup_name, 'w') as dst:
                        dst.write(src.read())
                print(f"Backed up transactions to {backup_name}")
            
            if os.path.exists(self.budget_file):
                backup_name = f"budget_backup_{timestamp}.json"
                with open(self.budget_file, 'r') as src:
                    with open(backup_name, 'w') as dst:
                        dst.write(src.read())
                print(f"Backed up budget to {backup_name}")
            
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False


