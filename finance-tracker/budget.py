"""This file manages the budget limits and spending tracking."""

class Budget:
    """This class manages the budget limits for different spending categories."""
    
    def __init__(self):
        """This method initializes a empty budget with no limits set."""
        self.limits = {}
        self.spent = {}
    
    def set_limit(self, category, limit):
        """This method sets or updates the budget limit for a category.
        
        Args:
            category (str): The category name like groceries or entertainment
            limit (float): The maximum spending limit for the category
            
        Raises:
            ValueError: If limit is not positive
        """
        category = category.strip().lower()
        
        try:
            limit = float(limit)
            if limit <= 0:
                raise ValueError("It must be a postive budget limit.")
            
            self.limits[category] = round(limit, 2)
            
            if category not in self.spent:
                self.spent[category] = 0.0
                
            print(f"Valid budget set: {category} = ${limit:.2f}")
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid budget limit: {limit}")
    
    def add_expense(self, category, amount):
        """This method adds expense amounts to the category spending.
        
        Args:
            category (str): The category name
            amount (float): The expense amount to add
        """
        category = category.strip().lower()
        amount = float(amount)
        
        if category not in self.spent:
            self.spent[category] = 0.0
        
        self.spent[category] += amount
    
    def get_remaining(self, category):
        """This method gets the remaining budget for a category.
        
        Args:
            category (str): The category name
            
        Returns:
            float: The remaining budget and negative if its over budget
            None: If there isn't a limit set for the category
        """
        category = category.strip().lower()
        
        if category not in self.limits:
            return None
        
        spent = self.spent.get(category, 0.0)
        return self.limits[category] - spent
    
    def is_over_budget(self, category):
        """This method checks if the category is over budget.
        
        Args:
            category (str): The category name
            
        Returns:
            bool: Returns true if over budget and false otherwise
        """
        remaining = self.get_remaining(category)
        if remaining is None:
            return False
        return remaining < 0
    
    def get_status(self, category):
        """This method returns a detailed status for a category.
        
        Args:
            category (str): The category name
            
        Returns:
            dict: The status information or None if no limit set
        """
        category = category.strip().lower()
        
        if category not in self.limits:
            return None
        
        limit = self.limits[category]
        spent = self.spent.get(category, 0.0)
        remaining = limit - spent

        if limit > 0:
            percentage = (spent / limit) * 100 
        else:
            percentage = 0
        
        return {
            'category': category,
            'limit': limit,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage,
            'over_budget': remaining < 0
        }
    
    def get_all_categories(self):
        """This method gets a set of all categories.
        
        Returns:
            set: All of the unique categories
        """
        all_categories = set(self.limits.keys()) | set(self.spent.keys())
        return all_categories
    
    def get_budget_report(self):
        """This method creates a complete budget report for all categories.
        
        Returns:
            list: The list of status dictionaries for all the categories with limits
        """
        report = []
        
        for category in sorted(self.limits.keys()):
            status = self.get_status(category)
            if status:
                report.append(status)
        
        return report
    
    def print_summary(self):
        """This method prints a formatted budget summary"""

        print("\n" + "="*60)
        print("BUDGET SUMMARY".center(60))
        print("="*60)
        
        if not self.limits:
            print("There isn't any budgets set yet.")
            return
        
        print(f"{'Category':<15} {'Limit':>10} {'Spent':>10} {'Remaining':>10} {'Status':>10}")
        print("-"*60)
        
        total_limit = 0
        total_spent = 0
        
        for category in sorted(self.limits.keys()):
            status = self.get_status(category)
            limit = status['limit']
            spent = status['spent']
            remaining = status['remaining']
            
            total_limit += limit
            total_spent += spent
            
            if status['over_budget']:
                indicator = "OVER BUDGET"
            elif status['percentage'] > 80:
                indicator = "HIGH PERCENTAGE"
            else:
                indicator = "Status ok!"
            
            print(f"{category:<15} ${limit:>9.2f} ${spent:>9.2f} ${remaining:>9.2f} {indicator:>10}")
        
        print("-"*60)
        print(f"{'TOTAL':<15} ${total_limit:>9.2f} ${total_spent:>9.2f} ${total_limit-total_spent:>9.2f}")
        print("="*60 + "\n")
    
    def to_dict(self):
        """This method converts the budget to a dictionary for saving.
        
        Returns:
            dict: The budget data
        """
        return {
            'limits': self.limits.copy(),
            'spent': self.spent.copy()
        }
    
    def from_dict(self, data):
        """This method loads the budget from the dictionary.
        
        Args:
            data (dict): The budget data that will be loaded
        """
        self.limits = data.get('limits', {})
        self.spent = data.get('spent', {})


