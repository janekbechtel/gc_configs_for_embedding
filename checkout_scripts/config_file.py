import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      '/store/user/jbechtel/gc_storage/New_Freiburg_ElTau_fullembedding_data_2016_CMSSW821_freiburg/TauEmbedding_ElTau_data_2016_CMSSW821_Run2016G/1/merged_10100.root'
   )
)
    
process.demo = cms.EDAnalyzer('Simple_Plots',
               genSource = cms.InputTag("generator")
)

process.p = cms.Path(process.demo)
