import json, os, re
from screeninfo import get_monitors

m = get_monitors()[1]
print(str(m))




def get_words(f1, f2):
    print(f1, f2)
    words_dict = {}
    
    with open('../eye_coordinates/' + f1, 'r') as eye_reader:
        with open('../bounding_boxes/' + f2, 'r') as page_boxes_reader:
            eye_data = json.load(eye_reader)
            page_data = json.load(page_boxes_reader)
            #print(eye_data)
    i_data = eye_data['eye_data']
    p_data = page_data['data']
    for key in i_data.keys():
        data = i_data[key]
        if data['left_pupil_validity'] and data['right_pupil_validity']:
            x = m.width * data['right_gaze_point_on_display_area'][0]#((data['right_gaze_point_on_display_area'][0] + data['left_gaze_point_on_display_area'][0]) / 2) 
            y = m.height * data['right_gaze_point_on_display_area'][1]#((data['right_gaze_point_on_display_area'][1] + data['left_gaze_point_on_display_area'][1]) / 2)
            for div_data in p_data:
                for datum in div_data:
                    word, *box = datum
                    box = box[0]
                    #print(box['left'] ,x , box['right'], '|||', box['top'] , y , box['bottom'])
                    if (box['left'] < x < box['right']) and (box['top'] < y < box['bottom']):

                        if word in words_dict:
                            #print(words_dict[word][1][0], x)
                            if words_dict[word][1][0] != box['x']:
                                count, coords, appearance = words_dict[word]
                                words_dict[word + '_' + str(appearance + 1)] = [1, [box['x'],box['y']], appearance + 1]
                            else:
                                words_dict[word][0] += 1
                        else:
                            words_dict[word] = [1, [box['x'],box['y']], 1]
    for key in sorted(words_dict):
        print(key, words_dict[key])
#        print(sorted(words_dict))
    

time = 0

eye_files = sorted(os.listdir("../eye_coordinates"))
box_files = sorted(os.listdir("../bounding_boxes"))
eye_fn_dict = {}

i = 0
for eye_fn in eye_files:
#    eye_fn = eye_files[0]
    i_uid, i_fid, i_time, i_ext = re.split(r'_|\.', eye_fn)
    if i_uid not in eye_fn_dict:
        eye_fn_dict[i_uid] = {}
        i = 0

    eye_fn_dict[i_uid][i]= eye_fn
    i += 1
    
#print(eye_fn_dict)
    
for uid in eye_fn_dict:
    for key in sorted(eye_fn_dict[uid]):
        eye_fn = eye_fn_dict[uid][key]
        time = 0
        nearest_box = ""
        print(eye_fn)
        i_uid, i_fid, i_time, i_ext = re.split(r'_|\.', eye_fn)
        for box_fn in box_files:
            b_uid, b_fid, b_time, b_ext = re.split(r'_|\.', box_fn)
            
            if i_uid == b_uid and i_fid == b_fid: 
                if int(i_time) >= int(b_time) > int(time):
                    time = b_time
                    nearest_box_fn = box_fn
#                    print(eye_fn, nearest_box_fn)
                if b_time > i_time:
#                    print(eye_fn, box_fn)
                    get_words(eye_fn, nearest_box_fn)
                    time = 0 
                    break
#    if time != 0 and box_f:
                
                



#print(eye_files)
#print()
#print(box_files)
#print()
#words_dict = {}

#with open('../eye_coordinates/3_33519720_1658846132.txt', 'r') as eye_reader:
#    with open('../bounding_boxes/3_45130803_1658846118.txt', 'r') as boxes_reader:
#        eye_data = json.load(eye_reader)
#        box_data = json.load(boxes_reader)
#        #print(eye_data)
#        i_data = eye_data['eye_data']
#        b_data = box_data['data']
#        for key in i_data.keys():
#            data = i_data[key]
#            if data['left_pupil_validity'] and data['right_pupil_validity']:
#                x = m.width * data['right_gaze_point_on_display_area'][0]#((data['right_gaze_point_on_display_area'][0] + data['left_gaze_point_on_display_area'][0]) / 2) 
#                y = m.height * data['right_gaze_point_on_display_area'][1]#((data['right_gaze_point_on_display_area'][1] + data['left_gaze_point_on_display_area'][1]) / 2)
#                for datum in b_data:
#                    word, *box = datum
#                    box = box[0]
#                    #print(box['left'] ,x , box['right'], '|||', box['top'] , y , box['bottom'])
#                    if (box['left'] < x < box['right']) and (box['top'] < y < box['bottom']):
#                    
#                    
#                    
#                        if word in words_dict:
#                            #print(words_dict[word][1][0], x)
#                            if words_dict[word][1][0] != box['x']:
#                                count, coords, appearance = words_dict[word]
#                                words_dict[word + '_' + str(appearance + 1)] = [1, [box['x'],box['y']], appearance + 1]
#                            else:
#                                words_dict[word][0] += 1
#                        else:
#                            words_dict[word] = [1, [box['x'],box['y']], 1]
#                         
                        
#                        print('looked at', word)
#print(words_dict)
