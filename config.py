# -*- coding: utf-8 -*-
import os
WEBSITENAME = "Zayzafoun"
DATABASE = os.path.join(os.getcwd(), "zayzafoun.db")
DEBUG = True
SECRET_KEY = os.urandom(20)
USERNAME = 'admin'
PASSWORD = 'default' # If you forget to modify this. You probably deserve it.
DISQUSNAME = "tajribython" # Don't forget to change the disqus name! Or the comments section won't be customized to yours, you should go to disqus.com and register a website there.
