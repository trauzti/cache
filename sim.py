#!/usr/bin/python
#! -*- coding: utf-8 -*-
import os
import time
import sys

import CLOCK, LRU, LFU, OPT, ARC, LIRS, RANDOM, kRANDOM_LRU, SkLRU

l = { "CLOCK": CLOCK,
      "LRU": LRU,
      "LFU": LFU,
      "OPT": OPT,
      "LIRS": LIRS,
      "ARC": ARC,
      "RANDOM": RANDOM,
#      "kRANDOM_LRU": kRANDOM_LRU, #  handled differently
}


def fillspace(s):
    return s + " " * (20 - len(s))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: %s <algorithm> <trace file> <cache size>" % sys.argv[0]
        exit()

    algn = sys.argv[1]
    k = None
    if algn.find("RANDOM_LRU") >= 0:
        algm = kRANDOM_LRU
        k = int(algn.replace("RANDOM_LRU_", ""))
    elif algn[0] == "S" and algn.find("LRU") > 0:
        algm = SkLRU
        k = int(algn[1:].replace("LRU", ""))
    elif algn not in l:
        print "Algorithm: %s does not exist" % algn
        exit()
    else:
        algm =  l[algn]

    f = open(sys.argv[2], "r")
    c = int(sys.argv[3])
    lines = f.readlines()
    f.close()
    alg = algm.alg(c, k=k)
    alg.setup(lines)

    time1 = time.time()
    lc = 0
    for line in lines:
        lc += 1
        key = line.replace("\n", "").split(" ")[0]
        ret = alg.get(key)
        if not ret:
            alg.put(key, 1)

    time2 = time.time()
    diff = time2-time1
    tp = lc / (0.0 + diff)
    hr = alg.hitcount / (0.0 + alg.count)
    print "%s %d %.4f %.2f" % (str(alg), c, 100.0*hr, tp)
    sys.stderr.write("%s with %d\tHit ratio: %.4f\tThroughput: %.2f (reqs/s)\n" % (fillspace(str(alg)), c, hr, tp))
