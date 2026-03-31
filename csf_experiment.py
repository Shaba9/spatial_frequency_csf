
# Spatial Frequency Sensitivity Experiment (Contrast Sensitivity Function)
# Python / PsychoPy implementation
print("RUNNING THIS FILE:", __file__)

from psychopy import visual, core, event, data
import numpy as np
import csv
import os

# =====================
# Experiment Parameters
# =====================
spatial_freqs = [0.5, 1, 2, 4, 8]  # cycles per degree
contrasts = np.linspace(0.01, 0.5, 9)
trials_per_condition = 10

# Create output directory
os.makedirs('data', exist_ok=True)

# =====================
# Window Setup
# =====================
win = visual.Window(size=(1024, 768), units='deg', fullscr=False, color=0)

# =====================
# Stimuli
# =====================
fixation = visual.TextStim(win, text='+', height=0.5, color='white')

instruction_text = visual.TextStim(
    win,
    text='Two intervals will appear. One contains a striped pattern. Press LEFT if the pattern was first. Press RIGHT if the pattern was second. Press SPACE to begin.',
    wrapWidth=20,
    color='white'
)

# =====================
# Instructions Screen
# =====================
instruction_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# =====================
# Trial List
# =====================
trials = []
for sf in spatial_freqs:
    for c in contrasts:
        for _ in range(trials_per_condition):
            trials.append({'spatial_freq': sf, 'contrast': c})

np.random.shuffle(trials)

# =====================
# Data File
# =====================
data_file = open('data/results.csv', 'w', newline='')
writer = csv.writer(data_file)
writer.writerow(['spatial_freq', 'contrast', 'correct'])

# =====================
# Experiment Loop
# =====================
clock = core.Clock()

for trial in trials:
    sf = trial['spatial_freq']
    contrast = trial['contrast']

    grating = visual.GratingStim(
        win,
        tex='sin',
        mask='gauss',
        sf=sf,
        contrast=contrast,
        size=8
    )

    correct_interval = np.random.choice([0, 1])

    # First interval
    fixation.draw()
    win.flip()
    core.wait(0.5)
    if correct_interval == 0:
        grating.draw()
    win.flip()
    core.wait(0.5)

    win.flip()
    core.wait(0.3)

    # Second interval
    fixation.draw()
    win.flip()
    core.wait(0.5)
    if correct_interval == 1:
        grating.draw()
    win.flip()
    core.wait(0.5)

    win.flip()

    # Response
    keys = event.waitKeys(keyList=['left', 'right', 'escape'])
    if 'escape' in keys:
        break

    response = 0 if keys[0] == 'left' else 1
    correct = int(response == correct_interval)

    writer.writerow([sf, contrast, correct])

# =====================
# Cleanup
# =====================
data_file.close()
win.close()
core.quit()
