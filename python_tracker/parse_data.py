#!/usr/bin/env python

import json, os, re
from statistics import median
from screeninfo import get_monitors
#import matplotlib
import matplotlib.cm
m = get_monitors()[0]
print(str(m))


SELECTED_UIDS = [4]

def get_words(f1, f2):
    print(f1, f2)
    print("============================================================")

    try:    
        with open('../eye_data/eye_coordinates/' + f1, 'r') as eye_reader:
            eye_data = json.load(eye_reader)
        with open('../eye_data/bounding_boxes/' + f2, 'r')  as page_boxes_reader:
            page_data = json.load(page_boxes_reader)
    except Exception as e:
        print(e)
        return False
       
       
                
    i_data = eye_data['eye_data']
    p_data = page_data['data']
    
                
    words_dict = {}
    for div_data in p_data:
        for datum in div_data:
            box_word, *box = datum
            box = box[0]
            appearance = 0
            for key in words_dict:
                dict_word, dict_appearance = (list(key.split('_')) + [None]*2)[:2]
                # if a word on the list matches the one we're looking at now, 
                if box_word == dict_word:
                    appearance = int(dict_appearance) + 1
                    
            key = box_word + '_' + str(appearance)
            
            words_dict[key] = [0, [box['x'], box['y']], appearance]
            
    
    for key in i_data.keys():
        data = i_data[key]
        if data['left_pupil_validity'] and data['right_pupil_validity']:
        
            rx,ry = data['right_gaze_point_on_display_area']
            lx, ly = data['left_gaze_point_on_display_area']
            
            if rx and ry and lx and ly:
                x = m.width * ((rx + lx) / 2)
                y = m.height * ((ry + ly) / 2)
        
            for div_data in p_data:
                for datum in div_data:
                    
                
                    box_word, *box = datum
                    box = box[0]
                    
                    word_appearance = 0
                    if words_dict == {}:                            
                        new_appearance = box_word + '_' + str(word_appearance)
                        words_dict[new_appearance] = [0, [box['x'],box['y']], word_appearance]
                
                    # first check if the current coordinates are in the bounding box for this word
                    if (box['left'] < x < box['right']) and (box['top'] < y < box['bottom']):
#                                print(words_dict)              
                        # if this is the word at the current gaze point, then check if we've seen this word before 
                        # this loops through our list of seen words, extracting the name and number of this word's appearance on the screen
                        for key in words_dict:
                            dict_word, appearance = (list(key.split('_')) + [None]*2)[:2]
                            # if a word on the list matches the one we're looking at now, 
#                                    print(box_word, dict_word)
                            if box_word == dict_word:
                                # check if it's in the same spot, eg if the x coordinate of the current word == x coordiate of the word in the dict     
                                # if we have indeed seen this word at this spot before, 
                                
                                if words_dict[key][1][0] == box['x']:
                                    # increment the counter for how often we've looked at this particular word
                                    words_dict[key][0] += 1
                                    # and we're done here
                                    word_appearance = 0
                                    break
                                else:
                                    # if we have not, keep looking, but increment the counter for how many instances of this word we've seen so far
                                    word_appearance += 1
                        else:
                            new_appearance = box_word + '_' + str(word_appearance)
                            words_dict[new_appearance] = [1, [box['x'],box['y']], word_appearance]
                            # if we run through the whole words_dict without finding a match, add a new entry
                        break
                
   
                                                
                        		
                                
    total_gaze_count = 0
    color_array = []
    words = []
    
    gaze_range = {
        'gaze_min': float('inf'),
        'gaze_max': 0,
        'gaze_mean': 0,
        'gaze_median': 0,
    }
    
    for key in words_dict:
        gaze_count = words_dict[key][0]
        if gaze_count > gaze_range['gaze_max']:
            gaze_range['gaze_max'] = gaze_count
        elif gaze_count < gaze_range['gaze_min']:
            gaze_range['gaze_min'] = gaze_count
        total_gaze_count += gaze_count
        color_array.append(gaze_count)
        words.append(key.split('_')[0])
        print(key, words_dict[key][0])
        
    gaze_range['gaze_mean'] = total_gaze_count / len(words_dict)
    gaze_range['gaze_median'] = median(color_array)
    color_array = [(e / total_gaze_count) for e in color_array]
    
    
    print(total_gaze_count)
    
    print(color_array)
    
    colorize(words, color_array, gaze_range)

    
    
    
def colorize(words, color_array, gaze_range):
    # words is a list of words
    # color_array is an array of numbers between 0 and 1 of length equal to words
    #cmap = matplotlib.cm.get_cmap('viridis')
    cmap = matplotlib.cm.get_cmap('Reds')
    template = '<span class="barcode" style="color: black; background-color: {}">{}</span>'
    colored_string = '<div style="padding-top: 50px; word-wrap:anywhere">'
    for word, color in zip(words, color_array):
        color = matplotlib.colors.rgb2hex(cmap(color)[:3])
        colored_string += template.format(color, '&nbsp' + word + '&nbsp')
        
    s = colored_string + "<br><br>  Min: " + str(gaze_range['gaze_min']) + ",  Max: " + str(gaze_range['gaze_max']) + ",  Mean: "  + str(gaze_range['gaze_mean']) + ",  Median: " + str(gaze_range['gaze_median']) + "</div>"
    

    with open('colorize.html', 'a') as f:
        f.write(s)
        
        
        
with open('colorize.html', 'w') as f:
    pass
time = 0    

eye_files = sorted(os.listdir("../eye_data/eye_coordinates"))
box_files = sorted(os.listdir("../eye_data/bounding_boxes"))
box_fn_dict = {}

i = 0
for box_fn in box_files:
#    eye_fn = eye_files[0]
    b_uid, b_fid, b_time, b_ext = re.split(r'_|\.', box_fn)
    if b_uid not in box_fn_dict:
        box_fn_dict[b_uid] = {}
        i = 0
    
    box_fn_dict[b_uid][i]= box_fn
    i += 1
    
#print(eye_fn_dict)
    
for eye_fn in eye_files:
    print("===================================================================================")
    time = 0
    nearest_box = ""
    i_uid, i_fid, i_time, i_ext = re.split(r'_|\.', eye_fn)
    for key in sorted(box_fn_dict[i_uid]):
        box_fn = box_fn_dict[i_uid][key]
        b_uid, b_fid, b_time, b_ext = re.split(r'_|\.', box_fn)
        if int(i_uid) in SELECTED_UIDS:

            if i_uid == b_uid and i_fid == b_fid: 
                # eyetracking.py should be saving bounding boxes at the same time or just before the eye data, but never after 
                if int(i_time) >= int(b_time) > int(time):
                    time = b_time
                    nearest_box_fn = box_fn
                    
                if b_time > i_time:
                    print("===================================================================================")
                    get_words(eye_fn, nearest_box_fn)
                    time = 0 
                    break
            print("...")
    if int(time) > 0: 
        print("===================================================================================")
        get_words(eye_fn, nearest_box_fn)
    if int(i_uid) > 4:
        break       
#    if time != 0 and box_f:
                
                

