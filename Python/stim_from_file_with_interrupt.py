from controller import Controller
import time
import os
import sys
import msvcrt
import threading

############################################
# PARAMETERS TO CHANGE
stim_dir = "stim_files"
stim_file = "motion_stim_vertical.csv"
# select the desired time duration per row (col_ms)
row_duration_ms = 1000
##################################################

# Flag to signal program exit
should_exit = False

# connect to the controller FIRST
controller = Controller(port="COM9")
controller.connect()
time.sleep(1)
# select the desired time duration per row (col_ms)
controller.send_stimulus_from_csv_vertical(os.path.join(stim_dir,stim_file), col_ms=row_duration_ms)

def listen_for_input():
    global should_exit
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            # wait for Q to quit the program
            if key == 'q':
                controller.send("stop")
                controller.disconnect()
                print("Done")
                should_exit = True
            # wait for S to start the stimulus
            elif key == 's':
                controller.exec()

print("\n=== To start the stimulus, press:         s ===")
print("\n=== To quit/interrupt the program, press: q ===\n")
sys.stdout.flush()

# Start input listener in background thread (daemon=True so it won't block exit)
input_thread = threading.Thread(target=listen_for_input, daemon=True)
input_thread.start()

# Keep the main thread alive to listen for input
while not should_exit:
    time.sleep(0.1)


