# Function to reconstruct neutrino four-momentum in W->lnu decay.
# Shorthand notations:
#   TLorentzVector p: four-momentum of the lepton with mass m
#   TLorentzVector k: four-momentum of the neutrino
#   TLorentzVector q: four-momentum of the W- or Higgs boson

from ROOT import TLorentzVector
from BaseControlPlots import BaseControlPlots
from math import sqrt, cos, sin
from itertools import combinations, product, chain # to make jets combinations
        # e.g. for 4 jets, gibt es 6 combinations:
        # indexComb = list(combinations(range(4),2))
        #           = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
from fold import fold
from copy import copy

MW = 80.4
MH = 125.7

min_offshell = 0
max_offshell = 80
window = 50 # i.e. 80.4 +/- 30 GeV
MW_max = 130
MH_min = MH-window-20
MH_max = MH+window



def index_min(list):
# alternative:
# from operator import itemgetter # to find index of minimum element
#       min(enumerate(list), key=itemgetter(1))[0] # get index of min
    return min(xrange(len(list)),key=list.__getitem__)



# note: assumption W is on-shell
def recoNeutrino(p, MET, M=MW):
    """ Reconstruction of neutrino from Wlnu with lepton and MET
        by imposing the W mass constrain M. Helpfunction for recoWlnu1. """
    
    E = p.E()
    m = p.M()
    px = p.Px()
    py = p.Py()
    pz = p.Pz()
    
    kx = MET.MET*cos(MET.Phi)
    ky = MET.MET*sin(MET.Phi)

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

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoWlnu1(lepton,MET,M=MW):
    """ Reconstruction of Wlnu, assuming it is on-shell in order to
        impose the W mass constrain. """

    #if PID == 11: m = 0.000511 # GeV, electron
    #elif PID == 13: m = 0.106 # GeV, muon
    #elif PID == 15: m = 1.78 # GeV, tau
    ## or if lepton.PID == 11,13,15
    ## or m = lepton.Mass
    
    p = TLorentzVector()
    p.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)

    return p + recoNeutrino(p,MET,M)



        ############################################
        # Wlnu reco algorithm, no W mass constrain #
        ############################################

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoWlnu2(lepton,MET):
    """ Reconstruction of Wlnu, without assuming it is on-shell. """

    #if PID == 11: m = 0.000511 # GeV, electron
    #elif PID == 13: m = 0.106 # GeV, muon
    #elif PID == 15: m = 1.78 # GeV, tau
    
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
    p_nu = TLorentzVector()
    p_nu.SetPtEtaPhiM(MET.MET, 0, MET.Phi, 0)

    return p_l + p_nu



        ##############################################
        # Wlnu reco algorithm, no W mass constrain 2 #
        ##############################################

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoWlnu3(q_Wjj,lepton,MET):
    """ Reconstruction of Wlnu, using cluster transverse mass approximation. """

    #if PID == 11: m = 0.000511 # GeV, electron
    #elif PID == 13: m = 0.106 # GeV, muon
    #elif PID == 15: m = 1.78 # GeV, tau

    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT,lepton.Eta,lepton.Phi,lepton.Mass)
    q_Wjjl = q_Wjj + p_l
    kx = MET.MET*cos(MET.Phi)
    ky = MET.MET*sin(MET.Phi)
    kz = q_Wjjl.Pz() * MET.MET / sqrt( q_Wjjl.E()*q_Wjjl.E() - q_Wjjl.Pz()*q_Wjjl.Pz() )
    k_nu = TLorentzVector( kx, ky, kz, abs(sqrt( kz*kz + ky*ky + kx*kx )))
    
    return p_l + k_nu



        ##################
        # Wlnu Mt reco 1 #
        ##################

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoWlnu1Mt(lepton,MET):
    """ Reconstruction of Mt of Wlnu from pT and Phi of lepton and MET. """
    
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
    E = p_l.E()*p_l.E() + MET.MET
    P = p_l.P()*p_l.P() + MET.MET
    
    return sqrt( E*E - P*P )



        ##################
        # Wlnu Mt reco 2 #
        ##################

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoWlnu2Mt(lepton,MET):
    """ Reconstruction of Mt of Wlnu from pT and Phi of lepton and MET. """
    
    return sqrt(2 * MET.MET * lepton.PT * (1-cos( lepton.Phi - MET.Phi)) )



        ##################
        # Wlnu Mc reco 1 #
        ##################

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoHWWMC1(p_Wjj,lepton,MET):
    """ Reconstruction of Mt of Wlnu from pT and Phi of lepton and MET. """
    
    #if PID == 11: m = 0.000511 # GeV, electron
    #elif PID == 13: m = 0.106 # GeV, muon
    #elif PID == 15: m = 1.78 # GeV, tau
    
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
    p_jjl = p_Wjj + p_l
    
    return sqrt( p_jjl.Pt()*p_jjl.Pt() + p_jjl.M()*p_jjl.M() ) + MET.MET



        ##################
        # Wlnu Mc reco 2 #
        ##################

# e.g. lepton = event.muon[0], MET = event.met[0]
def recoHWWMC2(p_Wjj,lepton,MET):
    """ Reconstruction of Mt of Wlnu from pT and Phi of lepton and MET. """
    
    #if PID == 11: m = 0.000511 # GeV, electron
    #elif PID == 13: m = 0.106 # GeV, muon
    #elif PID == 15: m = 1.78 # GeV, tau
    
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
    M = (p_Wjj+p_l).M()
    ET = MET.MET
    
    return sqrt( M*M + ET*ET ) + ET



        ################
        # Wjj M reco 1 #
        ################

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



def cut(jets0,min_jets=3):
    """ Make PT > 30 GeV and Eta < 2.5 cuts on jets0, but return at least
        min_jets jets. Helpfunction for the recoHWc's. """

    # make pT>30 GeV cut
    jets = [ ]
    jets_cut = [ ]
    for jet in jets0:
        if jet.PT > 30: #and jet.Eta < 2.5:
            jets.append(jet)
        else:
            jets_cut.append(jet)
    
    n = min(6,len(jets)) # take n leading jets

    # re-add jets if not enough
    if n < min_jets:
        d = min_jets-n
        jets.extend(jets_cut[:d])

    return jets



def cut15(jets0,min_jets=3):
    """ Make PT > 15 GeV and Eta < 2.5 cuts on jets0, but return at least
        min_jets jets. Helpfunction for the recoHWc's. """

    # make pT>15 GeV cut
    jets = [ ]
    jets_cut = [ ]
    for jet in jets0:
        if jet.PT > 15 and jet.Eta < 2.5:
            jets.append(jet)
        else:
            jets_cut.append(jet)
    
    n = min(8,len(jets)) # take n leading jets

    # re-add jets if not enough
    if n < min_jets:
        d = min_jets-n
        jets.extend(jets_cut[:d])

    return jets



def cutb(bjets,jets0,min_jets):
    """ Take bjet out of jets0, but return at least
        min_jets non-b-tagged jets. Helpfunction for the recoHWb's. """

    jets = [ ]
    jets_cut = [ ]
    for jet in jets0:
        if not jet in bjets: # don't include given b-jets
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



        ################################
        # Double b-tagging algorithm 2 #
        ################################

def recoHW_b3(bjets,jets0):
    """ Reconstruction of Hbb and Wjj, requiring at least two b-tags.
        The two leading bjets are combined to reconstruct Hbb.
        The remaining leading jets are used to form the combination for Wjj
        the highest Pt with exclusion of mass over MW_max, if possible. """

    jets = jets0[:]
    jets.remove(bjets[0])
    jets.remove(bjets[1])

    # 1) Make TLorentzVectors for every jet.
    p_bjets = [ TLorentzVector(), TLorentzVector() ]
    p_bjets[0].SetPtEtaPhiM(bjets[0].PT, bjets[0].Eta, bjets[0].Phi, bjets[0].Mass)
    p_bjets[1].SetPtEtaPhiM(bjets[1].PT, bjets[1].Eta, bjets[1].Phi, bjets[1].Mass)
    p_jets = [ ]
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    # 2) Make Higgs four-vector.
    qH = p_bjets[0] + p_bjets[1]
    
    # 3) Make combinations with remaining jets, excluding mass > MW_max
    PT_max = 0
    p_max = TLorentzVector(0,0,0,0)
    for p_jet1, p_jet2 in combinations(p_jets,2):
        p = p_jet1 + p_jet2
        if p.M() < MW_max and PT_max < p.Pt():
            p_max = p #.copy() not needed?
            PT_max = p.Pt()

    # 4) Make W four-vector of first combination with mass < MW_max
    if PT_max:
        qW = p_max
    else:
        qW = p_jets[0] + p_jets[1]

    return [qH, qW]



        ################################
        # Double b-tagging algorithm 3 #
        ################################

def recoHW_b4(bjets,jets0):
    """ Reconstruction of Hbb and Wjj, requiring at least two b-tags.
        The first combination of jets with 60<M<150 are combined to reconstruct Hbb,
        with a preference for combinations with b-jets.
        The remaining leading jets are used to form a combination for Wjj
        with exclusion of mass over 100 GeV, if possible. """

    # 1) Make TLorentzVectors for every jet.
    p_bjets = [ ]
    for bjet in bjets:
        p_bjets.append(TLorentzVector())
        p_bjets[-1].SetPtEtaPhiM(bjet.PT, bjet.Eta, bjet.Phi, bjet.Mass)
    if MH_min < (p_bjets[0]+p_bjets[1]).M() < MH_max:
        return recoHW_b3(bjets,jets0)
    jets = [ jet for jet in jets0 if not jet in bjets ]
    p_jets = [ ]
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    # 2) Make combinations for H
    masses = [ ]
    p_bjetCombs = [ ]
    # prefer                   (bjets,bjet)    above  (bjet,jet)   above   (jet,jet)
    for p_bjet1, p_bjet2 in chain( combinations(p_bjets,2), product(p_bjets,p_jets)):#, combinations(p_jets,2) ):
        mass = (p_bjet1+p_bjet2).M()
        if MH_min < mass < MH_max:
            masses.append(mass)
            p_bjetCombs = [p_bjet1,p_bjet2]
            break # only take first combination!
    p_jets = p_jets + p_bjets

    # 3) Make four-vector for H
    if len(masses)>0:
        qH = p_bjetCombs[0] + p_bjetCombs[1]
        p_jets.remove(p_bjetCombs[0])
        p_jets.remove(p_bjetCombs[1])
    else:
        qH = p_bjets[0] + p_bjets[1]
        p_jets.remove(p_bjets[0])
        p_jets.remove(p_bjets[1])
    
    # 4) Make combinations with remaining jets, excluding mass > MW_max
    PT_max = 0
    p_max = TLorentzVector(0,0,0,0)
    for p_jet1, p_jet2 in combinations(p_jets,2):
        p = p_jet1 + p_jet2
        if p.M() < MW_max and PT_max < p.Pt():
            p_max = p
            PT_max = p.Pt()
    
    # 5) Make W four-vector of first combination with mass < MW_max
    if PT_max:
        qW = p_max
    else:
        qW = p_jets[0] + p_jets[1]

    return [qH, qW]



def max_b2b(vectors):
    """ 1) Loop over all vector-vector combinations from vectors
        2) Boost back to rest frame of sum
        3) Return combination with DeltaPhi closest to pi: back-to-back """
    
    p_12_b2b = None
    DeltaPhi_b2b = 0 # > pi
    for p1,p2 in combinations(vectors,2):
        p_12 = p1 + p2
        q1 = copy(p1)
        q2 = copy(p2)
        q1.Boost(-beta)
        q2.Boost(-beta)
        beta = p_12.BoostVector()
        DeltaPhi = fold(abs(q1.Phi()-q2.Phi()))
        if DeltaPhi > DeltaPhi_b2b:
            p_12_b2b = copy(p_12)
            DeltaPhi_b2b = DeltaPhi

    return p_12_b2b



        #######################
        # Angular algorithm 1 #
        #######################

def recoHW_a1(bjets,jets0,lepton,MET):
    """ Reconstruction of HWW, requiring at least two b-tags.
        The two leading bjets are taken out the jets, and the
        next leading jets with
                DeltaPhi(jet,lepton)<1.8
                DeltaPhi(bjet,bjet)<1.8
        are used to form HWW. """

    jets = jets0[:]
    jets.remove(bjets[0])
    jets.remove(bjets[1])
    jets = [ jet for jet in jets if fold(abs(lepton.Phi-jet.Phi)) < 1.8 ]

    if len(jets)<2 or fold(abs(bjets[0].Phi-bjets[1].Phi)) > 2.2: # TODO: extend for cases with more than 2 bjets
        return [ ]
    
    #if abs(lepton.Eta-jets[0].Eta)>1 and abs(lepton.Eta-jets[1].Eta)>1:
        #return [ ]
    
    # 1) Make TLorentzVectors.
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
    p_bjets = [ TLorentzVector(), TLorentzVector() ]
    p_bjets[0].SetPtEtaPhiM(bjets[0].PT, bjets[0].Eta, bjets[0].Phi, bjets[0].Mass)
    p_bjets[1].SetPtEtaPhiM(bjets[1].PT, bjets[1].Eta, bjets[1].Phi, bjets[1].Mass)
    p_jets = [ TLorentzVector(), TLorentzVector() ]
    p_jets[0].SetPtEtaPhiM(jets[0].PT, jets[0].Eta, jets[0].Phi, jets[0].Mass)
    p_jets[1].SetPtEtaPhiM(jets[1].PT, jets[1].Eta, jets[1].Phi, jets[1].Mass)
    
    # 2) Make Hbb and Wjj LorentzVector.
    q_Hbb = p_bjets[0] + p_bjets[1]
    q_Wjj = p_jets[0] + p_jets[1]

#    # 3) TODO: Find Wlnu via boost to HWW restframe.
#    beta = q.BoostVector()
#    q_Wjj.Boost(beta)

    return [ q_Hbb, q_Wjj ]



        #######################
        # Angular algorithm 2 #
        #######################

def recoHW_a2(bjets,jets0,lepton,MET):
    """ Reconstruction of Hbb and Wjj, requiring at least two b-tags.
        The two leading bjets are combined to reconstruct Hbb.
        The remaining leading jets are used to form the combination that
        is back-to-back in the HWW frame. """

    jets = jets0[:]
    jets.remove(bjets[0])
    jets.remove(bjets[1])

    # 1) Make TLorentzVectors.
    p_l = TLorentzVector()
    p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
    p_bjets = [ TLorentzVector(), TLorentzVector() ]
    p_bjets[0].SetPtEtaPhiM(bjets[0].PT, bjets[0].Eta, bjets[0].Phi, bjets[0].Mass)
    p_bjets[1].SetPtEtaPhiM(bjets[1].PT, bjets[1].Eta, bjets[1].Phi, bjets[1].Mass)
    p_jets = [ ]
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    # 2) Make Higgs four-vector.
    qH = p_bjets[0] + p_bjets[1]
    
    # 3) Make combinations with remaining jets, excluding mass > MW_max
    PT_max = 0
    p_max = TLorentzVector(0,0,0,0)
    for p_jet1, p_jet2 in combinations(p_jets,2):
        p_Wjj = p_jet1 + p_jet2
        
#        if p.M() < MW_max and PT_max < p.Pt():
#            p_max = p
#            PT_max = p.Pt()

    return 0



        ###########################
        # Combination algorithm 1 #
        ###########################

def recoHW_c1(jets0):
    """ Reconstruction of Hbb and Wjj, by taking the best combination
        for both seperately, assuming they are on-shell. """

    jets = cut(jets0) # make pT>30 GeV
    indices = range(len(jets))

    # 1) Make TLorentzVectors for every jet.
    p_jets = [ ]
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    # 2) Calculate masses of all the jet combinations.
    masses = [ ]
    indexComb = list(combinations(range(len(jets)),2))
    for i, j in indexComb:
        masses.append( (p_jets[i]+p_jets[j]).M() )
    
    # 3) Calculate difference to the Higgs and W mass.
    DmassesH = [abs(MH-m) for m in masses]
    DmassesW = [abs(MW-m) for m in masses]
    
    # 4) Find jet combination with mass closest to H or W.
    indexH = index_min(DmassesH) # get index of min
    indexW = index_min(DmassesW)
    
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

    jets = cut(jets0) # make pT>30 GeV
    indices = range(len(jets))

    # 1) Make TLorentzVectors for every jet.
    p_jets = [ ]
    for jet in jets:
        p_jets.append(TLorentzVector())
        p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    
    # 2) Calculate masses of all the jet combinations.
    masses = [ ]
    indexComb = list(combinations(range(len(jets)),2))
    for i, j in indexComb:
        masses.append( (p_jets[i]+p_jets[j]).M() )
    
    # 3) Calculate difference to the Higgs.
    DmassesH = [abs(MH-m) for m in masses]
    
    # 4) Find jet combination with mass closest to H or W.
    min = index_min(DmassesH) # get index of min
    
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
        Returns [ ] if reco failed.
        Returns list of TLoretzVectors and integers:
        [q_Wlnu, q_Wjj, q_Hbb, q_HWW, q_HHbbWW, case, FailedReco1, FailedReco2].
        
        WW 2D-mass windows for HH -> bbWW,
        when one W off- and the other on-shell (~90% of the cases):
            - both:         M_W >= M_Wlnu + M_Wjj
            - on-shell:     70.4 - 90.4 GeV         (80.4 +/-10 GeV)
            - off-shell:    12.0 - 48.0 GeV         (32.0 -20 +16 GeV)
        
        WW 2D-mass windows for tt -> bbWW (~90% of the cases):
            - both: 70.4 - 90.4 GeV """


    # 0) Prepare stuff.
    # -------------------
    
    # 0a) Make H-vector.
    bjets = event.bjets30[:] # = [ jet for jet in event.cleanedJets30 if jet.BTag ]
    jets = event.cleanedJets30[:10]
    if len(bjets) > 0:
        bjet1 = bjets[0]
        if bjets > 1: # two b-tags
            bjet2 = bjets[1]
        else: # one b-tag
            bjet2 =  jets[0]
    elif len(bjets) == 0: # no b-tag
        bjet1 = event.cleanedJets[0]
        bjet2 = event.cleanedJets[1]
    jets.remove(bjet1)
    jets.remove(bjet2)
#    jets = cut(jets,2) # make Pt cuts
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
    
    # 0d) Make combinations of jets.
    masses = [ ]
    DmassesW = [ ]
    indexComb = list(combinations(range(len(jets)),2))
    for i, j in indexComb: # make all possible combinations
        masses.append( (p_jets[i]+p_jets[j]).M() )
    
    # 0e) Check leading lepton.
    lepton = event.leadingLeptons[0]
    if not lepton:
        print "Warning in recoHHW_d1: no lepton for Wlnu reco!"
        return [ ]



    # 1) Reco WW assuming Wjj on-shell, Wlnu off-shell.
    # ---------------------------------------------------
    FailedReco1 = 0
    
    # 1a) Reco on-shell Wjj by best combination of jets.
    DmassesW = [abs(MW-m) for m in masses] # mass differences
    minDm = index_min(DmassesW) # get index of min
    indexW = minDm[0]
    q_Wjj1 = p_jets[indexComb[indexW][0]] + p_jets[indexComb[indexW][1]] # make Wjj vector
    if minDm[1] > window: # Wjj not on-shell
        FailedReco1 = 1
    
    # 1b) Reco off-shell Wlnu.
    #       -> MWlnu in [ min( 12.0 GeV, M_T of lepton+MET ), 48.0 GeV ]
    WlnuMt = recoWlnu2Mt(lepton,event.met[0])
#    mean_M = 32.6
#    if WlnuMt < 15: mean_M = 33.4
#    elif WlnuMt < 20: mean_M = 34.1
#    elif WlnuMt < 25: mean_M = 36.2
#    elif WlnuMt < 30: mean_M = 38.5
#    elif WlnuMt < 35: mean_M = 39.9
#    elif WlnuMt < 40: mean_M = 43.1
#    elif WlnuMt < 45: mean_M = 47.5
#    elif WlnuMt < 50: mean_M = 49.5
#    q_Wlnu1 = recoWlnu1(leptonPID,lepton,event.met[0],M=WlnuMt) # reco off-shell Wlnu, assuming M = mean_M
    q_Wlnu1 = recoWlnu3(q_Wjj1,lepton,event.met[0])
    if q_Wlnu1.M() > max_offshell or WlnuMt > max_offshell:
        FailedReco1 += 2


    # 2) Reco WW assuming Wlnu on-shell, Wjj off-shell.
    # ---------------------------------------------------
    FailedReco2 = 0

    # 2a) Reco on-shell Wln by mass-constraint.
    q_Wlnu2 = recoWlnu1(lepton,event.met[0])
    if abs(q_Wlnu2.M()) > MW + 15:
        FailedReco2 = 1
    
    # 2b) Reco off-shell Wjj by taking making the best combination.
    DmassesW = [abs(20-m) for m in masses] # mass differences from middle of off-shell W mass window
    indexW = index_min(DmassesW) # get index of min
    q_Wjj2 = p_jets[indexComb[indexW][0]] + p_jets[indexComb[indexW][1]] # make Wjj vector
    if q_Wjj2.M() > max_offshell or q_Wjj2.M() < min_offshell:
        FailedReco2 += 2


    # 3) Determine best combination.
    # --------------------------------

    if FailedReco1:
        if FailedReco2: # both failed
#            print "Warning in recoHHW_d1: both failed!"
            return [ FailedReco1, FailedReco2, masses ]
        else:           # reco 2 succeeded, 1 failed
            return [ q_Wlnu2, q_Wjj2, q_Hbb, q_Wlnu2+q_Wjj2, q_Hbb+q_Wlnu2+q_Wjj2, [2, FailedReco1, FailedReco2]+masses ]
    elif FailedReco2:   # reco 1 succeeded, 2 failed
        return [ q_Wlnu1, q_Wjj1, q_Hbb, q_Wlnu1+q_Wjj1, q_Hbb+q_Wlnu1+q_Wjj1, [1, FailedReco1, FailedReco2]+masses ]
    else:               # both succeeded
        return [ q_Wlnu1, q_Wjj1, q_Hbb, q_Wlnu1+q_Wjj1, q_Hbb+q_Wlnu1+q_Wjj1, [3, FailedReco1, FailedReco2]+masses ] # TODO: find better way to choose


