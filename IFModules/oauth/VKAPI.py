# Date: 01.06.2015 - 06.06.2015
import repper, internettools, restapitools
import urllib, urllib2, cookielib, md5, json, urlparse, os
import lxml.html

"""oauth_data = {
        'scope_sep': ',',
        'url_toopendialog': 'https://oauth.vk.com/authorize',
        'url_api': 'https://api.vk.com',
        'query': '/method/',
        'uri_redirect': 'https://oauth.vk.com/blank.html',
        # названия параметров, передаваемые при выполнении логининга
        'name_for_email': 'email',
        'name_for_password': 'pass',
        'other': {} # не общая информация
    }

acceessPermission = {
        "notify": 1,
        "friends": 1,
        "photos": 1,
        "audio": 1,
        "video": 1,
        "docs": 1,
        "notes": 1,
        "pages": 1,
        "status": 1,
        "offers": 1,
        "questions": 1,
        "wall": 1,
        "groups": 1,
        "messages": 1,
        "email": 1,
        "notifications": 1,
        "stats": 1,
        "ads": 1,
        "offline": 0,
        "nohttps": 0
}"""

class VK():
    #settings_api = {"lang": "ru", "v": 5.33, "https": 0, "test_mode": 0}
    app_data = {}
    print_log = True
    def __init__(self, user_data, oauth_data, acceessPermission, settings_api, params):
        self.user_data = user_data
        self.oauth_data = oauth_data
        self.acceessPermission = acceessPermission
        self.settings_api  = settings_api
        self.rat = restapitools.RESTAPITools()
        self.it = internettools.InternetTools()

    """def _get_scope_parametr(self):
        scope = ""
        for key, value in acceessPermission.items():
            if value: scope += key + oauth_data['scope_separator']
        if len(scope) > 1: scope = scope[:-1]
        return scope"""

    def _extract_app_data(self, response):
        fragment = urlparse.urlparse(response.geturl()).fragment
        app_data = urlparse.parse_qs(fragment)
        for k in app_data: app_data[k] = app_data[k][0]
        return app_data

    def _is_there_token(self, response):
        fragment = urlparse.urlparse(response.geturl()).fragment
        app_data = urlparse.parse_qs(fragment)
        if app_data.has_key('access_token'): return True
        else: return False

    def _is_frozen(self, str_page):
        str_page = str_page.replace('text_panel login_blocked_panel', 'text_panel_login_blocked_panel')
        page = lxml.html.document_fromstring(str_page)
        div = page.cssselect('div.text_panel_login_blocked_panel')
        if len(div) == 1:
            print div[0].text
            return True
        else: return False

    """def do_authorize(self):
        params = {"client_id": self.user_data[0],
                  "redirect_uri": self.oauth_data['uri_redirect'],
                  "scope": self.rat.get_scope(self.acceessPermission, self.oauth_data['scope_sep']),
                  "response_type": "token",
                  'state': '',
                  self.params['display_name']: self.params['display_value_for_mobile']
                  }

        print u'Открываем страницу для логининга...'
        str_page, res = self.it.urlopen(self.oauth_data['url_toopendialog'], 1, GET=params)
        params2, action_url = self.it.get_dictforms(str_page, res).values()[0]
        params2[self.oauth_data['name_for_email']] = self.user_data[1]
        params2[self.oauth_data['name_for_password']] = self.user_data[2]

        print u'Логинимся...'
        str_page, res = self.it.urlopen(action_url, 2, POST=params2)
        # Если вместо страницы логининга была страница подтверждения прав
        # (т. е. мы уже были залогинены), то вынимаем токен.
        if not self._is_there_token(res):
            if self._is_frozen(str_page): return 'frozen'
            params2, action_url, form = self.it.get_dictforms(str_page, res, True).values()[0]
            self.it.get_captcha(form, params2, 'captcha_key', 'captcha_img')
            # если мы вводили капчу
            if oauth_data['name_for_password'] in params:
                params2[self.oauth_data['name_for_email']] = self.user_data[1]
                params2[self.oauth_data['name_for_password']] = self.user_data[2]
            params2 = urlparse.urlparse(action_url).query +"&"+ urllib.urlencode(params2)

            print u'Подтверждаем права доступа...'
            str_page, res = self.it.urlopen(action_url, 3, POST=params2)
        else: print u'Пользователь был залогинен ранее.'

        print u'Сохраняем токен доступа.\n'
        self.app_data = self._extract_app_data(res)"""

    """def _process_response(self, res):
        res = json.loads(res.read())
        if self.print_log: print '\nResponse\n', res
        if res.has_key('response'): return 'success', res['response']
        elif res.has_key('error'):
            res = res['error']
            return 'error', {'code': res['error_code'], 'msg': res['error_msg']}"""

    """def api(self, method_name, GET={}, POST={}):
        GET['access_token'] = self.app_data['access_token']
        GET.update(self.settings_api)
        POST = urllib.urlencode(POST)
        query = self.oauth_data['query'] + method_name +'?'+ urllib.urlencode(GET)
        if POST != '': _POST = '&'+POST
        else: _POST = ''
        if self.acceessPermission['nohttps']:
            sig = '&sig='+md5.new(query+_POST+self.app_data['secret']).hexdigest()
        else: sig = ''
        str_page, res = self.it.urlopen(self.oauth_data['url_api']+query+sig, None, POST=POST) 
        
        #return self._process_response(res)
        return res"""
