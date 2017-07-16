#!/bin/bash

touch .lock

while [ -f ".lock" ]
do
go.py MuTau_data_2017_CMSSW923p2/Run2017B.conf -G 
echo "rm .lock"
sleep 2
done
