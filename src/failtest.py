#!/usr/bin/env python3

import computeLatency



info, metrics = computeLatency.perform_main_analysis(audio_directory = "audiofiles", \
                                                     aubioonset_command = "aubioonset", \
                                                     onset_method = "hfc", \
                                                     buffer_size = 64, \
                                                     hop_size = 64, \
                                                     silence_threshold = -54.0, \
                                                     onset_threshold = 9.31, \
                                                     minimum_inter_onset_interval_s = 0.02,
                                                     failsafe = True)

results_string = computeLatency.create_string(info, metrics, True, failsafe = True)
print(results_string)
