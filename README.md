# gc_configs_for_embedding

This package collects the configs (cmsRun, gridcontroll, inputs dbs files) for embedding, such that one can starts a large scale production


e.g.

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch

source $VO_CMS_SW_DIR/cmsset_default.sh

cmsrel CMSSW_8_0_26_patch1

cd CMSSW_8_0_26_patch1/src

cmsenv

git cms-merge-topic swayand:fixingforembedding_cmss8026p1

scramv1 b -j12

git clone https://github.com/janekbechtel/grid-control

git clone https://github.com/swayand/gc_configs_for_embedding.git
