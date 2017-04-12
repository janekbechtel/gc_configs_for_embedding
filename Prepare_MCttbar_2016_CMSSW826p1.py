from Prepare_all import finale_state


if __name__ == "__main__":
	#final_states=["MuTau","ElTau","ElMu","TauTau"]
	final_states=["MuTau"]
	dbs_map = {}
	dbs_map["DYJetsToLLM50_FlatPU28to62"]="/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16DR80-FlatPU28to62HcalNZSRAWAODSIM_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/RAWAODSIM"

	generator_frag_map = {}
	generator_frag_map["MuTau"] = 'process.generator.HepMCFilter.filterParameters.MuHadCut = cms.string("Mu.Pt > 8 && Had.Pt > 18 && Mu.Eta < 2.2 && Had.Eta < 2.4")'
	#generator_frag_map["ElTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElHadCut = cms.untracked.string("El.Pt > 13 && Had.Pt > 18 && El.Eta < 2.2 && Had.Eta < 2.4 "))'
	#generator_frag_map["ElMu"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElMuCut = cms.untracked.string("(El.Pt > 13 && Mu.Pt > 8)"))'
	#generator_frag_map["TauTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(HadHadCut = cms.untracked.string("Had1.Pt > 38 && Had2.Pt > 38 && Had1.Eta < 2.2 && Had2.Eta < 2.2"))' 


	for finalstate in final_states:
		finale_state(finalstate=finalstate, identifier="MCttbar_2016_CMSSW826p1",runs=[], inputfolder="MC2016_CMSSW_8_0_26_p1", add_dbs=dbs_map, generator_frag_map=generator_frag_map)
