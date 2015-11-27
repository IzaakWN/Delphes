from ROOT import *


# dimensions for the legend box
legendTextSize = 0.032

x1 = 0
x2 = 0
y2 = 0
width = 0
height = [0.07,0.19,0.20] + [0.21+0.05*i for i in range(35)]
colors = [kRed+3,kAzure+4,kOrange-6,kMagenta+3,kGreen+3,kYellow+2,kRed-7, kAzure-4, kOrange+6, kMagenta-3, kYellow-2]


def makeCanvas(square=False, scaleleftmargin=1, scalerightmargin=1):
    
    # dimensions for the canvas
    global x1, x2, y1, y2, width
    if square:
        W = 800 # canvas size in pixels along X
        H  = 800 # canvas size in pixels along Y
        width = 0.30
        scalerightmargin = 3*scalerightmargin
    else:
        W = 800 # canvas size in pixels along X
        H  = 600 # canvas size in pixels along Y
        width = 0.24 # 0.195
    x2 = 0.95
    y2 = 0.76  # y1 determined in makeLegend()
    x1 = x2 - width
    T = 0.08*H
    B = 0.12*H
    L = 0.12*W*scaleleftmargin
    R = 0.04*W*scalerightmargin

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
    elif " Eta" in title and "Eta<" not in title:
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
    elif " DeltaR" in title:
        title = title.replace(" DeltaR","")
    elif " DeltaPhi" in title:
        title = title.replace(" DeltaPhi","")
    elif "MW" in title:
        title = title.replace("MW","M")#_{W}")
    
    if " " in title:
        
        if "reco" in title:
            title = title.replace(" reco","")

        elif "(" in title and "(cut)" not in title:
            title = title[:title.index(" ")] + title[title.index(" ("):] # only take proces and extra note
            if len(title)>25:
                title = "#splitline{" + title + "}" # make line break
                title = title[:title.index(" ",len(title)/2)] + "}{" + title[title.index(" ",len(title)/2)+1:]
            elif len(title)>16:
                title = "#splitline{" + title.replace("(","}{(") + "}" # make line break for note
            # vars
            if "Pt" in title:
                title = title.replace("Pt","p_{T}")
            if "Eta" in title:
                title = title.replace("Eta","#eta")
            elif "Phi" in title:
                title = title.replace("Phi","#phi")
            if "Delta" in title:
                title = title.replace("Delta","#Delta")

        elif len(title)>14 and title.count(" ")>1:
            print "Split!"
#            indixes = [ i for i, c in enumerate(title) if c == " " ]
            title = "#splitline{" + title + "}" # make line break
            title = title[:title.index(" ",len(title)/2)] + "}{" + title[title.index(" ",len(title)/2)+1:]

    # processes
    if "H" in title:
        if "bbWW" in title:
            title = title.replace("HH","HH #rightarrow ")
        else:
            title = title.replace("H","H #rightarrow ")
    elif "W" in title:
        if title.index("W")+1-len(title): # not W at the end!
            if not title[title.index("W")+1] in ["'", " ", "W",">","<", "}"]:
                title = title.replace("W","W #rightarrow ")
    title = title.replace("nu","#nu")

    return title



def makeEntryName1(hist):
    
    title = hist.GetTitle()
    
    # replace stuff
    if " Pt" in title:
        title = title.replace(" Pt","") # take away variable
    elif " Eta" in title and "Eta<" not in title:
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
    if "Delta" in title:
        title = title.replace("Delta","#Delta")

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
    elif " vs. " in title:
        print "Split!"
        title = "#splitline{" + title + "}" # make line break
        title = title[:title.index(" vs. ")+5] + "}{" + title[title.index(" vs. ")+5:]

    return title



def makeEntryName2(hist,tt=False):
    
    title = hist.GetTitle()
    
    # replace stuff
    if "neutrino" in title:
        title = "neutrino generator"
    elif " Pt" in title:
        title = title[title.index("Pt")+3:] # take away process, variable and space
#        title = title.replace(" Pt","") # take away variable
    elif " Eta" in title and "Eta<" not in title:
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
    if "Delta" in title:
        title = title.replace("Delta","#Delta")

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
    position = kwargs.get('position', "")
    transparant = kwargs.get('transparant', False)
    global x1, x2, y2
    
    if position:
        if position=="RightBottom":
            x1 = 1.15-x2
            x2 = x1 + width
            y2 = 1-y2+height[len(hists)-1]
        elif position=="RightTop":
            x1 = 1.15-x2
            x2 = x1 + width
        elif position=="RightTopTop":
            x1 = 1.15-x2
            x2 = x1 + width
            y2 = 0.88
#    if title == "":
#        y2 =

    y1 = y2 - height[len(hists)-1]
    legend = TLegend(x1,y1,x2,y2)
    if transparant:
        legend.SetFillStyle(0) # 0 = transparant
    else:
        legend.SetFillColor(kWhite)
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)

    # make entries
    if len(hists) == 1:
        if entries is None:
            legend.AddEntry(hist0,makeEntryName1(hist0))
        else:
            legend.AddEntry(hist0,entries)
    else:
    
        if title is None: legend.SetHeader(makeTitle(hists[-1]))
        else: legend.SetHeader(title)
        
        if tt:
            if len(hists) == 3:
                if "eutrino" in hist0.GetTitle():
                    legend.AddEntry(hist0,"neutrino gen signal")
                else:
                    legend.AddEntry(hist0,"gen signal")
            legend.AddEntry(hists[-2],"signal")
            legend.AddEntry(hists[-1],"t#bar{t} BG")
        elif entries is None:
            for hist in hists:
                legend.AddEntry(hist,makeEntryName2(hist))
        else:
            for i in range(len(hists)):
                legend.AddEntry(hists[i],entries[i])

    return legend



def makeLabels2D(hist, xaxis=False, yaxis=False):

    if xaxis:
        Xaxis = hist.GetXaxis()
        for i in range(1,Xaxis.GetNbins()+1):
            label = Xaxis.GetBinLabel(i)
            label = label.replace("_closest","1")
            if "_" in label:
                label = label[:label.index("_")+1]+"{"+label[label.index("_")+1:]+"}"
            label = label.replace("Pt"," p_{T}")
            label = label.replace("Delta","#Delta")
            label = label.replace("Phi","#phi")
            label = label.replace("Eta","#eta")
            label = label.replace("j1","j_{1}")
            label = label.replace("b1","b_{1}")
            Xaxis.SetBinLabel(i,label)

    if yaxis:
        Yaxis = hist.GetYaxis()
        for i in range(1,Yaxis.GetNbins()+1):
            label = Yaxis.GetBinLabel(i)
            label = label.replace("_closest","1")
            if "_" in label:
                label = label[:label.index("_")+1]+"{"+label[label.index("_")+1:]+"}"
            label = label.replace("Pt"," p_{T}")
            label = label.replace("Delta","#Delta")
            label = label.replace("Phi","#phi")
            label = label.replace("Eta","#eta")
            label = label.replace("j1","j_{1}")
            label = label.replace("b1","b_{1}")
            Yaxis.SetBinLabel(i,label)




def makeAxes2D(*hists, **kwargs):

    hist0 = hists[0]
    name = hist0.GetTitle()
    xlabel = kwargs.get('xlabel', "")
    ylabel = kwargs.get('ylabel', "")
    
    # make correct axis labels
    if xlabel + ylabel:
        hist0.GetXaxis().SetTitle(xlabel)
    elif "DeltaPhi vs. DeltaEta" in name:
        name.replace(" DeltaPhi vs. DeltaEta","")
        print "name = " + name
        var = ""
        if ("bjet-" or "bquark-") in name:
            var = "_{b"
        elif ("jets-" or "jet-jet-") in name:
            var = "_{jj,"
        elif "lepton-" in name:
            var = "_{l"
        elif "jet-" in name:
            var = "_{j"
        elif "quark-" in name:
            var = "_{q"
        elif "MET-" in name:
            var = "_{E^{miss}_{T},"
        if "-lepton-MET" in name:
            var += "l#nu}"
        elif "-lepton" in name:
            var += "l}"
        elif ("-bjet" or "-bquark") in name:
            var += "b}"
        elif "-jet" in name:
            var += "j}"
        elif "-quark" in name:
            var += "q}"
        elif "-MET" in name:
            var += ",E^{miss}_{T}}}"
        elif "-nu" in name:
            var += "#nu}"
        xlabel = "#Delta#eta" + var
        ylabel = "#Delta#phi" + var +" [rad]"
    elif " vs. " in name:
        xlabel = name[name.index(" vs. ")+5:].replace(" gen","")
        ylabel = name[:name.index(" vs. ")]
        if "H" in name:
            xlabel = xlabel.replace("H","H #rightarrow ")
            xlabel = xlabel.replace("Mass","mass [GeV]")
            xlabel = xlabel.replace("Mt","M_{T} [GeV]")
            ylabel = ylabel.replace("H","H #rightarrow ")
            ylabel = ylabel.replace("Mass","mass [GeV]")
            ylabel = ylabel.replace("Mt","M_{T} [GeV]")
        elif "W" in name:
            xlabel = xlabel.replace("W","W #rightarrow ")
            xlabel = xlabel.replace("nu","#nu")
            xlabel = xlabel.replace("Mass","mass [GeV]")
            xlabel = xlabel.replace("Mt","M_{T} [GeV]")
            ylabel = ylabel.replace("W","W #rightarrow ")
            ylabel = ylabel.replace("nu","#nu")
            ylabel = ylabel.replace("Mass","mass [GeV]")
            ylabel = ylabel.replace("Mt","M_{T} [GeV]")
        else: print "Warning: no axis labels!"
    else: print "Warning: no axis labels!"

    # set labels
    hist0.GetXaxis().SetTitle(xlabel)
    hist0.GetYaxis().SetTitle(ylabel)
    hist0.GetXaxis().SetTitleSize(0.051)
    hist0.GetYaxis().SetTitleSize(0.048)
    hist0.GetYaxis().SetTitleOffset(1.25)

    # set optimal range
    mins = [ ]
    maxs = [ ]
    for hist in hists: #(hist0,) + hists:
        mins.append(hist.GetMinimum())
        maxs.append(hist.GetMaximum())
    hist0.GetYaxis().SetRangeUser(min(mins),max(maxs)*1.12)



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
        elif " Pt" in name:
            hist0.GetXaxis().SetTitle("transverse momentum p_{T} [GeV]")
            ylabel += "GeV"
        elif "Delta" in name:
            xlabel = ""
            var = ""
            if "DeltaR" in name: var = "#DeltaR"
            elif "DeltaPhi": var = "#Delta#phi"
            elif "DeltaEta": var = "#Delta#eta"
            elif "DeltaPt": var = "#Delta p_{T}"
            
            if ("bjet-" or "bquark-") in name:
                xlabel = var+"_{b"
            elif ("jets-" or "jet-jet-") in name:
                xlabel = var+"_{jj,"
            elif "lepton-" in name:
                xlabel = var+"_{l"
            elif "jet-" in name:
                xlabel = var+"_{j"
            elif "quark-" in name:
                xlabel = var+"_{q"
            elif "MET-" in name:
                xlabel = var+"_{E^{miss}_{T},"
            if "-lepton-MET" in name:
                xlabel += "l#nu}"
            elif "-lepton" in name:
                xlabel += "l}"
            elif ("-bjet" or "bquark") in name:
                xlabel += "b}"
            elif "-jet" in name:
                xlabel += "j}"
            elif "-quark" in name:
                xlabel += "q}"
            elif "-MET" in name:
                xlabel += ",E^{miss}_{T}}}"
            elif "-nu" in name:
                xlabel += ",#nu}"
            hist0.GetXaxis().SetTitle(xlabel)
        elif "DeltaPhi_jjll" in name:
            hist0.GetXaxis().SetTitle("#Delta#phi_{jj,ll}")
            ylabel += "rad"
        elif " Eta" in name and " Eta<" not in name:
            hist0.GetXaxis().SetTitle("pseudorapidity #eta")
        elif " Phi" in name:
            hist0.GetXaxis().SetTitle("azimuthal angle #phi [rad]")
            ylabel += "rad"
        elif " Mass" in name:
            ylabel += "GeV"
            xlabel = ""
            if "vs." in name:
                hist0.GetXaxis().SetTitle("W #rightarrow l#nu mass [GeV]")
                ylabel = "W #rightarrow qq mass [GeV]"
            elif "lepton-" in name:
                xlabel = "invariant mass M_{l"
            elif "bjet-" in name or "bquark-" in name:
                xlabel = "invariant mass M_{b"
            elif "jets-" in name or "jet-jet-" in name:
                xlabel = "invariant mass M_{jj,"
            elif "jet-" in name:
                xlabel = "invariant mass M_{j"
            elif "quark-" in name:
                xlabel = "invariant mass M_{q"
            elif "hadronic top" in name:
                xlabel = "invariant mass M_{jj,b}"
            elif "leptonic top" in name:
                xlabel = "invariant mass M_{b,l#nu}"
            if "-lepton" in name:
                xlabel += "l} [GeV]"
            elif "-bjet" in name or "bquark" in name:
                xlabel += "b} [GeV]"
            elif "-jet" in name:
                xlabel += "j} [GeV]"
            elif "-quark" in name:
                xlabel += "q} [GeV]"
            elif "-MET" in name:
                xlabel += "E^{miss}_{T}} [GeV]"
            elif "-nu" in name:
                xlabel += ",#nu} [GeV]"
            else:
                xlabel = "invariant mass M [GeV]"
            hist0.GetXaxis().SetTitle(xlabel)
        elif " MET" in name:
            hist0.GetXaxis().SetTitle("MET [GeV]")
            ylabel += "GeV"
        elif " PID" in name:
            hist0.GetXaxis().SetTitle("PID")
        elif " Mt" in name:
            hist0.GetXaxis().SetTitle("transverse mass M_{T} [GeV]")
            ylabel += "GeV"
        else: print "Warning: no x-axis label!"

    # make correct y-axis labels
    hist0.GetYaxis().SetTitle(ylabel)
    hist0.SetLabelSize(0.044,"x")
    hist0.SetLabelSize(0.042,"y")
    hist0.GetXaxis().SetTitleSize(0.051)
    hist0.GetYaxis().SetTitleSize(0.044)
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

#    linewidth = kwargs.get('linewidth', 2)
    line = [1,2,3,4]
    for i in range(len(hists)):
        hists[i].SetLineColor(colors[i%len(colors)])
        hists[i].SetLineStyle(line[i%4])
        hists[i].SetLineWidth(3)



def setLineColor(*hists):
    for i in range(len(hists)):
        hists[i].SetLineColor(colors[i%len(colors)])



def setMarkerStyle(hist):

    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.8)



def norm(*hists):
    
    for hist in hists:
        I = hist.Integral()
        if I:
            hist.Scale(1/I)



