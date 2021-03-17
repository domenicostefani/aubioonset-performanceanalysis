#!/usr/bin/env python3

import computeLatency
import multiprocessing as mp
pool = mp.Pool(mp.cpu_count())

results = [pool.apply(computeLatency.perform_main_analysis, args=("audiofiles","aubioonset","hfc",64,64,silences,1.31,0.02)) for silences in [-52,-53,-54,-55,-56,-56,-58,-59,-60]]


pool.close()




# info1, metrics1 = computeLatency.perform_main_analysis(audio_directory = "audiofiles", \
#                                                      aubioonset_command = "aubioonset", \
#                                                      onset_method = "hfc", \
#                                                      buffer_size = 64, \
#                                                      hop_size = 64, \
#                                                      silence_threshold = -54.0, \
#                                                      onset_threshold = 1.31, \
#                                                      minimum_inter_onset_interval_s = 0.02)
#
# info2, metrics2 = computeLatency.perform_main_analysis(audio_directory = "audiofiles", \
#                                                   aubioonset_command = "aubioonset", \
#                                                   onset_method = "hfc", \
#                                                   buffer_size = 64, \
#                                                   hop_size = 64, \
#                                                   silence_threshold = -56.0, \
#                                                   onset_threshold = 1.31, \
#                                                   minimum_inter_onset_interval_s = 0.02)
#
# computeLatency.create_string(info1, metrics1, True)
# computeLatency.create_string(info2, metrics2, True)
