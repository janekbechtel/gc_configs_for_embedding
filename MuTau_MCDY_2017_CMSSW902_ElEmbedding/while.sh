#!/bin/bash

touch .lock

while [ -f ".lock" ]
do
go.py MuTau_MCDY_2017_CMSSW902/DAS.conf -G 
echo "rm .lock"
sleep 2
done
