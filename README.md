# futaba
![picture of futaba](images/futaba-portrait.png)

A Discord bot for the [Programming server](https://discord.gg/010z0Kw1A9ql5c1Qe).

Requires Python 3.6 or later. There is a sample configuration file at `misc/config.toml`.

Requires Discord "developer mode" to be [enabled](https://discord.com/developers/docs/game-sdk/store#:~:text=Open%20up%20the%20Discord%20app,and%20enter%20your%20application%20ID) to get User(Owner)and Channel IDs

Requires [an application and a bot](https://discordpy.readthedocs.io/en/stable/discord.html) to get a bot token

Requires [Privileged Gateway Intents](https://discord.com/developers/docs/topics/gateway#privileged-intents) during development


## Running locally

Config (replace the bot token and channel/owner IDs with yours after copying):

```
$ cp misc/config.toml config.toml
```

Setup:
```
$ pip3 install --user -r requirements.txt
```

To run:
```
$ python3 -m futaba <config.toml>
```

## Development
Docker compose (with image build):
```bash
cd docker
docker-compose -f docker-compose.dev.yml up --build
```

More setup:
```
$ pip3 install --user -r requirements-dev.txt
```

Formatting and linting code:
```
$ black futaba
$ pylint futaba
```

## Deployment
You can have a production system, complete with a systemd service file, you can use the provided
`deploy.sh` script. If there is a `futaba.service` file in the repository root, that service is installed, otherwise the one in `misc/` is used.

Usage:
```
$ ./deploy.sh <config.toml>
```

Installs dependencies, installs the service and configuration files, then restarts the unit.
