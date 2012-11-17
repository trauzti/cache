#!/usr/bin/python
#! -*- coding: utf-8 -*-
import time
import sys

#sys.path.append("/home/turtle/Research/TopSecret/")

#import CLOCK, LRU, LFU, OPT, ARC, CLOCKPRO, optimal as yopt
import CLOCK, LRU, LFU, OPT, ARC, LIRS

#DIVISOR = 40
l = [CLOCK, LRU, LFU, OPT, ARC, LIRS]
c = 10

lasttime = time.time()

def fillspace(s):
	return s + " " * (20 - len(s))

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: %s <trace file> <cache size>" % sys.argv[0]
		exit()

	f = open(sys.argv[1], "r")
	lines = f.readlines()
	f.close()
	c = int(sys.argv[2])
	for algorithm in l:
		alg = algorithm.alg(c)
		alg.setup(lines)
		for line in lines:
			key, size = line.replace("\n", "").split(" ")[:2]
			alg.get(key)

		print "%s\tHit ratio: %.4f (took %ds)" % (fillspace(str(alg)),  (0.0+alg.hitcount) / alg.count, time.time() - lasttime)
		lasttime = time.time()


