from Prepare_all import finale_state


if __name__ == "__main__":
	#final_states=["MuTau","ElTau","ElMu","TauTau"]
	final_states=["TauTau","ElMu"]
	dbs_map = {}
	dbs_map["DYJetsToLLM50_FlatPU28to62"]="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80-FlatPU28to62HcalNZSRAWAODSIM_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/RAWAODSIM"

	generator_frag_map = {}
	generator_frag_map["MuTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(MuHadCut = cms.untracked.string("Mu.Pt > 8 && Had.Pt > 18 && Mu.Eta < 2.2 && Had.Eta < 2.4"))'
	generator_frag_map["ElTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElHadCut = cms.untracked.string("El.Pt > 13 && Had.Pt > 18 && El.Eta < 2.2 && Had.Eta < 2.4 "))'
	generator_frag_map["ElMu"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElMuCut = cms.untracked.string("(El.Pt > 13 && Mu.Pt > 8)"))'
	generator_frag_map["TauTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(HadHadCut = cms.untracked.string("Had1.Pt > 38 && Had2.Pt > 38 && Had1.Eta < 2.2 && Had2.Eta < 2.2"))' 


	for finalstate in final_states:
		finale_state(finalstate=finalstate, identifier="MC_2016_CMSSW821",runs=[], inputfolder="MC2016_CMSSW_8_0_21", add_dbs=dbs_map, generator_frag_map=generator_frag_map)
