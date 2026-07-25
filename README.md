# Overview

Repo used to install and normalize some of the common tasks done in new machines.

# Playbooks
- Restart: Sets up machines that belong to the homelab cluster, drains and reboots them
- Demo: Scratch playbook used for recordings

# Testing
Since this is ansible we use molecule to test the various scenarios done by the roles/playbooks.

Everything is driven from `Taskfile.yml` at the repo root via
[Task](https://taskfile.dev) — no need to `cd` into a role or export
`ANSIBLE_ROLES_PATH` by hand.

```bash
task               # list every task and the roles that have a scenario
task test          # full molecule run for node_setup
task converge      # apply the role, leave the container up for poking at
task login         # shell into that container
task destroy       # clean up
task lint          # ansible-lint over the repo

task test ROLE=<role>   # pick a different role
```

Needs a running Docker daemon. If molecule isn't available, `task deps` rebuilds
`.venv` from `requirements.txt`.
