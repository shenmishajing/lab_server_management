## lab server management tools

### Requirements

- on every server, ensure that your account has been configured with the same password.
- copy config/config.example.yaml to config/config.yaml, and set <your password> part.
- add following host to /etc/hosts

```hosts
192.168.0.15 lab_15
192.168.0.217 lab_217
192.168.0.226 lab_226
192.168.0.235 lab_235
192.168.0.236 lab_236
192.168.0.237 lab_237
192.168.0.240 lab_240
192.168.0.241 lab_241
192.168.0.242 lab_242
192.168.0.243 lab_243
192.168.0.244 lab_244
192.168.0.245 lab_245
192.168.0.247 lab_247
```

- add following to ~/.ssh/config

```
Host lab_217 lab_235 lab_237 lab_244 lab_245
    User <your username>

Host lab_236
    Port 2222
    User <your username>

Host lab_15 lab_226 lab_240 lab_241 lab_242 lab_243 lab_247
    Port 18518
    User <your username>
```

### Installation

- create a python env by conda or venv
- install requirements

```bash
pip install -r requirements.txt
```

- install this.

```bash
pip install -v -e .
```

### Feature

see py file under tools directory.