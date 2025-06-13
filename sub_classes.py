# Current Account

import pandas as pd
import io
import streamlit as st
from abc import ABC, abstractmethod
from datetime import datetime
from bank import BankAccount

class CurrentAccount(BankAccount):
	def deposit(self, amount):
		if amount > 0:
			self._balance += amount
			self._log_transaction("Deposit", amount)
	
	def withdraw(self, amount):
		if 0 < amount <= self._balance:
			self._balance -= amount
			self._log_transaction("Withdraw", amount)
			return True
		return False

# Savings Account

class SavingsAccount(BankAccount):
	def __init__(self, owner, withdrawal_limit=5000000.0):
		super().__init__(owner)
		self._withdrawal_limit = withdrawal_limit
	
	def deposit(self, amount):
		if amount > 0:
			self._balance += amount
			self._log_transaction("Deposit", amount)
	
	def withdraw(self, amount):
		if 0 < amount <= self._withdrawal_limit and amount <= self._balance:
			self._balance -= amount
			self._log_transaction("Withdraw", amount)
			return True
		return False
