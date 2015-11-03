from ROOT import TFile, TTree, TBranch, TRandom


def tree1w()

    # create a tree file tree1.root - create the file, the Tree and a few branches
    f = TFile("tree1.root","recreate")
    t1 = TTree("t1","a simple Tree with simple variables")
    px = 0.0
    py = 0.0
    pz = 0.0
    ev = 0
    t1.Branch("px",&px,"px/F")
    t1.Branch("py",&py,"py/F")
    t1.Branch("pz",&pz,"pz/F")
    t1.Branch("ev",&ev,"ev/I")

    # fill the tree
    for i in range(0,1000):
        gRandom.Rannor(px,py)
        pz = px*px + py*py
        random = gRandom.Rndm()
        ev = i
        t1.Fill()

    # save the Tree heade the file will be automatically closed
    # when going out of the function scope
    t1.Write()
