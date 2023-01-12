import requests
from url_formats import (user_info, relationship_stat)
from database import MongoDB
from loguru import logger
from exceptions import (UIDNotFoundError, APIRequestError, UnkownAPIError)
import time
import numpy as np

#--配置日志记录器--
logger.add('tracker_log.log', rotation='1 MB')

#--配置cookie--
with open('cookies.txt', encoding='utf-8') as f:
    cookie = f.read()

#--配置HTTP请求头--
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'cookie': cookie
}  #User-Agent取自Chrome 108.0.0.0

#--配置网络代理--
proxy = {'http': 'SOME_HTTP_PROXY', 'https': 'SOME_HTTPS_PROXY'}


#--定义随机等待时间--
def random_delay(min=15, max=17):
    delay = np.random.rand() * (max - min) + min
    time.sleep(delay)


#--获取用户基本信息--


def get_user_info(uid: int):
    r = requests.get(user_info.format(mid=uid),
                     headers=header,
                     timeout=10,
                     proxies=proxy)
    try:
        assert r.status_code == 200, 'HTTP request faild with status code: ' + str(
            r.status_code)
    except AssertionError:
        logger.warning('HTTP request faild with status code: ' +
                       str(r.status_code))
        return 0

    try:
        if r.json()['code'] != 0:
            if r.json()['code'] == -404:
                raise UIDNotFoundError(r.json()['code'])
            elif r.json()['code'] == -400:
                raise APIRequestError(r.json()['code'])
            else:
                raise UnkownAPIError
    except (APIRequestError, UnkownAPIError):
        logger.warning('API request faild with status code: ' +
                       str(r.json()['code']))
        return 0
    except UIDNotFoundError:
        logger.warning('UID: ' + str(uid) + ' Not Found')
        return 0

    return r.json()['data']


#获取用户状态


def get_relationship_stat(uid: int):
    r = requests.get(relationship_stat.format(vmid=uid),
                     headers=header,
                     timeout=10,
                     proxies=proxy)
    try:
        assert r.status_code == 200, 'HTTP request faild with status code: ' + str(
            r.status_code)
    except AssertionError:
        logger.warning('HTTP request faild with status code: ' +
                       str(r.status_code))
        return 0

    try:
        if r.json()['code'] != 0:
            if r.json()['code'] == -404:
                raise UIDNotFoundError(r.json()['code'])
            elif r.json()['code'] == -400:
                raise APIRequestError(r.json()['code'])
            else:
                raise UnkownAPIError
    except (APIRequestError, UnkownAPIError):
        logger.warning('API request faild with status code: ' +
                       str(r.json()['code']))
        return 0
    except UIDNotFoundError:
        logger.warning('UID: ' + str(uid) + ' Not Found')
        return 0

    return r.json()['data']


#更新执行函数


def main_update(uid: int):

    user_info_json = get_user_info(uid)
    relationship_stat_json = get_relationship_stat(uid)
    if (user_info_json != 0) and (relationship_stat_json != 0):
        info = {
            'uid': user_info_json['mid'],
            'name': user_info_json['name'],
            'sex': user_info_json['sex'],
            'follower': relationship_stat_json['follower']
        }
        storage = MongoDB('users')
        storage.insert_one_info(info)
        random_delay()
        return True


#--main--

if __name__ == '__main__':
    logger.info('Start to Update Bilibili User Data')
    StartLoc = int(input('Please input the UID start location: '))
    EndLoc = int(input('Please input the UID end location: '))
    for uid in range(StartLoc, EndLoc):
        if main_update(uid):
            logger.info('Update UID ' + str(uid) + ' Successfully')
