# AGENTS.md - Ansible Playbooks Repository

Guidelines for AI agents working in this Ansible automation repository.

## Overview

This repository contains Ansible playbooks and roles for homelab infrastructure
automation, including machine setup and service deployment.

## Development Environment

Tasks are driven by [Task](https://taskfile.dev) (`Taskfile.yml` at the repo
root). Run `task` with no arguments to list everything.

### Setup

Requires [uv](https://docs.astral.sh/uv/) (`brew install uv`).

```bash
task deps   # rebuilds .venv with uv, installs requirements.txt and galaxy collections
```

### Environment Variables

`ANSIBLE_ROLES_PATH` is exported by the Taskfile. Only needed when invoking
ansible directly:

```bash
export ANSIBLE_ROLES_PATH="$(pwd)/roles"
```

## Build/Lint/Test Commands

### Linting

```bash
# Lint entire repository
task lint

# Syntax-check every playbook
task syntax

# Lint specific file
ansible-lint playbooks/restart.yaml

# Lint specific role
ansible-lint roles/node_setup/
```

### Running Playbooks

```bash
# Run playbook against inventory
ansible-playbook -i inventory/homelab.ini playbooks/restart.yaml

# Dry run (check mode)
ansible-playbook -i inventory/homelab.ini playbooks/restart.yaml --check

# Run with specific tags
ansible-playbook -i inventory/homelab.ini playbooks/restart.yaml --tags "pkg,motd"

# Limit to specific hosts
ansible-playbook -i inventory/homelab.ini playbooks/restart.yaml --limit eva01
```

### Testing with Molecule

Use the Taskfile. Every task runs from the repo root and sets
`ANSIBLE_ROLES_PATH` itself, so there is no need to `cd` into a role.

```bash
task                   # list tasks, show which roles have a scenario
task test              # full sequence: create, converge, idempotence, verify, destroy
task converge          # apply the role, leave the container up
task verify            # run verify.yml against the running container
task idempotence       # re-converge, fail on any change
task login             # shell into the container
task destroy           # tear it down
task test-all          # every role that has a scenario

task test ROLE=<role>  # target a specific role (defaults to node_setup)
```

Requires a running Docker daemon; the targets fail with a clear message if it
is unreachable or if molecule is not installed.

## Code Style Guidelines

### YAML Formatting

- Use 2-space indentation
- Use `.yaml` extension for playbooks, `.yml` for role files
- Start files with `---` for playbooks (optional for role files)
- Use double quotes for strings containing variables

### Task Naming

- Use Title Case for task names
- Be descriptive: `Install ssh package` not `ssh`
- Prefix with action verb: Install, Configure, Setup, Check, Create

```yaml
# Good
- name: Install Core Packages
- name: Setup SSH Configuration
- name: Check Tailscale Installed

# Bad
- name: packages
- name: do ssh stuff
```

### Module Usage - Always Use FQCNs

Always use Fully Qualified Collection Names:

```yaml
# Good
- ansible.builtin.file:
- ansible.builtin.copy:
- ansible.builtin.template:
- ansible.builtin.apt:
- ansible.builtin.systemd:
- community.general.sudoers:
- kubernetes.core.k8s_drain:

# Bad
- file:
- copy:
- apt:
```

### Variable Naming

- Use snake_case for all variables
- Prefix role-specific variables with role context
- Use descriptive names

```yaml
# Good
otel_version: 0.139.0
agent_endpoint: 'otel.local.net'
username_home: "/home/{{ username }}"

# Bad
ver: 0.139.0
ep: 'otel.local.net'
```

### Block Structure

Group related tasks using blocks:

```yaml
- name: Setup SSH Things
  block:
    - name: Install ssh package
      ansible.builtin.apt:
        name: openssh-server
        state: present
    - name: SSH Config
      ansible.builtin.copy:
        src: "sshd_config.j2"
        dest: "/etc/ssh/sshd_config"
```

### Tags

Apply meaningful tags for task filtering:

```yaml
- name: Setup Otel Agent
  tags:
    - otel
  block:
    # tasks here
```

### Handler Naming

Use PascalCase for handlers:

```yaml
# handlers/main.yml
- name: RestartSSH
  ansible.builtin.systemd:
    name: ssh
    state: restarted

- name: Restart Systemd Daemon
  ansible.builtin.systemd:
    daemon_reload: true
```

### File Permissions

Always specify mode as string with leading zero:

```yaml
# Good
mode: "0644"
mode: "0755"

# Bad
mode: 644
mode: 0644  # Octal can cause issues
```

### Conditionals

Use `when` for conditional execution:

```yaml
- name: Pihole running
  ansible.builtin.systemd:
    name: pihole-FTL.service
    state: started
  when: pihole_enabled
```

### Become (Privilege Escalation)

Apply `become: true` at block level when multiple tasks need elevation:

```yaml
- name: Setup Otel Agent
  block:
    - name: Create user
      ansible.builtin.user:
        name: otel
    - name: Download Agent
      ansible.builtin.get_url:
        url: "..."
  become: true
```

## Directory Structure

```
├── inventory/
│   ├── homelab.ini          # Main inventory
│   ├── group_vars/           # Group variables
│   └── host_vars/            # Host-specific variables
├── playbooks/
│   └── *.yaml                # Playbook files
├── roles/
│   └── <role_name>/
│       ├── defaults/main.yml # Default variables
│       ├── vars/main.yml     # Role variables
│       ├── tasks/main.yml    # Main tasks
│       ├── handlers/main.yml # Handlers
│       ├── templates/*.j2    # Jinja2 templates
│       ├── files/            # Static files
│       └── molecule/         # Molecule tests
└── requirements.yml          # Galaxy dependencies
```

## Error Handling

- Use `ignore_errors: true` sparingly and with `register`
- Prefer `failed_when` for specific failure conditions
- Use `block/rescue` for complex error handling

```yaml
- name: Check Vault
  ansible.builtin.uri:
    url: https://vault.example.com
  ignore_errors: true
  register: vault_check

- name: Get Certificate
  ansible.builtin.get_url:
    url: https://vault.example.com/cert
  when: vault_check.status == 200
```

## Ansible-Lint Configuration

The `.ansible-lint` file configures:
- Profile: `basic`
- Skipped rules: `var-naming`
- Excluded paths: `.git`, `.github`, `.direnv`

## Collections Used

- `chocolatey.chocolatey` - Windows package management
- `community.general` - General utilities (sudoers, etc.)
- `community.docker` - Docker operations
- `kubernetes.core` - Kubernetes operations
