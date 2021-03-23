# /report
This folder contains reports on different iterations of the evaluation.
- `00 - vanilla/` is the original report on aubioonset with its 8 methods.
- `01 - Compressor/` is the report on the effects of soft dynamic range compression on the audio files.
- `02-CompressorHard(bad)/` is the report on the effects of severe dynamic range compression on the audio files, which proved to be particularly detrimental.
- `03-onlyNG/` is the report on the effects of a noise gate on the audio files.
- `04-mkl/` is a report comparing the default Modified Kullback–Leibler divergence method, with a version that has Adatpive Whitening disabled (The latter works really well on our problem).
- `05-complessive-MANUAL-study/` is the report that ties together the first study with 04 and more data is collected. from 01 to 05 the optimization was performed manually.
- `06-EA-optimized_and_comparison/` is the report that shows the performance of an automated optimizer applied to the problem and compares it with the best results obtained with manual optimization.
