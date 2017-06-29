#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc530
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src
cmsenv

mkdir Embedding/plugins/ -p
mkdir Embedding/python/ 

wget https://raw.githubusercontent.com/swayand/gc_configs_for_embedding/master/checkout_scripts/BuildFile.xml -P Embedding/plugins/
wget https://raw.githubusercontent.com/swayand/gc_configs_for_embedding/master/checkout_scripts/ReadGeneratorWeight.cc -P Embedding/plugins/
wget https://raw.githubusercontent.com/swayand/gc_configs_for_embedding/master/checkout_scripts/config_file.py -P Embedding/python/

