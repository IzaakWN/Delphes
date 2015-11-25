

P_btag = 0.62
P_no_btag = 1 - P_btag
P_fake = 0.03
P_no_fake = 1 - P_fake


no_btags = 1 - P_no_btag * P_no_btag * P_no_fake * P_no_fake
print "No b-tags out of four jets:    %s" % no_btags

one_btags1 = 2 * P_btag    * P_no_btag * P_no_fake * P_no_fake
one_btags2 = 2 * P_no_btag * P_no_btag * P_fake    * P_no_fake
one_btags = one_btags1 + one_btags2
print "One b-tag out of four jets:    %s" % one_btags
print "    One correct b-tag: %s" % (one_btags1/one_btags)
print "    One fake b-tag:    %s" % (one_btags2/one_btags)

two_btags1 =     P_btag    * P_btag    * P_no_fake * P_no_fake
two_btags2 = 4 * P_btag    * P_no_btag * P_fake    * P_no_fake
two_btags3 =     P_no_btag * P_no_btag * P_fake    * P_fake
two_btags = two_btags1 + two_btags2 + two_btags3
print "Two b-tags out of four jets:   %s" % two_btags
print "    Two correct:           %s" % (two_btags1/two_btags)
print "    One correct, one fake: %s" % (two_btags2/two_btags)
print "    Two fake b-tags:       %s" % (two_btags3/two_btags)

three_btags1 = 2 * P_btag * P_btag    * P_fake * P_no_fake
three_btags2 = 2 * P_btag * P_no_btag * P_fake * P_fake
three_btags = three_btags1 + three_btags2
print "Three b-tags out of four jets: %s" % three_btags
print "    Two correct, one fake: %s" % (three_btags1/three_btags)
print "    One correct, two fake: %s" % (three_btags2/three_btags)

four_btags = P_btag * P_btag * P_fake * P_fake
print "Three b-tags out of four jets: %s" % four_btags