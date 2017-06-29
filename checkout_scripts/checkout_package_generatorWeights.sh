#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc530
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src
cmsenv

mkdir Embedding/Simple_Plots/plugins/ -p
mkdir Embedding/Simple_Plots/python/ 

wget https://raw.githubusercontent.com/swayand/gc_configs_for_embedding/master/checkout_scripts/BuildFile.xml -P Embedding/Simple_Plots/plugins/
wget https://raw.githubusercontent.com/swayand/gc_configs_for_embedding/master/checkout_scripts/Simple_Plots.cc -P Embedding/Simple_Plots/plugins/
wget https://raw.githubusercontent.com/swayand/gc_configs_for_embedding/master/checkout_scripts/config_file.py -P Embedding/Simple_Plots/python/

