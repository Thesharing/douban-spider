# 演职员表
import re


def appendDic(staffList,position,content,count):
    """
    analyse celebrities' message
    :param staffList: 所有演职人员组成的字典
    :param position: 某个演职人员的职位
    :param content:某个演职人员的信息
    :param count:某一类演职人员的数量，对应字典的index键
    :return:
    """
    directorList = list()
    director = dict()
    title = position.split(" ")[1] #获取职位
    director['name'] = content.a.text # 职员姓名
    works = content.select('span[class="works"]') #代表作的列表
    if works: # 防止works为空导致数组越界
        workList = list()
        for work in works[0].find_all('a'):
            workList.append(work.text)
        director['works'] = workList
    role = content.select('span[class="role"]')
    if role and role[0].text[:2] == "演员":
        role = role[0].text
        obj = re.search(r'[(](.*?)[)]', role)
        if obj:
            director['character'] = obj.group(1)[2:]

    director['index'] = count #每种职员的数量
    director['link'] = content.a['href'] #职员的主页连接
    directorList.append(director)
    if title in staffList:
        staffList[title].append(director)
    else:
        staffList[title] = directorList
    count += 1
    return count


def extract_celebrities(items):
    """
    Extract celebrities of the movie.
    :param items: 每一类演职人员信息组成的列表
    :return: dict[staff: value], the celebrities attributes of the movie
    """
    staffList = dict()
    for item in items:
        position = item.h2.text # 演职人员种类
        info = item.select('div[class="info"]') #这一类中每个演职人员信息组成的列表
        count = 1
        for content in info:
            count = appendDic(staffList,position,content,count)
    return staffList