import yaml

from odoo.tests import TransactionCase


class TestTowerCommand(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.Command = self.env["cx.tower.command"]

        # Expected YAML content of the test command
        self.command_test_yaml = """access_level: manager
action: ssh_command
allow_parallel_run: false
cetmix_tower_model: command
cetmix_tower_yaml_version: 1
code: |-
  cd /home/{{ tower.server.ssh_username }} \\
  && ls -lha
file_template_id: false
name: Test YAML
note: |-
  Test YAML command conversion.
  Ensure all fields are rendered properly.
path: false
reference: test_yaml_in_tests
"""

        # YAML content translated into Python dict
        self.command_test_yaml_dict = yaml.safe_load(self.command_test_yaml)

    def test_yaml_from_command(self):
        """Test if YAML is generated properly from a command"""

        # -- 0 --
        # Create test command
        # Test command
        command_test = self.Command.create(
            {
                "name": "Test YAML",
                "reference": "test_yaml_in_tests",
                "action": "ssh_command",
                "code": """cd /home/{{ tower.server.ssh_username }} \\
&& ls -lha""",
                "note": """Test YAML command conversion.
Ensure all fields are rendered properly.""",
            }
        )

        # -- 1 --
        # Check it YAML generated by the command matches
        # YAML from the template file

        self.assertEqual(
            command_test.yaml_code,
            self.command_test_yaml,
            "YAML generated from command doesn't match template file one",
        )

        # -- 2 --
        # Check if YAML key values match Cetmix Tower ones

        self.assertEqual(
            command_test.access_level,
            self.Command.TO_TOWER_ACCESS_LEVEL[
                self.command_test_yaml_dict["access_level"]
            ],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.action,
            self.command_test_yaml_dict["action"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.allow_parallel_run,
            self.command_test_yaml_dict["allow_parallel_run"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            self.Command.CETMIX_TOWER_YAML_VERSION,
            self.command_test_yaml_dict["cetmix_tower_yaml_version"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.code,
            self.command_test_yaml_dict["code"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.name,
            self.command_test_yaml_dict["name"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.note,
            self.command_test_yaml_dict["note"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.path,
            self.command_test_yaml_dict["path"],
            "YAML value doesn't match Cetmix Tower one",
        )
        self.assertEqual(
            command_test.reference,
            self.command_test_yaml_dict["reference"],
            "YAML value doesn't match Cetmix Tower one",
        )

    def test_command_from_yaml(self):
        """Test if YAML is generated properly from a command"""

        def test_yaml(command):
            """Checks if yaml values are inserted correctly

            Args:
                command(cx.tower.command): _description_
            """
            self.assertEqual(
                command.access_level,
                self.Command.TO_TOWER_ACCESS_LEVEL[
                    self.command_test_yaml_dict["access_level"]
                ],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.action,
                self.command_test_yaml_dict["action"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.allow_parallel_run,
                self.command_test_yaml_dict["allow_parallel_run"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                self.Command.CETMIX_TOWER_YAML_VERSION,
                self.command_test_yaml_dict["cetmix_tower_yaml_version"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.code,
                self.command_test_yaml_dict["code"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.name,
                self.command_test_yaml_dict["name"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.note,
                self.command_test_yaml_dict["note"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.path,
                self.command_test_yaml_dict["path"],
                "YAML value doesn't match Cetmix Tower one",
            )
            self.assertEqual(
                command.reference,
                self.command_test_yaml_dict["reference"],
                "YAML value doesn't match Cetmix Tower one",
            )

        # Create test command
        command_test = self.Command.create(
            {"name": "New Command", "action": "python_code"}
        )

        # -- 1 --
        # Insert YAML into the command and
        #   check if YAML key values match Cetmix Tower ones
        command_test.yaml_code = self.command_test_yaml
        test_yaml(command_test)

        # -- 2 --
        #  Insert some non supported keys and ensure nothing bad happens
        yaml_with_non_supported_keys = """access_level: manager
action: ssh_command
doge: wow
memes: much nice!
allow_parallel_run: false
cetmix_tower_model: command
cetmix_tower_yaml_version: 1
code: |-
  cd /home/{{ tower.server.ssh_username }} \\
  && ls -lha
file_template_id: false
name: Test YAML
note: |-
  Test YAML command conversion.
  Ensure all fields are rendered properly.
path: false
reference: test_yaml_in_tests
"""
        command_test.yaml_code = yaml_with_non_supported_keys
        test_yaml(command_test)

    def test_command_with_action_file_template(self):
        """Test command with 'File from template' action"""
        yaml_with_reference = """access_level: manager
action: file_using_template
allow_parallel_run: false
cetmix_tower_model: command
cetmix_tower_yaml_version: 1
code: false
file_template_id: my_custom_test_template
name: Such Much Command
note: Just a note
path: false
reference: such_much_test_command
"""
        # Add file template
        file_template = self.env["cx.tower.file.template"].create(
            {
                "name": "Such much demo",
                "reference": "my_custom_test_template",
                "file_name": "much_logs.txt",
                "server_dir": "/var/log/my/files",
                "source": "tower",
                "file_type": "text",
                "note": "Hey!",
                "keep_when_deleted": False,
            }
        )
        command_with_template = self.Command.create(
            {
                "name": "Such Much Command",
                "reference": "such_much_test_command",
                "action": "file_using_template",
                "note": "Just a note",
                "file_template_id": file_template.id,
            }
        )

        # -- 1 --
        # Check if final YAML composed correctly
        self.assertEqual(
            command_with_template.yaml_code,
            yaml_with_reference,
            "YAML is not composed correctly",
        )

        # -- 2 --
        # Explode related record and check the YAML

        yaml_with_reference_exploded = """access_level: manager
action: file_using_template
allow_parallel_run: false
cetmix_tower_model: command
cetmix_tower_yaml_version: 1
code: false
file_template_id:
  cetmix_tower_model: file_template
  cetmix_tower_yaml_version: 1
  code: false
  file_name: much_logs.txt
  file_type: text
  keep_when_deleted: false
  name: Such much demo
  note: Hey!
  reference: my_custom_test_template
  server_dir: /var/log/my/files
  source: tower
name: Such Much Command
note: Just a note
path: false
reference: such_much_test_command
"""
        command_with_template.write({"yaml_explode": True})
        command_with_template.invalidate_cache(["yaml_code"])
        self.assertEqual(
            command_with_template.yaml_code,
            yaml_with_reference_exploded,
            "YAML is not composed correctly",
        )
