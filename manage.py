#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from backend import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == "__main__":
    from backend import manager

    manager.run()