#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import sys

sys.path.append("/home/turtle/Research/TopSecret/")

import CLOCK, LRU, LFU, OPT, ARC, CLOCKPRO
#import CLOCK, LRU, LFU, OPT, ARC #, LIRS

l = { "CLOCK": CLOCK,
      "CLOCKPRO": CLOCKPRO,
      "LRU": LRU,
	  "LFU": LFU,
	  "OPT": OPT,
	  "ARC": ARC }

if not os.path.isdir("results/"):
	os.makedirs("results/")


lasttime = time.time()

def fillspace(s):
	return s + " " * (20 - len(s))

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Usage: %s <algorithm> <trace file> <cache size>" % sys.argv[0]
		exit()

	if sys.argv[1] not in l:
		print "Algorithm: %s does not exist" % sys.argv[3]
		exit()

	algm =  l[sys.argv[1]]
	f = open(sys.argv[2], "r")
	c = int(sys.argv[3])
	lines = f.readlines()
	f.close()
	alg = algm.alg(c)
	alg.setup(lines)
	for line in lines:
		key, size = line.replace("\n", "").split(" ")[:2]
		alg.get(key)

	print "%s %d %.1f" % (str(alg), c, 100.0*alg.hitcount / alg.count )
	sys.stderr.write("%s with %d\tHit ratio: %.4f (took %ds)\n" % (fillspace(str(alg)), c,  (0.0+alg.hitcount) / alg.count, time.time() - lasttime))
	lasttime = time.time()
