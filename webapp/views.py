from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
# Create your views here.
import jieba.posseg as pseg
import jieba
import sys
import os
import pickle as pk
import re
import json
import numpy as np
import pandas as pd
from keras.models import load_model
from keras import backend


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Before prediction
backend.clear_session()
jieba.load_userdict(r"./corpus/jieba.txt")
network = load_model('./dnn_model.h5')
print("network test:", network.predict(np.zeros((1, 53))))


def get_pair_by_jieba(str_demo):
    """

    :param str_demo: str
    :return: list<str>(list<str>)
    """
    """
        只用句号切开段落
        然后将句子以动词分割，每一个动词匹配跟随在之后的名词
    """
    return_list = []
    for sentence in re.split('。|;|：|；|，', str_demo.lower()):
        """
        sentence 是按照句号和分号切分的每一个小短句子
        """
        no_slash = str_demo.replace(r'/', '、')
        no_plus = no_slash.replace(r'+', '、')
        pseg.re_han_internal = re.compile('(.+)', re.U)
        print(sentence)
        level = ""
        flag = 0
        for word in pseg.lcut(sentence):
            if word.flag == 'vz':
                level = word.word
                flag = 1
        if flag == 1:
            for word in pseg.lcut(sentence):
                if word.flag == 'vz':
                    level = word.word
                if word.flag == 'entity':
                    print(level, word.word)
                    return_list.append([level, word.word])
                # print(word.word, word.flag)
        else:
            for word in pseg.lcut(sentence):
                if word.flag == 'entity':
                    print("++++++没有关键动词+++++")
                    print(level, word.word)
                    return_list.append(['', word.word])
                # print(word.word, word.flag)
    return return_list


def transfer_pair(list_demo):
    """

    :param list_demo: 接受技能描述对
    :return: return_dict 返回一个字典，字典的key为技能实体，匹配图数据库中的节点，value为对于技能的掌握要求
    """
    return_list = []
    for i in list_demo:
        level = 1
        if re.search(r"(了解|会使用|一般|能够|使用过)", i[0]):
            level = 1
        elif re.search(r"(经验|掌握|熟悉|良好|熟练)", i[0]):
            level = 2
        elif re.search(r"(精通|擅长|扎实|深刻)", i[0]):
            level = 3

        if re.search(r"(spring mvc)", i[1]):
            return_list.append([level, "springmvc"])
        elif re.search(r"(springboot|spring boot)", i[1]):
            return_list.append([level, "springmvc"])
        elif re.search(r"(springcloud|spring cloud)", i[1]):
            return_list.append([level, "springcloud"])
        elif re.search(r"(数据结构)", i[1]):
            return_list.append([level, "ds&algorithms"])
        elif re.search(r"(软工|软件工程|uml)", i[1]):
            return_list.append([level, "ds&algorithms"])
        elif re.search(r"(jsp|js|java script|javascript)", i[1]):
            return_list.append([level, "javascript"])
        elif re.search(r"(ts|type script|typescript)", i[1]):
            return_list.append([level, "typescript"])
        elif re.search(r"(vue)", i[1]):
            return_list.append([level, "vue"])
        elif re.search(r"(react)", i[1]):
            return_list.append([level, "react"])
        elif re.search(r"(angular)", i[1]):
            return_list.append([level, "angular"])
        elif re.search(r"(electron)", i[1]):
            return_list.append([level, "electron"])
        elif re.search(r"(node)", i[1]):
            return_list.append([level, "node"])
        elif re.search(r"(rabbit mq)", i[1]):
            return_list.append([level, "rabbitmq"])
        elif re.search(r"(rocket mq)", i[1]):
            return_list.append([level, "rocketmq"])
        elif re.search(r"(mq)", i[1]):
            return_list.append([level, "activemq"])
        elif re.search(r"(k8s)", i[1]):
            return_list.append([level, "kubernetes"])
        elif re.search(r"(微服务)", i[1]):
            return_list.append([level, "container"])
        elif re.search(r"(大数据)", i[1]):
            return_list.append([level, "big_data"])
        elif re.search(r"(github)", i[1]):
            return_list.append([level, "git"])
        elif re.search(r"(sessions)", i[1]):
            return_list.append([level, "session"])
        elif re.search(r"(cookies)", i[1]):
            return_list.append([level, "cookie"])
        elif re.search(r"(证券公司)", i[1]):
            return_list.append([level, "券商"])
        elif re.search(r"(ssh)", i[1]):
            return_list.append([level, "spring"])
            return_list.append([level, "struts"])
            return_list.append([level, "hibernate"])
        elif re.search(r"(ssm)", i[1]):
            return_list.append([level, "spring"])
            return_list.append([level, "springmvc"])
            return_list.append([level, "mybatis"])
        else:
            return_list.append([level, i[1]])
    return_dict = {}
    for pair in return_list:
        if pair[1] not in return_dict:
            return_dict[pair[1]] = pair[0]
        else:
            if pair[0] > return_dict[pair[1]]:
                return_dict[pair[1]] = pair[0]
    return return_dict


def index(request):
    return render(request, 'index.html')


def analysis(request):

    import jieba.posseg as pseg
    import jieba
    import json
    import sys
    import os
    import re
    jieba.load_userdict(r"./corpus/jieba.txt")

    jd_dict = {}
    jd_dict["job_name"] = request.POST.get("job_name")
    jd_dict["job_exp"] = request.POST.get("job_exp")
    jd_dict["job_salary"] = request.POST.get("job_salary")
    jd_dict["edu_degree"] = request.POST.get("edu_degree")
    jd_dict["com_scale"] = request.POST.get("com_scale")
    jd_dict["com_cat"] = request.POST.get("com_cat")
    jd_dict["job_duty"] = request.POST.get("job_duty")
    jd_dict["job_demand"] = request.POST.get("job_demand")
    jd_dict["skill_pair"] = transfer_pair(get_pair_by_jieba(request.POST.get("job_demand")))
    response = render(request, 'analysis.html', {'jd_dict': jd_dict})
    jd_dict_json = json.dumps(jd_dict)
    response.set_cookie('jd_dict_json', jd_dict_json)
    return response


def result(request):
    jd_dict_json = request.COOKIES['jd_dict_json']
    jd_dict = json.loads(jd_dict_json)
    new_dict = {}

    """
    ####################################################################################################################
    """
    """
    JD 特征处理
    """

    """
    jd_id jd唯一id
    """
    new_dict["jd_id"] = 0

    """
    salary 统一处理成 万元/month， 共三个维度，最低，最高和 mean
    """
    # 有工资信息的情况：
    if "-" in jd_dict["job_salary"]:
        low_str, high_str = jd_dict["job_salary"].split("-")

        # 首先是标记为年薪的情况
        if re.search(r"[年|y|year]", high_str) and re.search(r"[万|w]", high_str):
            low = round(float(re.search(r"[\d\.]+", low_str).group()) / 12, 2)
            high = round(float(re.search(r"[\d\.]+", high_str).group()) / 12, 2)
            mid = (low + high) / 2
            new_dict['salary_low'] = low
            new_dict['salary_mid'] = mid
            new_dict['salary_high'] = high

        # 其次是k/m
        elif re.search(r"[千|K]", high_str):
            low = float(re.search(r"[\d\.]+", low_str).group()) / 10 / 12
            high = float(re.search(r"[\d\.]+", high_str).group()) / 10 / 12
            mid = (low + high) / 2
            new_dict['salary_low'] = low
            new_dict['salary_mid'] = mid
            new_dict['salary_high'] = high

        # 再其次是w/m
        elif re.search(r"[万|w]", high_str):
            low = float(re.search(r"[\d\.]+", low_str).group()) / 12
            high = float(re.search(r"[\d\.]+", high_str).group()) / 12
            mid = (low + high) / 2
            new_dict['salary_low'] = low
            new_dict['salary_mid'] = mid
            new_dict['salary_high'] = high

    # 实习生的情况（日薪）
    elif '元/天' in jd_dict["job_salary"]:
        low = float(re.search(r"[\d\.]+", jd_dict["salary"]).group()) * 22 / 10000
        high = float(re.search(r"[\d\.]+", jd_dict["salary"]).group()) * 22 / 10000
        mid = (low + high) / 2
        new_dict['salary_low'] = low
        new_dict['salary_mid'] = mid
        new_dict['salary_high'] = high

    elif "面议" in jd_dict["job_salary"]:
        new_dict['salary_low'] = 0
        new_dict['salary_mid'] = 0
        new_dict['salary_high'] = 0
        pass

    # 没有工资信息的情况
    else:
        print(jd_dict["job_salary"])
        new_dict['salary_low'] = 0
        new_dict['salary_mid'] = 0
        new_dict['salary_high'] = 0

    # """
    # com_type 民营公司3 上市公司2  创业公司1 其它3
    # """
    # if "创业公司" in line["com_type"]:
    #     new_dict["com_type"] = 1
    # elif "上市公司" in line["com_type"]:
    #     new_dict["com_type"] = 2
    # if "民营公司" in line["com_type"]:
    #     new_dict["com_type"] = 3
    # else:
    #     new_dict["com_type"] = 3

    """
    com_cat 计算机+互联网1  游戏+文娱2  电子+硬件+通信3 金融4 其它5 
    """
    new_dict["com_cat"] = 5
    flag_list = []
    flag = 5
    for i in jd_dict["com_cat"].split(","):
        if re.search(r"(计算机|互联网|数据|信息|IT)", i):
            flag_list.append(1)
        elif re.search(r"(游戏|文娱)", i):
            flag_list.append(2)
        elif re.search(r"(电子|硬件|通信)", i):
            flag_list.append(3)
        elif re.search(r"(金融|证券|银行|保险|投行)", i):
            flag_list.append(4)
        else:
            flag_list.append(5)
    new_dict["com_cat"] = max(flag_list)

    # count_list.append(line["com_cat"])

    """
    com_scale
    """
    # count_list.append(line["com_scale"])
    if re.search(r"(1-49人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 1
    elif re.search(r"(50-99人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 2
    elif re.search(r"(100-499人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 3
    elif re.search(r"(500-999人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 4
    elif re.search(r"(1000-2000人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 5
    elif re.search(r"(2000-5000人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 6
    elif re.search(r"(5000-10000人)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 7
    elif re.search(r"(10000人以上)", jd_dict["com_scale"]):
        new_dict["com_scale"] = 8
    else:
        new_dict["com_scale"] = 3

    """
    edu_degree 关于招聘的学历要求 不限1 大专2  本科3  硕士4  博士5
    """
    if re.search(r"(大专)", jd_dict["edu_degree"]):
        new_dict["edu_degree"] = 2
    elif re.search(r"(本科)", jd_dict["edu_degree"]):
        new_dict["edu_degree"] = 3
    elif re.search(r"(硕士)", jd_dict["edu_degree"]):
        new_dict["edu_degree"] = 4
    elif re.search(r"(博士)", jd_dict["edu_degree"]):
        new_dict["edu_degree"] = 5
    else:
        new_dict["edu_degree"] = 1

    """
    edu_major 要求是计算机专业或邻近专业1  不要求0
    """
    new_dict["edu_major"] = 0
    if re.search(r"(相关专业)", ' '.join(jd_dict["job_demand"])):
        new_dict["edu_major"] = 1

    """
    job_exp 统一处理成年， 经验不限0  然后其余是实际年份， 大于10的标记为10
    """
    if re.search(r"[\d\.]+", jd_dict["job_exp"]):
        exp = float(re.search(r"[\d\.]+", jd_dict["job_exp"]).group())

        if re.search(r"[\d]+年", ' '.join(jd_dict["job_demand"])):
            exp2_str = re.search(r"(?P<exp>[\d]+)(?P<str>年)", ' '.join(jd_dict["job_demand"]))
            exp2 = float(exp2_str.group("exp"))
            exp = max(exp, exp2)
        if exp >= 10:
            new_dict["job_exp"] = 10
        else:
            new_dict["job_exp"] = exp
    else:
        new_dict["job_exp"] = 0

    # """
    # dep 意义不大，暂时不处理
    # """
    # count_list.append(line["department"])

    # """
    # job_cat 注意这个字段原本为空，不处理  jod_cat
    # """
    # count_list.append(line["jd_name"])
    """
    job_des 分为岗位职责 和 工作要求两个部分。

    job_duty

    job_demand
    """
    new_dict["job_duty"] = jd_dict["job_duty"]
    new_dict["job_demand"] = jd_dict["job_demand"]
    new_dict["skill_pair"] = transfer_pair(get_pair_by_jieba(jd_dict["job_demand"]))

    """
    job_name 职业名称
    """
    new_dict["job_name"] = jd_dict["job_name"]

    """
    level 分为 初级（如果没有默认初级）、 中级、 高级
    """
    if re.search(r"(专家|高级|资深|总监|架构)", jd_dict["job_name"]):
        new_dict["job_level"] = 3
    elif re.search(r"(中级|组长|负责人)", jd_dict["job_name"]):
        new_dict["job_level"] = 2
    else:
        new_dict["job_level"] = 1
    """
    ####################################################################################################################
    """
    """
    CV 特征处理略去，后台进行
    """
    from util.knowledge_graph import cal_similarity
    cv_data = pk.load(file=open("./data/sample_cv_1000_dict_id.bin", "rb"))

    cv_length = len(cv_data)
    sample_list = []
    """
    拼接向量成输入向量
    """
    # sample of jd+cv
    jd_features = ['is_valid', 'jd_id', 'salary_low', 'salary_mid', 'salary_high', 'com_cat', 'com_scale',
                   'edu_degree',
                   'edu_major', 'job_exp', 'job_demand', 'job_duty', 'job_name', 'job_level', 'skill_pair']
    selected_jd_features = ['salary_low', 'salary_mid', 'salary_high', 'com_cat', 'com_scale',
                            'edu_degree',
                            'edu_major', 'job_exp', 'job_level']

    cv_features = ['cv_id', 'age', 'gender', 'work_experience', 'degree', 'english', 'edu_gz_is', 'edu_dz_is',
                   'edu_dz_major', 'edu_bachelor_is', 'edu_bachelor_major', 'edu_bachelor_985',
                   'edu_bachelor_211',
                   'edu_bachelor_yiben', 'edu_bachelor_erben', 'edu_master_is', 'edu_master_major',
                   'edu_master_985',
                   'edu_master_211', 'edu_master_yiben', 'edu_master_erben', 'edu_doctor_is',
                   'edu_doctor_major',
                   'edu_doctor_985', 'edu_doctor_211', 'edu_doctor_yiben', 'edu_doctor_erben', 'is_cs_award',
                   'is_study_award', 'project_nums', 'work_nums', 'work_has_top_exp', 'work_is_admin',
                   'work_exp_mean',
                   'work_exp_long', 'work_exp_short', 'work_domain1', 'work_exp1', 'work_domain2', 'work_exp2',
                   'work_domain3', 'work_exp3', 'skill_tree', 'project_exp', 'intention_cur_status',
                   'intention_job',
                   'intention_cur_salary', 'skill_pair']
    selected_cv_features = ['age', 'gender', 'work_experience', 'degree', 'english', 'edu_gz_is',
                            'edu_dz_is',
                            'edu_dz_major', 'edu_bachelor_is', 'edu_bachelor_major', 'edu_bachelor_985',
                            'edu_bachelor_211',
                            'edu_bachelor_yiben', 'edu_bachelor_erben', 'edu_master_is', 'edu_master_major',
                            'edu_master_985',
                            'edu_master_211', 'edu_master_yiben', 'edu_master_erben', 'edu_doctor_is',
                            'edu_doctor_major',
                            'edu_doctor_985', 'edu_doctor_211', 'edu_doctor_yiben', 'edu_doctor_erben',
                            'is_cs_award',
                            'is_study_award', 'project_nums', 'work_nums', 'work_has_top_exp', 'work_is_admin',
                            'work_exp_mean',
                            'work_exp_long', 'work_exp_short', 'work_domain1', 'work_exp1', 'work_domain2',
                            'work_exp2',
                            'work_domain3', 'work_exp3', 'intention_cur_status', 'intention_cur_salary']
    label_features = ["skill_sim", "label"]
    sim_features = ["skill_sim"]

    all_columns = selected_jd_features + selected_cv_features + label_features
    columns = selected_jd_features + selected_cv_features + sim_features

    """
    此循环是实时计算使用的
    """
    # for i in range(cv_length):
    #     sample_data = {}
    #     print("%d====of===10000" % i)
    #     cv = cv_data[i]
    #
    #     for key in selected_jd_features:
    #         sample_data[key] = new_dict[key]
    #     for key in selected_cv_features:
    #         sample_data[key] = cv[key]
    #     sample_data["skill_sim"] = cal_similarity(new_dict, cv)
    #     sample_data["sample_id"] = i
    #     sample_list.append(sample_data)
    # pk.dump(sample_list, file=open("./data/sample_10000.bin", "wb"))
    sample_list = pk.load(file=open("./data/sample_1000.bin", "rb"))

    """
    新特征构造
    """
    import math
    from util.tools import pretty_dict
    new_sample_list = []
    for i in sample_list:
        # print(pretty_dict(i))
        """
        正样本特征构造
        """
        # i["score_edu"] = i["degree"] + 1 - i["edu_degree"] - i["edu_dz_is"] * 2
        i["score_edu"] = (i["edu_dz_is"] * 1 + i["edu_bachelor_is"] * 1 + i["edu_bachelor_211"] * 1 + i[
            "edu_bachelor_985"] * 1 + i["edu_master_is"] + i["edu_master_985"] + i["edu_master_985"] * 1 + i[
                              "edu_doctor_is"] + i["edu_doctor_985"] + i["edu_master_211"] * 1) / 10
        # i["score_work"] = (i["work_has_top_exp"] + (i["work_experience"] - i["job_exp"]) / 10) / 2

        gap_exp = i["work_experience"] - i["job_exp"]
        if gap_exp < 0:
            i["gap_exp"] = - math.log(-gap_exp)
        if gap_exp > 3:
            i["gap_exp"] = - math.log(gap_exp)
        else:
            i["gap_exp"] = 0
        i["score_work"] = i["work_has_top_exp"] + i["gap_exp"]
        i["skill_sim_filter"] = i["skill_sim"] if i["skill_sim"] > 0.3 else -1
        # i["score_edu_filter"] = i["score_edu"] if i["score_edu"] >= 0.1 else -1
        i["gap_edu"] = i["degree"] + 1 - i["edu_degree"]
        i["score"] = i["score_edu"] * 2 + i["score_work"] + i["skill_sim_filter"] + i["gap_edu"]
        # print(pretty_dict(i))

        """
        负样本特征构造
        """
        """
        gap
        """
        i["gap_edu"] = i["degree"] + 1 - i["edu_degree"] - i["edu_dz_is"] * 2

        i["gap_level"] = i["work_is_admin"] * 3 - i["job_level"]

        i["gap"] = i["gap_edu"] + i["gap_exp"] + i["gap_level"] + i["skill_sim"] - 1
        # print(pretty_dict(i))
        new_sample_list.append(i)

    """
    预测向量构造
    """
    df = pd.DataFrame(new_sample_list)
    print(len(columns))
    X = df[columns]
    # print(X.describe())
    X = X.values.reshape((1000, 53 * 1))

    df["predict"] = network.predict(X)

    print(df["predict"])

    df["class"] = df["predict"].apply(lambda x: 1 if x > 0.90 else 0)

    result_df = df[df["class"] == 1]
    # print(len(result_df.columns))
    id_list = result_df.sort_values("score", ascending=False)["cv_id"]
    print(id_list)
    result_df.set_index("cv_id")
    raw_cv = pk.load(file=open("./data/cv_1000_raw_id.bin","rb"))
    # book_list = [raw_cv[i] for i in id_list]
    book_list = []

    for i in id_list:
        temp_dict = raw_cv[i]

        temp_dict["skill_sim"] = float(df.loc[df['cv_id'] == i]["skill_sim"])
        temp_dict["score"] = float(df.loc[df['cv_id'] == i]["score"])
        book_list.append(temp_dict)

    """
    分页器模块
    """
    paginator = Paginator(book_list, 10)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            books = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            books = paginator.page(paginator.num_pages)

    response = render(request, 'result.html', {'books': books})
    return response


def about(request):
    response = render(request, 'about.html')
    return response
