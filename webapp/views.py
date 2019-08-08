from django.shortcuts import render


# Create your views here.


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
            elif re.search(r"(active mq)", i[1]):
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

    jd_dict["job_name"] = request.POST.get("job_name")
    jd_dict["job_exp"] = request.POST.get("job_exp")
    jd_dict["edu_degree"] = request.POST.get("edu_degree")
    jd_dict["com_scale"] = request.POST.get("com_scale")
    jd_dict["com_cate"] = request.POST.get("com_cate")
    jd_dict["job_duty"] = request.POST.get("job_duty")
    jd_dict["job_demand"] = request.POST.get("job_demand")
    jd_dict["skill_pair"] = transfer_pair(get_pair_by_jieba(request.POST.get("job_demand")))
    response = render(request, 'analysis.html', {'jd_dict': jd_dict})
    jd_dict_json = json.dumps(jd_dict)
    response.set_cookie('jd_dict_json', jd_dict_json)
    return response


def result(request):
    response = render(request, 'result.html')
    return response


def about(request):
    response = render(request, 'about.html')
    return response
