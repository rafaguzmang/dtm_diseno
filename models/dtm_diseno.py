from odoo import api,fields,models

class DisenoMateriales(models.Model):
    _name = 'dtm.diseno'


    def _compute_material_id(self): # llena el campo servicios_id con los datos de la tabla requerimientos
        requerimientos = self.env['dtm.materiales'].search([])
        lines = []
        # line = (5,0,{})
        for result in requerimientos:
            line =(4,result.id,{})
            lines.append(line)
        self.material_id = lines

    material_id = fields.Many2many('dtm.materiales.diseno', readonly="True")
    drawingname = fields.Char(string="Drawing Name")
    sheets = fields.Integer(string="Number of Sheets")

    def acction_button(self, view_id=None, view_type='form', **options):
         res = super(DisenoMateriales,self).get_view(view_id, view_type)

         get_info = self.env['dtm.materiales'].search([])
         self.env.cr("DELETE FROM dtm_materiales_diseno")
         print(get_info)
         lines = []
         for result in get_info:
             print(result.id)
             line = (0,0,{
                 'material' : result.material_id.nombre,
                 'calibre' : result.calibre_id.calibre,
                 'largo' : result.largo_id.largo,
                 'ancho' : result.ancho_id.ancho,
                 'cantidad' : result.cantidad,
                 'id' : result.id
             })

             lines.append(line)

         self.material_id = lines

         return res

