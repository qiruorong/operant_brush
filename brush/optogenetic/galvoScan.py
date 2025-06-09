import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import threading
import time
from scipy.signal import square

settings = {
    'xMirror_output': 'PXI1Slot2/ao0',
    'yMirror_output': 'PXI1Slot2/ao1',
    'laser_output': '/PXI1Slot2/port0/line0',
    # 'sync': '/PXI1Slot2/port0/line1',  # output to trigger NP recording

    'Fs': 30000,  # in samples/s
    'xV': 7.8,  # in Volts. Fixed voltage for mirror's x-axis
    'yV': 3.2,  # in Volts. Fixed voltage for mirror's y-axis

    'laser_duration': 0.0003,  # seconds
    'trial_duration': 0.5,  # seconds
    'rest_duration': 5,  # seconds
    'trial_buffer': 1,  # seconds
    'trial_num': 200,  # number of trains to pass (100 takes ~10 minutes; default = 50)
}

# Calculate trial_duration
trial_duration = (2 * settings['trial_buffer']) + (
        settings['trial_num'] * (settings['trial_duration'] + settings['rest_duration'])) - settings['rest_duration']
minutes = round(trial_duration / 60, 2)
print("This experiment will take {} minutes to complete...".format(minutes))

# Locations and probability distribution
foreS1_xV = settings['xV'] - 0.2 # modify based on actual location
hindS1_xV = settings['xV'] + 0.2 # modify based on actual location
PBC_xV = settings['xV'] + 0.5 # modify based on actual location
dentalCement_xV = settings['xV'] + 0.5 # modify based on actual location
foreS1_yV = settings['yV'] - 0.5 # modify based on actual location
hindS1_yV = settings['yV'] + 0.5 # modify based on actual location
PBC_yV = settings['xV'] + 0.5 # modify based on actual location
dentalCement_yV = settings['xV'] + 0.5  # modify based on actual location
x_out_values = np.arange(foreS1_xV, hindS1_xV, PBC_xV, dentalCement_xV, settings['stepV'])
y_out_values = np.arange(foreS1_yV, hindS1_yV, PBC_yV, dentalCement_yV, settings['stepV'])

prob_foreS1 = 0.10
prob_hindS1 = 0.10
prob_PBC = 0.10
prob_dentalCement = 0.70

# ao_out array with coordinates based on probabilities
numSamples = int(settings['Fs'] * trial_durationb
                 )ao_out = np.zeros((2, numSamples))

# Randomize assignment of laser
laser_locations = np.random.choice(['foreS1', 'hindS1', 'PBC', 'dentalCement'],
                                    size=settings['trial_num'],
                                    p=[prob_foreS1, prob_hindS1, prob_PBC, prob_dentalCement])

for i, location in enumerate(laser_locations):
    start_index = int((settings['trial_buffer'] + i * (settings['trial_duration'] + settings['rest_duration'])) * settings['Fs'])
    end_index = int(start_index + (settings['trial_duration'] * settings['Fs']))

    # Set coordinates based on the selected location
    if location == 'foreS1':
        ao_out[0, start_index:end_index] = foreS1[0]
        ao_out[1, start_index:end_index] = foreS1[1]
    elif location == 'hindS1':
        ao_out[0, start_index:end_index] = hindS1[0]
        ao_out[1, start_index:end_index] = hindS1[1]
    elif location == 'PBC':
        ao_out[0, start_index:end_index] = PBC[0]
        ao_out[1, start_index:end_index] = PBC[1]
    elif location == 'dentalCement':
        ao_out[0, start_index:end_index] = dentalCement[0]
        ao_out[1, start_index:end_index] = dentalCement[1]

# Rest of the code

def setupTasks(settings):
    numSamples = int(settings['Fs'] * trial_duration)

    ao_task = nidaqmx.Task()
    ao_task.ao_channels.add_ao_voltage_chan(settings['xMirror_output'], name_to_assign_to_channel='x_out')
    ao_task.ao_channels.add_ao_voltage_chan(settings['yMirror_output'], name_to_assign_to_channel='y_out')
    ao_task.timing.cfg_samp_clk_timing(settings['Fs'], samps_per_chan=numSamples)

    do_task = nidaqmx.Task()
    do_task.do_channels.add_do_chan(settings['laser_output'], name_to_assign_to_lines='laser')
    # do_task.do_channels.add_do_chan(settings['sync'], name_to_assign_to_lines='sync')
    do_task.timing.cfg_samp_clk_timing(settings['Fs'], samps_per_chan=numSamples)

    return ao_task, do_task

def runTasks(ao_task, do_task, settings, laser_locations):
    # initialize zeroed-out arrays
    numSamples = int(settings['Fs'] * trial_duration)
    ao_out = np.zeros((2, numSamples))
    do_out = np.zeros((2, numSamples), dtype=bool)

    # Fill ao_out with fixed mirror coordinates
    ao_out[0] = np.full(1, settings["xV"])
    ao_out[1] = np.full(1, settings["yV"])

    # Assign trains of laser pulses to the specified location
    train_onsets = np.arange((settings['trial_buffer']), (trial_duration),
                             ((settings['trial_duration'] + settings['rest_duration']))) * settings['Fs']
    laser_onsets = np.arange(0, settings['train_duration'], 1 / settings['Fs'])
    laser_onsets = (laser_onsets * settings['Fs']).astype(int)

    for train_onset in train_onsets:
        for laser_onset in laser_onsets:
            start_index = int(train_onset + laser_onset)
            end_index = int(start_index + (settings['laser_duration'] * settings['Fs']))
            do_out[0, start_index:end_index] = True

    # Turn NP sync signal on during trial
    # do_out[1, 1:(numSamples - 1)] = True

    # Write daq outputs onto the device
    do_task.write(do_out, timeout=trial_duration + 10)
    ao_task.write(ao_out, timeout=trial_duration + 10)

    # Starting tasks (make sure do_task is started last -- it triggers the others)
    ao_task.start()
    do_task.start()
    do_task.wait_until_done(timeout=trial_duration + 10)

    # Adding data to the outputs
    ao_data = ao_out
    do_data = do_out

    # Stopping tasks
    do_task.stop()
    ao_task.stop()

    do_task.close()
    ao_task.close()
    return ao_data, do_data


def countdown_timer(duration):
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        remaining_time = end_time - time.time()
        print("\rRemaining Time: {:.2f} minutes".format(remaining_time / 60), end="", flush=True)
        time.sleep(5)  # Update every 5 seconds


# Run a countdown timer for [trial_duration] seconds
timer_thread = threading
