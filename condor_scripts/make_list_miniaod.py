import os
import subprocess, time, sys, shlex

#/mnt/hadoop/store/group/phys_exotica/jmao/aodsim/RunIISummer16/MINIAODSIM/MSSM-1d-prod/n3n2-n1-hbb-hbb_mh400_prompt_ev100000/crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi400_prompt_ev100000_MINIAODSIM_CaltechT2/200222_054050/0000/SUS-RunIIFall17DRPremix-00183_MINIAOD_200.root
#/mnt/hadoop/store/group/phys_exotica/jmao/aodsim/RunIISummer16/MINIAODSIM/MSSM-1d-prod/n3n2-n1-hbb-hbb_mh400_pl1000_ev100000/crab_CMSSW_9_4_12_n3n2-n1-hbb-hbb_mchi400_pl1000_ev100000_MINIAODSIM_CaltechT2/200222_060935/0000/SUS-RunIIFall17DRPremix-00183_MINIAOD_20.root

model = ['n3n2-n1-hbb-hbb']
mh = [200,300,400]
ctau = ['prompt','pl1000']

pwd = os.getcwd()
home_dir = '/mnt/hadoop/store/group/phys_exotica/jmao/aodsim/RunIISummer16/MINIAODSIM/'
for i,m in enumerate(model):
    if m=='x1n2-n1-wlv-hbb':
        str1 = 'MSSM-2d-prod'
    else:
        str1 = 'MSSM-1d-prod'
        
    for j,mm in enumerate(mh):
	    for k,ct in enumerate(ctau):
	        print(j,mm,k,ct)
		str2 = m+'_mh'+str(mm)+'_'+ct+'_ev100000'
		str3 = 'crab_CMSSW_9_4_12_'+m+'_mchi'+str(mm)+'_'+ct+'_ev100000_MINIAODSIM_CaltechT2'
		#print(str2, str3)        
		list_dir = pwd.replace('condor_scripts','lists/')+m+'/'
		os.system('mkdir -p '+list_dir)
		list_name = str2+'_miniaod.list'
		cmd = 'ls '+home_dir+str1+'/'+str2+'/'+str3+'/*/*/*root > '+list_dir+list_name
		#print(cmd)
		make_list = subprocess.Popen([cmd],stdout=subprocess.PIPE, shell=True);
	        out = make_list.communicate()
	        print(list_dir+list_name)
	        print(out)

		
