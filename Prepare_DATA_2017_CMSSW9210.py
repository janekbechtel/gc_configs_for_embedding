from Prepare_all import finale_state

if __name__ == "__main__":
	final_states=["MuTau","ElTau","ElMu","TauTau"]
	for finalstate in final_states:
		finale_state(finalstate=finalstate, identifier="data_2017_CMSSW9210", runs=["Run2017D","Run2017E"], inputfolder="Run2017_CMSSW_9_2_10", add_dbs=None)