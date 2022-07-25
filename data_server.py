from signal import signal, SIGINT
from sys import exit
import time, os, json, math , cherrypy, cherrypy_cors



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
            print("data posted from survey at:", cherrypy.request.json['time'])
            save_data_to_file(cherrypy.request.json);
            return {'method': 'POST', 'payload': "data recieved"}
        return {'method': 'non-POST'}

        return {'method': 'non-POST'}
        print(data)
        return("accepted")

#-------------------------------------------------------------------------------------
#
#
#---------------------------------------------------------------
def save_data_to_file(data):
    global start_time
    fn = '../bounding_boxes/survey_bounding_boxes_' + str(data['UID']) + "_" + str(data['FID']) + "_" + str(data['time']) + '.txt'
    print(fn)
    f = open(fn, 'w+')
    # copy the data before saving it, since json.dump iterates over the data, 
    # to avoid issues if data is POSTed faster than it can write (unlikely)
    json.dump(data.copy(), f)
    f.close()

    pass

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
    
    cherrypy.quickstart(GazeDataController())
#-------------------------------------------------------------------------------------

