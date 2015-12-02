import os
processes = ["HH_bbWW","TTbar"]
designs = ["TP","Strawman5"]
for p in processes:
  for d in designs:
    f = open(p+"_"+d+".txt",'w')
    list = os.listdir("/pnfs/psi.ch/cms/trivcat/store/user/hinzmann")
    list2 = filter(lambda x: p in x and d in x, list)
    for i in list2:
      print>>f, i+"/"+i+".root"
    f.close()