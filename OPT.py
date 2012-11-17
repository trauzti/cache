from heapq import heappush, heappop

class alg:
	def __repr__(self):
		return "OPT"

	def __init__(self, c):
		self.c = c        # Cache size
		self.cn = 0       # Items in cache now
		self.stored = {}  # Stored keys
		self.heap = []    # (-dist, key, valid)
		self.hitcount = 0
		self.count = 0
		self.nextref = {}

	def getnextref(self, key):
		ne = float("inf")
		if self.nextref[key]:
			ne = self.nextref[key][-1]
		return ne

	def deletefurthest(self):
		valid = False
		delkey = None
		while not valid:
			deldist, delkey, valid = heappop(self.heap)
		realdeldist = -deldist
		#print "Deleting %s from cache, dist is %s" %(delkey, realdeldist)
		item = self.stored[delkey]
		assert item[0] == deldist
		assert item[1] == delkey
		del self.stored[delkey]
		for k,v in self.stored.items():
			thisdist, thiskey, valid = v
			realthisdist = -thisdist
			assert realthisdist <= realdeldist

	def setup(self, reqlist):
		# reqlist: (mode, key , size)
		index = len(reqlist) - 1
		for line in reversed(reqlist):
			key, size = line.replace("\n", "").split(" ")[:2]
			self.nextref.setdefault(key, []).append(index)
			index -= 1
		assert index == -1


	def get(self, key):
		#print "Cache: %s" % self.stored.keys()
		assert self.nextref[key]
		self.count += 1
		self.nextref[key].pop()
		if key in self.stored:
			#print "Hit on %s, next reference is %s" % (key, self.getnextref(key))
			old = self.stored[key]
			old[2] = False
			nr = self.getnextref(key)
			item = [-nr, key, True]
			self.stored[key] = item
			heappush(self.heap, item)
			self.hitcount += 1
		else:
			#print "Miss on %s" % (key)
			self.put(key)


	def put(self, key):
		if key not in self.stored:
			if self.cn == self.c:
				self.deletefurthest()
			else:
				self.cn += 1
			dist = self.getnextref(key)
			item  = [-dist, key, True]
			self.stored[key] = item
			heappush(self.heap, item)
