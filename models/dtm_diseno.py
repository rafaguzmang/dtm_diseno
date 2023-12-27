from odoo import api,fields,models

class DisenoMateriales(models.Model):
    _name = 'dtm.diseno'

    drawingname  = fields.Char(string="DRAWINGNAME")
    sheets = fields.Char(string="SHEETS")
    material_id = fields.Many2one('dtm.materiales')

    @api.onchange("sheets")
    def _onchange_apartado(self):
        print(self.material_id.id)

        self.env.cr.execute("UPDATE dtm_materiales SET apartado = "+ str(self.sheets) +" WHERE id = " + str(self.material_id.id) )
