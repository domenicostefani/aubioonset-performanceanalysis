#!/usr/bin/env python3

#!/usr/bin/env python3

import computeLatency

info, metrics = computeLatency.perform_main_analysis(audio_directory = "audiofiles", \
                                                    aubioonset_command = "aubioonset", \
                                                    onset_method = "hfc", \
                                                    buffer_size = 64, \
                                                    hop_size = 64, \
                                                    silence_threshold = -51.8646742524295, \
                                                    onset_threshold = 1.4464687316737181, \
                                                    minimum_inter_onset_interval_s = 0.02,
                                                    save_results=False)

print(computeLatency.create_string(info,metrics,use_oldformat=False,do_copy = True,failsafe = True))