import yaml

server_config = yaml.load(open('config/config.yaml'), Loader = yaml.Loader)

server_config['compute_servers'] = list(sorted(server_config['compute_servers']))
server_config['data_servers'] = list(sorted(server_config['data_servers']))
server_config['servers'] = list(sorted(server_config['data_servers'] + server_config['compute_servers']))

for k in ['servers', 'compute_servers', 'data_servers']:
    server_config[k] = [f'192.168.0.{s}' for s in server_config[k]]

if 'server_config' in server_config:
    for k, v in server_config['server_config'].items():
        server_config[f'192.168.0.{k}'] = v

for server in server_config['servers']:
    if server not in server_config:
        server_config[server] = {}
    for k, v in server_config['default'].items():
        server_config[server].setdefault(k, v)

if 'port_config' in server_config:
    for k, v in server_config['port_config'].items():
        if not isinstance(v, list):
            v = [v]
        for s in v:
            server_config[f'192.168.0.{s}']['port'] = k

for k in list(server_config['data_dir_path'].keys()):
    server_config['data_dir_path'][f'192.168.0.{k}'] = server_config['data_dir_path'][k]
    del server_config['data_dir_path'][k]
