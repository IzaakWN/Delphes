import os
for i in range(1,50):
  f=open("submit"+str(i)+".sh","w")
  f.write("""OUTFILES="*.txt"\n
SEOUTFILES="*.root"\n
HN_NAME=hinzmann\n
DBG=0\n
USER_SRM_HOME="srm://t3se01.psi.ch:8443/srm/managerv2?SFN=/pnfs/psi.ch/cms/trivcat/store/user/"\n
TOPWORKDIR=/scratch/`whoami`\n
JOBDIR=HH_bbWW_"""+str(i)+"""_TP\n
source /afs/cern.ch/cms/cmsset_default.sh\n
cd /shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes\n
eval `scram runtime -sh`\n
export PYTHIA8=`pwd`/external/pythia8201\n
STARTDIR=`pwd`\n
WORKDIR=$TOPWORKDIR/$JOBDIR\n
RESULTDIR=$STARTDIR/$JOBDIR\n
mkdir -p $WORKDIR\n
cd $WORKDIR\n
/shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes/DelphesCMSFWLite /shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes/Cards/JetStudies_Phase_II_140PileUp_conf4_TP.tcl HH_bbWW_"""+str(i)+"""_TP.root dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/yangyong//data/Delphes/GEN/HH_bbWW/HH_bbWW_"""+str(i)+""".root\n
source /shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes/job_copy.sh\n
""")
  f.close()
  os.system("qsub -o /shome/hinzmann/jobs -e /shome/hinzmann/jobs -q long.q submit"+str(i)+".sh")
  f=open("submit"+str(i)+"_sm.sh","w")
  f.write("""OUTFILES="*.txt"\n
SEOUTFILES="*.root"\n
HN_NAME=hinzmann\n
DBG=0\n
USER_SRM_HOME="srm://t3se01.psi.ch:8443/srm/managerv2?SFN=/pnfs/psi.ch/cms/trivcat/store/user/"\n
TOPWORKDIR=/scratch/`whoami`\n
JOBDIR=HH_bbWW_"""+str(i)+"""_Strawman5\n
source /afs/cern.ch/cms/cmsset_default.sh\n
cd /shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes\n
eval `scram runtime -sh`\n
export PYTHIA8=`pwd`/external/pythia8201\n
STARTDIR=`pwd`\n
WORKDIR=$TOPWORKDIR/$JOBDIR\n
RESULTDIR=$STARTDIR/$JOBDIR\n
mkdir -p $WORKDIR\n
cd $WORKDIR\n
/shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes/DelphesCMSFWLite /shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes/Cards/JetStudies_Phase_II_140PileUp_conf4_Strawman5.tcl HH_bbWW_"""+str(i)+"""_Strawman5.root dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/yangyong//data/Delphes/GEN/HH_bbWW/HH_bbWW_"""+str(i)+""".root\n
source /shome/hinzmann/Phase2UpgradeStudies/CMSSW_5_3_24/src/Delphes/job_copy.sh\n
""")
  f.close()
  os.system("qsub -o /shome/hinzmann/jobs -e /shome/hinzmann/jobs -q long.q submit"+str(i)+"_sm.sh")
