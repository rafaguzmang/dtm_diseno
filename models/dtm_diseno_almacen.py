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

    campo_nombre = fields.Selection(string="Item",selection=[("lamina","Lámina"),("perfileria","Perfilería"),
                                                         ("tornilleria","Tornillería"),("pintura","Pintura"),
                                                         ("ruedas","Ruedas")])

    perfileria = fields.Selection(string="Perfilería",selection=[("cuadrado","Cuadrado"),("redondo","Redondo"),
                                                                 ("rectangular","Rectangular"),("angulo","Ángulos"),
                                                                 ("ipr","IPR"),("canales","Canales"),
                                                                 ("varilla","Varilla"),("viga","Viga")])

    calibre_id = fields.Selection(string="Calibre", selection = [('10.0','10'),('11.0','11'),('12.0','12'),
                                                                 ('14.0','14'),('16.0','16'),('18.0','18'),
                                                                 ('20.0','20'),('22.0','22')])

    material_id = fields.Many2one("odt.diseno.tipomaterial",string="Material")
    material_tipo = fields.Many2one("odt.diseno.tipo",string="Tipo")
    perfileria = fields.Selection(string="Perfilería",selection=[("cuadrado","Cuadrado"),("redondo","Redondo"),
                                                          ("rectangular","Rectangular"),("angulo","Ángulos"),
                                                          ("ipr","IPR"),("canales","Canales"),
                                                          ("varilla","Varilla"),("viga","Viga")])

    pintura_tipo = fields.Selection(string="Tipo", selection=[("liquida","Líquida"),("polvo","Polvo"),("aerosol","Aerosol")])
    nombre_pintura = fields.Many2one("odt.diseno.pintura",string="Nombre")

    #---------------------------------------------Dimenciones----------------------------------------------------------------------------
    largo = fields.Float(string="Largo")
    alto = fields.Float(string="Alto")
    ancho = fields.Float(string="Ancho")

    @api.depends("cantidad")
    def _compute_disponible(self):#-----------------------------Saca la cantidad del material que hay disponible---------------
        for result in self:
            result.disponible = result.cantidad - result.apartado

    @api.onchange("campo_nombre","material_id","calibre_id","largo","ancho","perfileria","pintura_tipo","nombre_pintura","material_tipo")
    def _onchange_especificaciones(self):
        selection_dict = dict(self._fields['campo_nombre'].selection)
        valor_nombre = selection_dict.get(self.campo_nombre)

        selection_dict = dict(self._fields['perfileria'].selection)
        valor_perfileria = selection_dict.get(self.perfileria)

        selection_dict = dict(self._fields['pintura_tipo'].selection)
        valor_pintura = selection_dict.get(self.pintura_tipo)
        cantidad = "Litros" if self.pintura_tipo =="liquida" else "Kilos" if self.pintura_tipo == "polvo" else "Latas"

        campo_nombre = valor_perfileria if self.campo_nombre == "perfileria" else valor_nombre
        nombre = f"{campo_nombre if campo_nombre else ''} {self.material_id.nombre if self.material_id else ''} {self.material_tipo.nombre if self.material_tipo else ''} " if campo_nombre != "Pintura" else f"{campo_nombre} {self.nombre_pintura.nombre if self.nombre_pintura else ''} "
        medida = f"{self.largo if self.largo else ''} x {self.ancho if self.ancho else ''} @ {self.calibre_id if self.calibre_id else ''}" if campo_nombre != "Pintura" else f"{valor_pintura} en {cantidad}"
        self.nombre = nombre
        self.medida = medida if medida else ''

    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res


    def get_view(self, view_id=None, view_type='form', **options):#Carga los items de todos los módulos de Almacén en un solo módulo de diseño
        res = super(Materiales,self).get_view(view_id, view_type,**options)
        get_almacen = self.env['dtm.diseno.almacen'].search([])
        modelos = ['dtm.materiales',"dtm.materiales.angulos","dtm.materiales.solera","dtm.materiales.rodamientos","dtm.materiales.pintura","dtm.materiales.perfiles","dtm.materiales.otros","dtm.materiales.maquinados","dtm.materiales.canal","dtm.materiales.tornillos","dtm.materiales.tubos","dtm.materiales.varilla"]
        for item in get_almacen:
            item.write({
                "cantidad":0,
                "apartado":0,
                "disponible":0,
            })
            for modelo in modelos:
                get_lamina = self.env[modelo].search([("codigo","=",item.id)])
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
    _description = "Modelo para almacenar los diferentes tipos de items"
    _rec_name = "nombre"

    nombre = fields.Char()

class Pintura(models.Model):
    _name = "odt.diseno.pintura"
    _description = "Modelo para almacenar los diferentes tipos de pintura"
    _rec_name = "nombre"

    nombre = fields.Char()

class TipoMaterial(models.Model):
    _name = "odt.diseno.tipo"
    _description = "Modelo para almacenar los diferentes tipos de materiales"
    _rec_name = "nombre"

    nombre = fields.Char()


