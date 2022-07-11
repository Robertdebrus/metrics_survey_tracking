from signal import signal, SIGINT
from sys import exit
import tobii_research as tr
import time, os, json, math 
import cherrypy


debug = {
    'save_data':True,
    'eyetracker_info':True
}

# Get the list of all connected eyetrackers 
found_eyetrackers = tr.find_all_eyetrackers()
# We're using the first one, since it's unlikely we'll have more than one
et = found_eyetrackers[0]

#Some data about the chosen eyetracker
if debug['eyetracker_info'] :
    print("Address: " + et.address)
    print("Model: " + et.model)
    print("Name: " + et.device_name)
    print("Serial Number: " + et.serial_number)


#-------------------------------------------------------------------------------------
# callback function called when receiving data from the eyetracker. 
# takes the data from the left and right eyes, 
#---------------------------------------------------------------

def gaze_data_callback(gaze_data):
    
    lvalid = gaze_data['left_gaze_point_validity']
    rvalid = gaze_data['right_gaze_point_validity']  
    
    # only save data if deemed valid by the eyetracker
    if lvalid and rvalid:
        s = {
            'left_gaze_point' : gaze_data['left_gaze_point_on_display_area'],
            'right_gaze_point' : gaze_data['right_gaze_point_on_display_area'],
            'system_time_stamp' : gaze_data['system_time_stamp']
        }
        global eye_data 
        eye_data = json.dumps(s)
    
        
    
    # writes all data to gaze_data.txt, for reference
    if debug['save_data']:
        append_to_file(gaze_data, gaze_data.txt)
    
#-------------------------------------------------------------------------------------
# cleans up before quitting when recieving a ctrl-c or sigint
#---------------------------------------------------------------
def handler(signal_received, frame):
    # unsubscribe from the eyetracker data before exiting
    print("SIGINT or CTRL-C detected, unsubscribing from eyetracker")
    et.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    print("Unsubscription successful. Exiting.")
    exit(0)

#-------------------------------------------------------------------------------------
# Sets up the data feed from the eyetracker, which gets the gaze data and saves it to global variable gaze_data
# Also initializes the handler for SIGINT, then runs the webserver
#---------------------------------------------------------------
def start_service():
    # subscribe to eyetracker data feed, gaze_data_callback is the callback function,
    # receives the data as a dictionary
    print("Subscribing to eyetracker data...")
    et.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    print("Success!")
    # handler to clean up before quitting from sigint or ctrl-c
    signal(SIGINT, handler)
    
    
    # start the webserver 
    cherrypy.quickstart(GazeDataController())

#-------------------------------------------------------------------------------------
# Functions used to write and read from files, *** unused *** 
#---------------------------------------------------------------

# Accepts a filename are returns the entire contents of the file
def read_whole_file(fname):
    f = open(fname, 'r')
    return f.read()
    
# Accepts data and a filename, and writes the data to the file, erasing existing data
def write_over_file(data, fname):
    f = open(fname, 'w')
    print(data, file=f)
    f.close()
    
# Accepts data and a filename, and writes the data to the file, keeping existing data
def append_to_file(data, fname):
    f = open(fname, 'a')
    print(data, file=f)
    f.close()
    
#-------------------------------------------------------------------------------------
        
        
        
#-------------------------------------------------------------------------------------
# Runs a basic webserver that returns the current value of eye_data 
# when receiving a GET request. 
#---------------------------------------------------------------
class GazeDataController(object):
    @cherrypy.expose
    def index(self):
        return eye_data

#-------------------------------------------------------------------------------------
# Runs the start_service function on file run
#---------------------------------------------------------------
if __name__ == '__main__':
    start_service()
#-------------------------------------------------------------------------------------

