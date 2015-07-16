
# Function to reconstruct neutrino four-momentum in W->lnu decay.
# Shorthand notations:
#   TLorentzVector p: four-momentum of the lepton with mass m
#   TLorentzVector k: four-momentum of the neutrino
#   TLorentzVector q: four-momentum of the W- or Higgs boson

from ROOT import TLorentzVector
from BaseControlPlots import BaseControlPlots
from math import sqrt, cos, sin
from itertools import combinations # to make jets combinations
from operator import itemgetter # to find index of minimum element

MW = 80.4
MH = 125.7

min_offshell = 12
max_offshell = 70
MW_window = 10 # i.e. 80.4 +/- 10 GeV


# note: assumption W is on-shell
def recoNeutrino(p, MET, METphi, M=MW):
    """ Reconstruction of neutrino from Wlnu with lepton and MET
        by imposing the W mass constrain M. Helpfunction for recoWlnu1. """
    
    E = p.E()
    m = p.M()
    px = p.Px()
    py = p.Py()
    pz = p.Pz()
    
    kx = MET*cos(METphi)
    ky = MET*sin(METphi)

    a = M*M - m*m + 2*px*kx + 2*py*ky
    A = 4*(E*E - pz*pz)
    B = (-4)*a*pz
    C = 4*E*E*(kx*kx + ky*ky) - a*a
    D = B*B - 4*A*C

#    kz1 = 0
#    kz2 = 0
#    kzv   = 0

    if D > 0: # D positive, take smallest solution
        kz1 = ( -B + sqrt(D) )/( 2*A )
        kz2 = ( -B - sqrt(D) )/( 2*A )
        if abs(kz1) <= abs(kz2): kz = kz1
        else: kz = kz2
    elif D <= 0: # D negative, take real part of solutions
        kz = -B/(2*A)

    return TLorentzVector(kx, ky, kz, abs(sqrt( kz*kz + ky*ky + kx*kx )))



        #######################
        # Wlnu reco algorithm #
        #######################

# e.g. lepton = event.muon[0], MET = event.MET
def recoWlnu1(PID,lepton,MET):
    """ Reconstruction of Wlnu, assuming it is on-shell in order to
        impose the W mass constrain. """

    if PID == 11: m = 0.000511 # GeV, electron
    elif PID == 13: m = 0.106 # GeV, muon
    elif PID == 15: m = 1.78 # GeV, tau
    # or if lepton.PID == 11,13,15
    # or m = lepton.Mass
    
    p = TLorentzVector()
    p.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, m)

    return p + recoNeutrino(p,MET.MET,MET.Phi)



        ############################################
        # Wlnu reco algorithm, no W mass constrain #
        ############################################

# e.g. lepton = event.muon[0], MET = event.MET
def recoWlnu2(PID,lepton,MET):
    """ Reconstruction of Wlnu, without assuming it is on-shell. """

    if PID == 11: m = 0.000511 # GeV, electron
    elif PID == 13: m = 0.106 # GeV, muon
    elif PID == 15: m = 1.78 # GeV, tau
    # or if lepton.PID == 11,13,15
    # or m = lepton.Mass
    
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, m)
    p_nu = TLorentzVector()
    p_nu.SetPtEtaPhiM(MET.MET, 0, MET.Phi, 0)

    return p_l + p_nu



def recoWjj(jet1,jet2):
    
    p1 = TLorentzVector()
    p1.SetPtEtaPhiM(jet1.PT, jet1.Eta, jet1.Phi, jet1.Mass)
    p2 = TLorentzVector()
    p2.SetPtEtaPhiM(jet2.PT, jet2.Eta, jet2.Phi, jet2.Mass)
    # add check of invariant mass?
    return p1 + p2



def recoHjj(jet1,jet2):

    p1 = TLorentzVector()
    p1.SetPtEtaPhiM(jet1.PT, jet1.Eta, jet1.Phi, jet1.Mass)
    p2 = TLorentzVector()
    p2.SetPtEtaPhiM(jet2.PT, jet2.Eta, jet2.Phi, jet2.Mass)
    # add check of invariant mass?
    return p1 + p2



def cut(jets0):
    """ Make PT > 30 GeV cuts on jets0, but return at least
        min_jets jets. Helpfunction for the recoHWc's. """

    # make pT>30 GeV cut
    jets = [ ]
    jets_cut = [ ]
    for jet in jets0:
        if jet.PT > 30:
            jets.append(jet)
        else:
            jets_cut.append(jet)
    
    n = min(6,len(jets)) # take n leading jets

    # add jets if not enough
    if n < 3:
        d = 3-n
        jets.extend(jets_cut[:d])

    return jets



def cutb(bjets,jets0,min_jets):
    """ Take bjet out of jets0, but return at least
        min_jets non-b-tagged jets. Helpfunction for the recoHWb's. """

    jets = [ ]
    jets_cut = [ ]
    for jet in jets0:
        if jet is not bjets: # don't include given b-jets
#            if jet.PT > 30: # make pT>30 GeV cut
            jets.append(jet)
        else:
            jets_cut.append(jet)

    if len(jets) < min_jets: # add jets, if not enough
        d = min_jets-len(jets)
        jets.extend(jets_cut[:d])

    return jets[:min_jets]



        ##############################
        # Single b-tagging algorithm #
        ##############################

def recoHW_b1(bjets,jets0):
    """ Reconstruction of Hbb and Wjj, by requiring at least one b-tag.
        If there is only one b-tag, the next leading jet is taken to
        combine with the bjet for Hbb, and the two remaining leading jets
        are used for the Wjj-reconstruction.
        If there are more than one, the recoHW1-method is used. """

    if len(bjets) > 1:
        return recoHW_b2(bjets,jets0)
    
    jets = jets0[:]
    jets.remove(bjets[0])

    # 1) Make TLorentzVectors for every jet.
    p_bjet = TLorentzVector()
    p_bjet.SetPtEtaPhiM(bjets[0].PT, bjets[0].Eta, bjets[0].Phi, bjets[0].Mass)
    p_jets = [TLorentzVector(), TLorentzVector(), TLorentzVector()]
    for i in [0,1,2]:
        p_jets[i].SetPtEtaPhiM(jets[i].PT, jets[i].Eta, jets[i].Phi, jets[i].Mass)

    # 2) Make Higgs and W four-vectors.
    qH = p_bjet + p_jets[0]
    qW = p_jets[1] + p_jets[2]

    return [qH, qW]



        ##############################
        # Double b-tagging algorithm #
        ##############################

def recoHW_b2(bjets,jets0):
    """ Reconstruction of Hbb and Wjj, by requiring at least two b-tags.
        The two leading bjets are combined to reconstruct Hbb.
        And the two leading jets of the remaining are used for Wjj. """

    jets = jets0[:]
    jets.remove(bjets[0])
    jets.remove(bjets[1])

    # 1) Make TLorentzVectors for every jet.
    p_bjets = [ TLorentzVector(), TLorentzVector() ]
    p_bjets[0].SetPtEtaPhiM(bjets[0].PT, bjets[0].Eta, bjets[0].Phi, bjets[0].Mass)
    p_bjets[1].SetPtEtaPhiM(bjets[1].PT, bjets[1].Eta, bjets[1].Phi, bjets[1].Mass)
    p_jets = [ TLorentzVector(), TLorentzVector() ]
    p_jets[0].SetPtEtaPhiM(jets[0].PT, jets[0].Eta, jets[0].Phi, jets[0].Mass)
    p_jets[1].SetPtEtaPhiM(jets[1].PT, jets[1].Eta, jets[1].Phi, jets[1].Mass)

    # 2) Make Higgs and W four-vectors.
    qH = p_bjets[0] + p_bjets[1]
    qW = p_jets[0] + p_jets[1]

    return [qH, qW]



        ###########################
        # Combination algorithm 1 #
        ###########################

def recoHW_c1(jets0):
    """ Reconstruction of Hbb and Wjj, by taking the best combination
        for both seperately, assuming they are on-shell. """

    jets = cut(jets0) # make pT>30 GeV cut
    indices = range(len(jets))
    p_jets = [ ]
    masses = [ ]
    DmassesH = [ ]
    DmassesW = [ ]
    indexComb = list(combinations(indices,2))
        # e.g. for 4 jets, gibt es 6 combinations:
        # indexComb = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    # 1) Make TLorentzVectors for every jet.
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    # 2) Calculate masses of all the jet combinations.
    for comb in indexComb:
        masses.append( (p_jets[comb[0]]+p_jets[comb[1]]).M() )
    
    # 3) Calculate difference to the Higgs and W mass.
    DmassesH = [abs(MH-m) for m in masses]
    DmassesW = [abs(MW-m) for m in masses]
    
    # 4) Find jet combination with mass closest to H or W.
    indexH = min(enumerate(DmassesH), key=itemgetter(1))[0] # get index of min
    indexW = min(enumerate(DmassesW), key=itemgetter(1))[0]
    
    # 5) Make Higgs and W four-vectors
    qH = p_jets[indexComb[indexH][0]] + p_jets[indexComb[indexH][1]]
    qW = p_jets[indexComb[indexW][0]] + p_jets[indexComb[indexW][1]]

    return [qH, qW, masses]



        ###########################
        # Combination algorithm 2 #
        ###########################

# without W mass constrain: only assume Higgs on-shell
def recoHW_c2(jets0):
    """ Reconstruction of Hbb and Wjj, by taking the best combination
        for H first, assuming it is on-shell, and taking the next two leading
        jets of the remaining to make Wjj. """
    
    jets = cut(jets0) # make pT>30 GeV cut
    indices = range(len(jets))
    p_jets = [ ]
    masses = [ ]
    DmassesH = [ ]
    indexComb = list(combinations(indices,2))
        # e.g. for 4 jets, gibt es 6 combinations:
        # indexComb = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    # 1) Make TLorentzVectors for every jet.
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    
    # 2) Calculate masses of all the jet combinations.
    for comb in indexComb:
        masses.append( (p_jets[comb[0]]+p_jets[comb[1]]).M() )
    
    # 3) Calculate difference to the Higgs.
    DmassesH = [abs(MH-m) for m in masses]
    
    # 4) Find jet combination with mass closest to H or W.
    indexH = min(enumerate(DmassesH), key=itemgetter(1))[0] # get index of min
    
    # 5) Make Higgs four-vector
    qH = p_jets[indexComb[indexH][0]] + p_jets[indexComb[indexH][1]]
    
    # 6) Remove jets of Higgs and make W four-vector of remaining
    indices.remove(indexComb[indexH][0])
    indices.remove(indexComb[indexH][1])
    qW = p_jets[indices[0]] + p_jets[indices[0]]

    return [qH, qW, masses]



        #################
        # HWW algorithm #
        #################

def recoHWW_d1(event):
    """ Reconstuction of Hbb, Wjj and Wlnu by using taking best combination
        of one W on-shell and the other off-shell w.r.t. the Hbb reco.
        Returns [] if reco failed.
        Returns list of four-vectors: [q_Wlnu, q_Wjj, q_Hbb, q_HWW, q_HHbbWW].
        
        WW 2D-mass windows for HH -> bbWW,
        when one W off- and the other on-shell (~90% of the cases):
            - both:         M_W >= M_Wlnu + M_Wjj
            - on-shell:     70.4 - 90.4 GeV         (80.4 +/-10 GeV)
            - off-shell:    12.0 - 48.0 GeV         (32.0 -20 +16 GeV)
        
        WW 2D-mass windows for tt -> bbWW (~90% of the cases):
            - both: 70.4 - 90.4 GeV """


    # 0) Make H vector, make jet vectors and check for leptons.
    # -----------------------------------------------------------
    
    # 0a) Make H-vector.
    bjets = event.bjets
    jets = event.cleanedJets[:]
    if len(bjets) > 0:
        bjet1 = bjets[0]
        if bjets > 1: # two b-tags
            bjet2 = bjets[1]
        else: # one b-tag
            bjet2 =  jets[0]
    elif len(bjets) == 0: # no b-tag
        bjet1 = event.cleanedJets[0]
        bjet2 = event.cleanedJets[1]
    else:
        print "Error with len(bjets) recoHWW_d1"
    jets.remove(bjet1)
    jets.remove(bjet2)
    p_b1 = TLorentzVector()
    p_b2 = TLorentzVector()
    p_b1.SetPtEtaPhiM(bjet1.PT, bjet1.Eta, bjet1.Phi, bjet1.Mass)
    p_b2.SetPtEtaPhiM(bjet2.PT, bjet2.Eta, bjet2.Phi, bjet2.Mass)
    q_Hbb = p_b1 + p_b2
    
    # 0b) Make jet vectors.
    p_jets = [ ]
    for jet in jets: # make TLorentzVectors
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    
    # 0c) Check leading lepton.
    hasMuon = (event.muons.GetEntries()>0)
    hasElectron = (event.electrons.GetEntries()>0)
    recoMuon = False
    if hasMuon:
        if hasElectron:
            recoMuon = event.muons[0].PT > event.electrons[0].PT
        else:
            recoMuon = True
    elif not hasElectron:
        print "Warning in recoHHW_d1: no lepton for Wlnu reco!"
        return []
    if recoMuon:
        lepton = events.muons[0]
        leptonPID = 13
    else:
        lepton = events.electron[0]
        leptonPID = 11


    # 1) Reco WW assuming Wjj on-shell, Wlnu off-shell.
    # ---------------------------------------------------
    FailedReco1 = False
    
    # 1a) Reco on-shell Wjj by best combination of jets.
    indices = range(len(jets))
    masses = [ ]
    DmassesW = [ ]
    indexComb = list(combinations(indices,2)) # [ (0,1), (0,2), (1,2), ... ]
    for comb in indexComb: # make all possible combinations
        masses.append( (p_jets[comb[0]]+p_jets[comb[1]]).M() )
    DmassesW = [abs(MW-m) for m in masses] # mass differences
    indexW = min(enumerate(DmassesW), key=itemgetter(1))[0] # get index of min
    if min(DmassesW) > MW_window: # Wjj not on-shell
        FailedReco1 = True
    q_Wjj1 = p_jets[indexComb[indexW][0]] + p_jets[indexComb[indexW][1]] # make Wjj vector
    
    # 1b) Reco off-shell Wlnu.
    #       -> MWlnu in [ min( 12.0 GeV, M_T of lepton+MET ), 48.0 GeV ]
    WlnuMt = sqrt(2*event.met[0].MET*lepton.PT*(1-cos( lepton.Phi-event.met[0].Phi) ));
    if WlnuMT > max_offshell: # Wlnu not off-shell
        FailedReco1 = True
    elif WlnuMt < 10: mean_M = 36.4
    elif WlnuMt < 15: mean_M = 37.2
    elif WlnuMt < 20: mean_M = 38.0
    elif WlnuMt < 25: mean_M = 40.2
    elif WlnuMt < 30: mean_M = 43.0
    elif WlnuMt < 35: mean_M = 44.9
    elif WlnuMt < 40: mean_M = 49.0
    elif WlnuMt < 45: mean_M = 58.2
    elif WlnuMt < 50: mean_M = 60.9
    elif WlnuMt < 55: mean_M = 64.1
    elif WlnuMt < 60: mean_M = 66.6
    elif WlnuMt < 65: mean_M = 67.9
    q_Wlnu2 = recoWlnu1(leptonPID,lepton,event.met[0],M=mean_M) # reco off-shell Wlnu, assuming M = 32 GeV
    if q_Wlnu2.M() > 90:
        FailedReco1 = True


    # 2) Reco WW assuming Wlnu on-shell, Wjj off-shell.
    # ---------------------------------------------------
    FailedReco2 = False

    # 2a) Reco on-shell Wln by mass-constraint.
    q_Wlnu2 = recoWlnu1(lepton.PID,lepton,event.met[0])
    
    # 2b) Reco off-shell Wjj by taking the next two leading jets.
    q_Wjj1 = p_jets[0] + p_jets[1]
    
    if q_Wjj1.M() > max_offshell or q_Wlnu2.M() > 90:
        FailedReco2 = True


    # 3) Determine best combination.
    # --------------------------------

    if FailedReco1:
        if FailedReco2: # both failed
            return []
        else:
            return [ q_Wlnu2, q_Wjj2, q_Hbb, q_Wlnu2+q_Wjj2, q_Hbb+q_Wlnu2+q_Wjj2 ]
    elif FailedReco2:
        return [ q_Wlnu1, q_Wjj1, q_Hbb, q_Wlnu1+q_Wjj1 , q_Hbb+q_Wlnu1+q_Wjj1 ]
    else:
        return [ q_Wlnu2, q_Wjj2, q_Hbb, q_Wlnu2+q_Wjj2, q_Hbb+q_Wlnu2+q_Wjj2 ] # prefer second for some reason...





    # DROPPED HIGHS MASS CONSTRAINT for single b-tagging !!!
#    p_jets = []
#    masses = []
#    DmassesH = []
#    DmassesW = []
#    MW = 80.4
#    MH = 125.7
#
#    # 1) Make TLorentzVectors for every jet.
#    p_bjet = TLorentzVector()
#    p_bjet.SetPtEtaPhiM(bjet.PT, bjet.Eta, bjet.Phi, bjet.Mass)
#    for i in range(n):
#        p = TLorentzVector()
#        p.SetPtEtaPhiM(jets[i].PT, jets[i].Eta, jets[i].Phi, jets[i].Mass)
#        p_jets.append(p)
#    
#    # 2) Calculate masses of all combinations with b-jet.
#    masses_b = [(p_bjet+p_jets[i]).M() for i in range(n)]
#    
#    # 3) Calculate difference to Higgs mass.
#    DmassesH = [abs(MH-m) for m in masses_b]
#
#    # 4) Find jet combination with mass closest to H.
#    indexH = min(enumerate(DmassesH), key=itemgetter(1))[0] # get index of min
#
#    # 5) Remove indexH from indices and make combination of the others.
#    indices = range(n)
#    indices.remove(indexH)
#    indexComb = list(combinations(indices,2))
#        # e.g. for indices = [0, 1, 3]:
#        # indexComb = [(0, 1), (0, 3), (1, 3)]
#
#    # 5) Repeat steps 2 to 4 for W.
#    for comb in indexComb:
#        masses.append( (p_jets[comb[0]]+p_jets[comb[1]]).M() )
#    DmassesW = [abs(MW-m) for m in masses]
#    indexW = min(enumerate(DmassesW), key=itemgetter(1))[0]
#    
#    # 5) Make Higgs and W four-vectors.
#    qH = p_bjet + p_jets[indexH]
#    qW = p_jets[indexComb[indexW][0]] + p_jets[indexComb[indexW][1]]

