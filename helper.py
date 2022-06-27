import re

from urllib.parse import urlencode
from urllib.request import urlopen


class Helper:
    def validate(str):
        regex = ('((http|https)://)(www.)?' +
                '[a-zA-Z0-9@:%._\\+~#?&//=]' +
                '{2,256}\\.[a-z]' +
                '{2,6}\\b([-a-zA-Z0-9@:%' +
                '._\\+~#?&//=]*)')
        p = re.compile(regex)
        if (str == None):
            return False
        if(re.search(p, str)):
            return True
        else:
            return False

    def get_url(keyword):
        params = {'search_query': keyword}
        queryString = urlencode(params)
        html = urlopen('https://www.youtube.com/results?' + queryString)
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        return 'https://www.youtube.com/watch?v=' + video_ids[0]
