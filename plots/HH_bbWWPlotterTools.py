from ROOT import *

# dimensions for the canvas
W = 800 # canvas size in pixels along X
H  = 600 # canvas size in pixels along Y
T = 0.08*H
B = 0.12*H
L = 0.12*W
R = 0.04*W

# dimensions for the legend box
legendTextSize = 0.032
width = 0.21 # 0.195
height = [0.07,0.19,0.20]
x2 = 0.95
y2 = 0.76  # y1 determined in makeLegend()
x1 = x2 - width



def makeCanvas(square=False):
    
    if square:
        global W, H, T, B, L, R, x1
        W = 800 # canvas size in pixels along X
        H  = 800 # canvas size in pixels along Y
        T = 0.08*H
        B = 0.12*H
        L = 0.12*W
        R = 0.04*W
        x1 = x1/8*6
    c1 = TCanvas("c","c",100,100,W,H)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    
    return c1



def makeTitle(hist):
    
    # replace stuff
    title = hist.GetTitle()

    # replace stuff
    if " Pt" in title:
        title = title.replace(" Pt","") # take away variable
    elif " Eta" in title:
        title = title.replace(" Eta","")
    elif " Mass" in title:
        title = title.replace(" Mass","")
    elif " MET" in title:
        title = title.replace(" MET","")
    elif " Phi" in title:
        title = title.replace(" Phi","")
    elif " multiplicity" in title:
        title = title.replace(" multiplicity","")
    elif " PID" in title:
        title = title.replace(" PID","")
    
    if " " in title:
        
        if "reco" in title:
            title = title.replace(" reco","")

        if "(" in title:
            title = title[:title.index(" ")] + title[title.index(" ("):] # only take proces and extra note
            if len(title)>16:
                title = "#splitline{" + title.replace("(","}{(").replace(")",")}") # make line break for note
            # vars
            if "Pt" in title:
                title = title.replace("Pt","p_{T}")
            elif "Eta" in title:
                title = title.replace("Eta","#eta")
            elif "Phi" in title:
                title = title.replace("Phi","#phi")

    # processes
    if "H" in title:
        if "bbWW" in title:
            title = title.replace("HH","HH #rightarrow ")
        else:
            title = title.replace("H","H #rightarrow ")
    elif "W" in title:
        if title[title.index("W")+1] not in ["'", " "]:
            title = title.replace("W","W #rightarrow ",1)
    title = title.replace("nu","#nu")

    return title



def makeEntryName1(hist):
    
    title = hist.GetTitle()
    
    # replace stuff
    if " Pt" in title:
        title = title.replace(" Pt","") # take away variable
    elif " Eta" in title:
        title = title.replace(" Eta","")
    elif " Mass" in title:
        title = title.replace(" Mass","")
    elif " MET" in title:
        title = title.replace(" MET","")
    elif " Phi" in title:
        title = title.replace(" Phi","")
    elif " multiplicity" in title:
        title = title.replace(" multiplicity","")
    elif " PID" in title:
        title = title.replace(" PID","")
        
    if "Pt" in title:
        title = title.replace("Pt","p_{T}")
    elif "Eta" in title:
        title = title.replace("Eta","#eta")
    elif "Phi" in title:
        title = title.replace("Phi","#phi")

    if title[0]=="H":
        if title[2:6]=="bbWW":
            title = title.replace("HH","HH #rightarrow ")
        else:
            title = title.replace("H","H #rightarrow ")
    elif title[0]=="W":
        title = title.replace("W","W #rightarrow ")
    title = title.replace("nu","#nu")

    # take away note in parentheses (see makeTitle)
    if "(" in title:
        title = title[:title.index(" (")]
#        title = "#splitline{" + title.replace(" (","}{").replace(")","}")

    # TODO: line break if title too long

    return title



def makeEntryName2(hist,tt=False):
    
    title = hist.GetTitle()
    
    # replace stuff
    if "neutrino" in title:
        title = "neutrino generator"
    elif " Pt" in title:
        title = title[title.index("Pt")+3:] # take away process, variable and space
#        title = title.replace(" Pt","") # take away variable
    elif " Eta" in title:
        title = title[title.index("Eta")+4:]
    elif " Phi" in title:
        title = title[title.index("Phi")+4:]
    elif " Mass" in title:
        title = title[title.index("Mass")+5:]
    elif " multiplicity" in title:
        title = title[title.index("multiplicity")+13:]
    if "Pt" in title:
        title = title.replace("Pt","p_{T}")
    elif "Eta" in title:
        title = title.replace("Eta","#eta")
    elif "Phi" in title:
        title = title.replace("Phi","#phi")

    # make line break
    if "(" in title:
        title = "#splitline{" + title.replace("(","}{").replace(")","}")
#    elif "multiplicity" in title:
#        title = "#splitline{" + title.replace("multiplicity","city}{") + "}"
    # TODO: line break if title too long

    return title



def makeLegend(*hists, **kwargs):
# last hist should be tt-hist
    hist0 = hists[0]
    tt = kwargs.get('tt', False)
    y1 = y2 - height[len(hists)-1]
    legend = TLegend(x1,y1,x2,y2)
#    legend.SetFillStyle(0) # 0 = transparant
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)

    # make entries
    if len(hists)==1:
        legend.AddEntry(hist0,makeEntryName1(hist0))
    else:
        legend.SetHeader(makeTitle(hists[-1]))
        if tt:
            if len(hists)==3:
                if "eutrino" in hist0.GetTitle():
                    legend.AddEntry(hist0,"neutrino gen signal")
                else:
                    legend.AddEntry(hist0,"gen signal")
            legend.AddEntry(hists[-2],"signal")
            legend.AddEntry(hists[-1],"t#bar{t}-BG")
        else:
            for hist in hists:
                legend.AddEntry(hist,makeEntryName2(hist))

    return legend



def makeAxes(*hists):

    hist0 = hists[0]
    
    # make correct x-axis labels
    name = hist0.GetTitle()
    ylabel = "Events / %s " % hist0.GetXaxis().GetBinWidth(0)
    if "Pt" in name:
        hist0.GetXaxis().SetTitle("transverse momentum p_{T} [GeV]")
        ylabel += "GeV"
    elif "Eta" in name:
        hist0.GetXaxis().SetTitle("pseudorapidity #eta")
    elif "Phi" in name:
        hist0.GetXaxis().SetTitle("azimuthal angle #phi [rad]")
        ylabel += "rad"
    elif "Mass" in name:
        if "vs." in name:
            hist0.GetXaxis().SetTitle("W #rightarrow l#nu mass [GeV]")
            ylabel = "W #rightarrow qq mass [GeV]"
        else:
            hist0.GetXaxis().SetTitle("invariant mass M [GeV]")
            ylabel += "GeV"
    elif "MET" in name:
        hist0.GetXaxis().SetTitle("MET [GeV]")
        ylabel += "GeV"
    elif name in ["N", "multiplicity"]:
        hist0.GetXaxis().SetTitle("multiplicity")
    elif "PID" in name:
        hist0.GetXaxis().SetTitle("PID")
    else: print "Warning: no x-axis label!"

    # make correct y-axis labels
    hist0.GetYaxis().SetTitle(ylabel)
    hist0.GetYaxis().SetTitleOffset(1.5)

    # set optimal range
    mins = []
    maxs = []
    for hist in hists: #(hist0,) + hists:
        mins.append(hist.GetMinimum())
        maxs.append(hist.GetMaximum())
    hist0.GetYaxis().SetRangeUser(min(mins),max(maxs)*1.12)



def setFillStyle(hist):
    name = hist.GetTitle()
    if "M" in name:
        hist.SetFillColor(kRed+1)
        hist.SetLineColor(kRed+3)
    elif "Eta" in name:
        hist.SetFillColor(kAzure+5)
        hist.SetLineColor(kAzure+4)
#    elif "Eta" in name:
#        hist.SetFillColor(kMagenta+2)
#        hist.SetLineColor(kMagenta+3)
    else:
        hist.SetFillColor(kOrange)
        hist.SetLineColor(kOrange-6)
    hist.SetLineWidth(2)



def setLineStyle(*hists):

    colors = [kRed+3,kAzure+4,kOrange-6,kMagenta+3]
    line = [1,2,3,4]
    for i in range(len(hists)):
        hists[i].SetLineColor(colors[i%4])
        hists[i].SetLineStyle(line[i%4])
        hists[i ].SetLineWidth(3)



def setMarkerStyle(hist):
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.8)





# Garbage
#
#    title = hist.GetTitle()
#    if " " in title:
#        extra = ""
#        if "gen" in title:
#            if "from" in title:
#                extra = title[title.index(" ",2):title.index(" ",3)]+" gen"
#            elif "daughters" in title:
#                extra = title[:title.index(" daughters")]+" daughters gen"
#            elif "mother" in title:
#                extra = title[:title.index(" mother")]+" mother gen"
#            elif " W's" in title:
#                extra = " W's gen"
#            else:
#                extra = " gen"
#        if "(" in title:
#            title = title[:title.index(" ")] + extra + title[title.index(" ("):] # only take proces and extra note
##            title = "#splitline{" + title.replace("(","}{").replace(")","}") # make line break for note
#        else:
#            title = title[:title.index(" ")] + extra # only take proces
#
#    # processes
#    if "H" in title:
#        if "bbWW" in title:
#            title = title.replace("HH","HH #rightarrow ")
#        else:
#            title = title.replace("H","H #rightarrow ")
#    elif "W" in title:
#        if "W's" not in title:
#            title = title.replace("W","W #rightarrow ")
#    title = title.replace("nu","#nu")
#        
#    # vars
#    if "Pt" in title:
#        title = title.replace("Pt","p_{T}")
#    elif "Eta" in title:
#        title = title.replace("Eta","#eta")
#    elif "Phi" in title:
#        title = title.replace("Phi","#phi")
