from odoo import fields,api,models

class Consumibles(models.Model):
    _name = 'dtm.diseno.consumibles'
    _description = 'Modelo para llevar el conteo de los consumibles'

    codigo = fields.Integer(strind="ID")
    nombre = fields.Char(string="Nombre")
    caracteristicas = fields.Char(string="Caracteristicas")
    cantidad = fields.Integer(string="Stock", default=0)
    minimo = fields.Integer(string="Minimo", default=5)
    localizacion = fields.Char(string="Localización")
    entregado = fields.Char(string="Entregado")
    recibe = fields.Char(string="Recibe")
    notas = fields.Text(string="Notas")

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Consumibles, self).get_view(view_id, view_type, **options)

        get_almacen = self.env['dtm.diseno.almacen'].search([('caracteristicas','=','consumible')])
        # print(get_almacen)
        get_consumibles = self.env['dtm.diseno.consumibles'].search([])
        consumibles_list = self.env['dtm.diseno.consumibles'].search([]).mapped('id')
        for item in get_almacen:
            if item.id in consumibles_list:
                self.env['dtm.diseno.consumibles'].search([('codigo','=',item.id)]).write({
                    'codigo':item.id,
                    'nombre':item.nombre,
                    'cantidad':item.cantidad,
                    'localizacion':item.localizacion,
                })
            else:
                self.env['dtm.diseno.consumibles'].create({
                    'codigo':item.id,
                    'nombre':item.nombre,
                    'cantidad':item.cantidad,
                    'minimo':5,
                    'localizacion':item.localizacion,

                })


        return res


