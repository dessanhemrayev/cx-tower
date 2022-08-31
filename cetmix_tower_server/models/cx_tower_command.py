from odoo import _, api, fields, models


class CxTowerCommand(models.Model):
    _name = "cx.tower.command"
    _inherit = "cx.tower.template.mixin"
    _description = "Cetmix Tower Command"
    _order = "name"

    active = fields.Boolean(default=True)
    name = fields.Char()
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

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = default or {}
        default["name"] = _("%s (copy)", self.name)
        # Do not assign to an archived user
        return super(CxTowerCommand, self).copy(default=default)