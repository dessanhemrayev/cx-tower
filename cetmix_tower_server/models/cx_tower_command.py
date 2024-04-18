# Copyright (C) 2022 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class CxTowerCommand(models.Model):
    _name = "cx.tower.command"
    _inherit = "cx.tower.template.mixin"
    _description = "Cetmix Tower Command"
    _order = "name"

    active = fields.Boolean(default=True)
    name = fields.Char()
    allow_parallel_run = fields.Boolean(
        help="If enabled command can be run on the same server "
        "while the same command is still running.\n"
        "Returns ANOTHER_COMMAND_RUNNING if execution is blocked"
    )
    interpreter_id = fields.Many2one(
        comodel_name="cx.tower.interpreter",
    )
    server_ids = fields.Many2many(
        comodel_name="cx.tower.server",
        relation="cx_tower_server_command_rel",
        column1="command_id",
        column2="server_id",
        string="Servers",
    )
    tag_ids = fields.Many2many(
        comodel_name="cx.tower.tag",
        relation="cx_tower_command_tag_rel",
        column1="command_id",
        column2="tag_id",
        string="Tags",
    )
    os_ids = fields.Many2many(
        comodel_name="cx.tower.os",
        relation="cx_tower_os_command_rel",
        column1="command_id",
        column2="os_id",
        string="OSes",
    )
    note = fields.Text()

    access_level = fields.Selection(
        [
            ("1", "User"),
            ("2", "Manager"),
            ("3", "Root"),
        ],
        string="Access Level",
        default="2",
        groups="cetmix_tower_server.group_root,cetmix_tower_server.group_manager",
        required=True,
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = default or {}
        default["name"] = _("%(cmd)s (copy)", cmd=self.name)
        return super(CxTowerCommand, self).copy(default=default)

    def name_get(self):
        # Add 'command_show_server_names' context key
        # to append server names to command
        if not self._context.get("command_show_server_names"):
            return super().name_get()
        res = []
        for rec in self:
            if rec.server_ids:
                name = "{} ({})".format(
                    rec.name, ",".join(rec.server_ids.mapped("name"))
                )
            else:
                name = rec.name
            res.append((rec.id, name))
        return res
