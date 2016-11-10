# gc_configs_for_embedding

This package collects the configs (cmsRun, gridcontroll, inputs dbs files) for embedding, such that one can starts a large scale production


e.g.

export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch

source $VO_CMS_SW_DIR/cmsset_default.sh

cmsrel CMSSW_8_0_20

cd CMSSW_8_0_20/src

git cms-merge-topic swayand:fixingforembedding_cmss80x

scramv1 b -j12

svn co https://ekptrac.physik.uni-karlsruhe.de/svn/grid-control/trunk/grid-control

git clone https://github.com/swayand/gc_configs_for_embedding.git
