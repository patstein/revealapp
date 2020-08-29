#!/bin/bash -e
python /templates/render_template.py
cat /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'