from odoo import api,models,fields

class Materiales(models.Model):
    _name = 'dtm.materiales'
    _description = 'Registro para llevar la lista de los materiales materiales'
    _rec_name = 'nombre'
    _order = 'id'

    nombre = fields.Char(string='Material', readonly=True)
    medida = fields.Char(string='Medida',readonly=True)
    cantidad = fields.Integer(string="Stock",readonly=True)
    apartado = fields.Integer(string="Proyectado", readonly=True)
    disponible = fields.Integer(string="Disponible", readonly=True)
    minimo = fields.Integer(string="Minimo", readonly=True)


    # Se usa esta función para traer todos los materiales del inventario
    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Materiales, self).get_view(view_id, view_type, **options)

        inventarioMateriales = self.env['dtm.diseno.almacen'].search([('caracteristicas','!=','consumible'),('caracteristicas','!=','herramienta')])
        for item in inventarioMateriales:
            materiales = self.env['dtm.materiales'].search([('id','=',item.id)])
            if materiales:
                materiales.write({'nombre':item.nombre,'medida':item.medida if item.medida else '','cantidad':item.cantidad,'apartado':item.apartado,'disponible':item.disponible})
            else:
                materiales.create(
                    {'id': item.id, 'nombre': item.nombre, 'medida': item.medida if item.medida else '','cantidad': item.cantidad, 'apartado': item.apartado, 'disponible': item.disponible})


        return res

