from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def analysis(request):
    import jieba.posseg as pseg
    import jieba
    import sys
    import os
    import re
    jieba.load_userdict(r"./corpus/jieba.txt")

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

    print(request)
    print(request.POST.get("job_name"))
    print(request.POST.get("job_exp"))
    print(request.POST.get("edu_degree"))
    print(request.POST.get("com_scale"))
    print(request.POST.get("com_cate"))
    print(request.POST.get("job_duty"))
    print(request.POST.get("job_demand"))
    print(get_pair_by_jieba(request.POST.get("job_demand")))
    # name = request.POST.get('name')
    # print(name)
    return render(request, 'index.html')
