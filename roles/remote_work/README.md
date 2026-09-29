# remote_work

Prepares Linux machines for remote work sessions after `bootstrap.yaml`.
This playbook does not rerun the node baseline. `node_setup` owns the dotfiles
checkout and shell links; this role only consumes its AI bootstrap script.

## What it does

- Installs remote-dev packages (`git`, `tmux`, `neovim`, `ripgrep`, `fd`, `jq`, `bat`, `eza`, `atuin`, `stow`, Python venv support, etc.); baseline shell setup (`zsh`, `fzf`, `zoxide`, Starship, Oh My Zsh) lives in `node_setup`
- Installs Node.js 22 from NodeSource before installing pi, because pi's installer requires Node.js 22.19.0+ in non-interactive sessions
- Installs Herdr with `curl -fsSL https://herdr.dev/install.sh | sh`
- Installs mise with `curl -fsSL https://mise.run | sh` and links it into `/usr/local/bin`
- Installs Go Task with `curl -fsSL https://taskfile.dev/install.sh | sh -s -- -d -b /usr/local/bin`
- Installs pi with bounded curl/install timeouts and only retries when no usable pi binary exists
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
remote_work_sync_repositories: true
remote_work_dotfiles_dir: /home/mvaldes/git/dotfiles
remote_work_manage_nodejs: true
remote_work_nodejs_major_version: 22
remote_work_nodejs_min_version: 22.19.0
remote_work_install_herdr: true
remote_work_install_mise: true
remote_work_mise_install_script: https://mise.run
remote_work_mise_bin: /home/mvaldes/.local/bin/mise
remote_work_install_task: true
remote_work_install_pi: true
remote_work_pi_install_marker: /home/mvaldes/.local/share/pi-node
remote_work_pi_install_timeout: 300
remote_work_pi_curl_connect_timeout: 20
remote_work_pi_curl_max_time: 120
remote_work_install_obsidian_headless: true
remote_work_core_repositories:
  - name: ansible
    repo: git@github.com:mvaldes14/ansible.git
    dest: /home/mvaldes/git/ansible
    version: main
remote_work_obsidian_vault_repo: "" # set to clone vault
remote_work_obsidian_vault_dir: /home/mvaldes/Obsidian/wiki
remote_work_repositories: []
remote_work_run_ai_bootstrap: true
```

## Project Toolchains

Use checked-in `.mise.toml` files for project-specific Python, Go, and Node/TypeScript versions:

```toml
[tools]
python = "3.12"
go = "1.23"
node = "22"
uv = "latest"
pnpm = "latest"
```

Then run `mise trust && mise install` inside the repo.

## Run

```bash
ansible-playbook -i inventory/homelab.ini playbooks/remote-work.yaml --check
ansible-playbook -i inventory/homelab.ini playbooks/remote-work.yaml
```

Limit to one host:

```bash
ansible-playbook -i inventory/homelab.ini playbooks/remote-work.yaml --limit eva01
```
