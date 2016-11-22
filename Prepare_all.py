import os,stat

class finale_state():
	def __init__(self, finalstate, identifier="", generator_frag="", runs = ['Run2016B','Run2016C','Run2016D','Run2016E','Run2016F','Run2016G','Run2016H'], add_dbs=None, inputfolder = "Run2016_CMSSW_8_0_21"):
		self.finalstate=finalstate
		self.identifier=identifier
		self.name = finalstate+"_"+identifier
		self.gc_cfgs = [] 
		self.inputfolder = inputfolder
		self.cmsRun_order =  ['preselection.py','selection.py','lheprodandcleaning.py','generator.py','merging.py'] ## will be overwitten by copy_pyconfigs (checks is exsist in input folder)
		if not os.path.exists(self.name):
			os.mkdir(self.name)
		generator_frag_map=self.make_generator_frag_map(this_finalstate=self.finalstate)
		self.copy_pyconfigs(generator_frag=generator_frag_map[self.finalstate])
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
		se_output_pattern_str= 'se output pattern = '+self.finalstate+'_fullembedding_'+self.identifier+'_'+self.inputfolder+'_freiburg/@NICK@/@FOLDER@/@XBASE@_@GC_JOB_ID@.@XEXT@'
		rp_base_cfg['__SE_OUTPUT_PATTERN__']=se_output_pattern_str
		self.copy_file('grid_control_fullembedding_data_base.conf', copy_from_folder='./' ,replace_dict=rp_base_cfg)
		
		
	def copy_file(self, in_file_name, copy_from_folder = None ,add_fragment_to_end="", skip_if_not_there=False, overwrite=False, replace_dict={}):
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
		for replace in replace_dict: ## replace Variable by the value. 
			file_str = file_str.replace(replace,replace_dict[replace])
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
	def make_generator_frag_map(self,this_finalstate):
		generator_frag_map = {}
		if this_finalstate=="MuTau":
			generator_frag_map["MuTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(MuHadCut = cms.untracked.string("Mu.Pt > 18 && Had.Pt > 18 && Mu.Eta < 2.2 && Had.Eta < 2.4"))'
		elif this_finalstate=="ElTau":
			generator_frag_map["ElTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElHadCut = cms.untracked.string("El.Pt > 23 && Had.Pt > 18 && El.Eta < 2.2 && Had.Eta < 2.4 "))'
		elif this_finalstate=="ElMu":
			generator_frag_map["ElMu"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(ElMuCut = cms.untracked.string("(El.Pt > 16 && Mu.Pt > 8) || (El.Pt > 11 && Mu.Pt > 16)"))'
		elif this_finalstate=="TauTau":
			generator_frag_map["TauTau"] = 'process.generator.HepMCFilter.filterParameters = cms.PSet(HadHadCut = cms.untracked.string("Had1.Pt > 38 && Had2.Pt > 38 && Had1.Eta < 2.2 && Had2.Eta < 2.2"))' 
		return generator_frag_map

if __name__ == "__main__":
	final_states=["MuTau","ElTau","ElMu","TauTau"]

	for finalstate in final_states:
		finale_state(finalstate=finalstate, identifier="data", runs=["Run2016B","Run2016C","Run2016D","Run2016E","Run2016F","Run2016G","Run2016H"], inputfolder="Run2016_CMSSW_8_0_21", add_dbs=None)
