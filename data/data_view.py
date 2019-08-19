import pickle as pk
from util.tools import pretty_dict

data = pk.load(file=open('./cv_1000_raw_id_backup.bin', 'rb'))

clean_list = []

for i in data:
    each_dict = {}
    for k,v in i.items():
        each_dict[k] = v
    if not i["work_experience"]:
        each_dict["work_experience"] = "暂无工作经验"
    elif '工作经验' in i["work_experience"]:
        pass
    elif '年' in i["work_experience"]:
        each_dict["work_experience"] = i["work_experience"] + '工作经验'
    else:
        each_dict["work_experience"] = i["work_experience"] + '年工作经验'
    clean_list.append(each_dict)

pk.dump(clean_list, file=open('./cv_1000_raw_id.bin', 'wb'))