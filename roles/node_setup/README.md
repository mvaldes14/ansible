Role Name
=========

Common Linux node baseline for homelab machines.

Includes SSH access, Tailscale package/service setup, MOTD, CNI path setup, zsh, and Oh My Zsh.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

Key variables:

```yaml
node_setup_install_tailscale: true
node_setup_tailscale_channel: stable
node_setup_tailscale_auth_key: "" # optional; auto-joins if set from secrets
node_setup_tailscale_up_args: []
pihole_enabled: false
```

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
