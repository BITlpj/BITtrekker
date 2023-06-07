import json
import time

from .models import *
import  random
building = {"2":"文萃楼", "3":"综合教学楼A", "7":"综合教学楼B", "10":"理科教学楼"}
lable   =['插座多','离水房近','离女厕近','离男厕近','空调可调节']

# 注意，label_id = label + 1

'''
管理员限制或解除限制某个教室 
输入(教室id, cover状态) 
输出为0说明修改成功 否则添加失败
'''
def cover_classroom(id, covered):
    classroom = Classroom.objects.filter(id=id)
    if len(classroom) != 1:
        return 1
    Classroom.objects.filter(id=id).update(classroom_covered=covered)
    # Occupytable.objects.filter(classroom_id=id).update(covered=covered)
    if covered:
        print("Covered classroom:", classroom[0].classroom_name)
    else:
        print("Uncovered classroom:", classroom[0].classroom_name)
    return 0
def generate_rand_feature():
    LabelClassroom.objects.all().delete()

    all_classroom = Classroom.objects.all()
    classrooms_id = [i.id for i in all_classroom]

    all_label = Labeltable.objects.all()
    labels_id = [i.id for i in all_label]
    for classroom_id in classrooms_id:
        for label_id in labels_id:
            if random.randint(1, 10) == 1:
                LabelClassroom.objects.create(
                    classroom_id=classroom_id,
                    label_id=label_id
                )

'''
编辑教室信息 
输入(标准json格式参考api文档)
输出为0说明修改成功
'''
def edit_classroom(input):
    # 解包
    building = input['affiliated_teaching_building']
    classroom_id = input['classroom_id']
    classroom_name = input['classroom_name']
    print(input['free_time'])
    date = input['free_time']['date']
    tmp_times = input['free_time']['time']
    tmp_labels = input['classroom_features']
    
    # 检查是否为新教室
    classroom = Classroom.objects.filter(classroom_name=classroom_name)
    if not classroom:
        Classroom.objects.create(
            classroom_name=classroom_name,
            building=building,
            classroom_covered=0
        )
        classroom = Classroom.objects.filter(classroom_name=classroom_name)[0]
    else:
        classroom = classroom[0]
    
    # 修改Occupytable
    Occupytable.objects.filter(classroom_id=classroom.id,
                               date=date).delete()
    for i in range(5):
        Occupytable.objects.create(classroom_id=classroom_id,
                                   date=date,
                                   time=i,
                                   available=tmp_times[i],
                                   covered=0)
    
    # 修改LabelClassroom
    LabelClassroom.objects.filter(classroom_id=classroom_id).delete()
    for i, j in enumerate(tmp_labels):
        if j:
            LabelClassroom.objects.create(classroom_id=classroom_id,
                                          label_id=i+1)
    
    return 0


'''
删除标签
输入标签名称str
输出为0说明删除成功 为1说明不存在该名称的标签
'''
def del_label(name):
    label = Labeltable.objects.filter(label_name=name)
    if not label:
        return 1
    else:
        label = label[0]
    
    # 删除LabelClassroom中对应表项
    LabelClassroom.objects.filter(label_id=label.id).delete()

    # 删除Labeltable中对应表项
    Labeltable.objects.filter(id=label.id).delete()
    
    print("Deleted label:", name)
    return 0
        

'''
增加标签 
输入名字str 
输出为0说明添加成功 返回值为1说明已经有这个名字的标签了
'''
def add_label(name):
    label = Labeltable.objects.filter(label_name=name)
    if label:
        return 1
    Labeltable.objects.create(
        label_name=name
    )
    print("Added label:", name)
    return 0


'''
返回当前标签表，符合接口要求
'''
def ask_label_table():
    labeltable = Labeltable.objects.all()
    output = {}
    for label in labeltable:
        output[label.id] = label.label_name
    return output


'''
查询某个教室的信息 返回dict符合“获取详情页信息”要求
'''
def ask_class_info(input, covered=0):

    time.sleep(1)
    date = input['date']

    tmp_times = input['period']
    times = []
    if tmp_times:
        for i in range(5):
            if tmp_times[i]:
                times.append(i)
    else:
        times = [0, 1, 2, 3, 4]

    buildings = input['teaching_building']
    if not buildings:
        buildings = ["文萃楼", "综合教学楼A", "综合教学楼B", "理科教学楼"]

    tmp_labels = input['classroom_feature']
    labels = []
    labeltable = Labeltable.objects.all()
    num_label = len(labeltable)
    if tmp_labels:
        for i in range(num_label):
            if tmp_labels[i]:
                labels.append(labeltable[i].id)

    classrooms_valid = Classroom.objects.filter(building__in=buildings,
                                                classroom_covered=covered)
    classrooms_valid_id = [classroom.id for classroom in classrooms_valid]
    print(classrooms_valid_id)


    no_occupy_table = Occupytable.objects.filter(date=date,
                                                 time__in=times,
                                                 covered=0,
                                                 classroom_id__in=classrooms_valid_id,
                                                 available=1
                                                 )
    output = []
    chosen_classroom = []



    for i in no_occupy_table:
        classroom_id = i.classroom_id
        if classroom_id in chosen_classroom:
            continue
        chosen_classroom.append(classroom_id)
        classroom = Classroom.objects.get(id=classroom_id)

        # 检查是否教室是否具有指定标签，如果是全0的话就直接放行
        # for j in range(len(Labeltable.objects.all())):
        #     sign2 = sign2 | labels[j]
        #     if labels[j] and LabelClassroom.objects.filter(classroom_id=classroom_id,
        #                                      label_id=j):
        #         sign = 1
        #         break
        if labels and not LabelClassroom.objects.filter(classroom_id=classroom_id,
                                         label_id__in=labels):
            continue

        sign = 1
        for label in labels:
            if not LabelClassroom.objects.filter(classroom_id=classroom_id,
                                                 label_id=label):
                sign = 0
                break
        if not sign:
            continue

        # 装填
        tmp = {}
        tmp['affiliated_teaching_building'] = classroom.building
        tmp['classroom_id'] = classroom_id
        tmp['classroom_name'] = classroom.classroom_name
        tmp_times = []
        for j in range(0, 5):
            if Occupytable.objects.filter(classroom_id=classroom_id,
                                             date=date,
                                             time=j,
                                             available=1,
                                             covered=0):
                tmp_times.append(1)
            else:
                tmp_times.append(0)
        tmp['free_time'] = {'date':date, 'detailed_time_period':tmp_times}


        tmp['classroom_features'] = [0] * len(labeltable)
        for j, label in enumerate(labeltable):
            if LabelClassroom.objects.filter(label_id=label.id,
                                                  classroom_id=classroom_id):
                tmp['classroom_features'][j] = 1
        print(tmp)
        output.append(tmp)
    return output
def clear_all_database():
    Classroom.objects.all().delete()
    Occupytable.objects.all().delete()
    Labeltable.objects.all().delete()
    LabelClassroom.objects.all().delete()


def update_data(json_path):

    for i in lable:
        add_label(i)

    print("Updating date from json files...")
    
    with open(json_path, encoding='GBK') as f:
        data = json.load(f)
    

    # print(data["2"]["2023-05-19"]["文萃楼B129"])
    # 2文萃 3综教A 10理教 7综教B


    for bid, bname in building.items():
        if not bid in data.keys():
            continue
        # 删除表Occupytable中过期数据
        dates = [i for i in list(data[bid].keys())]
        Occupytable.objects.exclude(date__in=dates).delete()

        # 检查是否需要在Classroom表中添加表项
        for date in dates:
            for room in data[bid][date].values():
                if not Classroom.objects.filter(classroom_name=room[0]):
                    Classroom.objects.create(
                        classroom_name = room[0],
                        building = bname,
                        classroom_covered = 0
                    )
        
        # 检查是否需要添加至占用表
        for date in dates:
                for item in data[bid][date].values():
                    room = Classroom.objects.get(classroom_name=item[0])
                    for i in range(1, 6):
                        Occupytable.objects.create(
                            classroom_id=room.id,
                            date=date,
                            time=5-i,
                            available=1 if item[-i] == 'free' else 0,
                            covered=0
                        )
    generate_rand_feature()
    print("Database update complete")

    
# path = "D:\\Project\\Python\\django_news\\news\\ZA.json"
# update_models(path)