"""This file contains the transaction base class and subclasses."""

from datetime import datetime
import re

class Transaction:
    """This class is for all financial transactions."""
    
    def __init__(self, date, amount, category, description):
        """This method initializes a transaction.

        Args:
            date (str): This is the date in format 'YYYY-MM-DD'
            amount (float): The transaction amount
            category (str): The transaction category
            description (str): A brief description of the transaction
        """
        self.date = self.validate_date(date)
        self.amount = self.validate_amount(amount)
        self.category = category.strip().lower()
        self.description = description.strip()
        self.transaction_id = None 
    
    def validate_date(self, date):
        """This method validates the date format.

        Args:
            date (str): The date in string form for validation
            
        Returns:
            str: The validated date string
            
        Raises:
            ValueError: If date format is invalid
        """
        pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
        
        if not re.match(pattern, date):
            raise ValueError(f"Invalid date format: {date}. Use YYYY-MM-DD instead")
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date: {date}")
        
        return date
    
    def validate_amount(self, amount):
        """This method validates the transaction amount.
        
        Args:
            amount: The amount to validate which can be a string or number
            
        Returns:
            float: The validated amount
            
        Raises:
            ValueError: If amount is invalid
        """
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Has to be a positive amount.")
            return round(amount, 2)  
        except (ValueError, TypeError):
            raise ValueError(f"Invalid amount: {amount}")
    
    def to_dict(self):
        """This method converts the transaction to a dictionary.
        
        Returns:
            dict: The transaction data as a dictionary
        """
        return {
            'id': self.transaction_id,
            'date': self.date,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'type': self.__class__.__name__
        }
    
    def __str__(self):
        """The method returns the string representation of the transaction."""
        return f"{self.date} | {self.category:15} | ${self.amount:8.2f} | {self.description}"

class Income(Transaction):
    """This method works aa a income transaction subclass."""
    
    def __init__(self, date, amount, category, description):
        """This method initializes the income transaction"""
        super().__init__(date, amount, category, description)
    
    def __str__(self):
        """This method returns a string representation with a income indicator"""
        return f"{self.date} | {self.category:15} | +${self.amount:8.2f} | {self.description}"


class Expense(Transaction):
    """This class works as a expense transaction subclass."""
    
    def __init__(self, date, amount, category, description):
        """This method initializes the expense transaction"""
        super().__init__(date, amount, category, description)
    
    def __str__(self):
        """This method returns a string representation with a expense indicator"""
        return f"{self.date} | {self.category:15} | -${self.amount:8.2f} | {self.description}"


