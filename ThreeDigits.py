import sys
import heapq

class State:
	def __init__(self, state, parent = None, heuristic = -1):
		self.state = state
		self.parent = parent
		self.heuristic = heuristic
		self.children = []
		self.recently_added = False

	def __repr__(self):
		return self.state

	def __eq__(self, other):
		# if self.state == '011' and other.state == '011':
		# 	print(self.state + ":" + repr(self.children))
		# 	print(other.state + ":" + repr(other.children))
		# 	print(self.state == other.state and self._have_same_children(other))
		return self.state == other.state and self._have_same_children(other)

	def __lt__(self, other):
		if self.heuristic < other.heuristic:
			return True
		elif self.heuristic == other.heuristic:
			return self.recently_added and not other.recently_added

	def _have_same_children(self, other):
		if len(self.children) != len(other.children):
			return False
		for (self_child, other_child) in zip(self.children, other.children):
			if self_child.state != other_child.state:
				return False
		return True

	def _next(self, direction, arithmetic = "sub"):
		return None if (self.state[0], direction, arithmetic) in [("0", 2, "sub"),("9", 2, "add")] or \
			(self.state[1], direction, arithmetic) in [("0", 1, "sub"),("9", 1, "add")] or \
			(self.state[2], direction, arithmetic) in [("0", 0, "sub"),("9", 0, "add")] \
			else State(str(int(self.state) + pow(10,direction)).zfill(3), self, 0) if arithmetic is "add" else \
				State(str(int(self.state) - pow(10,direction)).zfill(3), self, 0)

	def _last_changed_digit(self):
		if int(self.parent.state) - int(self.state) in [-100, 100]:
			return 2
		if int(self.parent.state) - int(self.state) in [-10, 10]:
			return 1
		if int(self.parent.state) - int(self.state) in [-1, 1]:
			return 0

	def generate_children(self, forbidden_states, end_state, algorithm):
		if len(self.children) != 0:
			return
		digit_list = [2,1,0]
		if self.parent is not None:
			digit_list.remove(self._last_changed_digit())

		for i in digit_list:
			for arithmetic in ["sub", "add"]:
				child = self._next(i, arithmetic)
				if child is not None and not child._is_forbidden(forbidden_states):
					child.heuristic = child._heuristic(end_state) if algorithm in ["G", "A", "H"] else -1
					child.parent = self
					self.children.append(child)

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
		if self.end_state.state == self.start_state.state:
			self.result = [self.start_state.state, repr(self.start_state.state).replace(" ", "")[1:-1]]
			return
		self.algorithms[self.algorithm](self)
		self._print_result()

	def _print_result(self):
		print(self.result[0] + "\n" + self.result[1])

	def BFS(self):
		seen = [self.start_state]
		visited = [self.start_state]
		expanded = []

		while len(seen) != 0 and len(expanded) <= 1000:
			current_state = seen.pop(0)
			current_state.generate_children(self.forbidden_states, self.end_state, self.algorithm)
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
				state.generate_children(self.forbidden_states, self.end_state, self.algorithm)
				if state not in visited:
					seen.append(state)
					visited.append(state)

		self.result[0] = "No Solution Found"
		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		return

	def DFS(self):
		expanded = []
		self._depth_limited_search(expanded, -1)

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
		visited = [self.start_state]
		heapq.heapify(fringe)

		while len(fringe) > 0 and len(expanded) <= 1000:
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

			current_state.generate_children(self.forbidden_states, self.end_state, self.algorithm)

			for child in current_state.children:
				child.generate_children(self.forbidden_states, self.end_state, self.algorithm)
				if child not in visited:
					child.recently_added = True
					heapq.heappush(fringe, child)
					heapq.heapify(fringe)
					child.recently_added = False
					visited.append(child)

		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		return

	def a_star(self):
		pass

	def hill_climbing(self):
		pass

	def _depth_limited_search(self, expanded, depth):
		fringe = [self.start_state]
		visited = [self.start_state]
		d = depth

		if d == 0:
			expanded.append(fringe.pop(0))

		while len(fringe) > 0 and len(expanded) <= 1000:
			if d != 0:
				for states in fringe:
					states.generate_children(self.forbidden_states, self.end_state, self.algorithm)
				d -= 1

			current_state = fringe.pop(0)
			expanded.append(current_state)
			visited.append(current_state)

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
			for states in current_state.children:
				if d != 0:
					states.generate_children(self.forbidden_states, self.end_state, self.algorithm)

				if len(dfs_list) == 0 and states.state == self.end_state.state and len(expanded) <= 1000:
					expanded.append(states)
					path = []
					st = states
					while st is not None:
						path.insert(0, st)
						st = st.parent
					self.result[0] = repr(path).replace(" ", "")[1:-1]
					self.result[1] = repr(expanded).replace(" ", "")[1:-1]
					return

				if states not in visited:
					dfs_list.append(states)
					#visited.append(states)
			for item in reversed(dfs_list):
					fringe.insert(0, item)

		self.result[0] = "No Solution Found"
		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		return False



		# if d == 0:
		# 	expanded.append(seen.pop(0))
		#
		# while len(seen) != 0 and len(expanded) <= 1000:
		# 	if d != 0:
		# 		for states in seen:
		# 			states.generate_children(self.forbidden_states, self.end_state, self.algorithm)
		# 		d -= 1
		# 	current_state = seen.pop(0)
		# 	expanded.append(current_state)
		#
		# 	if self.end_state.state == current_state.state:
		# 		path = []
		# 		st = current_state
		# 		while st is not None:
		# 			path.insert(0, st)
		# 			st = st.parent
		# 		self.result[0] = repr(path).replace(" ", "")[1:-1]
		# 		self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		# 		return True
		#
		# 	dfs_list = []
		# 	for states in current_state.children:
		# 		# only generate children to check if its visited if there is depth left
		# 		if d != 0:
		# 		 	states.generate_children(self.forbidden_states, self.end_state, self.algorithm)
		#
		# 		if len(dfs_list) == 0 and states.state == self.end_state.state:
		# 			expanded.append(states)
		# 			path = []
		# 			st = states
		# 			while st is not None:
		# 				path.insert(0, st)
		# 				st = st.parent
		# 			self.result[0] = repr(path).replace(" ", "")[1:-1]
		# 			self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		# 			return
		#
		# 		if states not in visited:
		# 			dfs_list.append(states)
		# 			visited.append(states)
		# 	for item in reversed(dfs_list):
		# 		seen.insert(0, item)
		#
		# self.result[0] = "No Solution Found"
		# self.result[1] = repr(expanded).replace(" ", "")[1:-1]
		# return False

	algorithms = {"B" : BFS, "D" : DFS, "I" : IDS, "G" : greedy, "A" : a_star, "H" : hill_climbing}

def main():
	try:
		algorithm = sys.argv[1]
		if algorithm not in ["B", "D", "I", "G", "A", "H"]:
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
