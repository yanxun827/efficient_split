def greedy(balances_dict):
	positive_balance_dict = {name: balance for name, balance in balances_dict.items() if balance > 0}
	negative_balance_dict = {name: balance for name, balance in balances_dict.items() if balance < 0}

	transactions = []
	while not all(value == 0 for value in positive_balance_dict.values()):
		min_pos_name = min(positive_balance_dict, key=positive_balance_dict.get)
		max_neg_name = max(negative_balance_dict, key=negative_balance_dict.get)

		offset = positive_balance_dict[min_pos_name] + negative_balance_dict[max_neg_name]

		if offset > 0:
			num = round(abs(negative_balance_dict[max_neg_name]), 2)
			positive_balance_dict[min_pos_name] = offset
			del negative_balance_dict[max_neg_name]
			transactions.append([min_pos_name, max_neg_name, num])
		elif offset < 0:
			num = round(abs(positive_balance_dict[min_pos_name]), 2)
			negative_balance_dict[max_neg_name] = offset
			del positive_balance_dict[min_pos_name]
			transactions.append([min_pos_name, max_neg_name, num])
		elif offset == 0:
			num = round(abs(positive_balance_dict[min_pos_name]), 2)
			del positive_balance_dict[min_pos_name]
			del negative_balance_dict[max_neg_name]
			transactions.append([min_pos_name, max_neg_name, num])

		# To ignore floating point inaccuracies
		positive_balance_dict = {n: b for n, b in positive_balance_dict.items() if abs(b) > 0.01}
		negative_balance_dict = {n: b for n, b in negative_balance_dict.items() if abs(b) > 0.01}
	return transactions


def match_equal(balances_dict):
	positive_balance_dict = {name: balance for name, balance in balances_dict if balance > 0}
	negative_balance_dict = {name: balance for name, balance in balances_dict if balance < 0}

	transactions = []
	for pos_name, pos_balance in positive_balance_dict.items():
		for neg_name, neg_balance in negative_balance_dict.items():
			if pos_balance == -neg_balance:
				positive_balance_dict[pos_name] = 0
				negative_balance_dict[neg_name] = 0
				transactions.append([pos_name, neg_name, pos_balance])
				break
	return transactions


if __name__ == '__main__':
	pass
"""
def n():
	l = [name for name, balance in positive_balance_dict.items() if balance in negative_balance_dict.values()]

"""