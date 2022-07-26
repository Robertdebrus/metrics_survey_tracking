from signal import signal, SIGINT
from sys import exit
import tobii_research as tr
import time, os, json, math, copy
import cherrypy, cherrypy_cors
from copy import deepcopy
import pyautogui as pag
from pynput import mouse
from screeninfo import get_monitors
from PIL import Image
import tesserocr, subprocess, webbrowser


api = tesserocr.PyTessBaseAPI()
screen_coords = {}
code_coords = {} 
button_coords = {}
screenHistory = {}
eye_data = {}
UID = -1
FID = -1
saving_data = False
boxes_expired = True
start_time = str(round(time.time())) 
ready = False
"""
Screen Resolution: 1920x1080 (16:9)
Monitor Size: 22 inches 



"""



# Get the list of all connected eyetrackers 
found_eyetrackers = tr.find_all_eyetrackers()
# We're using the first one, since it's unlikely we'll have more than one
et = found_eyetrackers[0]


#Some data about the chosen eyetracker
print("Address: " + et.address)
print("Model: " + et.model)
print("Name: " + et.device_name)
print("Serial Number: " + et.serial_number)

eye_data = {};

#-------------------------------------------------------------------------------------
# callback function called when receiving data from the eyetracker. 
# takes the data from the left and right eyes, 
#---------------------------------------------------------------

def gaze_data_callback(gaze_data):
    
    global eye_data
    
    if not saving_data:
        t = gaze_data['system_time_stamp']
        eye_data[t] = gaze_data

            
         
             
#Mouse listener, detects when submit button is pressed


def on_click(x, y, button, pressed):
    global eye_data, start_time
    if(pressed and button_coords and not saving_data):
    
        point = [x ,y] 
        if(in_box(button_coords, point) ):
            print("Submit button clicked! Saving Data...")
            save_data_to_file({
                'eye_data' : eye_data, 
                'time' : start_time, 
                'UID' : UID,
                'FID' : FID,
            }, 'eye_coordinates')
            save_data_to_file(box_data, 'bounding_boxes')
#            save_data_to_file(cherrypy.request.json, 'bounding_boxes');
            global boxes_expired
            boxes_expired = True
            start_time = str(round(time.time()))
            
#def save_data_to_file(data):
#    global start_time
#    fn = '../eye_coordinates/survey_tracking_' + start_time + '.txt'
#    print(fn)
#    f = open(fn, 'w+')
#    # copy the data before saving it, since json.dump iterates over the data, 
#    # which has issues when the eyetracker adds to the data while iterating 
#    json.dump(data.copy(), f)
#    f.close()




# Get points of interest, the submit button, the screen coodinates, and the area of the code box. 
def get_POI():
    global start_time
    
    start_time = str(round(time.time())) 
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
    x, y, w, h = pag.locateOnScreen('bottom_right.png', region=(screen_coords['xmin'] * 0.5, screen_coords['ymin'] * 0.5, screen_coords['xmax'], screen_coords['ymax'] ))
    code_coords['xmin'] = x0
    code_coords['ymin'] = y0
    code_coords['xmax'] = x + w
    code_coords['ymax'] = y + h
    print("Code Block:\t", code_coords)
    
    
    
    return True
    
def in_box(box_coordinates, point):
    if (box_coordinates['xmin'] <= point[0] <= box_coordinates['xmax']) and (box_coordinates['ymin'] <= point[1] <= box_coordinates['ymax']):
        return True
    else:
        return False
    


def init_mouse():
    listener = mouse.Listener(on_click=on_click)
    listener.start()

#-------------------------------------------------------------------------------------
# Runs a basic webserver that returns the current value of eye_data 
# when receiving a GET request. 
#---------------------------------------------------------------
class GazeDataController(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()  # turn HTTP payload into an object; also checking the Content-Type header
    @cherrypy.tools.json_out()  # turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
    def elementBoxes(self):
        if cherrypy.request.method == 'OPTIONS':
            # This is a request that browser sends in CORS prior to
            # sending a real request.

            # Set up extra headers for a pre-flight OPTIONS request.
            cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

        if cherrypy.request.method == 'POST':
            global boxes_expired
            if boxes_expired:
                #print("data posted from survey at:", cherrypy.request.json.keys())
                global UID
                UID = cherrypy.request.json['UID']
                global FID
                FID = cherrypy.request.json['FID']
                global box_data
                box_data = cherrypy.request.json
#                save_data_to_file(cherrypy.request.json, 'bounding_boxes');
                boxes_expired = False 
            return {'method': 'POST', 'payload': ready}
        return {'method': 'non-POST'}

        return {'method': 'non-POST'}
        print(data)
        return("accepted")

#-------------------------------------------------------------------------------------
#
#
#---------------------------------------------------------------
def save_data_to_file(data, location):
    fn = '../' + location + '/' + str(UID) + "_" + str(FID) + "_" + str(data['time']) + '.txt'
    print(fn)
    saving_data = True
    with open(fn, 'w+') as f
        # copy the data before saving it, since json.dump iterates over the data, 
        # to avoid issues if data is POSTed faster than it can write (unlikely)
        global saving_data
        json.dump(copy.copy(data), f)
        saving_data = False

    
    
#-------------------------------------------------------------------------------------
# cleans up before quitting when recieving a ctrl-c or sigint
#---------------------------------------------------------------
def handler(signal_received, frame):
    # unsubscribe from the eyetracker data before exiting
    mouse.Listener.stop
    print("\nSIGINT or CTRL-C detected, unsubscribing from eyetracker")
    et.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
#    api.End()
    print("Unsubscription successful. Exiting.")
    exit(0)

#-------------------------------------------------------------------------------------
# Sets up the data feed from the eyetracker, which gets the gaze data and saves it to global variable gaze_data
# Also initializes the handler for SIGINT, then runs the webserver
#---------------------------------------------------------------
def start_service():
    global ready


    
    # Run get_POI to get the location of important points, such as the submit button, 
    # the code block, and the screen size, then  subscribe to eyetracker data feed,
    # gaze_data_callback is the callback function, the data is send as a dictionary
    # then loop infinitely until exited through CTRL-C
#    try:

    survey_page = subprocess.Popen(
        ['rails', 's']
    )
    while not ready:
        ready = get_POI()
    print("Initializing Eyetracker...")
    et.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    print("Success! Eyetracking enabled on Java Survey at", time.strftime("%H:%M:%S", time.localtime()))

    
    # set up handler to clean up before quitting from sigint or ctrl-c
    signal(SIGINT, handler)

    init_mouse()
    
    cherrypy.quickstart(GazeDataController())

#    except: 
#        print("Error: Survey not found ")
#   
        
    
    

#-------------------------------------------------------------------------------------
# Runs the start_service function on file run
#---------------------------------------------------------------
if __name__ == '__main__':
    cherrypy_cors.install()
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 3333,
        'cors.expose.on': True,
    })
    
    start_service()
#-------------------------------------------------------------------------------------

