# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


def results2dict(s):
    s_dict = {}
    s.strip('o/')
    msg = s.split('/')
    for s0 in msg:
        if '=' in s0:
            str1, str2 = s0.split('=')
            key, val = str1.strip(), str2.strip()
            val = val.rstrip('\r\n')
            if val.isdigit():
                val = int(val)
            s_dict[key] = val
    return s_dict


def append_results(allResults, trialResults):
    # Now append data to the lists of each elements
    if len(allResults) == 0:
        for var_key in trialResults.keys():
            allResults[var_key] = []

    for var_key in trialResults.keys():
        value = trialResults[var_key]
        allResults[var_key].append(value)
    return allResults


def movingAverage(x, N):
    y = np.zeros(len(x))
    for i in range(len(x)):
        y[i] = np.average(x[i:(i+N)])
    return y


def get_correct_trials(behavResults):
    correct = []
    correct_L = []
    correct_R = []

    trInds = []
    trInds_L = []
    trInds_R = []

    for trNum in range(len(behavResults['Trial_Type'])):
        # if behavResults['trialType'][trNum] == behavResults['Choice'][trNum]:
        if behavResults['Time_reward'][trNum] != 0:
            correct.append(1)
        else:
            correct.append(0)
        trInds.append(trNum)
        # Left trials
        if (behavResults['Trial_Type'][trNum] == 0):
            if (behavResults['Action_choice'][trNum] == 0):
                correct_L.append(1)
            else:
                correct_L.append(0)
            trInds_L.append(trNum)
        # Right trials        
        if (behavResults['Trial_Type'][trNum]== 1):
            if (behavResults['Action_choice'][trNum] == 1): 
                correct_R.append(1)
            else:
                correct_R.append(0)
            trInds_R.append(trNum)
                    
    return correct, correct_L, correct_R, trInds, trInds_L, trInds_R 



# <codecell>
import sys
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

data_file = sys.argv[1]

# data_file = '/home/xulab/Documents/behavior_data/2014.3.27/animal07'

# print data_file

behavResults = {}
with open(data_file) as f:
    for line in f.readlines():
        # print line
        if 'o/' in line:
            if 'EOL' in line or line[len(line) - 2:len(line)] == '\r\n':
                # print line[len(line) - 2 : len(line)]
    	    # Example line: o/trNum=270/trialType=0/trialStartTime=0_4_1_9_53_26_740/Stim_On_Time=1021/Answer_Time=1587/Reward_Time=1613/Choice=0
                resultsStr = line
                trial_results = results2dict(resultsStr)
                behavResults = append_results(behavResults,trial_results)
# print resultsStr            

correct, correct_L, correct_R, trInds, trInds_L, trInds_R = get_correct_trials(behavResults)


if len(sys.argv) > 2:
    a = int(sys.argv[2])
else:
    a = 0

if len(sys.argv) > 3:
    b = int(sys.argv[3])
else:
    b = len(correct)


# a = 0 # 200
# b = len(correct) #340

# <codecell>
temp_str = data_file.split('/')
title_str = temp_str[-2] + '_' + temp_str[-1]
plt.plot(trInds, movingAverage(correct, 20))
plt.plot(trInds_L, movingAverage(correct_L, 20))
plt.plot(trInds_R, movingAverage(correct_R, 20))
plt.xlabel('# Trials')
plt.ylabel('Percent Correct')
plt.title(title_str)

trNums = np.asarray(behavResults['Trial_Num'])
blockStartInds = np.where(trNums == 1)
for x in np.nditer(blockStartInds):
    plt.axvline(x, linewidth = 2, color = 'k')

plt.show()

# Convert trial inds from list to numpy array
trInds_L_array = np.asarray(trInds_L)
inds_L = (trInds_L_array > a) & (trInds_L_array < b)

trInds_R_array = np.asarray(trInds_R)
inds_R = (trInds_R_array > a) & (trInds_R_array < b)

trInds_array = np.asarray(trInds)
inds = (trInds_array > a) & (trInds_array < b)

correct = np.asarray(correct)
correct_L = np.asarray(correct_L)
correct_R = np.asarray(correct_R)

print 'Trial Range = ', a, b

print 'Overall_Performance = ', np.mean(correct[inds])*100, '%'
print 'Left_Performance = ', np.mean(correct_L[inds_L])*100, '%'
print 'Right_Performance = ', np.mean(correct_R[inds_R])*100, '%'

