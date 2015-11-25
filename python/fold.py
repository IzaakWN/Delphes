
import math
from ROOT import TLorentzVector



def fold(DeltaPhi):
    if DeltaPhi > math.pi:
        DeltaPhi = 2*math.pi - DeltaPhi
    return DeltaPhi



def foldObj(p,q):
    
    DeltaPhi = abs( p.Phi - q.Phi )
    if DeltaPhi > math.pi:
        DeltaPhi = 2*math.pi - DeltaPhi

    return DeltaPhi



def foldTLV(p,q):
    
    DeltaPhi = abs( p.Phi() - q.Phi() )
    if DeltaPhi > math.pi:
        DeltaPhi = 2*math.pi - DeltaPhi

    return DeltaPhi