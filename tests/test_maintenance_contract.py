"""Local safety-contract tests; these do not contact hosts or Kubernetes."""
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return yaml.safe_load((ROOT / path).read_text())


class MaintenanceContract(unittest.TestCase):
    def setUp(self):
        self.play = load('playbooks/maintenance.yaml')[0]
        self.tasks = load('roles/node_maintenance/tasks/main.yml')
        self.maintenance = next(t for t in self.tasks if 'block' in t)
        self.steps = self.maintenance['block']

    def test_rollout_is_serial_and_fail_closed(self):
        self.assertEqual(self.play['serial'], 1)
        self.assertTrue(self.play['any_errors_fatal'])
        self.assertIn('ansible.builtin.fail', self.maintenance['rescue'][0])
        self.assertNotIn('always', self.maintenance)

    def test_maintenance_tag_selects_whole_role(self):
        self.assertEqual(self.play['roles'][0]['tags'], ['maintenance'])
        self.assertFalse(any('tags' in task for task in self.steps))

    def test_order_protects_updates_and_readiness(self):
        self.assertEqual([t['name'] for t in self.steps], [
            'Drain Kubernetes Node', 'Upgrade System Packages',
            'Check Whether Reboot Is Required', 'Reboot Node When Required',
            'Wait For Kubernetes Node Readiness', 'Restore Original Schedulability',
            'Verify Cluster Before Continuing'])

    def test_drain_does_not_force(self):
        drain = self.steps[0]['kubernetes.core.k8s_drain']['delete_options']
        self.assertFalse(drain['force'])
        defaults = load('roles/node_maintenance/defaults/main.yml')
        self.assertFalse(defaults['node_maintenance_delete_emptydir_data'])

    def test_preserves_preexisting_cordon(self):
        self.assertIn('not (node_maintenance_was_cordoned | default(true) | bool)',
                      self.steps[5]['when'])
        self.assertIn('Remember Initial Scheduling State',
                      [t['name'] for t in self.tasks[:3]])

    def test_non_cluster_nodes_skip_cluster_operations(self):
        for task in (self.steps[0], self.steps[4], self.steps[5], self.steps[6]):
            self.assertIn('node_maintenance_kubernetes | bool', task['when'])

    def test_check_mode_skips_mutations(self):
        self.assertEqual(self.maintenance['when'], 'not ansible_check_mode')

    def test_no_provisioning_in_maintenance(self):
        self.assertEqual(self.play['roles'][0]['role'], 'node_maintenance')
        content = (ROOT / 'roles/node_maintenance/tasks/main.yml').read_text()
        for forbidden in ('ansible.builtin.git:', 'node_setup', 'remote_work', 'curl'):
            self.assertNotIn(forbidden, content)

    def test_roles_have_separate_entrypoints(self):
        expected = {'bootstrap': 'node_setup', 'k8s-node': 'k8s_node',
                    'remote-work': 'remote_work'}
        for play, role in expected.items():
            self.assertEqual(load(f'playbooks/{play}.yaml')[0]['roles'], [{'role': role}])
        self.assertNotIn('cni.yml',
                         (ROOT / 'roles/node_setup/tasks/main.yml').read_text())


if __name__ == '__main__':
    unittest.main()
