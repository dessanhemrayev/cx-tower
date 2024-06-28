# Copyright Cetmix OU
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Cetmix Tower Server Management",
    "summary": "Flexible Server Management directly from Odoo",
    "version": "14.0.0.3.17",
    "category": "Productivity",
    "website": "https://cetmix.com",
    "author": "Cetmix",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "external_dependencies": {
        "python": ["paramiko"],
        "bin": [],
    },
    "depends": [
        "mail",
    ],
    "data": [
        "security/cetmix_tower_server_groups.xml",
        "security/cx_tower_server_security.xml",
        "security/cx_tower_command_security.xml",
        "security/cx_tower_variable_value_security.xml",
        "security/cx_tower_plan_security.xml",
        "security/cx_tower_plan_line_security.xml",
        "security/cx_tower_plan_line_action_security.xml",
        "security/cx_tower_plan_log_security.xml",
        "security/ir.model.access.csv",
        "data/ir_actions_server.xml",
        "data/ir_cron.xml",
        "wizards/cx_tower_command_execute_wizard_view.xml",
        "wizards/cx_tower_plan_execute_wizard_view.xml",
        "views/cx_tower_server_view.xml",
        "views/cx_tower_os_view.xml",
        "views/cx_tower_tag_view.xml",
        "views/cx_tower_interpreter_view.xml",
        "views/cx_tower_variable_view.xml",
        "views/cx_tower_variable_value_view.xml",
        "views/cx_tower_command_view.xml",
        "views/cx_tower_plan_view.xml",
        "views/cx_tower_plan_line_view.xml",
        "views/cx_tower_command_log_view.xml",
        "views/cx_tower_plan_log_view.xml",
        "views/cx_tower_key_view.xml",
        "views/cx_tower_file_view.xml",
        "views/cx_tower_file_template_view.xml",
        "views/menuitems.xml",
    ],
    "demo": [
        "demo/demo_data.xml",
        "demo/demo_file_data.xml",
    ],
}
