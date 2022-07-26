import json, os, re
from screeninfo import get_monitors

m = get_monitors()[1]
print(str(m))


#eye_files = os.listdir("../eye_coordinates")
#box_files = os.listdir("../bounding_boxes")

#time = 0

#for f1 in eye_files:
#    i_uid, i_fid, i_time, i_ext = re.split(r'_|\.', f1)
#    for f2 in box_files:
#        b_uid, b_fid, b_time, b_ext = re.split(r'_|\.', f2)
#        if i_uid == b_uid and i_fid == b_fid: 
#            if int(i_time) > int(b_time) > time:
#                time = b_time
#                box_fn = f2
#            if b_time > i_time:
#                print(box_fn)



#print(eye_files)
#print()
#print(box_files)
#print()
words_dict = {}

with open('../eye_coordinates/3_33519720_1658846132.txt', 'r') as eye_reader:
    with open('../bounding_boxes/3_45130803_1658846118.txt', 'r') as boxes_reader:
        eye_data = json.load(eye_reader)
        box_data = json.load(boxes_reader)
        #print(eye_data)
        i_data = eye_data['eye_data']
        b_data = box_data['data']
        for key in i_data.keys():
            data = i_data[key]
            if data['left_pupil_validity'] and data['right_pupil_validity']:
                x = m.width * data['right_gaze_point_on_display_area'][0]#((data['right_gaze_point_on_display_area'][0] + data['left_gaze_point_on_display_area'][0]) / 2) 
                y = m.height * data['right_gaze_point_on_display_area'][1]#((data['right_gaze_point_on_display_area'][1] + data['left_gaze_point_on_display_area'][1]) / 2)
                for datum in b_data:
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
                         
                        
                        #print('looked at', word)
print(words_dict)
