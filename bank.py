import pandas as pd
import io
import streamlit as st
from abc import ABC, abstractmethod
from datetime import datetime


# Abstract base class
class BankAccount(ABC):
	def __init__(self, owner):
		self._owner = owner
		self._balance = 0.0
		self._transactions = []
	
	@abstractmethod
	def deposit(self, amount):
		pass
	
	# this was overridden
	
	@abstractmethod
	def withdraw(self, amount):
		pass
	
	# this was overridden
	
	def get_balance(self):
		return self._balance
	
	def get_transactions(self):
		return self._transactions
	
	def _log_transaction(self, type_, amount):
		self._transactions.append({
			"type": type_,
			"amount": amount,
			"balance": self._balance,
			"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		})


# Savings Account
class SavingsAccount(BankAccount):
	def __init__(self, owner, withdrawal_limit=2500000.0):
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


# Current Account
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


def main():
	st.set_page_config(page_icon="💰", page_title="Bank Account App", layout="centered")
	st.title("🏦 Simple Bank Account App")
	
	account_type = st.selectbox("Select Account Type", ["Savings", "Current"])
	name = st.text_input("Enter Account Holder Name", "")
	
	# Initialize account in session state
	if "account" not in st.session_state or st.session_state.account_type != account_type:
		st.session_state.account_type = account_type
		if account_type == "Savings":
			st.session_state.account = SavingsAccount(name)
		else:
			st.session_state.account = CurrentAccount(name)
	
	account = st.session_state.account
	
	st.subheader(f"Welcome, {name}")
	st.info(f"💵 Current Balance: ${account.get_balance():.2f}")
	
	choice = st.radio("Make a choice", ["Deposit", "Withdraw"])
	amount = st.number_input("Enter amount", min_value=10.0, step=100.0)
	
	if st.button("Submit Transactions"):
		if choice == "Deposit":
			account.deposit(amount)
			st.success(f"Deposited ${amount:.2f}")
		elif choice == "Withdraw":
			success = account.withdraw(amount)
			if success:
				st.success(f"Withdrew ${amount:.2f}")
			else:
				if account_type == "Savings":
					st.error(f"❌ Withdrawal failed: Max ${account._withdrawal_limit} or insufficient balance.")
				else:
					st.error("❌ Withdrawal failed: Insufficient balance.")
	
	# Show transactions history
	st.subheader("📜 Transaction History")
	transactions = account.get_transactions()
	if transactions:
		df = pd.DataFrame(transactions)
		st.table(df)
		
		# Create CSV format Download button
		csv = df.to_csv(index=False).encode("utf-8")
		st.download_button(label="📩 Download Transaction History as CSV", data=csv,
		                   file_name="transactions_history.csv",
		                   mime="text/csv")
	else:
		st.write("No transactions yet.")


if __name__ == "__main__":
	main()
