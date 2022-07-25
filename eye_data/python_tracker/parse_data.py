import json
from screeninfo import get_monitors
m = get_monitors()[1]
print(str(m))

words_dict = {}

with open('../eye_coordinates/1_19507735_1658774400.txt', 'r') as eye_reader:
    with open('../bounding_boxes/1_19507735_1658772314.txt', 'r') as boxes_reader:
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
                            print(words_dict[word][1][0], x)
                            if words_dict[word][1][0] != box['x']:
                                count, coords, appearance = words_dict[word]
                                words_dict[word + '_' + str(appearance + 1)] = [1, [box['x'],box['y']], appearance + 1]
                            else:
                                words_dict[word][0] += 1
                        else:
                            words_dict[word] = [1, [box['x'],box['y']], 1]
                         
                        
                        print('looked at', word)
print(words_dict)
