# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# save_behavData_2_mat_batch.py

def parse_save_results(filename, savename):
    import scipy.io as sio
    Results = {}
    Settings = {}
    Results['Trial_inds'] = []
    Settings['Trial_inds'] = []
    
    SessionResults = []
    SessionSettings = []
    newSettings_flag = 0
    allResults = {}
    
    settingStr = []
    ind_line = 0
    ind_trial = 0
    with open(filename) as f:
        print 'Processing' , filename, '..................'
        for line in f.readlines():
            ind_line += 1
            # For debugging
            # read updated settings
            if newSettings_flag == 1 and '=' in line:
                settingStr.append(line)
            
            if '====' in line or '#Push' in line:
                newSettings_flag = 1
                settingStr = []
            

            if 'Tone Freq' in line or 'Trial_Start' in line:
                newSettings_flag = 0
            
            if 'Tone Freq' in line:
                str1, str2 = line.split(':')
                str2 = str2.strip()
                if str2.isdigit():
                    currentTone = int(str2)
                
            if 'o/' in line:
                #               if 'EOL' in line or line[len(line) - 2 : len(line)] == '\r\n':
                if 'EOL' in line or (line[-1] == '\n' and 'Choice=' in line) or '\r\n' in line:
                    #print line
                    ind_trial += 1
                    # Results['Trial_inds'].append(ind_trial)
                    # Settings['Trial_inds'].append(ind_trial)
                    resultsStr = line
                    trial_results_dict = results2dict(resultsStr)
                    trial_results_dict['Trial_inds'] = ind_trial
                    SessionResults.append(trial_results_dict)

                    # Results = append_results(Results, trial_results_dict)
                    trial_settings_dict = settings2dict(settingStr)
                    if 'currentTone' in trial_settings_dict.keys():
                        trial_settings_dict['currentTone'] = currentTone
                    trial_settings_dict['Trial_inds'] = ind_trial
                    SessionSettings.append(trial_settings_dict)

                    # Settings = append_results(Settings, trial_settings_dict)
    
    if ind_trial < 1: # or (not savename):
        print 'Warning!: No trial results in ', filename, '!'
        print 'No data to be saved!'
    else:
        allResults = {'SessionResults' : SessionResults,
                    'SessionSettings' : SessionSettings}
        # save_path = '/Users/xun/Nutstore/Projects/'
        # save_name = 'results_{animalName}_{expDate}.mat'.format(**behavResults)
        sio.savemat(savename, allResults)

    return SessionResults, SessionSettings


def results2dict(s):
    # Match old and new var names
    varname_dict = {
                    'trNum' : 'Trial_Num',
                    'trialType' : 'Trial_Type',
                    'stimType' : 'Stim_Type',
                    'toneFreq' : 'Stim_toneFreq',
                    'toneIntensity' : 'Stim_toneIntensity',
                    'setVolume' : 'Stim_setVolume',
                    'trialStartTime' : 'Time_trialStart',
                    'Stim_On_Time' : 'Time_stimOnset',
                    'Answer_Time' : 'Time_answer',
                    'Reward_Time' : 'Time_reward',
                    'numLickLeft' : 'Action_numLickLeft',
                    'numLickRight' : 'Action_numLickRight',
                    'Choice' : 'Action_choice'
                    }
    trialResultsDict = {}
#     s = s.strip('o/')
    msg = s.split('/')
#     msg.remove(msg[0])
     
    for s0 in msg:
        if '=' in s0:
            str1, str2 = s0.split('=')
            key, val = str1.strip(), str2.strip()
            
            # update the old key names
            if key in varname_dict.keys():
                key = varname_dict[key]
                
            val = val.rstrip()
            if val.isdigit():
                val = int(val)
            trialResultsDict[key] = val
    return trialResultsDict



def settings2dict(strList):
    # input arg is a list data type
    s_dict = {}
#     s = s.replace('o/','')
#     print strList
    for s0 in strList:
        str1, str2 = s0.split('=')
        key, val = str1.strip(), str2.strip()
        key = key.rstrip('(L, R)')
        val = val.rstrip()
        val = val.split('\t')
        
        if type(val) is list:
            for i in range(len(val)):
                if val[i].isdigit():
                    val[i] = int(val[i])
        
        elif val.isdigit():
            val = int(val)
        
        s_dict[key] = val
    return s_dict


# def append_results(all_dict, trial_dict):
#     currentTrialNo = all_dict['Trial_inds'][-1]
# #     print currentTrialNo
#     for key in trial_dict.keys():
#         # If a new key appears after some trial, add the new key, 
#         # and put the value of all previous trials as 0 or ''.
#         if type(trial_dict[key]) is list:
#             tempvar = [] # trial_dict[key][0]
#         elif type(trial_dict[key]) is int:
#             tempvar = 0 #trial_dict[key]
#         elif type(trial_dict[key]) is str:
#             tempvar = ''
            
#         if not key in all_dict.keys():
# #             print trial_dict
#             all_dict[key] = []
#             all_dict[key][0:currentTrialNo-1] = [tempvar]*(currentTrialNo-1)

#         all_dict[key].append(trial_dict[key])
#     return all_dict


# <codecell>
import sys
import os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt


data_dir = sys.argv[1]
datafiles = os.listdir(data_dir)
os.chdir(data_dir)

for fname in datafiles:
    if '.beh' in fname:
        savename = data_dir + os.path.sep + fname.strip('.beh') + '.mat'
        print 'save results to : ', savename
        parse_save_results(fname, savename)


