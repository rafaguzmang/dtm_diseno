from odoo import api,fields,models

class Herramientas(models.Model):
    _name = 'dtm.herramientas'
    _description = 'Registro de herramientas'
    _rec_name = ''

    nombre = fields.Char(string='Nombre')
    cantidad = fields.Integer(string='Cantidad')
    responsable = fields.Char(string='Responsable')
    fecha_adquisicion = fields.Date(string='Fecha de adquisición')
    notas = fields.Text(string='Notas')

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Herramientas,self).get_view(view_id, view_type,**options)
        herramientas = self.env['dtm.diseno.almacen'].search([('caracteristicas','=','herramienta')])
        for herramienta in herramientas:
            thisHerramientas = self.env['dtm.herramientas'].search([('nombre','=',herramienta.nombre)],limit=1)
            vals = {'nombre':herramienta.nombre}
            thisHerramientas.write(vals) if thisHerramientas else thisHerramientas.create(vals)


        return res
