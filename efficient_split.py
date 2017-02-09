import tkinter as tk
import os
import sys

import algorithms


class EfficientSplitApp(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.pack()

		self.debtor_entries = []
		self.transactions = []

		self.create_widgets()

	def create_widgets(self):
		"""Builds GUI."""
		self.parent.title('SplitApp')

		# Inputs.
		self.creditor_input_label = tk.Label(self, text="Creditor")
		self.creditor_input_label.grid(row=0, column=0, sticky='e')

		self.creditor_input_entry = tk.Entry(self)
		self.creditor_input_entry.grid(row=0, column=1)

		self.price_input_label = tk.Label(self, text='Price')
		self.price_input_label.grid(row=1, column=0, sticky='e')

		vcmd = (self.register(self.validate_float),
				'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

		self.price_input_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
		self.price_input_entry.grid(row=1, column=1)

		self.food_input_label = tk.Label(self, text='Food')
		self.food_input_label.grid(row=2, column=0, sticky='e')

		self.food_input_entry = tk.Entry(self)
		self.food_input_entry.grid(row=2, column=1)

		# Dynamic addition of entries.
		self.add_debtor_label = tk.Label(self, text="new debtors")
		self.add_debtor_label.grid(row=3, column=1)

		vcmd = (self.register(self.validate_int),
				'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
		self.new_debtor_entry = tk.Entry(self, width=5, validate='key', validatecommand=vcmd)
		self.new_debtor_entry.insert(0, '1')
		self.new_debtor_entry.grid(row=3, column=1, sticky='w')

		self.add_debtor_button = tk.Button(self, text="Add", command=self.add_debtor_entry)
		self.add_debtor_button.grid(row=3, column=0, sticky='e')

		self.debtor_label = tk.Label(self, text="Debtors")
		self.debtor_label.grid(row=4, column=0, columnspan=2)

		# Operation buttons.
		self.enter_button = tk.Button(self, text="Enter", command=self.read_input)
		self.enter_button.grid(row=2, column=2)

		self.clear_button = tk.Button(self, text='Clear All', fg='red', command=self.clear_entries)
		self.clear_button.grid(row=6, column=2)

		self.delete_button = tk.Button(self, text="delete entry", command=self.delete_input)
		self.delete_button.grid(row=4, column=2)

		# Listboxes.
		self.input_listbox_label = tk.Label(self, text="Transactions")
		self.input_listbox_label.grid(row=0, column=3)

		self.input_listbox = tk.Listbox(self)
		self.input_listbox.grid(row=1, column=3, columnspan=2, rowspan=6, sticky='nsew')

		self.results_listbox_label = tk.Label(self, text="Results")
		self.results_listbox_label.grid(row=7, column=3)

		self.results_listbox = tk.Listbox(self)
		self.results_listbox.grid(row=8, column=3, columnspan=2, rowspan=6, sticky='nsew')

		# Initial debtor entries.
		self.new_debtor_row = 4
		self.new_debtor_col = 0
		self.add_debtor_entry(10)

	# Buttons functions
	def read_input(self):
		creditor = self.creditor_input_entry.get().title()
		self.creditor_input_entry.delete(0, 'end')

		price = float(self.price_input_entry.get())
		self.price_input_entry.delete(0, 'end')

		food = self.food_input_entry.get()
		self.food_input_entry.delete(0, 'end')

		debtors = []
		for debtor_ent in self.debtor_entries:
			debtor_name = debtor_ent.get().title()
			if debtor_name:
				debtors.append(debtor_name)
				debtor_ent.delete(0, 'end')

		debtors_str = ', '.join(debtors)
		input_text = '{} paid {} for {} for {}'.format(creditor, price, food, debtors_str)
		self.input_listbox.insert('active', input_text)

		self.transactions.append([creditor, price, debtors, input_text])

		self.calculate()

	def add_debtor_entry(self, new_debtor_num=None):
		if new_debtor_num == None:
			new_debtor_num = int(self.new_debtor_entry.get())

		for i in range(new_debtor_num):
			new_entry = tk.Entry(self)
			new_entry.grid(column=self.new_debtor_col, row=self.new_debtor_row)
			self.debtor_entries.append(new_entry)

			if self.new_debtor_col == 0:
				self.new_debtor_col = 1
			else:
				self.new_debtor_col = 0
				self.new_debtor_row += 1

	def clear_entries(self):
		self.creditor_input_entry.delete(0, 'end')
		self.price_input_entry.delete(0, 'end')
		self.food_input_entry.delete(0, 'end')
		self.results_listbox.delete(0, 'end')
		self.input_listbox.delete(0, 'end')
		for ent in self.debtor_entries:
			ent.delete(0, 'end')

	def delete_input(self):
		selected = self.input_listbox.curselection()
		if selected:
			selected_index = selected[0]
			selection = self.input_listbox.get(selected_index)
			for t in self.transactions:
				if t[3] == selection:
					self.transactions.remove(t)
					break
			self.input_listbox.delete(selected_index)

		self.calculate()

	# Validations
	def validate_int(self, d, i, P, s, S, v, V, W):
		if not P:
			return True
		try:
			int(P)
			return True
		except ValueError:
			return False

	def validate_float(self, d, i, P, s, S, v, V, W):
		if not P:
			return True
		try:
			float(P)
			return True
		except ValueError:
			return False

	# Calculation and algorithms
	def calculate(self):
		self.results_listbox.delete(0, 'end')
		people = {}

		# read from database to prepare for calculation.
		for [creditor, price, debtors, _] in self.transactions:
			if creditor not in people:
				people[creditor] = 0
			people[creditor] -= price

			num_debtor = len(debtors)
			debtor_price = round((price / num_debtor), 2)

			for debtor_name in debtors:
				if debtor_name not in people:
					people[debtor_name] = 0

				people[debtor_name] += debtor_price

		# Calculation algorithm here.
		results = algorithms.greedy(people)

		for r in results:
			result_str = '{} owes {} {}'.format(r[0], r[1], r[2])
			self.results_listbox.insert('active', result_str)


if __name__ == "__main__":
	root = tk.Tk()

	if sys.platform == 'darwin':
		os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

	app = EfficientSplitApp(root)
	app.mainloop()

# wgeomtrical positon problem
# https://luckytoilet.wordpress.com/2014/04/05/splitting-utility-costs-between-roommates-is-np-complete/
# http://stackoverflow.com/questions/877728/what-algorithm-to-use-to-determine-minimum-number-of-actions-required-to-get-the