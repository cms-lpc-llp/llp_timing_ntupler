#!/bin/sh 
voms-proxy-info -all 
eval `scram unsetenv -sh` 
gfal-copy -f ntuple_RunIIFall17_x1n2-n1-wlv-hbb_mh200_pl1000_ev100000_fullsim_signal_aod.root gsiftp://transfer.ultralight.org//store/group/phys_exotica/jmao/susy_llp/fullsim/MSSM-2d-prod/x1n2-n1-wlv-hbb/ntuple_RunIIFall17_x1n2-n1-wlv-hbb_mh200_pl1000_ev100000_fullsim_signal_aod.root 
