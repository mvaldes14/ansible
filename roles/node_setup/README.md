# node_setup

Linux baseline: SSH access, Tailscale, MOTD, zsh, Oh My Zsh, shell plugins and
Starship. Kubernetes integration belongs to `k8s_node`; agent tooling belongs to
`remote_work`.

## Shell ownership

Dotfiles is the source of truth for shell configuration. The role clones the
public repo over HTTPS (no GitHub SSH credentials needed), then links:

- `~/.zshenv` → `~/git/dotfiles/.zshenv`
- `~/.config/zsh` → `~/git/dotfiles/.config/zsh`

Existing files/directories are preserved at `<path>.pre-ansible-dotfiles`.
Conflicting backups cause a failure rather than data loss. Legacy `~/.zshrc`
is left untouched; `ZDOTDIR` selects the dotfiles configuration instead.
The role no longer rewrites plugin lists, PATH or prompt initialization in zshrc.
It installs the custom plugins used by dotfiles. Shell configuration changes
belong in dotfiles, not this role.

Existing checkouts are not pulled by default. Enable updates deliberately during
provisioning, never as part of monthly maintenance. Local changes are not forced
away. Existing SSH-origin checkouts may still require working SSH credentials.

## Variables

```yaml
node_setup_dotfiles_repo: https://github.com/mvaldes14/dotfiles.git
node_setup_dotfiles_dir: /home/mvaldes/git/dotfiles
node_setup_dotfiles_version: main
node_setup_dotfiles_update: false
node_setup_install_tailscale: true
node_setup_tailscale_auth_key: "" # supply through secrets when auto-joining
node_setup_tailscale_up_args: []
pihole_enabled: false
```

The target user/home must exist (the existing inventory assumes `mvaldes`).
Run `task bootstrap LIMIT=eva01`. See `defaults/main.yml` for shell dependency
settings. Molecule uses local Git fixtures and verifies effective zsh startup,
backup preservation and repeat convergence.
