# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


def parse_save_results(filename, savename):
    import scipy.io as sio
    behavResults = {}
    with open(filename) as f:
        for line in f.readlines():
            newSettings_flag = 0
            settingStr = []
            if '====' in line:
                newSettings_flag = 1

            if 'Tone Freq' in line:
                newSettings_flag = 0

            if newSettings_flag == 1 and '=' in line:
                settingStr.append(line)

            if 'o/' in line:
                resultsStr = line
                trial_results = results2dict(resultsStr)
                behavResults = append_results(behavResults, trial_results)

    # save_path = '/Users/xun/Nutstore/Projects/'
    # save_name = 'results_{animalName}_{expDate}.mat'.format(**behavResults)
    sio.savemat(savename, behavResults)


def results2dict(s):
    s_dict = {}
    s = s.replace('o/','')
    msg = s.split('/')
    for s0 in msg:
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



# <codecell>
import sys
import os
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt


data_dir = sys.argv[1]
datafiles = os.listdir(data_dir)

for fname in datafiles:
    savename = data_dir + fname + '.mat'
    parse_save_results(fname, savename)


