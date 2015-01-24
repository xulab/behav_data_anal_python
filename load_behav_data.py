#!/usr/bin/python
# Filename: load_behav_data.py

# Load and parse behavioral data, which should be text files

def parse_behav_data(filename):
# allResults = parse_behav_data(filename)
# Load behavior data (.beh) file, extract settings and trial by trial data.
# Store the retrieved data to dictionary data type.

    Results = {}
    Settings = {}
    Results['Trial_inds'] = []
    Settings['Trial_inds'] = []
    Results['Block_id'] = []
    Settings['Block_id'] = []
    
    behavResults = {}
    behavSettings = {}
    newSettings_flag = 0
    allResults = {}
    
    settingStr = []
    ind_line = 0
    ind_trial = 0
    with open(filename) as f:
        for line in f.readlines():
            ind_line += 1
            # For debugging
            # read updated settings
            if newSettings_flag == 1 and '=' in line:
                settingStr.append(line)
            
            if '====' in line or '#Push' in line:
                newSettings_flag = 1
                settingStr = []
            
            if 'Tone Freq' in line or '####' in line:
                newSettings_flag = 0
            
            # if 'Tone Freq' in line:
            #     str1, str2 = line.split(':')
            #     str2 = str2.strip()
            #     if str2.isdigit():
            #         currentTone = int(str2)
                
            if 'o/' in line:
                #               if 'EOL' in line or line[len(line) - 2 : len(line)] == '\r\n':
                if 'EOL' in line or (line[-1] == '\n' and 'Choice=' in line) or '\r\n' in line:
                    #print line
                    block_id = 0
                    ind_trial += 1

                    Results['Trial_inds'].append(ind_trial)
                    Settings['Trial_inds'].append(ind_trial)
                    
                    resultsStr = line
                    trial_results = results2dict(resultsStr)
                    Results = append_results(Results, trial_results)

                    trial_settings = settings2dict(settingStr)
                    # trial_settings['currentTone'] = currentTone
                    Settings = append_results(Settings, trial_settings)

                    # If settings were changed during behavior, the Trial_Num will become 1 after arduino reset
                    # Count it as a new block of trials.
                    if trial_results['Trial_Num'] == 1:
                        block_id += 1
                    
                    Results['Block_id'].append(block_id)
                    Settings['Block_id'].append(block_id)
    
    if (not Results):
        print 'Warning!: No trial results in ', filename, '!'
        print 'No data to be saved!'
    else:
        allResults = {'behavResults': Results,
                      'behavSettings': Settings}
        # save_path = '/Users/xun/Nutstore/Projects/'
        # save_name = 'results_{animalName}_{expDate}.mat'.format(**behavResults)
        # sio.savemat(savename, allResults)

    return allResults


def save_results_as_mat_file(savename, ResultsDict):
    import scipy.io as sio
    sio.savemat(savename, ResultsDict)


def results2dict(s):
    # Match old and new var names
    varname_mapping = {
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
    s_dict = {}
#     s = s.strip('o/')
    msg = s.split('/')
#     msg.remove(msg[0])
     
    for s0 in msg:
        if '=' in s0:
            str1, str2 = s0.split('=')
            key, val = str1.strip(), str2.strip()
            
            # update the old key names
            if key in varname_mapping.keys():
                key = varname_mapping[key]
                
            val = val.rstrip()
            if val.isdigit():
                val = int(val)
            s_dict[key] = val
    return s_dict


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


def append_results(all_dict, trial_dict):
    currentTrialNo = all_dict['Trial_inds'][-1]
#     print currentTrialNo
    for key in trial_dict.keys():
        # If a new key appears after some trial, add the new key,
        # and put the value of all previous trials as 0 or ''.
        if type(trial_dict[key]) is list:
            tempvar = []  # trial_dict[key][0]
        elif type(trial_dict[key]) is int:
            tempvar = 0  # trial_dict[key]
        elif type(trial_dict[key]) is str:
            tempvar = ''
            
        if not key in all_dict.keys():
#             print trial_dict
            all_dict[key] = []
            all_dict[key][0:currentTrialNo - 1] = [tempvar] * (currentTrialNo - 1)
            
#             if type(tempvar) is int:
#                 all_dict[key][0:currentTrialNo-1] = [0]*(currentTrialNo-1)
                
#             elif type(tempvar) is str:
#                 all_dict[key][0:currentTrialNo-1] = ['']*(currentTrialNo-1)
            
#             all_dict[key].append(tempvar)
#             if key == 'responseDelay':
#                     print all_dict[key]
#         else:
 #             all_dict[key].append(tempvar)

        all_dict[key].append(trial_dict[key])
    return all_dict


def get_trial_results(data_path, anmName, expDate, suffix=''):
    # Load data, and return results of all trials, not including settings.
    import os

    fname = expDate + '_' + anmName + suffix + '.beh'
    data_file = os.path.join(data_path, anmName, fname)
    
    allResults = parse_behav_data(data_file)
    
    trialResults = allResults['behavResults']
    
    return trialResults

    

