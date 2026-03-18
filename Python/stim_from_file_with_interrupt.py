from controller import Controller
import time
import os
import sys
import msvcrt
import threading

############################################
# PARAMETERS TO CHANGE
# select the desired time duration per row (col_ms)
row_duration_ms = 1000
# default stim folder and file name (can be overridden by CLI)
stim_file = os.path.join("stim_files","motion_stim_vertical.csv")
##################################################
# If a command-line argument is provided, use it as the stim file.
# Accept either a plain filename, a path, or a filename with a leading dash
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.startswith("-") and not arg.startswith("--"):
        arg = arg.lstrip("-")
        arg = os.path.normpath(arg)  # Normalize path to handle different separators
    # if the argument looks like a path (contains a separator) or the file exists, use it directly
    if os.path.exists(arg):
        stim_file = arg
    else:
        print(f"Stimulus file not found: {arg}")
        sys.stdout.flush()
        sys.exit(1)


print(f"\nStimulus file: {stim_file}\n")
sys.stdout.flush()
# Flag to signal program exit
should_exit = False

# connect to the controller FIRST
try:
    controller = Controller()
    controller.connect()
    time.sleep(1)
    if os.path.exists(stim_file):
        # select the desired time duration per row (col_ms)
        controller.send_stimulus_from_csv_vertical(stim_file, col_ms=row_duration_ms)
    else:
        print(f"Stimulus file not found: {stim_file}")
        sys.stdout.flush()
        sys.exit(1)
except Exception as e:
    print(f"Error connecting/initializing controller:\n{e}")
    sys.stdout.flush()
    sys.exit(1)

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


