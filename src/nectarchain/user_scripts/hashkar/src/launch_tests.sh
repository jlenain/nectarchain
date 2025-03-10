#launching DIRAC proxy
dirac-proxy-init -M -g cta_nectarcam d


#DEADTIME
########################################################################
#python deadtime.py  -o "../output/" -s 2 2 1 2 2 1 2 2 1 -r 3702 3701 3700 3765 3766 3767 3799 3800 3801
########################################################################


#LINEARITY
########################################################################
#python linearity.py -o "../output/"
#default=[i for i in range(3404, 3424)] #+ [i for i in range(3435, 3444)],
########################################################################


#PIX TIM UNCE
########################################################################
#python pix_tim_uncertainty_test.py -o "../output/" -r 3759 3741 3742 3794 3743 3775 3708 3759 3741 3742 3796 3721 3722 3723 3761 #7360 3759 3741 3742 3796 3795 3794 3743 3775 3708 3707 3706 3705 3776 3777 #GOOD
########################################################################


#PEDESTALS
########################################################################
#python pedestal.py  -o "../output/" -r 3696 3697 3698 3699 3751 3752 3753 3754 3785 3786 3787 3788 #GOOD
#do it for high gain and low gain ? might add low gain later 
# how many events ? 
########################################################################


#DQM FOR CHARGE
########################################################################
#cd ../../../../dqm/
#pwd
#runs=("3630" "3631" "3629" "3628" "3627" "3626" "3625" "3624" "3622" "3623" "3714" "3713" "3712" "3711" "3710" "3709" "3708" "3707" "3706" "3705" "3764" "3763" "3762" "3761" "3760" "3759" "3758" "3757" "3756" "3755" "3798" "3797" "3796" "3795" "3794" "3793" "3792" "3791" "3790" "3789")
#python start_dqm_thermal.py $NECTARDIR/data ../output/charge -r 3793 --method GlobalPeakWindowSum --extractor_kwargs '{"window_width":16,"window_shift":4}'  -n --max-events 100

########################################################################

#FF
########################################################################
#runs = [3731, 3750, 3784]
#python flatfield_example.py -r 3731
########################################################################


#GAIN SPEFit
########################################################################
#runs = [3731, 3750, 3784]
#python gain_SPEfit_computation.py -r 3942  --reload_events --max_events 100  --method GlobalPeakWindowSum --extractor_kwargs '{"window_width":8,"window_shift":4}' --overwrite -v DEBUG
########################################################################


#GAIN Photostatistic
########################################################################
#runs = [3731, 3750, 3784] and there associated pedestal and FF runs
#python gain_PhotoStat_computation.py --FF_run_number 3937 --Ped_run_number 3938 --SPE_run_number 3942 --max_events 100  --method GlobalPeakWindowSum --extractor_kwargs '{"window_width":8,"window_shift":4}' --overwrite -v INFO --reload_events
########################################################################


#THRESHOLD HG/LG
########################################################################
#python no code for the moment -> Francois
########################################################################


#REMANAING work : 

#Photostat script
#THRESHOLD HG/LG script

#THRESHOLD HG/LG plots
