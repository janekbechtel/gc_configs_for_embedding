import os
import argparse
import gzip
from datetime import datetime
import json
import time

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Track status of gridcontrol job.")
	parser.add_argument("-w", "--workdir", required=False, default = "",
						help="GC working directory [Default: here]")
	parser.add_argument("--loop", default=None,	help="Loop the script all LOOP seconds.")
	parser.add_argument("-o","--output", default='tracking.json',	help="Output file. If it exists, values stay and new values will be added to the end.")
	parser.add_argument("--include-job-ids", default=False, action='store_true',	help="Save not only total amount of jobs per state but also every job ID for every state. Will increase output file size by a lot.")

	args = parser.parse_args()
	
	
	workdir=args.workdir

	if not args.output[-5:]=='.json':
		print "Output file needs to be a json file."
		exit()
	if not os.path.isabs(args.output):
		args.output=os.path.join(os.getcwd(),args.output)
	if not os.path.isabs(workdir):
		workdir=os.path.join(os.getcwd(),workdir)
	if not os.path.exists(os.path.join(workdir,'current.conf')):
		print "Workdir "+workdir+" is not a valid grid control workdir."
		exit()
	all_subdirs = [d for d in os.listdir(workdir) if os.path.isdir(workdir+d)]
	dirdict = {}
	with gzip.open(workdir+'/params.map.gz','r') as f:
		n_jobs=int(f.read().strip('\n'))

	if args.loop is not None:
		loop=True
		delay=int(args.loop)
	else: 
		loop=False
	
	while True:
		done=[]
		success=[]
		failed=[]
		exitcode=[]
		submitted=[]
		current_time = str(datetime.now())
		
		if os.path.exists(os.path.join(workdir,'sandbox')):
			for d in os.listdir(os.path.join(workdir,'sandbox')):
				submitted.append(d)
				
		if os.path.exists(os.path.join(workdir,'output')):

			for d in os.listdir(os.path.join(workdir,'output')):
				if d[4:] not in submitted:
					done.append(d[4:])
					f=open(os.path.join(workdir,'output',d,'job.info'))
					for line in f.readlines():
						line=line.strip('\n')
						if line=='EXITCODE=0':
							
							success.append(d[4:])
							continue
						elif line[:9]=='EXITCODE=':
							failed.append(d[4:])
							exitcode.append(line[9:])
							continue
					f.close()


		n_success=len(success)
		n_failed=len(failed)
		n_submitted=len(submitted)
		i=0
		codes={}
		for code in set(exitcode):
			codes.setdefault(code,exitcode.count(code))
		print 'Time:		'+current_time[:-7]
		print 'Total jobs:	'+str(n_jobs)
		print '\033[94m'+'Submitted:	'+str(n_submitted)+'\033[0m'
		print '\033[92m'+'Successful:	'+str(n_success)+'\033[0m'
		print '\033[91m'+'Failed:		'+str(n_failed)+'\033[0m'
		if len(exitcode)>0:
			print '\nExitcodes:	'
			for code in codes.keys():
				print code+':	occured '+str(codes[code])+' times.'
		
		
		if os.path.exists(args.output):
		
			t_json=open(args.output,'r+')
			trackingdict = json.load(t_json)
			t_json.close()
		else:
			trackingdict = {}
			trackingdict.setdefault('SUBMITTED',[])
		#	trackingdict.setdefault('RUNNING',[])
			trackingdict.setdefault('FAILED',[])
			trackingdict.setdefault('SUCCESS',[])
			trackingdict.setdefault('TOTAL',[])
			trackingdict.setdefault('ERRORCODE',[])
			if args.include_job_ids:
				trackingdict.setdefault('JOB_ID_FAILED',[])
				trackingdict.setdefault('JOB_ID_SUCCESS',[])
				trackingdict.setdefault('JOB_ID_SUBMITTED',[])
				trackingdict.setdefault('JOB_ID_ERRORCODE',[])
			trackingdict['SUBMITTED']={}
			#trackingdict['RUNNING']={}
			trackingdict['FAILED']={}
			trackingdict['SUCCESS']={}
			trackingdict['TOTAL']={}
			trackingdict['ERRORCODE']={}
			if args.include_job_ids:
				trackingdict['JOB_ID_FAILED']={}
				trackingdict['JOB_ID_SUCCESS']={}
				trackingdict['JOB_ID_SUBMITTED']={}
				trackingdict['JOB_ID_ERRORCODE']={}
				
				
		trackingdict['SUBMITTED'].update({current_time: n_submitted})
	#	trackingdict['RUNNING'].update({current_time: []})
		trackingdict['FAILED'].update({current_time: n_failed})
		trackingdict['SUCCESS'].update({current_time: n_success})
		trackingdict['TOTAL'].update({current_time: n_jobs})
		trackingdict['ERRORCODE'].update({current_time: codes})
		if args.include_job_ids:
			trackingdict['JOB_ID_FAILED'].update({current_time: []})
			trackingdict['JOB_ID_SUCCESS'].update({current_time: []})
			trackingdict['JOB_ID_SUBMITTED'].update({current_time: []})
			trackingdict['JOB_ID_ERRORCODE'].update({current_time: []})
			for x in success:
				trackingdict['JOB_ID_SUCCESS'][current_time].append(x)
			for x in failed:
				trackingdict['JOB_ID_FAILED'][current_time].append(x)
			for x in submitted:
				trackingdict['JOB_ID_SUBMITTED'][current_time].append(x)
			for x in exitcode:
				trackingdict['JOB_ID_ERRORCODE'][current_time].append(x)
			
		
		t_json=open(args.output,'w')
		t_json.write(json.dumps(trackingdict, sort_keys=True, indent=2))
		t_json.close()
		print '\nJob info was written to '+args.output
		if not loop:
			exit()
		time.sleep(delay)
