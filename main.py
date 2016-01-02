#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import os
import sys
import json
import spynner
import PyQt4.QtGui
from PyQt4.QtWebKit import QWebPage

import subprocess


class Editor:
    def __init__(self, icon, title, url):
        self._url = url

        self.filename = ''
        self._pycall = {}
        self.register_pycall('open', self.open)
        self.register_pycall('save', self.save)
        self.register_pycall('save_as', self.save_as)
        self.register_pycall('render', self.render)

        self.browser = spynner.Browser()
        self.browser.set_javascript_prompt_callback(
            self._javascript_prompt_callback
        )

        self.browser.load(self._url)
        self.browser.show()
        self.main_window = self._get_main_window()

        # 设置标题
        self.browser.webview.setWindowTitle(title)
        # 去掉右键出现的 Reload 菜单
        self.browser.webview.page().action(QWebPage.Reload).setVisible(False)

    def run(self):
        self.browser.browse()

    def open(self):
        dlg = PyQt4.QtGui.QFileDialog(self.main_window)
        filename = dlg.getOpenFileName()
        if filename:
            data = open(filename).read()
            self.filename = filename
            self.browser.webview.setWindowTitle(os.path.abspath(filename))
            return data

    def save(self, data):
        if os.path.isfile(self.filename):
            open(self.filename, 'w').write(data.encode('utf-8'))
        else:
            self.save_as(data)

    def save_as(self, data):
        dlg = PyQt4.QtGui.QFileDialog(self.main_window)
        filename = dlg.getSaveFileName()
        if filename:
            open(filename, 'w').write(data.encode('utf-8'))
            self.filename = filename
            self.browser.webview.setWindowTitle(os.path.abspath(filename))

    def read(self, filename):
        data = open(filename).read().decode('utf-8')
        self.filename = filename
        self.browser.runjs('simplemde.value(%s)' % repr(data)[1:])
        self.browser.webview.setWindowTitle(os.path.abspath(filename))

    def render(self, data):
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        pandoc = subprocess.Popen(
            ['pandoc'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            startupinfo=startupinfo
        )
        output = pandoc.communicate(input=data.encode('utf-8'))[0]
        return output

    def _get_main_window(self):
        for widget in self.browser.application.allWidgets():
            if widget.__class__ == PyQt4.QtGui.QWidget:
                return widget

    def register_pycall(self, name, func):
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
    home = os.path.dirname(sys.argv[0])
    if not home: home = '.'
    os.chdir(home)
    editor = Editor('', '7L', 'data/index.html')
    if len(sys.argv) > 1:
        editor.read(sys.argv[1])
    editor.run()
