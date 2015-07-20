from ROOT import *

f=TFile("controlPlots_HH.root")
h=f.Get("stage_1/gen/b2Pt")
print "pt"
print h.Integral(h.FindBin(0),h.FindBin(10000))/h.Integral(h.FindBin(0),h.FindBin(10000))
print h.Integral(h.FindBin(20),h.FindBin(10000))/h.Integral(h.FindBin(0),h.FindBin(10000))
print h.Integral(h.FindBin(30),h.FindBin(10000))/h.Integral(h.FindBin(0),h.FindBin(10000))
print h.Integral(h.FindBin(50),h.FindBin(10000))/h.Integral(h.FindBin(0),h.FindBin(10000))
print "eta"
h=f.Get("stage_1/gen/b2Eta")
print (h.Integral(h.FindBin(0),h.FindBin(2.0)-1)+h.Integral(h.FindBin(-2.0),h.FindBin(-0)-1))/h.GetEntries()
print (h.Integral(h.FindBin(2.0),h.FindBin(2.5)-1)+h.Integral(h.FindBin(-2.5),h.FindBin(-2.0)-1))/h.GetEntries()
print (h.Integral(h.FindBin(2.5),h.FindBin(3.0)-1)+h.Integral(h.FindBin(-3.0),h.FindBin(-2.5)-1))/h.GetEntries()
print (h.Integral(h.FindBin(3.0),h.FindBin(3.5)-1)+h.Integral(h.FindBin(-3.5),h.FindBin(-3.0)-1))/h.GetEntries()
print (h.Integral(h.FindBin(3.5),h.FindBin(4.0)-1)+h.Integral(h.FindBin(-4.0),h.FindBin(-3.5)-1))/h.GetEntries()
print (h.Integral(h.FindBin(0),h.FindBin(2.0)-1)+h.Integral(h.FindBin(-2.0),h.FindBin(-0)-1))/h.GetEntries()
print (h.Integral(h.FindBin(2.0),h.FindBin(3.0)-1)+h.Integral(h.FindBin(-3.0),h.FindBin(-2.0)-1))/h.GetEntries()
print (h.Integral(h.FindBin(3.0),h.FindBin(4.0)-1)+h.Integral(h.FindBin(-4.0),h.FindBin(-3.0)-1))/h.GetEntries()
