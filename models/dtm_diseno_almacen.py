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

    campo_nombre = fields.Selection(string="Item",selection=[("lamina","Lámina"),("perfil","Perfil"),("placa","Placa"),
                                                         ("tornillo","Tornillo"),("pintura","Pintura"),
                                                         ("ruedas","Ruedas")])

    perfileria = fields.Selection(string="Perfilería",selection=[("cuadrado","Cuadrado"),("redondo","Redondo"),
                                                                 ("rectangular","Rectangular"),("angulo","Ángulos"),
                                                                 ("ipr","IPR"),("canales","Canales"),
                                                                 ("varilla","Varilla"),("viga","Viga")])


    calibre = fields.Selection(string="Calibre", selection = [('10.0','10'),('11.0','11'),('12.0','12'),
                                                                 ('14.0','14'),('16.0','16'),('18.0','18'),
                                                                 ('20.0','20'),('22.0','22')])
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
    largo_perfil = fields.Selection(string="Largo", selection=[('236.0',236)])
    seccion = fields.Selection(string="Alto", selection=[('120.0',120),('96',96)])

    @api.onchange("campo_nombre","material","tipo_carbon","tipo_inoxidable","tipo_aluminio","acabado_carbon","acabado_inoxidable","acabado_aluminio","largo","ancho","calibre","antiderrapante")
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

        selection_dict = dict(self._fields['largo'].selection)
        valor_largo = selection_dict.get(self.largo)

        selection_dict = dict(self._fields['ancho'].selection)
        valor_ancho = selection_dict.get(self.ancho)

        selection_dict = dict(self._fields['calibre'].selection)
        valor_calibre = selection_dict.get(self.calibre)

        selection_dict = dict(self._fields['pintura_tipo'].selection)
        valor_pintura = selection_dict.get(self.pintura_tipo)
        cantidad = "Litros" if self.pintura_tipo =="liquida" else "Kilos" if self.pintura_tipo == "polvo" else "Latas"

        nombre = ""
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
            nombre = f""
            medida = f""
        else:
            nombre = valor_nombre if valor_nombre != "Pintura" else f"{valor_nombre} {self.nombre_pintura.nombre if self.nombre_pintura else ''} "
            medida = valor_nombre if valor_nombre != "Pintura" else f"{valor_pintura} en {cantidad}"
        self.nombre = nombre
        self.medida = medida

    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res

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
    def _compute_disponible(self):#-----------------------------Saca la cantidad del material que hay disponible---------------
        for result in self:
            result.disponible = result.cantidad - result.apartado









