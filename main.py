# -*- encoding: utf-8 -*-
#!/usr/bin/env python2

import os
import json
import spynner
import PyQt4.QtGui


class Editor:
    def __init__(self, icon, title, url):
        self._url = url

        self.filename = ''
        self._pycall = {}
        self._register_pycall('open', self._open)
        self._register_pycall('save', self._save)
        self._register_pycall('save_as', self._save_as)

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
        filename = dlg.getOpenFileName()
        if filename:
            data = open(filename).read()
            self.filename = filename
            self.browser.webview.setWindowTitle(filename)
            return data

    def _save(self, data):
        if os.path.isfile(self.filename):
            open(self.filename, 'w').write(data)
        else:
            self._save_as(data)

    def _save_as(self, data):
        dlg = PyQt4.QtGui.QFileDialog(self.main_window)
        filename = dlg.getSaveFileName()
        if filename:
            open(filename, 'w').write(data)
            self.filename = filename
            self.browser.webview.setWindowTitle(filename)

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
                ret['errmess'] = str(e)

            return json.dumps(ret)


if __name__ == '__main__':
    editor = Editor('', '', 'data/index.html')
    editor.run()
