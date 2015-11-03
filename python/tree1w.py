from ROOT import TFile, TTree, TBranch, TRandom
import array

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
    ev = array('i', [0])
    t1.Branch("px",px,"px/F")
    t1.Branch("py",py,"py/F")
    t1.Branch("pz",pz,"pz/F")
    t1.Branch("ev",ev,"ev/I")

    # fill the tree
    for i in range(0,1000):
        gRandom.Rannor(px[0],py[0])
        pz[0] = px[0]*px[0] + py[0]*py[0]
        random = gRandom.Rndm()
        ev[0] = i
        t1.Fill()

    # save the Tree heade the file will be automatically closed
    # when going out of the function scope
    #t1.Write()
    f.Write()
    f.Close()
