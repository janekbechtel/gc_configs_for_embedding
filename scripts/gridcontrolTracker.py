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
		states={}
		possible_states=[]
		runtime={}
		if os.path.exists(os.path.join(workdir,'jobs')):
			for d in os.listdir(os.path.join(workdir,'jobs')):
				f=open(os.path.join(workdir,'jobs',d))
				for line in f.readlines():
					if not line[:9]=='retcode=0' and line[:8]=='retcode=':
						exitcode.append(line[8:].strip('\n'))
					elif line[:7]=='status=':
						job_status=line[8:].strip('"\n')
						if job_status not in possible_states:
							possible_states.append(job_status)
							states.setdefault(job_status,[])
							states[job_status].append(int(d[4]))
						else:
							states[job_status].append(int(d.strip('job_').strip('.txt')))
					elif not line.strip('\n')=='runtime=-1' and not line.strip('\n')=='runtime=0' and line[:8]=='runtime=':
						runtime.setdefault(d.strip('job_').strip('.txt'),float(line[8:].strip('\n')))
				f.close()

		n_success=0
		n_failed=0
		n_submitted=0
		n_running=0
		n_ready=0
		
		if 'SUCCESS' in possible_states:
			n_success=len(states['SUCCESS'])
		if 'READY' in possible_states:
			n_ready=len(states['READY'])
		if 'FAILED' in possible_states:
			n_failed=len(states['FAILED'])
		if 'SUBMITTED' in possible_states:
			n_submitted=len(states['SUBMITTED'])
		if 'RUNNING' in possible_states:
			n_running=len(states['RUNNING'])
		codes={}
		for code in set(exitcode):
			codes.setdefault(code,exitcode.count(code))
		print 'Time:		'+current_time[:-7]
		print 'Total jobs:	'+str(n_jobs)
		print 'Submitted:	'+str(n_submitted)
		print 'Ready:		'+str(n_ready)
		print '\033[94m'+'Running:	'+str(n_running)+'\033[0m'
		print '\033[92m'+'Successful:	'+str(n_success)+'\033[0m'
		print '\033[91m'+'Failed:		'+str(n_failed)+'\033[0m'
		if len(exitcode)>0:
			print '\nExitcodes:	'
			for code in codes.keys():
				print code+':	occured '+str(codes[code])+' times.'
		
		
		if os.path.exists(args.output):
		
			t_json=open(args.output,'r+')
			trackingdict = json.load(t_json)
			trackingdict.setdefault('INFO',workdir)

			t_json.close()
		else:
			trackingdict = {}
			trackingdict.setdefault('INFO',workdir)
			trackingdict.setdefault('SUBMITTED',[])
			trackingdict.setdefault('READY',[])
			trackingdict.setdefault('RUNNING',[])
			trackingdict.setdefault('FAILED',[])
			trackingdict.setdefault('SUCCESS',[])
			trackingdict.setdefault('TOTAL',[])
			trackingdict.setdefault('ERRORCODE',[])
			trackingdict.setdefault('RUNTIME',[])
			trackingdict.setdefault('JOB_ID',[])

			trackingdict['SUBMITTED']={}
			trackingdict['READY']={}
			trackingdict['RUNNING']={}
			trackingdict['FAILED']={}
			trackingdict['SUCCESS']={}
			trackingdict['TOTAL']=n_jobs
			trackingdict['ERRORCODE']={}
			trackingdict['RUNTIME']={}
			trackingdict['JOB_ID']={}
	
		trackingdict['SUBMITTED'].update({current_time: n_submitted})
		trackingdict['READY'].update({current_time: n_ready})
		trackingdict['RUNNING'].update({current_time: n_running})
		trackingdict['FAILED'].update({current_time: n_failed})
		trackingdict['SUCCESS'].update({current_time: n_success})
		trackingdict['ERRORCODE'].update({current_time: codes})
		trackingdict['RUNTIME'].update(runtime)
		trackingdict['JOB_ID'].update(states)

		t_json=open(args.output,'w')
		t_json.write(json.dumps(trackingdict, sort_keys=True, indent=2))
		t_json.close()
		print '\nJob info was written to '+args.output
		if not loop:
			exit()
		time.sleep(delay)
