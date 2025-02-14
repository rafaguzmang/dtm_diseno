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
        get_invent = self.env['dtm.diseno.almacen'].search([('caracteristicas','=','herramienta')])
        for record in get_invent:
            get_this = self.env['dtm.herramientas'].search([('nombre','=',record.nombre)],limit=1)
            vals = {'nombre':record.nombre}
            get_this.write(vals) if get_this else get_this.create(vals)
        return res
