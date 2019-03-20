import sys

class State:
	def __init__(self, state, parent, heuristic):
		self.state = state
		self.parent = parent
		self.heuristic = heuristic
		self.children = []

	def __repr__(self):
		return self.state

	def __eq__(self, other):
		print(self.state)
		print(other.state)
		return self.state == other.state and self.children == other.children

	def next(self, direction, arithmetic = "sub"):
		return State(str(int(self.state) + pow(10,direction)).zfill(3), self.parent, 0) if arithmetic is "add" else \
			State(str(int(self.state) - pow(10,direction)).zfill(3), self.parent, 0)

	def last_changed_digit(self):
		if int(self.parent) - int(self.state) in [-100, 100]:
			return 2
		if int(self.parent) - int(self.state) in [-10, 10]:
			return 1
		if int(self.parent) - int(self.state) in [-1, 1]:
			return 0

	def generate_children(self):
		digit_list = [2,1,0] if self.parent is None else [2,1,0].last_changed_digit()
		for i in digit_list:
			self.children.append(self.next(i))
			self.children.append(self.next(i, "add"))

class ThreeDigitsSolver:

	def __init__(self, start_state, end_state, forbidden_states, algorithm):
		self.start_state = State(start_state, None, 0)
		self.end_state = State(end_state, None, 0)
		self.algorithm = algorithm
		self.forbidden_states = forbidden_states
		self.result = ""

	def solve(self):
		self.algorithms[self.algorithm](self)

	def print_result(self):
		print(self.result)

	def BFS(self):
		seen = [self.start_state]
		visited = [self.start_state]

		while len(seen) is not 0:
			current_state = seen.pop(0)
			current_children = current_state.generate_children()
			for state in current_state.children:
				if state not in visited and state not in self.forbidden_states:
					seen.append(state)
					if state == self.end_state:
						return seen

		return "No solution found"


	def DFS(self):
		pass

	def IDS(self):
		pass

	def greedy(self):
		pass

	def a_star(self):
		pass

	def hill_climbing(self):
		pass

	algorithms = { \
		"B" : BFS, \
		"D" : DFS, \
		"I" : IDS, \
		"G" : greedy, \
		"A" : a_star, \
		"H" : hill_climbing
	}

def main():
	try:
		algorithm = sys.argv[1]
		if algorithm not in ["B", "D", "I","G", "A", "H"]:
			raise ValueError("No algorithm is a acronym for the specified argument " + algorithm)
	except:
		sys.exit(-1)

	file = sys.argv[2]
	try:
		with open(file) as f:
			lines = f.readlines()
			lines = [line.strip() for line in lines]
	except:
		sys.exit(-1)

	solver = None
	try:
		forbidden_states = lines[2].split(",")
		solver = ThreeDigitsSolver(lines[0], lines[1], forbidden_states, algorithm)
	except:
		solver = ThreeDigitsSolver(lines[0], lines[1], None, algorithm)

	solver.solve()
	solver.print_result()
	print(lines)
	return

if __name__ == "__main__":
	main()
