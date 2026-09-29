# Overview

Repo used to install and normalize some of the common tasks done in new machines.

# Playbooks

| Playbook | Purpose |
| --- | --- |
| `bootstrap.yaml` | Linux baseline, SSH/Tailscale/MOTD, shell dependencies and dotfiles links |
| `k8s-node.yaml` | CNI path integration for explicitly inventoried `k8s_nodes`; does not install k3s |
| `remote-work.yaml` | Agent/dev tooling and work repositories; run after bootstrap |
| `maintenance.yaml` | Serial package upgrades and required reboots; no bootstrap or repository updates |
| `demo.yaml` | Scratch playbook used for recordings |

```bash
task bootstrap LIMIT=eva01
task k8s-node LIMIT=eva01
task remote-work LIMIT=eva01
task maintenance LIMIT=eva01 -- --check  # preflight only, not an upgrade simulation
task maintenance LIMIT=homelab_nodes
```

Run bootstrap, Kubernetes integration (cluster nodes only), then remote work in
sequence when provisioning. Maintenance runs independently afterward.

Task wrappers require an explicit `LIMIT`; arguments after `--` pass to Ansible.
Direct playbook runs still require `ANSIBLE_ROLES_PATH=$PWD/roles` when not using Task.
Use `task deps` to provide the controller's Kubernetes Python client at `.venv/bin/python`.
Override `node_maintenance_python` if using another controller interpreter.

## Rolling Maintenance

All six current homelab nodes are explicitly listed in `k8s_nodes`. Keep this group
accurate: other `homelab_nodes` receive OS maintenance without Kubernetes calls.
Override `node_maintenance_node_name` when Kubernetes and inventory names differ.
The controller needs a working kubeconfig and permission to inspect nodes,
cordon/uncordon and evict pods.

For each node: require all cluster nodes Ready → drain → safe apt upgrades → reboot
if `/var/run/reboot-required` exists → wait for Node Ready → restore schedulability
→ verify cluster readiness. Non-Kubernetes hosts skip the cluster operations.
`serial: 1` and `any_errors_fatal: true` stop rollout on failure. Previously cordoned
nodes remain cordoned. Failure does **not** automatically uncordon unhealthy nodes;
inspect the failure and node before manual recovery. Cluster readiness checks do
not guarantee application health; monitor workloads during a maintenance window.

Drain respects PodDisruptionBudgets and refuses unmanaged pods. EmptyDir deletion
is disabled by default. If disposable EmptyDir data is acceptable, explicitly set
`node_maintenance_delete_emptydir_data: true` in inventory or extra vars. Do not
bypass a failed drain to continue updates. `node_maintenance_force_reboot: true`
reboots even without the Debian/Ubuntu reboot marker.

The `maintenance` tag selects the **entire** maintenance sequence; individual
steps have no separate tags. Do not use `--start-at-task` or custom skip-tags to
bypass safety steps. Check mode performs cluster preflight
only and makes no maintenance changes.

Schedule from **one controller**, using its scheduler's no-overlap/concurrency
control, captured logs and failure notifications. For example, a monthly job can
run `task maintenance LIMIT=homelab_nodes` from this repository with the controller's
kubeconfig available. Provisioning/agent installers are deliberately excluded.
No schedule is installed by this repository.

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
