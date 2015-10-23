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

file = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_dilep_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_dilep_all.root")



    ###############
    # basic plots #
    ###############

def plotBasic(stage):
    print "\n  %s: Basic plots" % stage[:-1]

    names = [ ]

    if stage == "stage_0/":
        names.append("selection/category")

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

    #for hist in ["NMuons20","NElectrons20","NLeptons20","Lepton1Pt","Lepton1Eta"]:
        #names.append("leptons/"+hist)

    for hist in ["M_ll","M_jj","DeltaR_ll","DeltaR_jj","DeltaPhi_jjll"]:
        names.append("cleanup/"+hist)
    
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

        legend = makeLegend(hist_S,hist_tt,tt=True)
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_S,hist_tt)
        
        name = name.replace("selection/","basic_dilep/"+stage)
        name = name.replace("gen/","basic_dilep/"+stage)
        name = name.replace("leptons/","basic_dilep/"+stage)
        name = name.replace("jets/","basic_dilep/"+stage)
        name = name.replace("cleanup/","basic_dilep/"+stage)
        c.SaveAs(name+".png")
        c.Close()



    ############
    # 2D plots #
    ############

def plot2D(stage):
    print "\n  %s: 2D plots" % stage[:-1]
    gStyle.SetPalette(1) # for rainbow colors

    #...



    ###############
    # extra plots #
    ###############

def plotExtra(stage):
    print "\n  %s: Extra plots" % stage[:-1]
    
    
    #  ...



    ###############
    # Pies, mmmmm #
    ###############

def plotPie(stage):
    print "\n  %s: Pie charts" % stage[:-1]
    
    # ...



    ########
    # main #
    ########

def main():

    for stage in ["stage_0/","stage_1/","stage_2/","stage_3/"]:
#        plotExtra(stage)
        plotBasic(stage)
#        plot2D(stage)
#        plotPie(stage)

    print "\nDone with this, son.\n"



if __name__ == '__main__':
    main()


