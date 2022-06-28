import yaml

config = yaml.load(open('config/config.yaml'), Loader = yaml.Loader)

server_config = {} if 'server_config' not in config or config['server_config'] is None else config['server_config']

config['compute_servers'] = list(sorted(config['compute_servers']))
config['data_servers'] = list(sorted(config['data_servers']))
config['servers'] = list(sorted(config['data_servers'] + config['compute_servers']))
for k in ['servers', 'compute_servers', 'data_servers']:
    server_config[k] = [f'lab_{s}' for s in config[k]]
for server in server_config['servers']:
    if server not in server_config:
        server_config[server] = {}
    for k, v in config['default'].items():
        server_config[server].setdefault(k, v)
