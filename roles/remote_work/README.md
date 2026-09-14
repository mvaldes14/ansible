# remote_work

Prepares Linux machines for remote work sessions.

## What it does

- Installs core CLI/dev packages (`git`, `tmux`, `neovim`, `ripgrep`, `fd`, `jq`, Node/npm, Python venv support, etc.)
- Installs Herdr with `curl -fsSL https://herdr.dev/install.sh | sh`
- Installs pi with `curl -fsSL https://pi.dev/install.sh | sh`
- Installs Obsidian Headless with `npm install -g obsidian-headless`
- Creates the remote workspace under `~/git`
- Clones missing core repos and runs `git pull --ff-only` on every execution
- Optionally clones/pulls the Obsidian vault
- Optionally clones/pulls extra work repos
- Runs the dotfiles AI bootstrap to link shared AI config

## Variables

```yaml
remote_work_user: mvaldes
remote_work_workspace_dir: /home/mvaldes/git
remote_work_dotfiles_repo: git@github.com:mvaldes14/dotfiles.git
remote_work_install_herdr: true
remote_work_install_pi: true
remote_work_install_obsidian_headless: true
remote_work_core_repositories:
  - name: dotfiles
    repo: git@github.com:mvaldes14/dotfiles.git
    dest: /home/mvaldes/git/dotfiles
    version: main
  - name: ansible
    repo: git@github.com:mvaldes14/ansible.git
    dest: /home/mvaldes/git/ansible
    version: main
remote_work_obsidian_vault_repo: "" # set to clone vault
remote_work_obsidian_vault_dir: /home/mvaldes/Obsidian/wiki
remote_work_repositories: []
remote_work_run_ai_bootstrap: true
```

## Run

```bash
ansible-playbook -i inventory/homelab.ini playbooks/remote-work.yaml --check
ansible-playbook -i inventory/homelab.ini playbooks/remote-work.yaml
```

Limit to one host:

```bash
ansible-playbook -i inventory/homelab.ini playbooks/remote-work.yaml --limit eva01
```
