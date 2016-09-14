# -*- coding: utf-8 -*-
import os
WEBSITENAME = "Zayzafoun"
DATABASE = os.path.join(os.getcwd(), "zayzafoun.db")
DEBUG = True
SECRET_KEY = os.urandom(20)
USERNAME = 'admin'
PASSWORD = 'default'
# Don't forget to change the disqus name! Or the comments section won't be customized to yours, you should go to disqus.com and register a website there.
DISQUSNAME = "tajribython"
