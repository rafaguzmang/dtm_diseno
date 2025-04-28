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
    minimo = fields.Integer(string="Mínimo", readonly=True)
    maximo = fields.Integer(string="Máximo", readonly=True)

    def name_get(self):
        res = []
        for result in self:
            res.append((result.id,f"{result.id} {result.nombre} {result.medida}"))
        return res


    # Se usa esta función para traer todos los materiales del inventario
    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Materiales, self).get_view(view_id, view_type, **options)

        inventario_ids = self.env['dtm.diseno.almacen'].search([('caracteristicas','not in',['consumible','herramienta'])]).mapped('id')
        materiales_existentes = self.env['dtm.materiales'].search([('id','in',inventario_ids)])
        diccionario = {mat.id:mat for mat in materiales_existentes}
        invetarioMateriales = self.env['dtm.diseno.almacen'].browse(inventario_ids)

        for item in invetarioMateriales:

            materiales = diccionario.get(item.id)
            # if materiales:
            #     materiales.write({'nombre':item.nombre,
            #                       'medida':item.medida or '',
            #                       'cantidad':item.cantidad,
            #                       'apartado':item.apartado,
            #                       'disponible':item.disponible})
            # else:
            #     self.env.cr.execute(f"SELECT setval('dtm_materiales_id_seq', {item.id}, false);")
            #     materiales.create({'id': item.id,
            #                        'nombre': item.nombre,
            #                        'medida': item.medida or '',
            #                        'cantidad': item.cantidad,
            #                        'apartado': item.apartado,
            #                        'disponible': item.disponible})

        # inventario = self.env['dtm.diseno.almacen'].search([]).mapped('id')
        # materiales = self.env['dtm.materiales'].search([('id','not in',inventario)])
        # print(materiales)
        return res

