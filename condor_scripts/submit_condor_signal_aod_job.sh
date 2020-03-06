#!/bin/bash
mkdir -p log
mkdir -p submit

echo `pwd`

cd ../
ScriptDir=`pwd`
cd -

job_script=${CMSSW_BASE}/src/cms_lpc_llp/llp_timing_ntupler/condor_scripts/run_signal_aod_job.sh
echo $job_script

year=Fall17
filesPerJob=5
for sample in \
n3n2-n1-hbb-hbb_mh200_pl1000_ev100000_fullsim_test \
#n3n2-n1-hbb-hbb_mh200_pl1000_ev100000_fullsim \

do
	echo "Sample " ${sample}
	output=/store/group/phys_exotica/delayedjets/jmao/susy_llp/fullsim/MSSM-1d-prod/n3n2-n1-hbb-hbb/${sample}
	echo "output ${output}"
	inputfilelist=/src/cms_lpc_llp/llp_timing_ntupler/lists/n3n2-n1-hbb-hbb/${sample}.list
	nfiles=`cat ${CMSSW_BASE}$inputfilelist | wc | awk '{print $1}' `
        maxjob=`python -c "print int($nfiles.0/$filesPerJob)+1"`
	mod=`python -c "print int($nfiles.0%$filesPerJob)"`
        if [ ${mod} -eq 0 ]
        then
                maxjob=`python -c "print int($nfiles.0/$filesPerJob)"`
        fi
	config=displacedJetTiming_ntupler_MC_${year}_Fullsim_condor
	echo "${config}"
	rm -f submit/${config}_{sample}_Job*.jdl
	rm -f log/${config}_${sample}_Job*
	echo "number of jobs: " ${maxjob}

	jdl_file=submit/${config}_${sample}_${maxjob}.jdl
	echo "Universe = vanilla" > ${jdl_file}
	echo "Executable = ${job_script}" >> ${jdl_file}
        echo "Arguments = ${config}.py ${inputfilelist} ${filesPerJob} \$(ProcId) ${sample}_Job\$(ProcId)_Of_${maxjob}.root ${output} ${CMSSW_BASE} ${HOME}/ ${year}" >> ${jdl_file}
	
	# option should always be 1, when running condor
	echo "Log = log/${config}_${sample}_Job\$(ProcId)_Of_${maxjob}_\$(Cluster).\$(Process).log" >> ${jdl_file}
	echo "Output = log/${config}_${sample}_Job\$(ProcId)_Of_${maxjob}_\$(Cluster).\$(Process).out" >> ${jdl_file}
	echo "Error = log/${config}_${sample}_Job\$(ProcId)_Of_${maxjob}_\$(Cluster).\$(Process).err" >> ${jdl_file}

	#echo "Requirements=(TARGET.OpSysAndVer==\"CentOS7\" && regexp(\"blade.*\", TARGET.Machine))" >> ${jdl_file}
	echo "RequestMemory = 2000" >> ${jdl_file}
	echo "RequestCpus = 1" >> ${jdl_file}
	echo "RequestDisk = 4" >> ${jdl_file}
	echo "+RunAsOwner = True" >> ${jdl_file}
	echo "+InteractiveUser = true" >> ${jdl_file}
	echo "+SingularityImage = \"/cvmfs/singularity.opensciencegrid.org/bbockelm/cms:rhel7\"" >> ${jdl_file}
	#if [ ${year} == "Summer16" ]
	#then
	#	echo "+SingularityImage = \"/cvmfs/singularity.opensciencegrid.org/bbockelm/cms:rhel7\"" >> ${jdl_file}
	#else
	#	echo "+SingularityImage = \"/cvmfs/singularity.opensciencegrid.org/bbockelm/cms:rhel6\"" >> ${jdl_file}
	#fi
	echo '+SingularityBindCVMFS = True' >> ${jdl_file}
#	echo "transfer_input_files = tarball/${sample}.tar" >> ${jdl_file}
	echo "run_as_owner = True" >> ${jdl_file}
	echo "x509userproxy = ${HOME}/x509_proxy" >> ${jdl_file}
	echo "should_transfer_files = YES" >> ${jdl_file}
	echo "when_to_transfer_output = ON_EXIT" >> ${jdl_file}
	echo "Queue ${maxjob}" >> ${jdl_file}
	echo "condor_submit ${jdl_file}"
	#condor_submit ${jdl_file}
done
