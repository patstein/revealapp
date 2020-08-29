import jinja2


env = jinja2.Environment(loader=jinja2.FileSystemLoader('/templates'))
template = env.get_template('default.conf')
conf = template.render()

with open('/etc/nginx/conf.d/default.conf', 'w') as f:
    f.write(conf)
