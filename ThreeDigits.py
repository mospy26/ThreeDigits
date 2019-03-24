import sys
import heapq

class State:
	def __init__(self, state, parent = None, heuristic = 99):
		self.state = state
		self.parent = parent
		self.heuristic = heuristic
		self.children = []
		self.recently_added = False

	def __repr__(self):
		return self.state

	def __eq__(self, other):
		is_same_parent = False if self.parent is None or other.parent is None else self.parent.state == other.parent.state
		return self.state == other.state and self.children == other.children and is_same_parent

	def __lt__(self, other):
		return self.heuristic < other.heuristic and self.recently_added and not other.recently_added

	def _next(self, direction, arithmetic = "sub"):
		if (self.state[0], direction, arithmetic) in [("0", 2, "sub"),("9", 2, "add")] or \
			(self.state[1], direction, arithmetic) in [("0", 1, "sub"),("9", 1, "add")] or \
			(self.state[2], direction, arithmetic) in [("0", 0, "sub"),("9", 0, "add")]:
				return None
		return State(str(int(self.state) + pow(10,direction)).zfill(3), self, 0) if arithmetic is "add" else \
			State(str(int(self.state) - pow(10,direction)).zfill(3), self, 0)

	def _last_changed_digit(self):
		if int(self.parent.state) - int(self.state) in [-100, 100]:
			return 2
		if int(self.parent.state) - int(self.state) in [-10, 10]:
			return 1
		if int(self.parent.state) - int(self.state) in [-1, 1]:
			return 0

	def generate_children(self, forbidden_states):
		digit_list = [2,1,0]
		if self.parent is not None:
			digit_list.remove(self._last_changed_digit())

		for i in digit_list:
			child = self._next(i)
			if child is not None and not self._is_forbidden(forbidden_states):
				child.parent = self
				self.children.append(child)

			child = self._next(i, "add")
			if child is not None and not self._is_forbidden(forbidden_states):
				child.parent = self
				self.children.append(child)
		return

	def generate_children_with_heuristic(self, forbidden_states, end_state):
		digit_list = [2,1,0]
		if self.parent is not None:
			digit_list.remove(self._last_changed_digit())

		for i in digit_list:
			child = self._next(i)
			if child is not None and not self._is_forbidden(forbidden_states):
				child.heuristic = child._heuristic(end_state)
				child.parent = self
				self.children.append(child)

			child = self._next(i, "add")
			if child is not None and not self._is_forbidden(forbidden_states):
				child.heuristic = child._heuristic(end_state)
				child.parent = self
				self.children.append(child)
		return

	def _is_forbidden(self, forbidden_states):
		if forbidden_states is None:
			return False
		for forbidden_state in forbidden_states:
			if self.state == forbidden_state.state:
				return True
		return False

	def _heuristic(self, end_state):
		return None if self.parent is None else sum(abs(int(d2) - int(d1)) for (d1,d2) in zip(self.state, end_state.state))


class ThreeDigitsSolver:

	def __init__(self, start_state, end_state, forbidden_states, algorithm):
		self.start_state = State(start_state)
		self.end_state = State(end_state)
		self.algorithm = algorithm
		self.forbidden_states = forbidden_states
		self.result = ["No solution Found", ""]

	def solve(self):
		self.algorithms[self.algorithm](self)
		self._print_result()

	def _print_result(self):
		print(self.result[0] + "\n" + self.result[1])

	def BFS(self):

		if self.end_state.state == self.start_state.state:
			self.result[0] = self.start_state.state
			self.result[1] = repr(self.start_state.state).replace(" ", "")[1:-1]
			return

		seen = [self.start_state]
		visited = [self.start_state]

		expanded = []

		while len(seen) != 0 and len(expanded) <= 1000:
			current_state = seen.pop(0)
			current_state.generate_children(self.forbidden_states)
			expanded.append(current_state)

			if self.end_state.state == current_state.state:
				path = []
				st = current_state
				while st is not None:
					path.insert(0, st)
					st = st.parent
				self.result[0] = repr(path).replace(" ", "")[1:-1]
				self.result[1] = repr(expanded).replace(" ", "")[1:-1]
				return

			for state in current_state.children:
				if state not in visited:
					seen.append(state)
					visited.append(state)

		self.result[0] = "No Solution Found"
		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		return


	def DFS(self):

		if self.end_state.state == self.start_state.state:
			self.result[0] = self.start_state.state
			self.result[1] = repr(self.start_state.state).replace(" ", "")[1:-1]
			return

		seen = [self.start_state]
		visited = [self.start_state]

		expanded = []

		while len(seen) != 0 and len(expanded) <= 1000:
			current_state = seen.pop(0)
			current_state.generate_children(self.forbidden_states)
			expanded.append(current_state)

			if self.end_state.state == current_state.state:
				path = []
				st = current_state
				while st is not None:
					path.insert(0, st)
					st = st.parent
				self.result[0] = repr(path).replace(" ", "")[1:-1]
				self.result[1] = repr(expanded).replace(" ", "")[1:-1]
				return

			dfs_list = []
			for state in current_state.children:
				if state not in visited:
					dfs_list.append(state)
					visited.append(state)
				for item in reversed(dfs_list):
					seen.insert(0, item)
			dfs_list = []

		self.result[0] = "No Solution Found"
		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		return

	def IDS(self):
		depth = 0
		expanded = []
		while len(expanded) <= 1000:
			if self._depth_limited_search(expanded, depth):
				return
			else:
				depth += 1

	def greedy(self):
		expanded = []
		fringe = [self.start_state]
		heapq.heapify(fringe)

		while len(expanded) <= 1000:
			current_state = fringe.pop(0)
			expanded.append(current_state)

			if self.end_state.state == current_state.state:
				path = []
				st = current_state
				while st is not None:
					path.insert(0, st)
					st = st.parent
				self.result[0] = repr(path).replace(" ", "")[1:-1]
				self.result[1] = repr(expanded).replace(" ", "")[1:-1]
				return

			current_state.generate_children_with_heuristic(self.forbidden_states, self.end_state)
			for child in current_state.children:
				child.recently_added = True
				heapq.heappush(fringe, child)
				child.recently_added = False


	def a_star(self):
		pass

	def hill_climbing(self):
		pass

	def _depth_limited_search(self, expanded, depth):
		seen = [self.start_state]
		visited = [self.start_state]

		if self.end_state.state == self.start_state.state:
			self.result[0] = self.start_state.state
			self.result[1] = repr(self.start_state.state).replace(" ", "")[1:-1]
			return True

		d = depth

		if d == 0:
			expanded.append(seen.pop(0))

		while len(seen) != 0 and len(expanded) <= 1000:
			if d > 0:
				for state in seen:
					state.generate_children(self.forbidden_states)
			d -= 1
			current_state = seen.pop(0)
			expanded.append(current_state)

			if self.end_state.state == current_state.state:
				path = []
				st = current_state
				while st is not None:
					path.insert(0, st)
					st = st.parent
				self.result[0] = repr(path).replace(" ", "")[1:-1]
				self.result[1] = repr(expanded).replace(" ", "")[1:-1]
				return True

			dfs_list = []
			for state in current_state.children:
				if state not in visited:
					dfs_list.append(state)
					visited.append(state)
			for item in reversed(dfs_list):
				seen.insert(0, item)

		#expanded = []
		# += reversed(seen)

		self.result[0] = "No Solution Found"
		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		return False

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
		forbidden = lines[2].split(",")
		forbidden_states = [State(state, None, 0) for state in forbidden]
		solver = ThreeDigitsSolver(lines[0], lines[1], forbidden_states[:], algorithm)
	except:
		solver = ThreeDigitsSolver(lines[0], lines[1], None, algorithm)

	solver.solve()
	return

if __name__ == "__main__":
	main()
