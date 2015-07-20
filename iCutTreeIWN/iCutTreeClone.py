import time
start = time.time()

from ROOT import TFile, gDirectory, TObjArray, TList
# use execfile("name.py") to execute

oldfile = TFile("HH_bbWW_1_TP.root")
oldtree = gDirectory.Get("Delphes")
#event = Event()
#oldtree.SetBranchAddress("oldtree",oldtree)
#oldtree.SetBranchStatus("*",0)
#oldtree.SetBranchStatus("Electron",1)
oldtree.GetListOfBranches().Remove(oldtree.GetBranch("Track"))
oldfile.Write()

#newfile = TFile("HH_bbWW_1_TP_cut.root","RECREATE")
#newfile.Write()
#newfile.Close()
#newtree = oldtree.CloneTree()

end = time.time()
print "\nThe program lasted",end-start,"wseconds.\n"
