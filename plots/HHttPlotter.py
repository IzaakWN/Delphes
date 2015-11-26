from ROOT import *
import CMS_lumi, tdrstyle
from HHPlotterTools import *

# CMS style
# CMS_lumi.CMS_lumi( c, 4, 33) # TPad, iPeriod, iPosX
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Simulation preliminary"
CMS_lumi.cmsTextSize = 0.65
#CMS_lumi.drawLogo = True
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()

file = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")



    ###############
    # basic plots #
    ###############

def plotBasic(stage):
    print "\n  %s: Basic plots" % stage[:-1]

    names = [ ]

#    for comb in [ "qq","q1l","q2l",
#                  "bb","b1l","b1l", ]:
#        names.append("gen/DeltaR_"+comb)
#    names.append("gen/DeltaPhi_qq")

    #for particle in ["b1","b2","q","nu","l","e","mu"]:
        #for var in ["Pt","Eta","M"]:
            #names.append("gen/"+particle+var)

    #for particle in ["NVirtualWs","NLeptons","NElectrons","NMuons","NTaus",
                     #"NWlnu","WDPID","tDPID"]: #NWjj
        #names.append("gen/"+particle)

    #for jet in ["jet","bjet"]:
        #for var in ["Pt","Eta","M"]:
            #for i in ["1","2","3","4"]:
                #names.append("jets/"+jet+i+var)
    #jet = "nonbjet"
    #for var in ["Pt","Eta","M"]:
        #for i in ["1","2"]:
            #names.append("jets/"+jet+i+var)

    #for jet in ["NJets30","NUncleanedJets30","NBjets30","NJets15"]:
        #names.append("jets/"+jet)

#    names.append("match/NJetiWMatch")
#    names.append("match/JetWMatchEta")
#    names.append("match/JetWUnMatchEta")
#    names.append("jets/NJetsEta3")
#    names.append("jets/NJetsEta25")
#    names.append("jets/NJetsEta2")

    #for particle in ["NMuons20","NElectrons20","NLeptons20"]:
        #names.append("leptons/"+particle)
    #names.append("leptons/Lepton1Pt")
    #names.append("leptons/Lepton1Eta")

    #for process in ["Hbb", "HWW"]:
##        for alg in ["_b2","_b3","_b4","_d1"]: #["_b1","_b2","_c1","_c2"]:
        #for var in ["Pt","Eta","M"]:
            #names.append("reco/"+process+"_b2"+var)
            #names.append("reco/"+process+"_b3"+var)
            #names.append("reco/"+process+"_b4"+var)
            #names.append("reco2/"+process+"_d1"+var)
    #names.append("reco/HWW_b2Mc")
    #names.append("reco/HWW_b3Mc")
    #names.append("reco/HWW_b4Mc")
    #names.append("reco/Hbb_a1M")
    #names.append("reco/Hbb_a1Eta")

    if stage == "stage_0/":
        names.append("selection/category")

    for comb in [ "jj","jjl","b1l","blnu",
                  "jjb_leading","bb_farthest","jjl_leading",
                  "jj_cut","jj_leading","jj_leading_cut",
                  "bb_cut","bb_leading","bb_leading_cut",
                           "bb_closest","bb_closest_cut" ]:
        names.append("cleanup/M_"+comb)
    names.append("cleanup/MT_lnu")
    names.append("cleanup/MT_jjlnu")

    for comb in [ "jj","j1l","j2l","jjl","jjl_leading",
                        "b1l","b2l","bb1" ]:
        names.append("cleanup/DeltaR_"+comb)
        names.append("cleanup/DeltaPhi_"+comb)
    names.append("cleanup/DeltaPhi_METl")
    names.append("cleanup/DeltaPhi_jjlnu")
    names.append("cleanup/DeltaRi_b1l")
    names.append("cleanup/DeltaRi_b2l")

#    names.append("cleanup/DeltaPhi_METl")
    names.append("cleanup/jet1Pt")
    names.append("cleanup/jet2Pt")
    names.append("cleanup/bjet1Pt")
    names.append("cleanup/bjet2Pt")
    names.append("cleanup/leptonPt")
    names.append("cleanup/MET")

    for name in names:

        c = makeCanvas()
        hist_S = file.Get(stage+name) # signal: HH -> bbWW
        hist_tt = file_tt.Get(stage+name) # BG: tt -> bbWW

        if "H" not in name:
            norm(hist_S,hist_tt)

        hist_S.Draw()
        hist_tt.Draw("same")
        makeAxes(hist_S,hist_tt)
        
        if "category" in name:
            hist_S.Scale(1./hist_S.GetBinContent(1))
            hist_tt.Scale(1./hist_tt.GetBinContent(1))

#        if "a1" in name:
#            legend = makeLegend(hist_S,hist_tt,tt=True,title="#splitline{H#rightarrowbb}{(angular alg.)}")
#            legend.Draw()
        if "DeltaPhi_b1l" in name:
            legend = makeLegend(hist_S,hist_tt,tt=True,position="RightTop")
            legend.Draw()
        else:
            legend = makeLegend(hist_S,hist_tt,tt=True)
            legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_S,hist_tt)

        if "gen/Delta" in name:
            name = name.replace("gen/Delta","cleanup/"+stage+"Delta") + "_gen"
        else:
            name = name.replace("selection/","basic/"+stage)
            name = name.replace("cleanup/","cleanup/"+stage)
            name = name.replace("gen/","basic/"+stage)
            name = name.replace("leptons/","basic/"+stage)
            name = name.replace("jets/","basic/"+stage)
            name = name.replace("match/","basic/"+stage)
            name = name.replace("reco/","reco/"+stage)
            name = name.replace("reco2/","reco/"+stage)
        c.SaveAs(name+".png")
        c.Close()



    ############################
    # overlay "reco" and "gen" #
    ############################

def plotOverlay(stage):
    print "\n  %s: Overlay plots: reco and gen" % stage[:-1]
    
    names2 = [ ]

    #names2.extend([ ("gen/WlnuPt", "reco/Wlnu1Pt"),
                    #("gen/WlnuEta", "reco/Wlnu1Eta"),
                    #("gen/WlnuM", "reco/Wlnu1M"),
                    #("gen/WlnuMt", "reco/WlnuMt") ])
    #names2.append(("gen/nuPt", "jets/MET")) # beware of normalization above!

   #names2.extend([("gen/lPt", "leptons/lPt")])

    #for process in ["Wjj","HHbbWW"]:
        #for alg in ["_b2","_b3","_b4"]: #["_b1","_b2","_c1","_c2"]:
            #for var in ["Pt","Eta","M"]:
                #names2.append( ("gen/"+process+var,\
                                #"reco/"+process+alg+var) )
    #process = "Wjj"
    #alg = "_a1"
    #for var in ["Pt","Eta","M"]:
        #names2.append( ("gen/"+process+var,\
                        #"reco/"+process+alg+var) )
                                
    #for process in ["Wlnu","Wjj","HHbbWW"]:
        #for alg in ["_d1"]: #["_b1","_b2","_c1","_c2"]:
            #for var in ["Pt","Eta","M"]:
                #names2.append( ("gen/"+process+var,\
                                #"reco2/"+process+alg+var) )

    for gen, reco in names2:

        c = makeCanvas()
        hist_gen = file.Get(stage+gen) # "data"
        hist_reco = file.Get(stage+reco) # "MC"
        hist_reco_tt = file_tt.Get(stage+reco) ## "MC" from tt

        hist_reco.Draw("histsame")
        hist_reco_tt.Draw("histsame")
        hist_gen.Draw("P0same")
        makeAxes(hist_reco,hist_reco_tt,hist_gen)
        
        if "MET" in reco:
            if hist_reco_tt.GetMaximum() > 1000:
                max = hist_reco_tt.GetMaximum()*1.12
            else:
                max = 1000
            hist_gen.GetYaxis().SetRangeUser(0,max)
            hist_reco.GetYaxis().SetRangeUser(0,max)
            hist_reco_tt.GetYaxis().SetRangeUser(0,max)

        if "a1" in reco:
            if "Hbb" in reco:
                legend = makeLegend(hist_gen,hist_reco,hist_reco_tt,tt=True,title="#splitline{H #rightarrow bb}{(angular alg.)}")
                legend.Draw()
            else:
                legend = makeLegend(hist_gen,hist_reco,hist_reco_tt,tt=True,title="#splitline{W #rightarrow jj}{(angular alg.)}")
                legend.Draw()
        else:
            legend = makeLegend(hist_gen,hist_reco,hist_reco_tt,tt=True)
            legend.Draw()
            legend.Draw()
        
        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_reco,hist_reco_tt)
        setMarkerStyle(hist_gen)
        
        reco = reco.replace("reco/","reco/"+stage)
        reco = reco.replace("reco2/","reco/"+stage)
        reco = reco.replace("jets/","basic/"+stage)
        c.SaveAs(reco+".png")
        c.Close()



    ############
    # 2D plots #
    ############

def plot2D(stage):
    print "\n  %s: 2D plots" % stage[:-1]
    gStyle.SetPalette(1) # for rainbow colors

    ## WWM signal
    #c = makeCanvas(square=True)
    #hist = file.Get(stage+"gen/WWM")
    
    #hist.Draw()
    #makeAxes2D(hist)
    #legend = makeLegend(hist)
    #legend.Draw()
    #hist.SetMarkerColor(kRed+3)

    #CMS_lumi.CMS_lumi(c,14,33)

    #c.SaveAs("basic/"+stage+"WWM.png")
    #c.Close()


    ## WWM BG
    #c = makeCanvas(square=True)
    #hist_tt = file_tt.Get(stage+"gen/WWM")
    
    #hist_tt.Draw()
    #makeAxes2D(hist_tt)
    #legend = makeLegend(hist)
    #legend.Draw()
    #hist.SetMarkerColor(kRed+3)

    #CMS_lumi.CMS_lumi(c,14,33)

    #c.SaveAs("basic/"+stage+"WWM_tt.png")
    #c.Close()


    ## WWM signal vs BG
    #c = makeCanvas(square=True)
    #hist = file.Get(stage+"gen/WWM")
    #hist_tt = file_tt.Get(stage+"gen/WWM")

    #hist_tt.Draw()
    #hist.Draw("same")
    #makeAxes2D(hist_tt,hist)
    #legend = makeLegend(hist,hist_tt,tt=True)
    #legend.Draw()
    #hist.SetMarkerColor(kRed+3)
    #hist_tt.SetMarkerColor(kAzure+4)

    #CMS_lumi.CMS_lumi(c,14,33)

    #c.SaveAs("basic/"+stage+"WWM_both.png")
    #c.Close()
    

    ## bbWWM signal vs BG
    #c = makeCanvas(square=True)
    #hist = file.Get(stage+"gen/bbWWM")
    #hist_tt = file_tt.Get(stage+"gen/bbWWM")

    #hist_tt.Draw()
    #hist.Draw("same")
    #makeAxes2D(hist)
    #hist.SetMarkerColor(kRed+3)
    #hist_tt.SetMarkerColor(kAzure+4)

    #CMS_lumi.CMS_lumi(c,14,33)

    #c.SaveAs("basic/"+stage+"bbWWM_both.png")
    #c.Close()

    # GEN LEVEL: DeltaPhi vs. DeltaEta
    names = [ ]#"qq","bb","q1l","q2l","b1l","b2l" ]

    for name in names:
        c = makeCanvas(square=True)
        hist = file.Get(stage+"gen/DeltaEtaDeltaPhi_"+name)
        hist.Draw("colz")
        makeAxes2D(hist)
        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("cleanup/"+stage+"DeltaEtaDeltaPhi_"+name+"_gen.png")
        c.Close()

        c = makeCanvas(square=True)
        hist_tt = file_tt.Get(stage+"gen/DeltaEtaDeltaPhi_"+name)
        hist_tt.Draw("colz")
        makeAxes2D(hist_tt)
        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("cleanup/"+stage+"DeltaEtaDeltaPhi_"+name+"_gen_tt.png")
        c.Close()
      
    # RECO LEVEL: DeltaPhi vs. DeltaEta
    names = [ "jj" ,"j1l","j2l","j3l","jjl","jjl_leading",
              "bb1","b1l","b2l" ]

    for name in names:
        c = makeCanvas(square=True)
        hist = file.Get(stage+"cleanup/DeltaEtaDeltaPhi_"+name)
        hist.Draw("colz")
        makeAxes2D(hist)
        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("cleanup/"+stage+"DeltaEtaDeltaPhi_"+name+".png")
        c.Close()

        c = makeCanvas(square=True)
        hist_tt = file_tt.Get(stage+"cleanup/DeltaEtaDeltaPhi_"+name)
        hist_tt.Draw("colz")
        makeAxes2D(hist_tt)
        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("cleanup/"+stage+"DeltaEtaDeltaPhi_"+name+"_tt.png")
        c.Close()



    ###############
    # extra plots #
    ###############

def plotExtra(stage):
    print "\n  %s: Extra plots" % stage[:-1]
    
    
    # __HH_vs._tt__
    
    for var in [ "M","Pt","Eta" ]:

        c = makeCanvas()
        hist_S = file.Get(stage+"gen/HHbbWW"+var) # signal: HH -> bbWW
        hist_tt = file_tt.Get(stage+"gen/ttbbWW"+var) # BG: tt -> bbWW
        hist_S.Scale(1./hist_S.Integral())
        hist_tt.Scale(1./hist_tt.Integral())
        
        hist_S.Draw()
        hist_tt.Draw("same")
        makeAxes(hist_S,hist_tt)

        y1 = y2 - height[1]
        legend = TLegend(x1,y1,x2,y2)
        legend.SetBorderSize(0)
        legend.SetTextSize(legendTextSize)
        legend.SetHeader("gen level")
        legend.AddEntry(hist_S,"HH #rightarrow bbWW")
        legend.AddEntry(hist_tt,"t#bar{t} #rightarrow bbWW")
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_S,hist_tt)
        
        c.SaveAs("basic/HHtt"+var+".png")
        c.Close()


    # __NJetiWMatch__
    c = makeCanvas()
    hist = file.Get(stage+"match/NJetiWMatch")
    norm(hist)
    hist.Draw()
    makeAxes(hist)
    setLineStyle(hist)
    legend = makeLegend(hist,entries="#splitline{jet i matches}{q from W}")
    legend.Draw()

    CMS_lumi.CMS_lumi(c,14,33)
    
    c.SaveAs("basic/"+stage+"NJetiWMatch.png")
    c.Close()


    # __jetWMatchEta_vs._jetWUnMatchEta___
    c = makeCanvas()
    hist = file.Get(stage+"match/JetWMatchEta")
    hist_un = file.Get(stage+"match/JetWUnMatchEta")
    hist.Draw()
    hist_un.Draw("same")
    makeAxes(hist,hist_un)
    setLineStyle(hist,hist_un)
    legend = makeLegend(hist,hist_un,title="jet and q from W",entries=["matched","unmatched"])
    legend.Draw()

    CMS_lumi.CMS_lumi(c,14,33)
    
    c.SaveAs("basic/"+stage+"JetWMatchEta_unscaled.png")
    c.Close()


    # __WlnuM vs Wjj__
    c = makeCanvas()
    hist_Wlnu = file_tt.Get(stage+"gen/WlnuM")
    hist_Wjj = file_tt.Get(stage+"gen/WjjM")
    hist_Wlnu.Draw()
    hist_Wjj.Draw("same")
    setLineStyle(hist_Wlnu,hist_Wjj)

    makeAxes(hist_Wlnu,hist_Wjj)
    hist_Wlnu.GetXaxis().SetRangeUser(0, 120)
#    hist_Wjj.GetXaxis().SetRangeUser(0, 120)
    hist_Wlnu.GetYaxis().SetTitleOffset(1.88)

    y1 = y2 - height[1]
    legend = TLegend(x1,y1,x2,y2)
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)
    legend.SetHeader("W at gen level")
    legend.AddEntry(hist_Wlnu,"W #rightarrow l#nu")
    legend.AddEntry(hist_Wjj,"W #rightarrow qq")
    legend.Draw()


    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic/"+stage+"WWM_1D.png")
    c.Close()



    ###############
    # Pies, mmmmm #
    ###############

def plotPie(stage):
    print "\n  %s: Pie charts" % stage[:-1]
    
    W = 1200
    H = 1200
    
    c = makeCanvas(square=True)
    hist = file_tt.Get(stage+"gen/NWlnu")
    hist.GetXaxis().SetRangeUser(0, 3)
    pie = TPie(hist)
    pie.SetCircle(.53,.5,.2)
#    pie.SetAngularOffset(200)
    pie.SetEntryRadiusOffset(2,.03)

    labels = [" hadronic"," semi-leptonic"," dileptonic"]
    colors = [kAzure-4,kGreen-3,kRed] #kOrange-3
    linecolors = [kAzure-6,kGreen+4,kRed+4] #Orange+4
    pie.SetLabelFormat("#splitline{#scale[1.4]{#font[2]{%txt}}}{#scale[1.2]{  %perc}}")
    pie.SetLabelsOffset(0.026)
    for i in range(3):
        pie.SetEntryFillColor(i,colors[i])
        pie.SetEntryLineColor(i,linecolors[i])
        pie.SetEntryLineWidth(i,1)
        pie.SetEntryLabel(i,labels[i])
    
    if "0" in stage:
        pie.SetEntryRadiusOffset(0,.02)
    else:
        pie.SetEntryRadiusOffset(1,.02)

    pie.Draw("SC>")

    c.SaveAs("basic/"+stage+"branchfraction"+stage[-2]+".png")
    c.Close()



    ########
    # main #
    ########

def main():

    for stage in ["stage_0/","stage_1/","stage_2/","stage_3/"]:#,"stage_4/","stage_5/","stage_6/"]:
#        plotOverlay(stage)
#        plotExtra(stage)
        plotBasic(stage)
        plot2D(stage)
#        plotPie(stage)

    print "\nDone with this, son.\n"



if __name__ == '__main__':
    main()


