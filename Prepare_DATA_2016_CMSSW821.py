from Prepare_all import finale_state

if __name__ == "__main__":
	final_states=["MuTau","ElTau","ElMu","TauTau"]

	for finalstate in final_states:
		finale_state(finalstate=finalstate, identifier="data_2016_CMSSW821", runs=["Run2016B","Run2016C","Run2016D","Run2016E","Run2016F","Run2016G","Run2016H"], inputfolder="Run2016_CMSSW_8_0_21", add_dbs=None)
