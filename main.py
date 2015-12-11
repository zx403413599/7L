# -*- encoding: utf-8 -*-
#!/usr/bin/env python2

import os
import json
import spynner
import PyQt4.QtGui


class Editor:
    def __init__(self, icon, title, url):
        self._url = url

        self._filename = ''
        self._pycall = {}
        self._register_pycall('open', self._open)

        self.browser = spynner.Browser()
        self.browser.set_javascript_prompt_callback(
            self._javascript_prompt_callback
        )
        self.main_window = None  # run 之后才能获取

    def run(self):
        self.browser.load(self._url)
        self.browser.show()
        self.main_window = self._get_main_window()
        self.browser.browse()

    def _open(self):
        dlg = PyQt4.QtGui.QFileDialog(self.main_window)  
        self._filename = dlg.getOpenFileName()  
        data = open(self._filename).read()
        return data

    def _save(self, text):
        if os.path.isfile(self._filename):
            open(self._filename, 'w').write(text)
        else:
            self._save_as(text)

    def _save_as(self, text):
        # 选择文件
        # open write
        pass

    def _get_main_window(self):
        for widget in self.browser.application.allWidgets():
            if widget.__class__ == PyQt4.QtGui.QWidget:
                return widget

    def _register_pycall(self, name, func):
        self._pycall[name] = func

    def _javascript_prompt_callback(self, url, message, defaultvalue):
        '''
        message 作为函数名, defaultvalue 作为参数(Json字符串)
        '''
        name = message
        kwargs = json.loads(unicode(defaultvalue))
        ret = {'success': True}
        if name in self._pycall:
            try:
                data = self._pycall[name](**kwargs)
                ret['data'] = data
            except Exception as e:
                ret['success'] = False
                ret['errmess'] = unicode(e)

            return json.dumps(ret)


if __name__ == '__main__':
    editor = Editor('', '', 'data/index.html')
    editor.run()
