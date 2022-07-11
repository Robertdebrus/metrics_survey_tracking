import pickle
import random
import csv


print("Loading!")

attendgru = {}
with open("../../data/attendgru.txt", "r") as f:
    for line in f:
        fid, text = line.split(maxsplit=1)
        fid = int(fid.strip())
        text_processed = text.replace("<s>", "").replace("</s>", "").replace("<NULL>", "")
        text = " ".join(text_processed.split())
        attendgru[fid] = text

refs = {}
with open ("../../data/com_pp.txt", "r") as f:
    for line in f:
        fid, text = line.split(maxsplit=1)
        fid = int(fid.strip()[:-1])
        text = " ".join(text.split())
        if fid in attendgru:
            refs[fid] = text

functions = {}
names = {}
with open ("../../data/functions.txt", "r") as f:
    text = ""
    name = ""
    fid = None

    text_active = False
    name_captured = False
    l1 = ""
    l2 = f.readline()
    l3 = f.readline()

    for line in f:
        l1 = l2
        l2 = l3
        l3 = line
        if not text_active and len(l1)>2:
            #start new one
            text_active = True
            fid, l = l1.split(",", 1)
            fid = int(fid)
            text += l

            if len(l.split("(")[0].split())>0:
                name = l.split("(")[0].split()[-1]
                names[fid] = name
                name_captured = True

        elif not(l1 == "\n" and l2=="\n" and l3==" \n"):
            #add to text
            text += l1
            if not name_captured and len(l1.split("(")[0].split())>0:
                name = l1.split("(")[0].split()[-1]
                names[fid] = name
                name_captured = True
        else:
            #end and add text
            text_active = False
            name_captured = False
            if fid in attendgru:
                functions[fid] = text
            text = ""
            fid = None

with open("seeds.csv", "w") as out:
    fieldnames = "fid", "name", "ref", "attendgru", "function"
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    for fid in functions:
        writer.writerow({"fid": fid, "name": names[fid], "ref": refs[fid], "attendgru": attendgru[fid], "function": functions[fid]})


# print("Reading")

# comments = []
# for fid in fids:
#     comment = {}
#     comment['fid'] = fid
#     comment['body'] = fcoms[fid].replace("\\", "\\\\").replace('"', '\\"').replace("#{", "\\#{")
#     comments.append(comment)

# tags = []
# for fid in fids:
#     for user in pro_labels[fid]:
#         tag = {}
#         tag['fid'] = fid
#         tag['pro'] = "true"
#         tag['user'] = user
#         tag['label'] = pro_labels[fid][user].replace("\\", "\\\\").replace('"', '\\"').replace("#{", "\\#{")
#         tag['multiple'] = "false"
#         tag['start_index'] = pro_tags[fid][user][0]
#         tag['end_index'] = pro_tags[fid][user][1]
#         tags.append(tag)
#     for user in turk_labels[fid]:
#         tag = {}
#         tag['fid'] = fid
#         tag['pro'] = "false"
#         tag['user'] = user
#         tag['label'] =  turk_labels[fid][user].replace("\\", "\\\\").replace('"', '\\"').replace("#{", "\\#{")
#         tag['multiple'] = "false"
#         tag['start_index'] = turk_tags[fid][user][0]
#         tag['end_index'] = turk_tags[fid][user][1]
#         tags.append(tag)


# print("writing")

# with open("seeds.rb", "w") as fo, open("fids.txt", "w") as fids:

#     fo.write("comment_list = [\n")
#     for comment in comments:
#         fid = comment['fid']
#         body = comment['body']
#         comment_entry = '[{}, "{}"],\n'.format(
#             fid, body)
#         fo.write(comment_entry)
#         fids.write("{}\n".format(fid))
#     fo.write("]\n")

#     fo.write("tag_list = [\n")
#     for tag in tags:
#         fid = tag['fid']
#         pro = tag['pro']
#         user = tag['user']
#         label = tag['label']
#         multiple = tag['multiple']
#         start_index = tag['start_index']
#         end_index = tag['end_index']
#         tag_entry = '[{}, {}, "{}", "{}", {}, {}, {}],\n'.format(
#             fid, pro, user, label, multiple, start_index, end_index)
#         fo.write(tag_entry)
#         fids.write("{}\n".format(fid))
#     fo.write("]\n")

#     fo.write("comment_list.each do |fid, body|\n")
#     fo.write("\tComment.create(fid: fid, body: body)\n")
#     fo.write("end\n")
#     fo.write("tag_list.each do |fid, pro, user, label, multiple, start_index, stop_index|\n")
#     fo.write("\tTag.create(fid: fid, pro: pro, user: user, label: label, multiple: multiple, start_index: start_index, stop_index: stop_index)\n")
#     fo.write("end")






