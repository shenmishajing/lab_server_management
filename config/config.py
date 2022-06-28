import yaml

server_config = yaml.load(open('config/config.yaml'), Loader = yaml.Loader)

server_config['compute_servers'] = list(sorted(server_config['compute_servers']))
server_config['data_servers'] = list(sorted(server_config['data_servers']))
server_config['servers'] = list(sorted(server_config['data_servers'] + server_config['compute_servers']))

for k in ['servers', 'compute_servers', 'data_servers']:
    server_config[k] = [f'lab_{s}' for s in server_config[k]]

for server in server_config['servers']:
    if server not in server_config:
        server_config[server] = {}
    for k, v in server_config['default'].items():
        server_config[server].setdefault(k, v)

for k in list(server_config['data_dir_path'].keys()):
    server_config['data_dir_path'][f'lab_{k}'] = server_config['data_dir_path'][k]
    del server_config['data_dir_path'][k]
