export PYTHONPATH=`pwd`/python:$PYTHONPATH
export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
scram setup /cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_0_pre9/config/toolbox/slc6_amd64_gcc491/tools/selected/python.xml
alias python='python2.7'
