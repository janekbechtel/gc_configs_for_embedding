import os,stat

class finale_state():
	def __init__(self, name, generator_frag="", runs = ['Run2016B','Run2016C','Run2016D','Run2016E','Run2016F','Run2016G'], add_dbs=None, inputfolder = "Run2016_CMSSW_8_0_21"):
		self.name = name
		self.gc_cfgs = [] 
		self.inputfolder = inputfolder
		self.cmsRun_order =  ['preselection.py','selection.py','lheprodandcleaning.py','generator.py','merging.py'] ## will be overwitten by copy_pyconfigs (checks is exsist in input folder)
		if not os.path.exists(self.name):
			os.mkdir(self.name)
		self.copy_pyconfigs(generator_frag=generator_frag)
		self.copy_gcconfigs(runs=runs,add_dbs=add_dbs)
		self.write_while()
	def copy_pyconfigs(self, generator_frag=""):
		is_first = True ## can be late used to init the first config with customize_for_gc and the later with the dummy stings 
		self.cmsRun_order = []
		for file_to_copy in ['preselection.py','selection.py','lheprodandcleaning.py','generator.py','merging.py']:
		        add_fragment_to_end = ""
			if file_to_copy == 'generator.py':
				add_fragment_to_end=generator_frag
			if self.copy_file(file_to_copy, add_fragment_to_end=add_fragment_to_end, skip_if_not_there=True):
				is_first = False
				self.cmsRun_order.append(file_to_copy)
	def copy_gcconfigs(self, runs=[], add_dbs=None):
	  	for add_run in runs:
			self.copy_file(add_run+'.dbs', copy_from_folder = 'dbs')
			if not os.path.exists(self.name+'/'+add_run+'.conf'):
				self.write_cfg(add_run=add_run)
		if add_dbs:
			self.write_cfg(add_dbs=add_dbs)	
		cmsRun_order_str = 'config file = '
		for cmsRun_cfg in self.cmsRun_order:
			cmsRun_order_str += cmsRun_cfg+'\n\t\t'
		rp_base_cfg = {}
		rp_base_cfg['__CMSRUN_ORDER__'] = cmsRun_order_str
		self.copy_file('grid_control_fullembedding_data_base.conf', copy_from_folder='./' ,repalce_dict=rp_base_cfg)
		 
		
	def copy_file(self, in_file_name, copy_from_folder = None ,add_fragment_to_end="", skip_if_not_there=False, overwrite=False, repalce_dict={}):
		if not copy_from_folder:
			copy_from_folder = self.inputfolder
		if skip_if_not_there and not os.path.isfile(copy_from_folder.rstrip('/')+'/'+in_file_name):
			return False
		in_file = open (copy_from_folder.rstrip('/')+'/'+in_file_name, 'r')
		file_str = in_file.read()
		in_file.close()
		if os.path.isfile(self.name+'/'+in_file_name) and not overwrite: ## do not overwrit if the file exists
			return True
		file_str += add_fragment_to_end
		for replace in repalce_dict: ## replace Variable by the value. 
			file_str = file_str.replace(replace,repalce_dict[replace])
		out_file = open(self.name+'/'+in_file_name,'w')
		out_file.write(file_str)
		out_file.close()
		return True
	def write_cfg(self, add_run=None, add_dbs=None):
		try:
			out_file = open(self.name+'/'+add_run+'.conf','w')
		except:
			out_file = open(self.name+'/DAS.conf','w')
		out_file.write('[global]\n')
		out_file.write('include=grid_control_fullembedding_data_base.conf\n')
		out_file.write('workdir = /portal/ekpbms2/home/${USER}/embedding/gc_workdir/TauEmbedding_'+out_file.name.split('.')[0]+'\n')
		out_file.write('[CMSSW]\n')
		if add_run:
			out_file.write('dataset = TauEmbedding_'+self.name+'_'+add_run+' :  list:'+add_run+'.dbs\n')
		if add_dbs:
			for akt_name in add_dbs:
				out_file.write('dataset = TauEmbedding_'+self.name+'_'+akt_name+' :  dbs:'+add_dbs[akt_name]+'\n')
		out_file.close()
		self.gc_cfgs.append(out_file.name) ## save the 
		
	def write_while(self, overwrite=False):
	        if os.path.isfile(self.name+'/while.sh') and not overwrite:
			return
		out_file = open(self.name+'/while.sh','w')
		out_file.write('#!/bin/bash\n')
		out_file.write('\n')
		out_file.write('touch .lock\n')
		out_file.write('\n')
		out_file.write('while [ -f ".lock" ]\n')
		out_file.write('do\n')
		for akt_cfg in self.gc_cfgs:
			out_file.write('go.py '+akt_cfg+' -G \n')
		out_file.write('echo "rm .lock"\n')
		out_file.write('sleep 2\n')
		out_file.write('done\n')
		out_file.close()
		os.chmod(self.name+'/while.sh',stat.S_IRWXU)




generator_frag_map = {}

generator_frag_map["MuTau_"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(MuHadCut = cms.untracked.string("Mu.Pt > 18 && Had.Pt > 18 && Mu.Eta < 2.2 && Had.Eta < 2.4"))'
generator_frag_map["ElTau_"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElHadCut = cms.untracked.string("El.Pt > 23 && Had.Pt > 18 && El.Eta < 2.2 && Had.Eta < 2.4 "))'
generator_frag_map["ElMu_"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElMuCut = cms.untracked.string("(El.Pt > 16 && Mu.Pt > 8) || (El.Pt > 11 && Mu.Pt > 16)"))'
generator_frag_map["TauTau_"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(HadHadCut = cms.untracked.string("Had1.Pt > 38 && Had2.Pt > 38 && Had1.Eta < 2.2 && Had2.Eta < 2.2"))' 

dbs_map = {}
dbs_map["DYJetsToLLM50_FlatPU28to62"]="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80-FlatPU28to62HcalNZSRAWAODSIM_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/RAWAODSIM"


for akt_final_states in generator_frag_map:
  finale_state(name=akt_final_states+'rmc2016_v1', runs=[], inputfolder="MC2016_CMSSW_8_0_21" ,generator_frag = generator_frag_map[akt_final_states],add_dbs=dbs_map)

to_process = []

#to_process.append(finale_state(name='MuTau_run2016_2016D_v1', selection=True, runs=["Run2016D"], inputfolder="Run2016_CMSSW_8_0_21" ,generator_frag = '' ))
#to_process.append(finale_state(name='MuTau_Gridka_2016D_v1', selection=True, runs=["Run2016D"], inputfolder="Run2016_CMSSW_8_0_21" ,generator_frag = '' ))
#to_process.append(finale_state(name='MuTau_run2015_v1', selection=False, runs=["Run2015D"], inputfolder="Run2015_CMSSW_7_6_5_p1" ,generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(MuHadCut = cms.untracked.string("Mu.Pt > 18 && Had.Pt > 18 && Mu.Eta < 2.2 && Had.Eta < 2.4"))' ))
#to_process.append(finale_state(name='ElTau_test2', generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElHadCut = cms.untracked.string("El.Pt > 23 && Had.Pt > 18 && El.Eta < 2.2 && Had.Eta < 2.4 "))' ))
#to_process.append(finale_state(name='ElMu_test2', generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElMuCut = cms.untracked.string("(El.Pt > 16 && Mu.Pt > 8) || (El.Pt > 11 && Mu.Pt > 16)"))' ))
#to_process.append(finale_state(name='TauTau_test2', generator_frag = 'process.generator.HepMCFilter.filterParameters = cms.PSet(HadHadCut = cms.untracked.string("Had1.Pt > 38 && Had2.Pt > 38 && Had1.Eta < 2.2 && Had2.Eta < 2.2"))' ))
