# coding:utf-8
from py2neo import Graph, Node, Relationship
from py2neo.data import walk

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', username='neo4j', password='admin')


# 查询root节点相连的n度 子 节点,后继节点
def get_children(base, degree=1) -> list:
    """
    :param base: 出发的图节点
    :param degree: 度数，默认为一
    :return: 符合条件的node集合
    """
    target_list = []
    nodes = graph.run("MATCH (node)-[:contains*" + str(
        degree) + "]->(s_node) where node.name='" + base + "' return s_node.name").data()
    for i in nodes:
        target_list.append(i["s_node.name"])
        # print(i["s_node.name"])
    return target_list


# 查询root节点相连的n度 父亲 节点，前驱结点
def get_parent(base, degree=1) -> list:
    """
    :param base: 出发的图节点
    :param degree: 度数，默认为一
    :return: 符合条件的node集合
    """
    target_list = []
    nodes = graph.run("MATCH (node)<-[:contains*" + str(
        degree) + "]-(s_node) where node.name='" + base + "' return s_node.name").data()
    for i in nodes:
        target_list.append(i["s_node.name"])
        # print(i["s_node.name"])
    return target_list


# 查询兄弟节点（同一个父节点），同前驱节点
def get_bro(base) -> list:
    """
    :param base: 出发的图节点
    :return: 符合条件的node集合
    """
    target_list = []
    nodes = graph.run(
        "MATCH (s_node)-[:contains*1]->(node) where node.name='" + base + "' MATCH (s_node)-[:contains*1]->(b_node) where b_node.name <> node.name  return b_node.name").data()
    for i in nodes:
        target_list.append(i["b_node.name"])
        # print(i["s_node.name"])
    return target_list


# 查询兄弟节点（同一个爷爷节点），前驱的前驱节点相同
def get_cousin(base) -> list:
    """
    :param base: 出发的图节点
    :return: 符合条件的node集合
    """
    target_list = []
    nodes = graph.run(
        "MATCH (g_node)-[:contains*2]->(node) where node.name='" + base + "' MATCH (p_node)-[:contains*1]->(node) where node.name='" + base + "' MATCH (g_node)-[:contains*1]->(b_node)  where b_node.name <> p_node.name MATCH (b_node)-[:contains*1]->(c_node) return c_node.name").data()
    for i in nodes:
        target_list.append(i["c_node.name"])
        # print(i["s_node.name"])
    return target_list


# 是否为叶子节点
def is_leaf(base) -> bool:
    """
    :param base: 出发的图节点
    :return: 判断是否为叶子节点
    """
    nodes = graph.run(
        "MATCH (node)-[:contains*1]->(c_node) where node.name='" + base + "'return c_node.name").data()
    if nodes:
        return False
    return True


# 是否有孩子节点
def has_children(base):
    """
    :param base: 出发的图节点
    :return: 判断是否有孩子节点
    """
    nodes = graph.run(
        "MATCH (node)-[:contains*1]->(c_node) where node.name='" + base + "'return c_node.name").data()
    if nodes:
        return True
    return False


# 是否有兄弟节点
def has_bro(base):
    """
    :param base: 出发的图节点
    :return: 是否有兄弟节点
    """
    target_list = []
    nodes = graph.run(
        "MATCH (s_node)-[:contains*1]->(node) where node.name='" + base + "' MATCH (s_node)-[:contains*1]->(b_node) where b_node.name <> node.name  return b_node.name").data()
    for i in nodes:
        target_list.append(i["b_node.name"])
        # print(i["s_node.name"])
    return target_list is not None


# 是否为叶子节点的父节点，也就是说是不是倒数第二层节点
def is_p_leaf(base) -> bool:
    """
    :param base: 出发的图节点
    :return: 判断是否为叶子节点
    """
    nodes = graph.run(
        "MATCH (node)-[:contains*2]->(c_node) where node.name='" + base + "'return c_node.name").data()
    if nodes:
        return False
    return True


# 是否为语言相关节点
def is_language_node(base) -> bool:
    """
    :param base: 出发的图节点
    :return: 判断是否为叶子节点
    """
    if not get_parent(base):
        return False
    if get_parent(base)[0] == "language":
        return True
    return False


def cal_similarity(i, j):
    """
    similarity 计算
    :param i: dict of jd
    :param j: dict of cv
    :return:
    """
    jd_skill_dict = i["skill_pair"]
    jd_skill_set = set(jd_skill_dict.keys())

    # print(jd_skill_dict)
    length_of_jd = len(jd_skill_set)

    count = 0
    cv_skill_dict = j["skill_pair"]
    # print(cv_skill_dict)
    cv_skill_set = set(cv_skill_dict.keys())

    for k in jd_skill_set:
        # 为叶子节点
        if is_leaf(k):
            # cv 有相同节点
            if k in cv_skill_set:
                # 给完全匹配的语言节点高权重
                if is_language_node(k):
                    if jd_skill_dict[k] <= cv_skill_dict[k]:
                        count += 1 * 2
                    # 双方都有实体，且工作要求高于CV的掌握
                    elif jd_skill_dict[k] > cv_skill_dict[k]:
                        count += (3 - (jd_skill_dict[k] - cv_skill_dict[k])) / 3 * 2
                else:
                    if jd_skill_dict[k] <= cv_skill_dict[k]:
                        count += 1
                    # 双方都有实体，且工作要求高于CV的掌握
                    elif jd_skill_dict[k] > cv_skill_dict[k]:
                        count += (3 - (jd_skill_dict[k] - cv_skill_dict[k])) / 3

            else:
                # 有兄弟节点,如果cv中有一个兄弟节点就退出循环
                if has_bro(k):
                    flag = 0
                    for node in get_bro(k):
                        if node in cv_skill_set:
                            flag = 1
                            if jd_skill_dict[k] <= cv_skill_dict[node]:
                                count += 1 * 0.9
                            # 双方都有实体，且工作要求高于CV的掌握
                            elif jd_skill_dict[k] > cv_skill_dict[node]:
                                count += (3 - (jd_skill_dict[k] - cv_skill_dict[node])) / 3 * 0.9
                            break
                    if flag == 0:
                        count += 0
                else:
                    if get_parent(k)[0] in cv_skill_set:
                        node = get_parent(k)[0]
                        if jd_skill_dict[k] <= cv_skill_dict[node]:
                            count += 1 * 0.6
                        # 双方都有实体，且工作要求高于CV的掌握
                        elif jd_skill_dict[k] > cv_skill_dict[node]:
                            count += (3 - (jd_skill_dict[k] - cv_skill_dict[node])) / 3 * 0.6
        # 非叶节点
        else:
            if k in cv_skill_set:
                if jd_skill_dict[k] < cv_skill_dict[k]:
                    count += 1
                # 双方都有实体，且工作要求高于CV的掌握
                elif jd_skill_dict[k] > cv_skill_dict[k]:
                    count += (3 - (jd_skill_dict[k] - cv_skill_dict[k])) / 3

            else:
                if has_children(k):
                    flag = 0
                    for node in get_children(k):
                        if node in cv_skill_set:
                            flag = 1
                            if jd_skill_dict[k] <= cv_skill_dict[node]:
                                count += 1
                            # 双方都有实体，且工作要求高于CV的掌握
                            elif jd_skill_dict[k] > cv_skill_dict[node]:
                                count += (3 - (jd_skill_dict[k] - cv_skill_dict[node])) / 3
                            break
                    if flag == 0:
                        count += 0
                # 有兄弟节点,如果cv中有一个兄弟节点就退出循环
                elif has_bro(k):
                    flag = 0
                    for node in get_bro(k):
                        if node in cv_skill_set:
                            flag = 1
                            if jd_skill_dict[k] <= cv_skill_dict[node]:
                                count += 1 * 0.9
                            # 双方都有实体，且工作要求高于CV的掌握
                            elif jd_skill_dict[k] > cv_skill_dict[node]:
                                count += (3 - (jd_skill_dict[k] - cv_skill_dict[node])) / 3 * 0.9
                            break
                    if flag == 0:
                        count += 0
                else:
                    if get_parent(k)[0] in cv_skill_set:
                        node = get_parent(k)[0]
                        if jd_skill_dict[k] <= cv_skill_dict[node]:
                            count += 1 * 0.6
                        # 双方都有实体，且工作要求高于CV的掌握
                        elif jd_skill_dict[k] > cv_skill_dict[node]:
                            count += (3 - (jd_skill_dict[k] - cv_skill_dict[node])) / 3 * 0.6

    # print(count / length_of_jd)
    # print("==============================")
    return count / length_of_jd


if __name__ == '__main__':
    print(is_language_node("java"))
