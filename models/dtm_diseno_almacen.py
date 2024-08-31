from odoo import api,fields,models,http
from odoo.exceptions import ValidationError
import re
from odoo.http import request


class Materiales(models.Model):
    _name = "dtm.diseno.almacen"
    _description = "Modelo donde se concentrán todos los materiales disponibles en almacén"
    # _rec_name = "nombre"


    # -------------------------------------Datos del material -------------------------------------------------
    nombre = fields.Char(string="Nombre")
    medida = fields.Char(string="Medidas", readonly=False)
    caracteristicas = fields.Char(string="Caracteristicas")
    notas = fields.Text(string="Notas")
    area = fields.Float(string="Área/Largo")

    # --------------------------------------Cantidades, datos para operaciones --------------------------------
    cantidad = fields.Integer(string="Stock", default=0)
    apartado = fields.Integer(string="Proyectado", readonly="True", default=0)
    disponible = fields.Integer(string="Disponible", readonly="True", compute="_compute_disponible" ,store=True)



    campo_nombre = fields.Selection(string="Tipo",selection=[("lamina","Lámina"),("perfileria","Perfilería"),
                                                         ("tornilleria","Tornillería"),("pintura","Pintura"),
                                                         ("llantas","Llantas")])

    perfileria = fields.Selection(string="Perfilería",selection=[("cuadrado","Cuadrado"),("redondo","Redondo"),
                                                                 ("rectangular","Rectangular"),("angulo","Ángulos"),
                                                                 ("ipr","IPR"),("canales","Canales"),
                                                                 ("varilla","Varilla"),("viga","Viga")])

    calibre_id = fields.Selection(string="Calibre", selection = [('10','10'),('11','11'),('12','12'),
                                                                 ('14','14'),('16','16'),('18','18'),
                                                                 ('20','20'),('22','22')])

    material_id = fields.Many2one("odt.diseno.tipomaterial",string="Material")


    @api.depends("cantidad")
    def _compute_disponible(self):#-----------------------------Saca la cantidad del material que hay disponible---------------
        for result in self:
            result.disponible = result.cantidad - result.apartado



    @api.onchange("campo_nombre","material_id","calibre_id")
    def _onchange_especificaciones(self):
        criterio_nombre = ""
        criterio_medida = ""
        if self.campo_nombre:
            criterio_nombre = dict(self._fields['campo_nombre'].selection)[self.campo_nombre]+"%"
        if self.campo_nombre and self.material_id.nombre:
            tipo = dict(self._fields['campo_nombre'].selection)[self.campo_nombre]
            material = self.material_id.nombre
            criterio_nombre = f'{tipo} {material}%'
            if self.calibre_id:
                criterio_medida = f'%@ {self.calibre_id}%'

        medida_120_48 = f'%120.0 x 48.0%%{criterio_medida}%'
        medida_120_36 = f'%120.0 x 36.0%%{criterio_medida}%'
        medida_96_48 = f'%96.0 x 48.0%%{criterio_medida}%'
        medida_96_36 = f'%96.0 x 36.0%%{criterio_medida}%'
        get_campo = self.env['dtm.diseno.almacen'].search([("nombre","like",criterio_nombre), '|', '|', '|',("medida","like",medida_120_48),
                                                                                             ("medida","like",medida_120_36),
                                                                                             ("medida","like",medida_96_48),
                                                                                             ("medida","like",medida_96_36)])
        self.materials_list = get_campo[0].id
        lines = get_campo.mapped("id")
        self.diseno_almacen = [(5,0,{})]
        self.diseno_almacen = [(6,0,lines)]



    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res


    def get_view(self, view_id=None, view_type='form', **options):#Carga los items de todos los módulos de Almacén en un solo módulo de diseño
        res = super(Materiales,self).get_view(view_id, view_type,**options)
        get_almacen = self.env['dtm.diseno.almacen'].search([])
        for item in get_almacen:
            get_lamina = self.env['dtm.materiales'].search([("codigo","=",item.id)])
            if get_lamina:
                item.write({
                    "cantidad": get_lamina.cantidad,
                    "apartado": get_lamina.apartado,
                    "disponible": get_lamina.disponible,
                })

        for find_id in range(1,self.env['dtm.diseno.almacen'].search([], order='id desc', limit=1).id+2):
                if not self.env['dtm.diseno.almacen'].search([("id","=",find_id)]):
                    self.env.cr.execute(f"SELECT setval('dtm_diseno_almacen_id_seq', {find_id}, false);")
                    break
        return res


class MaterialTipo(models.Model):
    _name = "odt.diseno.tipomaterial"
    _description = "Modelo para almacenar los diferentes tipos de materiales"

    nombre = fields.Char()


