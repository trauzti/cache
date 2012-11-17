class alg:
	def __repr__(self):
		return "OPT"

	def __init__(self, c):
		self.c = c        # Cache size
		self.cn = 0       # Items in cache now
		self.stored = {}  # Stored keys
		self.hitcount = 0
		self.count = 0
		self.nextref = {}

	def getnextref(self, key):
		ne = float("inf")
		if self.nextref[key]:
			ne = self.nextref[key][-1]
		return ne

	def deletefurthest(self):
		delkey = None
		furthest = -1
		for k in self.stored.iterkeys():
			ne = self.getnextref(k)
			if ne > furthest:
				furthest = ne
				delkey = k
		assert delkey
		#print "Deleted: %s" % delkey
		del self.stored[delkey]

	def setup(self, reqlist):
		# reqlist: (mode, key , size)
		index = len(reqlist) - 1
		for line in reversed(reqlist):
			key, size = line.replace("\n", "").split(" ")[:2]
			self.nextref.setdefault(key, []).append(index)
			index -= 1
		assert index == -1

	def get(self, key):
		self.count += 1
		if key in self.stored:
			#print "Hit: %s" % key
			self.hitcount += 1
		else:
			#print "Miss: %s" % key
			self.put(key)
		assert self.nextref[key]
		self.nextref[key].pop()


	def put(self, key):
		if key not in self.stored:
			if self.cn == self.c:
				self.deletefurthest()
			else:
				self.cn += 1
			self.stored[key] = 1
