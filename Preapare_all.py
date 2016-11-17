import os,stat

class finale_state():
  def __init__(self, name, generator_frag, runs = ['Run2016B','Run2016C','Run2016D','Run2016E','Run2016F','Run2016G'], inputfolder = "Run2016_CMSSW_8_0_21" ):
    self.name = name
    self.runs = runs
    self.inputfolder = inputfolder
    self.generator_base = 'generator.py'
    self.files_to_copy = ['lheprodandcleaning.py','generator.py','merging.py','grid_control_fullembedding_data_base.conf']
    if not os.path.exists(self.name):
      os.mkdir(self.name)
    for add_run in self.runs	:
         self.files_to_copy.append(add_run+'.dbs')
         if not os.path.exists(self.name+'/'+add_run+'.conf'):
	   self.write_cfg(add_run)
    for file_to_copy in self.files_to_copy:
        if os.path.exists(self.name+'/'+file_to_copy):
	  continue
	if file_to_copy == 'generator.py':
	  self.copy_file(file_to_copy, add_fragment_to_end=generator_frag, copy_from_folder = self.inputfolder)
	elif file_to_copy in ['lheprodandcleaning.py','merging.py']:
	  self.copy_file(file_to_copy, copy_from_folder = self.inputfolder)
	elif file_to_copy.endswith('.dbs'):
	  self.copy_file(file_to_copy, copy_from_folder = 'dbs')
	else:
	  self.copy_file(file_to_copy)
    if not os.path.exists(self.name+'/while.sh'+file_to_copy):
      self.write_while(self.runs)
  def copy_file(self, in_file_name, copy_from_folder = './' ,add_fragment_to_end=""):
      in_file = open (copy_from_folder.rstrip('/')+'/'+in_file_name, 'r')
      file_str = in_file.read()
      in_file.close()
      file_str += add_fragment_to_end
      out_file = open(self.name+'/'+in_file_name,'w')
      out_file.write(file_str)
      out_file.close()
  def write_cfg(self, add_run):
      out_file = open(self.name+'/'+add_run+'.conf','w')
      out_file.write('[global]\n')
      out_file.write('include=grid_control_fullembedding_data_base.conf\n')
      out_file.write('workdir = /portal/ekpbms1/home/wayand/embedding/gc_workdir/TauEmbedding_'+self.name+'_'+add_run+'\n')
      out_file.write('[CMSSW]\n')
      out_file.write('dataset = TauEmbedding_'+self.name+'_'+add_run+' :  list:'+add_run+'.dbs\n')
      out_file.close()
  def write_while(self, all_runs=[]):
      out_file = open(self.name+'/while.sh','w')
      out_file.write('#!/bin/bash\n')
      out_file.write('\n')
      out_file.write('touch .lock\n')
      out_file.write('\n')
      out_file.write('while [ -f ".lock" ]\n')
      out_file.write('do\n')
      for add_run in all_runs:
	out_file.write('go.py '+self.name+'/'+add_run+'.conf -G \n')
      out_file.write('echo "rm .lock"\n')
      out_file.write('sleep 2\n')
      out_file.write('done\n')
      out_file.close()
      os.chmod(self.name+'/while.sh',stat.S_IRWXU)
      


to_process = []

to_process.append(finale_state(name='MuTau_run2015_v1', runs=["Run2015D"], inputfolder="Run2015_CMSSW_7_6_5_p1" ,generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(MuHadCut = cms.untracked.string("Mu.Pt > 18 && Had.Pt > 18 && Mu.Eta < 2.2 && Had.Eta < 2.4"))' ))
#to_process.append(finale_state(name='ElTau_test2', generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElHadCut = cms.untracked.string("El.Pt > 23 && Had.Pt > 18 && El.Eta < 2.2 && Had.Eta < 2.4 "))' ))
#to_process.append(finale_state(name='ElMu_test2', generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElMuCut = cms.untracked.string("(El.Pt > 16 && Mu.Pt > 8) || (El.Pt > 11 && Mu.Pt > 16)"))' ))
#to_process.append(finale_state(name='TauTau_test2', generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(HadHadCut = cms.untracked.string("Had1.Pt > 38 && Had2.Pt > 38 && Had1.Eta < 2.2 && Had2.Eta < 2.2"))' ))
