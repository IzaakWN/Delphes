from ROOT import *


# dimensions for the legend box
legendTextSize = 0.032

x1 = 0
x2 = 0
y2 = 0
height = [0.07,0.19,0.20]


def makeCanvas(square=False):
    
    # dimensions for the canvas
    global x1, x2, y1, y2
    if square:
        W = 800 # canvas size in pixels along X
        H  = 800 # canvas size in pixels along Y
        width = 0.30
    else:
        W = 800 # canvas size in pixels along X
        H  = 600 # canvas size in pixels along Y
        width = 0.24 # 0.195
    x2 = 0.95
    y2 = 0.76  # y1 determined in makeLegend()
    x1 = x2 - width
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W
    R = 0.04*W

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
    elif " Mt" in title:
        title = title.replace(" Mt","")
    
    if " " in title:
        
        if "reco" in title:
            title = title.replace(" reco","")

        if "(" in title:
            title = title[:title.index(" ")] + title[title.index(" ("):] # only take proces and extra note
            if len(title)>16:
                title = "#splitline{" + title.replace("(","}{(") + "}" # make line break for note
            # vars
            if "Pt" in title:
                title = title.replace("Pt","p_{T}")
            elif "Eta" in title:
                title = title.replace("Eta","#eta")
            elif "Phi" in title:
                title = title.replace("Phi","#phi")

        elif len(title)>14 and title.count(" ")>1:
            print "Split!"
            title = "#splitline{" + title + "}" # make line break
            title = title[:title.index(" ",len(title)-5)] + "}{" + title[title.index(" ",len(title)-5)+1:]

    # processes
    if "H" in title:
        if "bbWW" in title:
            title = title.replace("HH","HH #rightarrow ")
        else:
            title = title.replace("H","H #rightarrow ")
    elif "W" in title:
        if title[title.index("W")+1] not in ["'", " ", "W"]:
            title = title.replace("W","W #rightarrow ")
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
    hist0 = hists[0]
    tt = kwargs.get('tt', False) # last hist should be tt-hist!
    title = kwargs.get('title', None)
    entries = kwargs.get('entries', None)
    
    y1 = y2 - height[len(hists)-1]
    legend = TLegend(x1,y1,x2,y2)
#    legend.SetFillStyle(0) # 0 = transparant
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)

    # make entries
    if len(hists)==1:
        legend.AddEntry(hist0,makeEntryName1(hist0))
    else:
    
        if title is None: legend.SetHeader(makeTitle(hists[-1]))
        else: legend.SetHeader(title)
        
        if tt:
            if len(hists)==3:
                if "eutrino" in hist0.GetTitle():
                    legend.AddEntry(hist0,"neutrino gen signal")
                else:
                    legend.AddEntry(hist0,"gen signal")
            legend.AddEntry(hists[-2],"signal")
            legend.AddEntry(hists[-1],"t#bar{t}-BG")
        elif entries == None:
            for hist in hists:
                legend.AddEntry(hist,makeEntryName2(hist))
        else:
            for i in len(hists):
                legend.AddEntry(hists[i],entries[i])

    return legend



def makeAxes(*hists, **kwargs):

    hist0 = hists[0]
    xlabel = kwargs.get('xlabel', "")
    ylabel = kwargs.get('ylabel', "")
    
    # make correct x-axis labels
    if xlabel + ylabel:
        hist0.GetXaxis().SetTitle(xlabel)
    else:
        name = hist0.GetTitle()
        ylabel = "Events / %s " % hist0.GetXaxis().GetBinWidth(0)
        if name in ["N", "multiplicity"]:
            hist0.GetXaxis().SetTitle("multiplicity")
        elif "Pt" in name:
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
        elif "PID" in name:
            hist0.GetXaxis().SetTitle("PID")
        elif "Mt" in name:
            hist0.GetXaxis().SetTitle("transverse mass M_{T} [GeV]")
            ylabel += "GeV"
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


