import sys
from collections import OrderedDict
LIR = 0
HIR = 1

class entry:
    def __init__(self, key):
        self.key = key
        self.flag = HIR
        self.resident = True

class alg:
    def __repr__(self):
        return "LIRS"

    def __init__(self, c, **kwargs):
        # c is cache size
        self.c = c  # Max
        self.lirs = 0
        self.hirs = 0
        self.maxhirs = max(1, 0.01*c)
        self.maxlirs = c - self.maxhirs
        self.S = OrderedDict()  # Recently accessed pages (LIR pages and non-resident HIR pages), newest element is last
        self.Q = OrderedDict()  # Resident HIR pages
        self.hitcount = 0
        self.count = 0

    def setup(self, reqlist):
        # I'm an online algorithm :-)
        pass

    def get(self, key):
        #if self.count % 100 == 0:
        #       sys.stderr.write("S: %d\n" % len(self.S))
        self.countResident()
        self.count += 1
        if (key in self.S and self.S[key].resident) or key in self.Q:
            #print "HIT for %s" % key
            self.hitcount += 1
            return 1
        return 0
        #print "MISS for %s" % key

    def put(self, key, val=1):
        if key in self.S:
            e = self.S[key]
            del self.S[key]
            if e.flag == HIR:
                # A HIR block with lower reuse distance than the bottom LIR element
                if e.resident:
                    del self.Q[key]
                    self.hirs -= 1
                assert self.oldestS().flag == LIR
                assert self.hirs <= self.maxhirs
                self.swap()   # Change one LIR page to a HIR page
                self.evict()  # Keep the number of resident HIR pages <= self.maxhirs
                self.lirs += 1
            e.resident = True
            e.flag = LIR
            self.S[key] = e
            self.prune()  #  If this was a LIR element at the bottom
        elif key in self.Q:
            # Resident HIR page which is not in S, reuse distance is large so we don't make it a LIR page
            e = self.Q[key]
            assert e.resident and e.flag == HIR
            del self.Q[key]
            self.Q[key] = e
            self.S[key] = e
        else:
            # not in cache
            # When a miss occurs and a free block is needed for replacement, we choose an HIR block that is resident in the cache
            e = entry(key)
            if self.lirs < self.maxlirs:
                e.flag = LIR   # Not using all the cache, make it a LIR page
                self.lirs += 1
            else:
                # NOTE: Not changing the number of LIR blocks!
                self.Q[key] = e
                self.hirs += 1
                self.evict() # Evicting if we have max number of HIR blocks
            self.S[key] = e

        assert self.oldestS().flag == LIR
        self.countResident()

    def countResident(self):
        sm = 0
        for key, e in self.S.items():
            sm += 1 if e.resident else 0
        for key, e in self.Q.items():
            sm += 1 if key not in self.S else 0
        if sm != self.lirs + self.hirs:
            print "sm=%d, self.lirs=%d, self.hirs=%d" % (sm, self.lirs, self.hirs)
        assert sm == self.lirs + self.hirs

    def evict(self):
        if self.hirs > self.maxhirs:        # Setting the size of Q
            k, e_hir = self.Q.popitem(last=False)
            assert e_hir.flag == HIR and e_hir.resident
            e_hir.resident = False                # It is maybe in S
            self.hirs -= 1
        if self.hirs > self.maxhirs:
            print "hirs: %d maxhirs: %d" % (self.hirs, self.maxhirs)
        assert self.hirs <= self.maxhirs
        # TODO: If there are many nonresident entries in S, should we delete this from S?

    def swap(self):
        key, e = self.S.popitem(last=False)
        assert e.flag == LIR and e.resident
        e.flag = HIR
        self.hirs += 1
        self.lirs -= 1
        self.Q[e.key] = e
        # Switched this LIR block to HIR and put it in Q
        # Important! We don't put it back in S


    def prune(self):
        while self.S:
            oldest = self.oldestS()
            if oldest.flag == LIR:
                break
            k, dele = self.S.popitem(last=False)
            assert dele.flag == HIR
            if dele.resident:
                assert k in self.Q
            else:
                assert k not in self.Q

    def oldestS(self):
        return self.S.itervalues().next()

    def oldestQ(self):
        return self.Q.itervalues().next()
