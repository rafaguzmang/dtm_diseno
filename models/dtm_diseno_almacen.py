from odoo import api,fields,models,http
from odoo.exceptions import ValidationError
import re
from odoo.http import request


class Materiales(models.Model):
    _name = "dtm.diseno.almacen"
    _description = "Modelo donde se concentrán todos los materiales disponibles en almacén"
    _rec_name = "nombre"

    # -------------------------------------Datos del material -------------------------------------------------
    nombre = fields.Char(string="Nombre", readonly=True)
    medida = fields.Char(string="Medidas", readonly=True)
    caracteristicas = fields.Char(string="Caracteristicas")
    notas = fields.Text(string="Notas")
    area = fields.Float(string="Área/Largo")

    # --------------------------------------Cantidades, datos para operaciones --------------------------------
    cantidad = fields.Integer(string="Stock", default=0)
    apartado = fields.Integer(string="Proyectado", readonly="True", default=0)
    # disponible = fields.Integer(string="Disponible", readonly="True", compute="_compute_disponible" ,store=True)
    disponible = fields.Integer(string="Disponible", readonly="True",store=True)
    #---------------------------------------Tipo de item ------------------------------------------------------
    campo_nombre = fields.Selection(string="Item",selection=[("lamina","Lámina"),("perfil","Perfil"),("placa","Placa"),
                                                         ("tornillo","Tornillo"),("pintura","Pintura"),
                                                         ("ruedas","Ruedas")])

    calibre = fields.Selection(string="Calibre", selection = [('10.0',10.0),('11.0',11.0),('12.0',12.0),
                                                                 ('14.0',14.0),('16.0',16.0),('18.0',18.0),
                                                                 ('20.0',20.0),('22.0',22.0)])
    #-----------------------------------------------------Materiales-------------------------------------------------------------------
    material = fields.Selection(string="Material", selection=[('carbon','Acero al Carbón'),('inoxidable','Inoxidable'),('galvanizado','Galvanizado'),
                                                              ('aluminio','Aluminio')])
    tipo_carbon = fields.Selection(string="tipo", selection=[('carbona36','ASTM A36'),('carbona570','ASTM A570 Grado 50')])
    tipo_inoxidable = fields.Selection(string="tipo", selection=[('inoxidable304','304'),('inoxidable316','316'),('inoxidable430','430')])
    tipo_aluminio = fields.Selection(string="tipo", selection=[('aluminio303','303'),('aluminio552','552')])

    acabado_carbon = fields.Selection(string="tipo", selection=[('antiderrapante','Antiderrapante'),('decapado','Decapado')])
    acabado_inoxidable = fields.Selection(string="tipo", selection=[('reflejante','Reflejante'),('pulido','Pulido')])
    acabado_aluminio = fields.Selection(string="tipo", selection=[('reflejante','Reflejante'),('pulido','Pulido'),('mate','Mate'),('natural','Natural')])

    clasificacion_id = fields.Many2one("odt.diseno.clasificacion",string="Clasificación")
    #------------------Otros--------------
    pintura_tipo = fields.Selection(string="Tipo", selection=[("liquida","Líquida"),("polvo","Polvo"),("aerosol","Aerosol")])
    nombre_pintura = fields.Many2one("odt.diseno.pintura",string="Nombre")

    #---------------------------------------------Dimenciones Lámina----------------------------------------------------------------------------
    largo = fields.Selection(string="Alto", selection=[('120.0',120),('96',96)])
    ancho = fields.Selection(string="Ancho", selection=[('48.0',48),('36.0',36)])
    #---------------------------------------------Dimenciones Perfil----------------------------------------------------------------------------
    largo_perfil = fields.Integer(string="Largo", default=236.0)
    seccion_perfil_cuadrado = fields.Selection(string="Sección", selection=[('1x1','1.0 x 1.0'),('125x125','1.25 x 1.25'),('15x15','1.5 x 1.5'),('2x2','2.0 x 2.0'),('25x25','2.5 x 2.5'),('3x3','3.0 x 3.0'),('35x35','3.5 x 3.5'),('4x4','4.0 x 4.0'),
                                                            ('45x45','4.5 x 4.5'),('5x5','5.0 x 5.0'),('6x6','6.0 x 6.0'),('7x7','7.0 x 7.0'),('8x8','8.0 x 8.0'),('10x10','10.0 x 10.0'),('12x12','12.0 x 12.0'),('14x14','14.0 x 14.0'),
                                                            ('16x16','16.0 x 16.0')])
    seccion_perfil_rectangular = fields.Selection(string="Sección", selection=[('3x2','3.0 x 2.0'),('4x2','4.0 x 2.0'),('4x3','4.0 x 3.0'),('5x3','5.0 x 3.0'),('6x2','6.0 x 2.0'),('6x3','6.0 x 3.0'),('6x4','6.0 x 4'),('7x5','7.0 x 5.0'),
                                                            ('8x4','8.0 x 4.0'),('8x6','8.0 x 6.0'),('10x2','10.0 x 2.0'),('10x4','10.0 x 4.0'),('10x6','10.0 x 6.0'),('12x2','12.0 x 2.0'),('12x4','12.0 x 4.0'),('12x6','12.0 x 6.0'),
                                                            ('12x8','12.0 x 8.0'),('14x4','14.0 x 4.0'),('14x6','14.0 x 6.0')
                                                            ])
    perfileria = fields.Selection(string="Perfilería",selection=[("angulo","Ángulos"),("canales","Canales"),("cuadrado","Cuadrado"),
                                                                 ("ipr","IPR"),("redondo","Redondo"),("rectangular","Rectangular"),
                                                                 ("varilla","Varilla"),("viga","Viga")])

    @api.onchange("campo_nombre","material","tipo_carbon","tipo_inoxidable","tipo_aluminio","acabado_carbon","acabado_inoxidable","acabado_aluminio","largo","ancho","calibre","antiderrapante","seccion_perfil_cuadrado","calibre","largo_perfil","perfileria","seccion_perfil_rectangular")
    def _onchange_especificaciones(self):
        selection_dict = dict(self._fields['campo_nombre'].selection)
        valor_nombre = selection_dict.get(self.campo_nombre)

        selection_dict = dict(self._fields['material'].selection)
        valor_material = selection_dict.get(self.material)

        selection_dict = dict(self._fields['tipo_carbon'].selection)
        valor_tipo_carbon = selection_dict.get(self.tipo_carbon)
        selection_dict = dict(self._fields['tipo_inoxidable'].selection)
        valor_tipo_inoxidable = selection_dict.get(self.tipo_inoxidable)
        selection_dict = dict(self._fields['tipo_aluminio'].selection)
        valor_tipo_aluminio = selection_dict.get(self.tipo_aluminio)

        selection_dict = dict(self._fields['acabado_carbon'].selection)
        valor_acabado_carbon = selection_dict.get(self.acabado_carbon)
        selection_dict = dict(self._fields['acabado_inoxidable'].selection)
        valor_acabado_inoxidable = selection_dict.get(self.acabado_inoxidable)
        selection_dict = dict(self._fields['acabado_aluminio'].selection)
        valor_acabado_aluminio = selection_dict.get(self.acabado_aluminio)

        selection_dict = dict(self._fields['perfileria'].selection)
        valor_perfileria = selection_dict.get(self.perfileria)

        selection_dict = dict(self._fields['largo'].selection)
        valor_largo = selection_dict.get(self.largo)

        selection_dict = dict(self._fields['ancho'].selection)
        valor_ancho = selection_dict.get(self.ancho)

        selection_dict = dict(self._fields['calibre'].selection)
        valor_calibre = selection_dict.get(self.calibre)

        selection_dict = dict(self._fields['seccion_perfil_cuadrado'].selection)
        valor_perfil_cuadrado = selection_dict.get(self.seccion_perfil_cuadrado)

        selection_dict = dict(self._fields['seccion_perfil_rectangular'].selection)
        valor_perfil_rectangular = selection_dict.get(self.seccion_perfil_rectangular)

        selection_dict = dict(self._fields['pintura_tipo'].selection)
        valor_pintura = selection_dict.get(self.pintura_tipo)
        cantidad = "Litros" if self.pintura_tipo =="liquida" else "Kilos" if self.pintura_tipo == "polvo" else "Latas"

        nombre = ""
        medida = ""
        if valor_nombre == 'Lámina':
            if self.material == 'carbon':
                nombre = f"Lámina {valor_material if valor_material else ''} {valor_tipo_carbon if valor_tipo_carbon else ''} {valor_acabado_carbon if valor_acabado_carbon else ''}"
            if self.material == 'inoxidable':
                nombre = f"Lámina {valor_material if valor_material else ''} {valor_tipo_inoxidable if valor_tipo_inoxidable else ''} {valor_acabado_inoxidable if valor_acabado_inoxidable else ''}"
            if self.material == 'aluminio':
                nombre = f"Lámina {valor_material if valor_material else ''} {valor_tipo_aluminio if valor_tipo_aluminio else ''} {valor_acabado_aluminio if valor_acabado_aluminio else ''}"
            if self.material == 'galvanizado':
                nombre = f"Lámina {valor_material if valor_material else ''} "
            medida = f"{valor_largo} x {valor_ancho} @ {valor_calibre}"
        elif valor_nombre == 'Perfil':
            nombre = "Perfil"
            if valor_perfileria == 'Cuadrado' :
                nombre = f"Perfil {valor_perfileria if valor_perfileria else ''} {valor_material if valor_material else ''}"
                medida = f"{valor_perfil_cuadrado if valor_perfil_cuadrado else ''} @ {valor_calibre if valor_calibre else ''},{self.largo_perfil}"
                self.seccion_perfil_rectangular = None
            if valor_perfileria == 'Rectangular' :
                nombre = f"Perfil {valor_perfileria if valor_perfileria else ''} {valor_material if valor_material else ''}"
                medida = f"{valor_perfil_rectangular if valor_perfil_rectangular else ''} @ {valor_calibre if valor_calibre else ''},{self.largo_perfil}"
                self.seccion_perfil_cuadrado = None
        else:
            nombre = valor_nombre if valor_nombre != "Pintura" else f"{valor_nombre} {self.nombre_pintura.nombre if self.nombre_pintura else ''} "
            medida = valor_nombre if valor_nombre != "Pintura" else f"{valor_pintura} en {cantidad}"

        self.nombre = nombre
        self.medida = medida

    def get_view(self, view_id=None, view_type='form', **options):#Carga los items de todos los módulos de Almacén en un solo módulo de diseño
        res = super(Materiales,self).get_view(view_id, view_type,**options)
        # get_almacen = self.env['dtm.diseno.almacen'].search([])
        # modelos = ['dtm.materiales',"dtm.materiales.angulos","dtm.materiales.solera","dtm.materiales.rodamientos","dtm.materiales.pintura","dtm.materiales.perfiles","dtm.materiales.otros","dtm.materiales.maquinados","dtm.materiales.canal","dtm.materiales.tornillos","dtm.materiales.tubos","dtm.materiales.varilla"]
        # for item in get_almacen:
        #     item.write({
        #         "cantidad":0,
        #         "apartado":0,
        #         "disponible":0,
        #     })
        #     for modelo in modelos:
        #         get_lamina = self.env[modelo].search([("codigo","=",item.id)])
        #         if get_lamina:
        #             item.write({
        #                 "cantidad": get_lamina.cantidad,
        #                 "apartado": get_lamina.apartado,
        #                 "disponible": get_lamina.disponible,
        #             })
        #
        # for find_id in range(1,self.env['dtm.diseno.almacen'].search([], order='id desc', limit=1).id+2):
        #         if not self.env['dtm.diseno.almacen'].search([("id","=",find_id)]):
        #             self.env.cr.execute(f"SELECT setval('dtm_diseno_almacen_id_seq', {find_id}, false);")
        #             break
        return res

    @api.depends("cantidad")
    #-----------------------------Saca la cantidad del material que hay disponible---------------
    def _compute_disponible(self):
        for result in self:
            result.disponible = result.cantidad - result.apartado









