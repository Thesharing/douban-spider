# 演职员表
import re


def _collect_staff_list(staff_list,title,info):
    """
    analyse celebrities' message
    :param title: 职位名称
    :param info: 某种演职人员的所有人员信息
    :param staff_list: 所有演职人员组成的字典
    :return:
    """
    one_staff_list = list()
    count = 1
    for content in info:
        one_staff = dict()
        one_staff['name'] = content.a.text # 职员姓名
        works = content.select('span[class="works"]') #代表作的列表
        if works: # 防止works为空导致数组越界
            one_staff['works'] = [work.text for work in works[0].find_all('a')]
        role = content.select('span[class="role"]')
        if role and role[0].text[:2] == "演员":
            role = role[0].text
            obj = re.search(r'[(](.*?)[)]', role)
            if obj:
                one_staff['character'] = obj.group(1)[2:]
        one_staff['index'] = count #每种职员的数量
        one_staff['link'] = content.a['href'] #职员的主页连接
        one_staff_list.append(one_staff)
        count += 1
    staff_list[title] = one_staff_list


def extract_celebrities(items):
    """
    Extract celebrities of the movie.
    :param items: 每一类演职人员信息组成的列表
    :return: dict[staff: value], the celebrities attributes of the movie
    """
    staff_list = dict()
    for item in items:
        position = item.h2.text # 演职人员种类
        title = position.split()[1]  # 获取职位
        info = item.select('div[class="info"]') #这一类中每个演职人员信息组成的列表
        _collect_staff_list(staff_list,title,info)
    return staff_list