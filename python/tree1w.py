#import ROOT
from ROOT import TFile, TTree, TBranch, TRandom, gRandom
from array import array

# http://wlav.web.cern.ch/wlav/pyroot/tpytree.html
# ftp://root.cern.ch/root/doc/ROOTUsersGuideHTML/ch12s14.html
# https://root.cern.ch/root/html/tutorials/tree/tree1.C.html

def tree1w():

    # create a tree file tree1.root - create the file, the Tree and a few branches
    f = TFile("tree1.root","recreate")
    t1 = TTree("t1","a simple Tree with simple variables")
    
    px = array('f', [0])
    py = array('f', [0])
    pz = array('f', [0])
    random = array('f', [0])
    ev = array('i', [0])
    t1.Branch("px",0,"px/F")
    t1.SetBranchAddress("px",px) # test this method
    t1.Branch("py",py,"py/F")
    t1.Branch("pz",pz,"py/F")
    t1.Branch("random",random,"random/D")
    t1.Branch("ev",ev,"ev/I")

    # fill the tree
    for i in range(1000):
        random = gRandom.Rndm()
        px[0] = gRandom.Gaus()
        py[0] = gRandom.Gaus()
        pz[0] = px[0]*px[0] + py[0]*py[0]
        ev[0] = i
        t1.Fill()

    # save the Tree heade the file will be automatically closed
    # when going out of the function scope
    #t1.Write()
    f.Write()
    f.Close()



def tree2w():

    f = TFile("tree2.root","recreate")
    t = TTree("t","a simple Tree with simple variables")
    
    max = 5
#    t1.Branch("nTracks",0,"nTracks/F")
    t.Branch("px",0,"px[max]/F")

    # fill the tree
    for i in range(100):
        n = gRandom.Integer(5)
        px = array('f', [0]*n)
        t.SetBranchAddress("px",px)
        for j in range(n):
            px[j] = gRandom.Gaus()
        t.Fill()

    f.Write()
    f.Close()



if __name__ == '__main__':
    tree1w()
    tree2w()




