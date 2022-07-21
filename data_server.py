from signal import signal, SIGINT
from sys import exit
import tobii_research as tr
import time, os, json, math , cherrypy
import pyautogui as pag
from pynput import mouse
from screeninfo import get_monitors
from PIL import Image
screen_coords = {}
code_coords = {} 
button_coords = {}

eye_data = {}

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
    global eye_data
    lvalid = gaze_data['left_gaze_point_validity']
    rvalid = gaze_data['right_gaze_point_validity']  
    
    # only save data if deemed valid by the eyetracker
    if lvalid and rvalid and ready:
        eye_data = {
            'left_gaze_point' : gaze_data['left_gaze_point_on_display_area'],
            'right_gaze_point' : gaze_data['right_gaze_point_on_display_area'],
            'system_time_stamp' : gaze_data['system_time_stamp']
        }

        gaze_data['left_gaze_point'][0] = gaze_data['left_gaze_point'][0] * screen_coords['xmax'] 
        gaze_data['left_gaze_point'][1] = gaze_data['left_gaze_point'][1] * screen_coords['ymax'] 
        gaze_data['right_gaze_point'][0] = gaze_data['right_gaze_point'][0] * screen_coords['xmax'] 
        gaze_data['right_gaze_point'][1] = gaze_data['right_gaze_point'][1] * screen_coords['ymax'] 

        

        if(in_box(code_coords, [gaze_data['left_gaze_point'][0] ,gaze_data['left_gaze_point'][1]])):
            eye_data = json.dumps(s)
    
        
    

# Get points of interest, the submit button, the screen coodinates, and the area of the code box. 
def get_POI():     
    if get_screen_with_button() and get_code():
        return True
    else:
        return False
        

def get_screen_with_button():
    for m in get_monitors():
        # since the button is always going to be in the bottom right corner, 
        # assume we only have to look in that corner of the current screen, rather than all of it
        button = pag.locateOnScreen('submit.png', region=((m.x + m.width) * 0.8, (m.y + m.height) * 0.8, (m.x + m.width), (m.y + m.height)))
        #if we find the submit button, this is also the screen we want to watch in, so save the coordinates for this screen too 
        if button:
            # saves the coordinates of the submit button 
            x, y, w, h = button
            button_coords['xmin'] = x
            button_coords['xmax'] = x + w
            button_coords['ymin'] = y
            button_coords['ymax'] = y + h
            print("Submit Button:\t", button_coords)
             
            # saves the local screen coordinates
            screen_coords['xmin'] = m.x
            screen_coords['xmax'] = m.x + m.width
            screen_coords['ymin'] = m.y
            screen_coords['ymax'] = m.y + m.height
            print("Screen:\t\t", screen_coords)
            button = None
            return True
    print("Submit button not found: Do you have the survey website visible?")
    return False
        
def get_code(): 
    print("Finding code block...")
#    try:
    x0, y0, *data = pag.locateOnScreen('upper_left.png', region=(screen_coords['xmin'], screen_coords['ymin'], screen_coords['xmax'] * 0.5, screen_coords['ymax'] * 0.5 ))
    x, y, w, h = pag.locateOnScreen('bottom_right.png', region=(screen_coords['xmin'], screen_coords['ymin'], screen_coords['xmax'] * 0.5, screen_coords['ymax'] * 0.5 ))
    code_coords['xmin'] = x0
    code_coords['ymin'] = y0
    code_coords['xmax'] = x + w
    code_coords['ymax'] = y + h
    print("Code Block:\t", code_coords)
    
    
    
    return True
#    except:
#        print("Code box coordinates not found: is the code box visible?")
#        return False
    
def in_box(box_coordinates, point):
    if (box_coordinates['xmin'] <= point[0] <= box_coordinates['xmax']) and (box_coordinates['ymin'] <= point[1] <= box_coordinates['ymax']):
        return True
    else:
        return False
    
    
#Mouse listener, detects when submit button is pressed


def on_click(x, y, button, pressed):
    global eye_data
    if(pressed):
    
        if len(code_coords) == 0:
            if get_POI(): 
                ready = True

def init_mouse():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    
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
# Runs a basic webserver that returns the current value of eye_data 
# when receiving a GET request. 
#---------------------------------------------------------------
class GazeDataController(object):
    @cherrypy.expose
    def index(self):
        return eye_data

#-------------------------------------------------------------------------------------
# Sets up the data feed from the eyetracker, which gets the gaze data and saves it to global variable gaze_data
# Also initializes the handler for SIGINT, then runs the webserver
#---------------------------------------------------------------
def start_service():

    try:
        ready = get_POI()
    except: 
        print("Points of interest not found, waiting until next click to retry")
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
# Runs the start_service function on file run
#---------------------------------------------------------------
if __name__ == '__main__':
    start_service()
#-------------------------------------------------------------------------------------

