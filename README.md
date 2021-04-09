# gitlab-service-desk-discord

An integration with GitLab's Service Desk allowing to report new issues
and receiving updates within Discord.

## Setup

The integration is one Python package `gitlab_sdesk_discord`
containing 2 apps within it:

### `gitlab_sdesk_discord.bot`

This is a Discord bot (daemon) that has commands for reporting new issues
and responding to existing ones.

This can be set up to run using a systemd service:

```text
[Unit]
Description=GitLab Service Desk - Discord bot integration

[Service]
ExecStart=/path/to/python -Om gitlab_sdesk_discord.bot
User=ubuntu
Type=idle
Restart=always
RestartPreventExitStatus=0

[Install]
WantedBy=multi-user.target
```

### `gitlab_sdesk_discord.hook`

This is a hook script that can be called with JSON payload that was received
by webhook in the first argument.
It does not take care of any HTTP handling and is meant to be ran by a separate app
that already handles HTTP like [adnanh/webhook](https://github.com/adnanh/webhook).

Here's a hook configuration that can be directly used with adnanh/webhook:

```json
[
  {
    "id": "gitlab_sdesk_hook",
    "execute-command": "{{ getenv "PYTHON" | js }}",
    "pass-environment-to-command": [
      {
        "source": "string",
        "envname": "GITLAB_TOKEN",
        "name": "{{ getenv "GITLAB_SDESK_DISCORD_GITLAB_TOKEN" | js }}"
      }
    ],
    "pass-arguments-to-command": [
      {
        "source": "string",
        "name": "-Om"
      },
      {
        "source": "string",
        "name": "gitlab_sdesk_discord.hook"
      },
      {
        "source": "entire-payload"
      }
    ],
    "trigger-rule": {
      "and": [
        {
          "match": {
            "type": "value",
            "value": "{{ getenv "GITLAB_SDESK_DISCORD_WEBHOOK_SECRET" | js }}",
            "parameter": {
              "source": "header",
              "name": "X-Gitlab-Token"
            }
          }
        }
      ]
    }
  }
]
```

Parameters of the hook are passed using environment variables:

- `PYTHON`
    Path to Python executable
- `GITLAB_SDESK_DISCORD_GITLAB_TOKEN`
    GitLab token for commenting on the issue
- `GITLAB_SDESK_DISCORD_WEBHOOK_SECRET`
    GitLab webhook secret with which the webhook was set up in GitLab's settings.

## Available commands

TODO
