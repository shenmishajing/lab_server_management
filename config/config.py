import yaml

config = yaml.load(open('config/config.yaml'), Loader = yaml.Loader)

server_config = {} if 'server_config' not in config or config['server_config'] is None else config['server_config']

server_config['servers'] = [f'lab_{s}' for s in config['servers']]
server_config['data_servers'] = [f'lab_{s}' for s in config['data_servers']]
for server in server_config['servers']:
    if server not in server_config:
        server_config[server] = {}
    server_config[server].setdefault('password', config['password'])
