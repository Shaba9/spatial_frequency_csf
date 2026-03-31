
# Spatial Frequency Sensitivity Experiment (Contrast Sensitivity Function)
# Python / PsychoPy implementation

from psychopy import visual, core, event, data, monitors
import numpy as np
import csv
import os

# =====================
# Experiment Parameters
# =====================
mon = monitors.Monitor(
    name='testMonitor',
    width=53.0,        # physical screen width in cm (CHANGE THIS)
    distance=57.0      # viewing distance in cm (CHANGE THIS)
)
spatial_freqs = [1, 2, 4]          # cycles per degree
contrasts = [0.05, 0.1, 0.2, 0.4] # contrast levels
trials_per_condition = 3

# Create output directory
os.makedirs("data", exist_ok=True)

# =====================
# Window
# =====================
win = visual.Window(
    size=(1024, 768),
    monitor=mon,
    units='deg',
    fullscr=False,
    color=0
)
fixation = visual.TextStim(win, "+", color="white", height=0.5)
progress_text = visual.TextStim(win, "", pos=(0, -6), height=0.6)

instructions = visual.TextStim(
    win,
    text="Two intervals will appear.\n"
         "One contains faint stripes.\n\n"
         "LEFT = first interval\n"
         "RIGHT = second interval\n\n"
         "Press SPACE to begin.",
    wrapWidth=25,
    color="white"
)

# =====================
# Instructions
# =====================
instructions.draw()
win.flip()
event.waitKeys(keyList=["space"])

# =====================
# Trial List
# =====================
trials = []
for sf in spatial_freqs:
    for c in contrasts:
        for _ in range(trials_per_condition):
            trials.append({"sf": sf, "contrast": c})

np.random.shuffle(trials)

# =====================
# Data File
# =====================
data_file = open("data/results.csv", "w", newline="")
writer = csv.writer(data_file)
writer.writerow(["spatial_freq", "contrast", "correct"])

total_trials = len(trials)

# =====================
# Experiment Loop
# =====================
for i, trial in enumerate(trials):
    sf = trial["sf"]
    contrast = trial["contrast"]

    grating = visual.GratingStim(
        win,
        tex="sin",
        sf=sf,
        contrast=contrast,
        size=8,
        mask="gauss"
    )

    correct_interval = np.random.choice([0, 1])

    # Fixation
    fixation.draw()
    progress_text.text = f"Trial {i+1} / {total_trials}"
    progress_text.draw()
    win.flip()
    core.wait(0.4)

    # Interval 1
    if correct_interval == 0:
        grating.draw()
    win.flip()
    core.wait(0.4)

    win.flip()
    core.wait(0.2)

    # Interval 2
    if correct_interval == 1:
        grating.draw()
    win.flip()
    core.wait(0.4)

    win.flip()

    # Response
    keys = event.waitKeys(keyList=["left", "right", "escape"])
    if "escape" in keys:
        break

    response = 0 if keys[0] == "left" else 1
    correct = int(response == correct_interval)

    writer.writerow([sf, contrast, correct])

# =====================
# Ending Screen
# =====================
end_text = visual.TextStim(
    win,
    text="Experiment complete.\n\nThank you!",
    height=1,
    color="white"
)
end_text.draw()
win.flip()
core.wait(3)

data_file.close()
win.close()
core.quit()