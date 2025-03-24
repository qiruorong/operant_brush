import nidaqmx
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from numpy import matlib
import threading
import time
from datetime import datetime
import os


settings = {
            'sync' : '/PXI1Slot2/port0/line1',   
            'trial_start' : 'PXI1Slot2/port0/line3', 
            'laser' : 'PXI1Slot2/port0/line0', 
            'x_out': 'PXI1Slot2/ao0',      
            'y_out': 'PXI1Slot2/ao1',
            #'trigger_output' :  '/PXI1Slot2/PFI1',
            #'trigger_input': '/PXI1Slot2/port0/line2'

            'Fs':30000, # Hz
            'laser_Fs': 40, # Hz
            'xV': 0,
            'yV': 0,
            'num_spots': 7,
            'trial_repeat': 1,
            'opto_onset_time': 0.9, # seconds
            'opto_duration': 1.2, # seconds
            #'galvo_onset_time': 0.4, # seconds
            #'galvo_duration': 0.7, # seconds
            'duty': 0.02, # seconds
            'trial_duration': 7, # seconds
            'intersweep_duration': 1, # seconds
            }

# laser_duration, pulse_duration, 
# session = 30 trials, 1 trial = 1 pulse on each spot
# location of each spot
# 1 pulse needed: laser_duration, laser_frequency(=Fs?)
# 1 trial needed: trial_duration(2*buffer + pulse_duration*num_spots + 6*rest_duration)
# 1 session needed: settings['session_duration'](30*trial duration)

# calculate trial_duration
settings['session_duration'] = (settings['num_spots'] * settings['trial_repeat'] * (settings['trial_duration'] + settings['intersweep_duration']))
settings['numSamples'] = int(settings['session_duration'] * settings['Fs'])
minutes = round(settings['session_duration']/60, 2)
print("This experiment will take {} minutes to complete...".format(minutes))


def setupTasks(settings):

    ao_task = nidaqmx.Task()
    ao_task.ao_channels.add_ao_voltage_chan(settings['x_out'], name_to_assign_to_channel='x_out')
    ao_task.ao_channels.add_ao_voltage_chan(settings['y_out'], name_to_assign_to_channel='y_out')
    ao_task.timing.cfg_samp_clk_timing(settings['Fs'], samps_per_chan=settings['numSamples'])

    do_task = nidaqmx.Task()
    do_task.do_channels.add_do_chan(settings['laser'], name_to_assign_to_lines='laser')
    do_task.do_channels.add_do_chan(settings['sync'], name_to_assign_to_lines='sync')
    #do_task.do_channels.add_do_chan(settings['sync'], name_to_assign_to_lines='sync')
    do_task.timing.cfg_samp_clk_timing(settings['Fs'], samps_per_chan=settings['numSamples'])

    return (ao_task, do_task)


def runTasks(ao_task, do_task, settings):

    session_duration = (settings['num_spots'] * settings['trial_repeat'] * (settings['trial_duration'] + settings['intersweep_duration']))
    # coordinate array in full session
    x_coord = np.full(settings['num_spots'], settings['xV'])
    settings['x_coord_array'] = np.matlib.repmat(x_coord,1,settings['trial_repeat']).reshape(-1)
    np.random.shuffle(settings['x_coord_array'])
    x_coord_session = np.matlib.repmat(settings['x_coord_array'], settings['Fs'] * (settings['trial_duration'] + settings['intersweep_duration']), 1).T.reshape(-1)

    y_coord = settings['yV'] - (0.04 * np.arange(settings['num_spots']))
    settings['y_coord_array'] = np.matlib.repmat(y_coord,1,settings['trial_repeat']).reshape(-1)
    np.random.shuffle(settings['y_coord_array'])
    y_coord_session = np.matlib.repmat(settings['y_coord_array'], settings['Fs'] * (settings['trial_duration'] + settings['intersweep_duration']), 1).T.reshape(-1)


    # opto sweep in full session
    opto_onset_time_insample = int(settings['opto_onset_time'] * settings['Fs'])
    opto_duration_insample = int(settings['opto_duration'] * settings['Fs'])
    opto_offset_time_insample = int((settings['trial_duration'] - (settings['opto_onset_time'] + settings['opto_duration']))* settings['Fs'])
    intersweep_duration_insample = int(settings['intersweep_duration'] * settings['Fs'])

    opto_stim = np.arange(0, settings['opto_duration'], 1/settings['Fs'])
    opto_stim_amp = (signal.square( 2 * np.pi * opto_stim * settings['Fs'], duty = settings['duty']) + 1) / 2
    opto_sweep = np.concatenate([np.zeros(opto_onset_time_insample), opto_stim_amp, np.zeros(opto_offset_time_insample), np.zeros(intersweep_duration_insample)])
    opto_sweep_trial = np.tile(opto_sweep, settings['num_spots'])
    opto_sweep_session = np.tile(opto_sweep_trial, settings['trial_repeat'])

    # trial trigger signal
    trial = int(settings['trial_duration'] * settings['Fs'])
    sync = np.zeros(trial, dtype=bool)
    sync[1:-1] = True
    sync_trial = np.concatenate([sync, np.zeros(int(settings['Fs'] * settings['intersweep_duration']))])
    sync_session = np.tile(sync_trial, settings['num_spots'] * settings['trial_repeat'])

    # npx sync channel
    #session = int(settings['session_duration'] * settings['Fs'])
    #sync = np.zeros(session, dtype=bool)
    #sync[1:-1] = True

    # put into nidaq output
    ao_out = np.zeros((2, settings['numSamples']))
    do_out = np.zeros((2, int(settings['Fs'] * session_duration)), dtype=bool)
    # fill up ao_out and do_out
    ao_out[0] = x_coord_session
    ao_out[1] = y_coord_session
    do_out[0] = opto_sweep_session
    do_out[1] = sync_session
    #do_out[2] = sync


    ## writing daq outputs onto device
    do_task.write(do_out, timeout = settings['session_duration'] + 10)
    ao_task.write(ao_out, timeout = settings['session_duration'] + 10)

    ## starting tasks (make sure do_task is started last -- it triggers the others)
    ao_task.start()
    do_task.start()
    do_task.wait_until_done(timeout = settings['session_duration'] + 10)

    ## adding data to the outputs
    ao_data = ao_out
    do_data = do_out

    ## stopping tasks
    do_task.stop()
    ao_task.stop()
    do_task.close()
    ao_task.close()

    return(ao_data,do_data)


def countdown_timer(duration):
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        remaining_time = end_time - time.time()
        print("\rRemaining Time: {:.2f} minutes".format(remaining_time/60), end="", flush=True)
        time.sleep(5)  # Update every 5 seconds


# setup saving directory
settings['saving_dir'] = input("Please identify your saving directory (e.g. D:\\Ruorong_Qi\\test\\): \n")
# Check if the directory exists
if os.path.isdir(settings['saving_dir']):
    print(f"Saving directory exists. The data will be saved to the following directory: \n'{settings['saving_dir']}'.")
else:
    raise FileNotFoundError(f"The directory '{settings['saving_dir']}' does not exist.")

# run countdown timer for [trial_duration] seconds
timer_thread = threading.Thread(target=countdown_timer, args=(settings['session_duration'],))
timer_thread.start()


# save the settings for recording
current_date = datetime.now()
date = current_date.strftime('%Y-%m-%d_%H%M%S')
settings['file_name'] = "Mapping_{}_settings.npy".format(date)
full_path = os.path.join(settings['saving_dir'], settings['file_name'])
np.save(full_path, settings)
print(f"\nSettings saved to '{full_path}'")


# perform recording
ao_task, do_task = setupTasks(settings)
ao_data, do_data, = runTasks(ao_task, do_task, settings)

settings['file_name'] = "Mapping_{}_ao_input.npy".format(date)
full_path = os.path.join(settings['saving_dir'], settings['file_name'])
np.save(full_path, ao_data)
settings['file_name'] = "Mapping_{}_do_input.npy".format(date)
full_path = os.path.join(settings['saving_dir'], settings['file_name'])
np.save(full_path, do_data)
print(f"Coordinate and Optogenetic information saved to '{full_path}'")

print("\nTrial Complete.")

# Wait for the timer thread to complete before exiting the program
timer_thread.join()
