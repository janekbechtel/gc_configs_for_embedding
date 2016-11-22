import os,stat
from Prepare_all import finale_state

dbs_map = {}
dbs_map["DYJetsToLLM50_FlatPU28to62"]="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80-FlatPU28to62HcalNZSRAWAODSIM_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/RAWAODSIM"

final_states=["MuTau","ElTau","ElMu","TauTau"]
for finalstate in final_states:
  finale_state(finalstate=finalstate, identifier="MC",runs=["Run2016B","Run2016C","Run2016D","Run2016E","Run2016F","Run2016G","Run2016H"], inputfolder="Run2016_CMSSW_8_0_21", add_dbs=dbs_map)


