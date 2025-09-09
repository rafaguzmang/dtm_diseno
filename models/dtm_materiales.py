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
    mostrador = fields.Float(string="Mostrador")
    mayoreo = fields.Float(string="Mayoreo")
    localizacion = fields.Char(string="Localización")

    def name_get(self):
        res = []
        for result in self:
            res.append((result.id,f"{result.id} {result.nombre} {result.medida}"))
        return res


    # Se usa esta función para traer todos los materiales del inventario
    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Materiales, self).get_view(view_id, view_type, **options)
        # for find_id in range(1, self.env['dtm.materiales'].search([], order='id desc', limit=1).id + 1):
        #     if not self.env['dtm.materiales'].search([("id", "=", find_id)]):
        #         self.env.cr.execute(f"SELECT setval('dtm.materiales_id_seq', {find_id}, false);")
        #         break

        return res

