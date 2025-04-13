# -*- coding: utf-8 -*-
import os
from apps import create_app

app = create_app('settings')

port = int(os.getenv('PORT', '9001'))

if __name__ == '__main__':
    if port is None:
        app.run(host='0.0.0.0', port=9001, use_reloader=False)
    else:
        app.run(host='0.0.0.0', port=int(port), use_reloader=False)