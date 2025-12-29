"""This file is the main program for the finace tracker."""

from transaction import Transaction, Income, Expense
from budget import Budget
from file_manager import FileManager
from datetime import datetime


class FinanceTracker:
    """This class is the main finance tracker application."""
    
    def __init__(self):
        """This method initializes the finance tracker and loads the existing data."""

        self.transactions = []
        self.budget = Budget()
        self.file_manager = FileManager()
        self.load_data()
    
    def load_data(self):
        """This method loads the data from files during the startup of the application"""

        print("\nLoading existing data")
        self.transactions = self.file_manager.load_transactions()
        self.budget = self.file_manager.load_budget()
        
        if self.transactions:
            for t in self.transactions:
                if isinstance(t, Expense):
                    if t.category not in self.budget.spent:
                        self.budget.spent[t.category] = 0.0
            
            for t in self.transactions:
                if isinstance(t, Expense):
                    self.budget.spent[t.category] = self.budget.spent.get(t.category, 0.0) + t.amount
    
    def save_data(self):
        """This method saves the data to files"""

        self.file_manager.save_transactions(self.transactions)
        self.file_manager.save_budget(self.budget)
    
    def add_transaction(self):
        """This method adds a new transaction either a income or expense"""

        print("\nAdd A New Transaction")
        
        try:
            print("Transaction type:")
            print("  1. Income")
            print("  2. Expense")
            choice = input("Enter either 1 or 2: ").strip()
            
            if choice not in ['1', '2']:
                print("Invalid choice. Please enter 1 or 2.")
                return
            
            date = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            
            amount = input("Amount: $").strip()
            category = input("Category (ex: groceries, salary, entertainment): ").strip()
            description = input("Description: ").strip()
            
            if choice == '1':
                transaction = Income(date, amount, category, description)
                print(f"Income added: +${transaction.amount:.2f}")
            else:
                transaction = Expense(date, amount, category, description)
                print(f"Expense added: -${transaction.amount:.2f}")
                
                self.budget.add_expense(category, transaction.amount)
                
                remaining = self.budget.get_remaining(category)
                if remaining is not None:
                    if remaining < 0:
                        print(f"WARNING: Over budget by ${abs(remaining):.2f}!")
                    elif remaining < self.budget.limits[category] * 0.2:
                        print(f"Warning: Only ${remaining:.2f} left in budget")
            
            self.transactions.append(transaction)
            
            self.save_data()
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def view_transactions(self):
        """This method allows users to view all transactions"""

        print("\nAll Transactions")
        
        if not self.transactions:
            print("No transactions.")
            return
        
        incomes= []
        expenses = []
        for t in self.transactions:
            if isinstance(t, Income):
                incomes.append(t)
            else:
                expenses.append(t)
        
        if incomes:
            print("\nINCOME:")
            print(f"{'Date':<12} {'Category':<15} {'Amount':>10} {'Description':<30}")
            print("-" * 70)
            for t in sorted(incomes, key=lambda x: x.date):
                print(f"{t.date:<12} {t.category:<15} +${t.amount:>8.2f} {t.description:<30}")
        
        if expenses:
            print("\nEXPENSES:")
            print(f"{'Date':<12} {'Category':<15} {'Amount':>10} {'Description':<30}")
            print("-" * 70)
            for t in sorted(expenses, key=lambda x: x.date):
                print(f"{t.date:<12} {t.category:<15} -${t.amount:>8.2f} {t.description:<30}")
        
        total_income = sum(t.amount for t in incomes)
        total_expenses = sum(t.amount for t in expenses)
        net = total_income - total_expenses
        
        print("\n" + "=" * 70)
        print(f"Total Income:    ${total_income:>10.2f}")
        print(f"Total Expenses:  ${total_expenses:>10.2f}")
        print(f"Net:             ${net:>10.2f}")
        print("=" * 70)
    
    def view_by_category(self):
        """This method allows users to view transactions grouped by categories"""

        print("\nTransactions by Category")
        
        if not self.transactions:
            print("No transactions.")
            return
        
        by_category = {}
        
        for t in self.transactions:
            if t.category not in by_category:
                by_category[t.category] = []
            by_category[t.category].append(t)
        
        for category in sorted(by_category.keys()):
            print(f"\n{category.upper()}:")
            print("-" * 70)

            total = 0
            sorted_transactions = sorted(by_category[category], key=lambda x: x.date)
            for t in sorted_transactions:
                if isinstance(t, Income):
                    sign = "+"
                    amount = t.amount
                else:
                    sign = "-"
                    amount = -t.amount
                total += amount
                print(f"  {t.date} | {sign}${t.amount:.2f} | {t.description}")

            print(f"  Category Total: ${total:.2f}")
    
    def set_budget(self):
        """This method sets or updates the budget for a category"""
        print("\nSet Budget")
        
        try:
            category = input("Category name: ").strip()
            limit = input("Monthly budget limit: $").strip()
            
            self.budget.set_limit(category, limit)
            
            self.save_data()
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_budget_status(self):
        """This method allows users to view the current budget status"""

        print("\nBudget Status")
        self.budget.print_summary()
    
    def generate_summary(self):
        """This method generates the financial summary report"""

        print("\n" + "="*70)
        print("FINANCIAL SUMMARY REPORT".center(70))
        print("="*70)
        
        if not self.transactions:
            print("No transactions to summarize.")
            return
        incomes = []
        expenses = []
        for t in self.transactions:
            if isinstance(t, Income):
                incomes.append(t)
            else: 
                expenses.append(t)
        
        total_income = 0
        for t in incomes:
            total_income += t.amount

        total_expenses = 0
        for t in expenses:
            total_expenses += t.amount

        net_savings = total_income - total_expenses
        expense_by_category = {}
        for e in expenses:
            expense_by_category[e.category] = expense_by_category.get(e.category, 0) + e.amount
        
        print(f"\nTotal Transactions: {len(self.transactions)}")
        print(f"  Income transactions: {len(incomes)}")
        print(f"  Expense transactions: {len(expenses)}")
        
        print(f"\nFinancial Overview:")
        print(f"  Total Income:   ${total_income:>10.2f}")
        print(f"  Total Expenses: ${total_expenses:>10.2f}")
        print(f"  Net Savings:    ${net_savings:>10.2f}")
        
        if total_income > 0:
            savings_rate = (net_savings / total_income) * 100
            print(f"  Savings Rate:   {savings_rate:>10.1f}%")
        
        if expense_by_category:
            print(f"\nTop Spending Categories:")
            sorted_categories = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)
            top_5 = sorted_categories[:5]
    
            i = 1
            for cat, amount in top_5:
                if total_expenses > 0:
                    percentage = (amount / total_expenses) * 100
                else:
                    percentage = 0
                print(f"  {i}. {cat:15} ${amount:>8.2f} ({percentage:>5.1f}%)")
                i += 1
        print("="*70)
    
    def export_data(self):
        """This method exports data to a CSV"""

        print("\nExport Data")
        
        if not self.transactions:
            print("No transactions to export.")
            return
        
        filename = input("Enter filename (or press Enter for 'export.csv'): ").strip()
        if not filename:
            filename = "export.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        if self.file_manager.export_to_csv(self.transactions, filename):
            print(f"Data exported successfully to {filename}")
    
    def backup_data(self):
        """This method creates a backup of data files"""

        print("\nBackup Data")
        if self.file_manager.backup_data():
            print("Backup created successfully!")
    
    def display_menu(self):
        """This method displays the main menu"""

        print("\n" + "="*50)
        print("PERSONAL FINANCE TRACKER".center(50))
        print("="*50)
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Transactions by Category")
        print("4. Set Budget")
        print("5. View Budget Status")
        print("6. Generate Summary Report")
        print("7. Export to CSV")
        print("8. Backup Data")
        print("9. Exit")
        print("="*50)
    
    def run(self):
        """This method will create the Main program loop"""
        print("\nWelcome to your Personal Finance Tracker!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == '1':
                self.add_transaction()
            elif choice == '2':
                self.view_transactions()
            elif choice == '3':
                self.view_by_category()
            elif choice == '4':
                self.set_budget()
            elif choice == '5':
                self.view_budget_status()
            elif choice == '6':
                self.generate_summary()
            elif choice == '7':
                self.export_data()
            elif choice == '8':
                self.backup_data()
            elif choice == '9':
                print("\nSaving data")
                self.save_data()
                print("Thank you for using Personal Finance Tracker!")
                print("Goodbye!\n")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 9.")
            
            input("\nPress Enter to continue")

if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.run()