class alg:
	def __repr__(self):
		return "LFU"

	def __init__(self, c):
		# c is cache size
		self.c = c
		self.cache = []
		self.stored = {}
		self.hitcount = 0
		self.count = 0

	def setup(self, reqlist):
		# I'm an online algorithm :-)
		pass

	def get(self, key):
		self.count += 1
		if key in self.stored:
			self.hitcount += 1
			self.stored[key] += 1
		else:
			self.put(key)

	def put(self, key):
		if key not in self.stored:
			self.stored[key] = 1
			if len(self.cache) == self.c:
				_min = float("inf")
				_mindex = -1
				_minitem = None
				for i in xrange(self.c):
					item = self.cache[i]
					if self.stored[item] < _min:
						# Maybe a little biased to delete the first low item
						_min = self.stored[item]
						_mindex = i
						_minitem = item
				assert _mindex >= 0
				del self.stored[_minitem]
				self.cache[_mindex] = key
			else:
				self.cache.append(key)
			self.stored[key] = 1
