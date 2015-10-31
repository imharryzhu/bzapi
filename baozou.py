import requests
import copy

g_client_id = "10230158"
g_secret_key = "18a75cf12dff8cf6e17550e25c860839"

def curtimespan():
    import time
    return int(time.time())

def login(name, password):
    """
    :param name: user name
    :param password: user pwd
    :return: an tuple (bool, class:`BZUser` object, class:`Response` object)
    and if Failed, the BZUser retun None
    """
    post_map = {}
    post_map["client_id"] = g_client_id
    post_map["username"] = name
    post_map["password"] = password
    post_map["timestamp"] = str(curtimespan())
    post_map["sign"] = get_sign(post_map)
    success = False
    user = None
    resp = None

    try:
        resp = requests.post("http://api.ibaozou.com/api/v2/login", post_map)
        jsonObj = resp.json()

        user = BZUser()
        user.name = name
        user.pwd = password
        user.uid = str(jsonObj['user_id'])
        user.token = jsonObj['access_token']
        success = True
    except Exception,e:
        success = False

    return (success, user, resp,)

def article_up(article, user):
    """
    :param article: the articleID (string)
    :param user: class:`BZUser` object
    :return: (bool, class:`Response` object)
    """
    post_map = {}
    post_map["client_id"] = g_client_id
    post_map["article_id"] = article
    post_map["user_id"] = user.uid
    post_map["access_token"] = user.token
    post_map["timestamp"] = str(curtimespan())
    post_map["sign"] = get_sign(post_map)
    url = "http://api.ibaozou.com/articles/%s/up.app" % article
    success = False
    resp = None
    try:
        html_data = requests.post(url, post_map).text
        if '1' in html_data:
            success = True
    except Exception, e:
        pass

    return (success, resp,)


def get_detail(user):
    """
    :param user:  class:`BZUser` object and i need `uid` and `token`
    :return: (bool, class:`Response` object)
    ### this function will update and fill the user ###
    """
    post_map = {}
    post_map["client_id"] = g_client_id
    post_map["access_token"] = user.token
    post_map["id"] = user.uid
    post_map["user_id"] = user.uid
    post_map["timestamp"] = str(curtimespan())
    post_map["sign"] = get_sign(post_map)
    url = "http://api.ibaozou.com/api/v2/" + "users/" + "27823699" + "?" + create_post_string(post_map)

    success = False
    resp = None
    try:
        resp = requests.get(url)
        #
        # fill the user
        #
        success = True
    except Exception, e:
        pass

    return (success, resp,)

def article_commet(user, article, content):
    """
    :param user: class:`BZUser` object and i need `uid` and `token`
    :param article: the articleID
    :param content: the text what you want to say
    :return: (bool, class:`Response` object)
    """
    post_map = {}
    post_map["client_id"] = g_client_id
    post_map["user_id"] = user.uid
    post_map["access_token"] = user.token
    post_map["anonymous"] = "false"
    post_map["content"] = content
    post_map["timestamp"] = str(curtimespan())
    tmp_map = copy.copy(post_map)
    tmp_map["id"]=article
    post_map["sign"] = get_sign(tmp_map)

    url = "http://api.ibaozou.com/api/v1/articles/" + article + "/comments"

    success = False
    resp = None
    try:
        resp = requests.post(url, post_map)
        if 'error' not in resp.text:
            success = True
    except Exception, e:
        pass

    return success, resp

def create_post_string(dict):
    res = []
    map(lambda k: res.append(k+"="+str(dict[k])), dict.keys())
    return "&".join(res)

def get_sign(dict):
    import urllib
    str = ""

    keys = dict.keys()
    keys.sort()

    for key in keys:
        if key in dict:
            str += key + "=" + dict[key]
    str += g_secret_key
    return get32md5(urllib.quote_plus(str))

def get32md5(input):
    import hashlib
    m = hashlib.md5()
    m.update(input)
    return m.hexdigest()


class BZUser:
    def __init__(self):
        self.name = ''
        self.pwd = ''
        self.mail = ''
        self.token = ''
        self.uid = ''

