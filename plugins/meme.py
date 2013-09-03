from util import hook, http, web
import shlex

import requests

GENURL = 'http://version1.api.memegenerator.co'

POPULAR_URL = '{0}/Generators_Select_ByPopular'.format(GENURL)
POPULAR_DAT = {
    'pageIndex': '0',
    'pageSize': '24',
    'days': '',
}

SEARCH_URL = '{0}/Generators_Search'.format(GENURL)
SEARCH_DAT = {
    'q': None,
    'pageIndex': '0',
    'pageSize': '24',
}

INFO_URL = "{0}/Generator_Select_ByUrlNameOrGeneratorID".format(GENURL)
INFO_DAT = {'urlName': None}

ACTION_URL = "{0}/Instance_Create".format(GENURL)
ACTION_DAT = {
    'username': None,
    'password': None,
    'languageCode': 'en',
    'generatorID': None,
    'imageID': None,
    'text0': None,
    'text1': None,
}


def get_image_id_from_url(url):
    return url.split("/")[-1].split(".")[0]


@hook.command(autohelp=False)
def listmemes(pattern):
    memeinfo = []
    if pattern:
        url = SEARCH_URL
        SEARCH_DAT.update({'q': pattern})
        params = SEARCH_DAT
    else:
        url = POPULAR_URL
        params = POPULAR_DAT

    result = requests.get(url, params=params).json()
    if not result.get('success', False):
        if result.get('errorMessage', None):
            return result['errorMessage']
        else:
            return FIX_MEME

    out = ""
    for m in result['result']:
      if out == "":
        out = m['urlName'] + ": " + m['imageUrl']
      else:
        out = out + "\n" + m['urlName'] + ": " + m['imageUrl']
    return "List of memes: %s" % web.haste(out)


def get_api_result(*args, **kwargs):
    response = requests.get(*args, **kwargs)
    result = None
    message = "API is broken. Please tell blha303 about this."
    try:
        jsondata = response.json()
    except ValueError:
        pass # out is already set for this state
    else:
        if jsondata.get('success', False):
            result = jsondata['result']
            message = None
        elif jsondata.get('errorMessage', False):
            message = jsondata['errorMessage']
    return result, message


@hook.command
def meme(inp, bot=None):
    """meme <meme> "<topline>" "<bottomline>" - Generate meme. Get meme ID using .listmemes. You can make a section blank with .meme Meme "" "Bottom text only" """
    keys = bot.config['api_keys']
    if keys['meme_user'] == "MEMEGENERATOR USERNAME":
        return "Please set username and password in config"
    try:
        user = keys['meme_user']
        passw = keys['meme_pass']
    except:
        keys['meme_user'] = "MEMEGENERATOR USERNAME"
        keys['meme_pass'] = "MEMEGENERATOR PASSWORD"
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        return "Please set username and password in config"
    inpsplit = shlex.split(inp)
    INFO_DAT.update({'urlName': inpsplit[0]})
    result, message = get_api_result(INFO_URL, params=INFO_DAT)
    if result:
        ACTION_DAT.update({
          'username': user,
          'password': passw,
          'generatorID': result['generatorID'],
          'imageID': get_image_id_from_url(result['imageUrl']),
          'text0': inpsplit[1],
          'text1': inpsplit[2],
        })
    else:
        return message
    result, message = get_api_result(ACTION_URL, params=ACTION_DAT)
    if result:
        try:
            return web.isgd(result['instanceImageUrl'])
        except (web.ShortenError, http.HTTPError) as error:
            return result['instanceImageUrl']
    else:
        return message
