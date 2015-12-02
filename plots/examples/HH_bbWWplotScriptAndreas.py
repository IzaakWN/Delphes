from ROOT import *
gROOT.LoadMacro("tdrstyle.C");
setTDRStyle();
gROOT.LoadMacro("CMS_lumi.C");

f=TFile("controlPlots_HH.root")

variables=[("stage_1/gen/b1Pt","p_{T} [GeV]")]

for variable,label in variables:
  c=TCanvas("c","c",200,200)
  hist=f.Get(variable)
  hist.GetXaxis().SetTitle(label)
  hist.Draw()
  CMS_lumi( c, 4, 33 );
  c.SaveAs(variable.replace("/","_")+".pdf")
  c.SaveAs(variable.replace("/","_")+".png")
