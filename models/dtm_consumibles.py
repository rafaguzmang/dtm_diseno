from odoo import api,models,fields


class Consumibles(models.Model):
    _name = 'dtm.consumibles'
    _description = 'Registro para llevar la lista de los consumibles'
    _rec_name = 'nombre'
    _order = 'id'

    nombre = fields.Char(string='Material', readonly=True)
    cantidad = fields.Integer(string="Stock", readonly=False)
    minimo = fields.Integer(string="Mínimo", readonly=False)
    maximo = fields.Integer(string="Máximo", readonly=False)

    # Se usa esta función para traer todos los materiales del inventario
    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Consumibles, self).get_view(view_id, view_type, **options)


        consumibles = self.env['dtm.diseno.almacen'].search([('caracteristicas', '=', 'consumible')])

        for consumible in consumibles:
            thisconsumible = self.env['dtm.consumibles'].search([('id', '=', consumible.id)], limit=1)
            if thisconsumible:
                thisconsumible.write({'nombre': consumible.nombre})
            else:
                self.env.cr.execute(f"SELECT setval('dtm_consumibles_id_seq', {consumible.id}, false);")
                self.env['dtm.consumibles'].create({'nombre': consumible.nombre})

        return res

class HistorialConsumibles(models.Model):
    _name = 'dtm.consumibles.historial'
    _description = 'Modelo para llevar el historial de los consumibles'

    codigo = fields.Integer(string="Código", readonly=True)
    nombre = fields.Char(string='Material', readonly=True)
    cantidad = fields.Integer(string="Entregado", readonly=True)
    recibe = fields.Char(string='Recibe',readonly=True)
    notas = fields.Char(string='Notas',readonly=True)
