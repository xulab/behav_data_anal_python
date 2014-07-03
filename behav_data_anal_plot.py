#!/usr/bin/python
# Filename: behav_data_anal_plot.py


def get_correct_inds(Results):
    correct = []
    correct_L = []
    correct_R = []

    trInds = []
    trInds_L = []
    trInds_R = []

    for trNum in range(len(Results['Trial_Type'])):
        # if Results['trialType'][trNum] == Results['Choice'][trNum]:
        if Results['Time_reward'][trNum] != 0:
            correct.append(1)
        else:
            correct.append(0)
        trInds.append(trNum)
        # Left trials
        if (Results['Trial_Type'][trNum] == 0):
            if (Results['Action_choice'][trNum] == 0):
                correct_L.append(1)
            else:
                correct_L.append(0)
            trInds_L.append(trNum)
        # Right trials
        if (Results['Trial_Type'][trNum] == 1):
            if (Results['Action_choice'][trNum] == 1):
                correct_R.append(1)
            else:
                correct_R.append(0)
            trInds_R.append(trNum)
                    
    return correct, correct_L, correct_R, trInds, trInds_L, trInds_R


def movingAverage(x, N):
	import numpy as np
	# import scipy as sp
	y = np.zeros(len(x))
	for i in range(len(x)):
		y[i] = np.average(x[i:(i + N)])
	return y


def plot_moving_average(behavResults, trStart=0, trEnd=0):
    # Plot data
    # import sys
    import numpy as np
    # import scipy as sp
    # import matplotlib as mpl
    import matplotlib.pyplot as plt

    if trEnd == 0:
        trEnd = len(behavResults['Trial_Num'])

    correct, correct_L, correct_R, trInds, trInds_L, trInds_R = get_correct_inds(behavResults)

    # Convert trial inds from list to numpy array
    trInds_L_array = np.asarray(trInds_L)

    inds_L = (trInds_L_array >= trStart) & (trInds_L_array <= trEnd)

    trInds_R_array = np.asarray(trInds_R)
    inds_R = (trInds_R_array >= trStart) & (trInds_R_array <= trEnd)

    trInds_array = np.asarray(trInds)
    inds = (trInds_array >= trStart) & (trInds_array <= trEnd)

    correct = np.asarray(correct)
    correct_L = np.asarray(correct_L)
    correct_R = np.asarray(correct_R)

    overall_score = np.mean(correct[inds]) * 100
    left_score = np.mean(correct_L[inds_L]) * 100
    right_score = np.mean(correct_R[inds_R]) * 100
    
    fig = plt.figure(figsize=(6, 8))
    ax1 = plt.subplot(211)
    # txt1 = ax1.text(0., 0.98, 'Trial Range =  {} -- {}'.format(trStart, trEnd), fontsize=15)
    # txt2 = ax1.text(0., 0.9, 'Overall_Performance =  {}%'.format('%0.2f' % overall_score), fontsize=15)
    # txt3 = ax1.text(0., 0.85, 'Left_Score =  {}%'.format('%0.2f' % left_score), fontsize=15)
    # txt4 = ax1.text(0., 0.8, 'Right_Score =  {}%'.format('%0.2f' % right_score), fontsize=15)
    ax1.set_axis_off()
    ax1.set_ybound(0.5, 1)
    
    ax2 = plt.subplot(212)
    # temp_str = data_file.split('/')
    # title_str = temp_str[-2] + '_' + temp_str[-1]
    plt.plot(trInds_array[inds], movingAverage(correct[inds], 20))
    plt.plot(trInds_L_array[inds_L], movingAverage(correct_L[inds_L], 20))
    plt.plot(trInds_R_array[inds_R], movingAverage(correct_R[inds_R], 20))
    plt.xlabel('# Trials')
    plt.ylabel('Percent Correct')
    # plt.title(title_str)
    
    trNums = np.asarray(behavResults['Trial_Num'])
    blockStartInds = np.where(trNums == 1)
    for x in np.nditer(blockStartInds):
        plt.axvline(x, linewidth=2, color='k')
    
    # plt.show()

    print 'Trial Range = ', trStart, trEnd

    print 'Overall_Performance = ', overall_score, '%'
    print 'Left_Performance = ', left_score, '%'
    print 'Right_Performance = ', right_score, '%'

    return fig

	
