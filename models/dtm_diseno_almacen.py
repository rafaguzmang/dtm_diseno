from odoo import api,fields,models,http
from odoo.exceptions import ValidationError
import re
from odoo.http import request


class Materiales(models.Model):
    _name = "dtm.diseno.almacen"
    _description = "Modelo donde se concentrán todos los materiales disponibles en almacén"
    _rec_name = "nombre"

    # -------------------------------------Datos del material -------------------------------------------------
    nombre = fields.Char(string="Nombre", readonly=False)
    medida = fields.Char(string="Medidas", readonly=False)
    caracteristicas = fields.Selection(string="Tipo",selection=[('material','Material'),('consumible','Consumible'),('herramienta','Herramienta')])
    notas = fields.Text(string="Notas")
    area = fields.Float(string="Área/Largo")
    localizacion = fields.Char(string="Localización")
    minimo = fields.Integer(string="Mínimo")

    # --------------------------------------Cantidades, datos para operaciones --------------------------------
    cantidad = fields.Integer(string="Stock", default=0)
    apartado = fields.Integer(string="Proyectado", readonly="True", default=0)
    # disponible = fields.Integer(string="Disponible", readonly="True", compute="_compute_disponible" ,store=True)
    disponible = fields.Integer(string="Disponible", readonly="True",store=True)
    #---------------------------------------Tipo de item ------------------------------------------------------
    campo_nombre = fields.Selection(string="Item",selection=[("lamina","Lámina"),("perfil","Perfil"),("placa","Placa"),
                                                         ("tornilleria","Tornillería"),("pintura","Pintura"),
                                                         ("ruedas","Ruedas"),("barras","Barras")])

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
    largo = fields.Selection(string="Alto", selection=[('120.0',120.0),('96',96.0)])
    ancho = fields.Selection(string="Ancho", selection=[('48.0',48.0),('36.0',36.0)])
    #---------------------------------------------Dimenciones Perfil----------------------------------------------------------------------------
    largo_perfil = fields.Selection(string="Largo", selection = [("236.0","236.0")])
    seccion_perfil_cuadrado = fields.Selection(string="Sección", selection=[('1x1','1.0 x 1.0'),('125x125','1.25 x 1.25'),('15x15','1.5 x 1.5'),('2x2','2.0 x 2.0'),('25x25','2.5 x 2.5'),('3x3','3.0 x 3.0'),('35x35','3.5 x 3.5'),('4x4','4.0 x 4.0'),
                                                            ('45x45','4.5 x 4.5'),('5x5','5.0 x 5.0'),('6x6','6.0 x 6.0'),('7x7','7.0 x 7.0'),('8x8','8.0 x 8.0'),('10x10','10.0 x 10.0'),('12x12','12.0 x 12.0'),('14x14','14.0 x 14.0'),
                                                            ('16x16','16.0 x 16.0')])
    seccion_perfil_rectangular = fields.Selection(string="Sección", selection=[('3x2','3.0 x 2.0'),('4x2','4.0 x 2.0'),('4x3','4.0 x 3.0'),('5x3','5.0 x 3.0'),('6x2','6.0 x 2.0'),('6x3','6.0 x 3.0'),('6x4','6.0 x 4.0'),('7x5','7.0 x 5.0'),
                                                            ('8x4','8.0 x 4.0'),('8x6','8.0 x 6.0'),('10x2','10.0 x 2.0'),('10x4','10.0 x 4.0'),('10x6','10.0 x 6.0'),('12x2','12.0 x 2.0'),('12x4','12.0 x 4.0'),('12x6','12.0 x 6.0'),
                                                            ('12x8','12.0 x 8.0'),('14x4','14.0 x 4.0'),('14x6','14.0 x 6.0')
                                                            ])
    perfileria = fields.Selection(string="Perfilería",selection=[("angulo","Ángulos"),("canales","Canales"),("cuadrado","Cuadrado"),
                                                                 ("ipr","I.P.R."),("ptr","P.T.R."),("redondo","Redondo"),("rectangular","Rectangular"),
                                                                 ("varilla","Varilla"),("viga","Viga")])
    material_perfil = fields.Selection(string="Material", selection=[('carbon','Acero al Carbón'),('inoxidable','Inoxidable'),('galvanizado','Galvanizado'),
                                                              ('aluminio','Aluminio')])
    # -----------------------------Redondo---------------
    tubo_cedula = fields.Selection(string="Cedula",selection=[("30","30"),("40","40"),("80","80"),("industrial","Industrial")])
    tubo_diametro_30 = fields.Selection(string="30",selection=[("75",0.75),("1",1.0),("125",1.25),("15",1.5),("2",2.0),("25",2.5),("3",3.0),("4",4.0),("6625",6.625)])
    tubo_diametro_40 = fields.Selection(string="40",selection=[("375",0.375),("05",0.5),("75",0.75),("1",1.0),("125",1.25),("15",1.5),("2",2.0)])
    tubo_diametro_80 = fields.Selection(string="40",selection=[("05",0.5),("75",0.75),("1",1.0),("125",1.25),("15",1.5),("2",2.0),("25",2.5),("3",3.0),("4",4.0),("6625",6.625)])
    tubo_diametro_industrial = fields.Selection(string="Industrial",selection=[("05",0.5),("625",0.625),("75",0.75),("875",0.875),("1",1.0),("125",1.25)])
    #------------------------------Cuadrado---------------------
    calibre_perfil = fields.Selection(string="Calibre", selection = [('10.0',10.0),('11.0',11.0),('12.0',12.0),
                                                                 ('14.0',14.0),('16.0',16.0),('18.0',18.0),
                                                                 ('20.0',20.0),('22.0',22.0)])
    # -----------------------------P.T.R.-----------------------
    ptr_calibre = fields.Selection(string="PTR",selection=[("125",0.125),("1875",0.1875),("25",0.25),("50",0.5),("10",10.0),("11",11.0),("09",9.0),("10",10.0),("11",11.0),("12",12.0),("13",13.0),("14",14.0)])
    ptr_seccion = fields.Selection(string="Seccion",selection=[('1x1','1.0 x 1.0'),('15x15','1.5 x 1.5'),('2x1','2.0 x 1.0'),('2x2','2.0 x 2.0'),('25x25','2.5 x 2.5'),('3x3','3.0 x 3.0'),('35x35','3.5 x 3.5'),('3x2','3.0 x 2.0'),('4x2','4.0 x 2.0'),
                                                            ('4x3','4.0 x 3.0'),('4x4','4.0 x 4.0'),('5x5','5.0 x 5.0'),('6x4','6.0 x 4.0')])
    # -----------------------------Varilla-----------------------
    varilla_material = fields.Selection(string="Material",selection=[("redonda","Redonda"),("hexagonal","Hexagonal")])
    varilla_tipo = fields.Selection(string="Tipo",selection=[("pulida","Pulida"),("corrugada","Corrugada")])
    varilla_calibre = fields.Selection(string="Redondo",selection=[("025",0.25),("3125",0.3125),("375",0.375),("50",0.5),("625",0.625),("75",0.75),("875",0.875),("1",1.0),
                                                                   ("1125",1.125),("125",1.25),("1375",1.375),("15",1.5),("1625",1.625),("175",1.75),("1875",1.875),("2",2.0),
                                                                   ("225",2.25),("25",2.5)])
    # -----------------------------Tornilleria-----------------------
    tornilleria = fields.Selection(string="Tornillería",selection=[("tornillo","Tornillo"),("tuerca","Tuerca"),("arandela","Arandela"),("varilla","Varilla Roscada")])
    # -----------------------------Tornillo--------------------------
    tornilleria_tornillo = fields.Selection(string="Tipo",selection=[("maquina","Máquina"),("madera","Madera"),("autorroscante","Autorroscante"),("anclaje","Anclaje"),
                                                                     ("seguridad","Seguridad"),("concreto","Concreto"),("elevador","Elevador")])
    tornillo_cabeza = fields.Selection(string="Cabeza",selection=[("boton","Botón"),("plana","Plana"),("phillips","Phillips"),("torx","Estrella (Torx)"),("hexagonal","Hexagonal"),
                                                                   ("redonda","Redonda"),("avellanada","Avellanada"),("seguridad","Avellanada"),("cuadrada","Cuadrada"),
                                                                   ("coche","Coche"),("socket","Socket")])
    tornillo_material = fields.Selection(string="Material",selection=[("carbon","Acero al carbón"),("inoxidable","Inoxidable"),("laton","Latón"),("aluminio","Aluminio"),
                                                                      ("plastico","Plástico"),("galvanizado","Galvanizado"),("termicamente","Térmicamente")])

    tornillo_tipo = fields.Selection(string="Tipo", selection=[("estandar","Estandar"),("milimetrico","Milimético")])
    tornillo_diametro_estandar = fields.Selection(string="Diámetro - Paso",selection=[("4-40","4.0 - 40.0"),("6-32","6.0 - 32.0"),("8-32","8.0 - 32.0"),("10-24","10.0 - 24.0"),("10-32","10.0 - 32.0"),
                                                                      ("025-20","0.25 - 20.0"),("025-28","0.25 - 28.0"),("03125-18","0.3125 - 18.0"),("03125-24","0.3125 - 24.0"),("0375-16","0.375 - 16.0"),
                                                                      ("0375-24","0.375 - 24.0"),("03475-14","0.4375 - 14.0"),("03475-20","0.4375 - 20.0"),("05-13","0.5 - 13.0"),("05-20","0.5 - 20.0"),
                                                                      ("05625-12","0.5625 - 12.0"),("05625-18","0.5625 - 18.0"),("0625-11","0.625 - 11.0"),("0625-18","0.625 - 18.0"),("075-18","0.75 - 10.0"),
                                                                      ("075-16","0.75 - 16.0"),("0875-9","0.875 - 9.0"),("0875-14","0.875 - 14.0"),("0875-14","0.875 - 14.0"),("1-8","1.0 - 8.0"),("1-12","1 - 12.0")
                                                                      ])
    tornillo_diametro_milimetrico = fields.Selection(string="Diámetro - Paso",selection=[("m2","M2 - 0.4"),("m3","M3 - 0.5"),("m4","M4 - 0.7"),("m5","M5 - 0.8"),("m6","M6 - 1.0"),("m7","M7 - 1.0"),("m8","M8 - 1.25"),
                                                                                         ("m9","M9 - 1.25"),("m10","M10 - 1.5"),("m11","M11 - 1.5"),("m12","M12 - 1.75")
                                                                      ])

    tornillo_longitud  = fields.Float(string="Longitud")
    # -----------------------------Tuerca--------------------------
    tuerca_tipo = fields.Selection(string="Tuerca",selection=[("normal","Normal"),("nylon","Seguridad Nylon"),("temperatura","Seguridad Temperatura"),("falda","Falda"),("contratuerca","Contratuerca"),("ciega","Ciega"),
                                                              ("remachable","Remachable"),("remach","Remachable Hexagonal")])
    tornillo_tipo = fields.Selection(string="Tipo", selection=[("estandar","Estandar"),("milimetrico","Milimético")])
    tornillo_diametro_estandar = fields.Selection(string="Diámetro - Paso",selection=[("4-40","4.0 - 40.0"),("6-32","6.0 - 32.0"),("8-32","8.0 - 32.0"),("10-24","10.0 - 24.0"),("10-32","10.0 - 32.0"),
                                                                      ("025-20","0.25 - 20.0"),("025-28","0.25 - 28.0"),("03125-18","0.3125 - 18.0"),("03125-24","0.3125 - 24.0"),("0375-16","0.375 - 16.0"),
                                                                      ("0375-24","0.375 - 24.0"),("03475-14","0.4375 - 14.0"),("03475-20","0.4375 - 20.0"),("05-13","0.5 - 13.0"),("05-20","0.5 - 20.0"),
                                                                      ("05625-12","0.5625 - 12.0"),("05625-18","0.5625 - 18.0"),("0625-11","0.625 - 11.0"),("0625-18","0.625 - 18.0"),("075-18","0.75 - 10.0"),
                                                                      ("075-16","0.75 - 16.0"),("0875-9","0.875 - 9.0"),("0875-14","0.875 - 14.0"),("0875-14","0.875 - 14.0"),("1-8","1.0 - 8.0"),("1-12","1 - 12.0")
                                                                      ])
    tornillo_diametro_milimetrico = fields.Selection(string="Diámetro - Paso",selection=[("m2","M2 - 0.4"),("m3","M3 - 0.5"),("m4","M4 - 0.7"),("m5","M5 - 0.8"),("m6","M6 - 1.0"),("m7","M7 - 1.0"),("m8","M8 - 1.25"),
                                                                                         ("m9","M9 - 1.25"),("m10","M10 - 1.5"),("m11","M11 - 1.5"),("m12","M12 - 1.75")
                                                                      ])
    #---------------------------------------------Ruedas------------------------------------------------------------------------------------------Ranuradas Nylon AltaTemperatura
    descripcion_rueda = fields.Selection(string="Tipo",selection=[("giratorio","Giratoria"),("fijo","Fija")])
    material_rueda = fields.Selection(string="Material",selection=[("poliuretano","Poliuretano"),("performa","Performa"),("poliolefino","Poliolefino"),("maxim","Maxim"),("fenolicas","Fenolicas"),("hule","Hule"),("acero","Acero"),("transForma","TransForma"),("endura","Endura")])
    diametro_rueda = fields.Selection(string="Diámetro", selection=[("25",2.5),("3",3.0),("3",3.25),("35",3.5),("4",4.0),("5",5.0),("6",6.0),("8",8.0),("10",10.0)])
    ancho_rueda = fields.Selection(string="Ancho",selection=[("875",0.875),("125",1.25),("14375",1.4375),("146875",1.46875),("13125",1.3125),("15",1.5),("2",2),("25",2.5)])
    balero_rueda = fields.Selection(string="Balero",selection=[("delrin","Delrin"),("bola","Bola"),("plano","Plano"),("roller","Roller"),("teflon","Teflon"),("sleeve","Sleeve")])
    #----------------------------Barra-----------------------------
    barras = fields.Selection(string="Barras",selection=[("redonda","Redonda"),("cuadrada","Cuadrada")])
    barra_tipo = fields.Selection(string="Tipo",selection=[("1045","1045"),("1018","1018")])
    barra_diametro = fields.Float(string="Diametro")
    barra_alto = fields.Float(string="Alto")
    barra_largo = fields.Float(string="Largo")

    @api.onchange("campo_nombre","material","tipo_carbon","tipo_inoxidable","tipo_aluminio",
      "acabado_carbon","acabado_inoxidable","acabado_aluminio","largo","ancho","calibre","antiderrapante",
      "seccion_perfil_cuadrado","calibre","largo_perfil","perfileria","seccion_perfil_rectangular",
      "descripcion_rueda","material_rueda","diametro_rueda","ancho_rueda","balero_rueda","tubo_cedula","tubo_diametro_30",
      "tubo_diametro_40","tubo_diametro_industrial","tubo_diametro_80","ptr_calibre","ptr_seccion","varilla_material","varilla_tipo",
      "tornilleria","tornilleria_tornillo","tornillo_cabeza","tornillo_material","tornillo_diametro_estandar","tornillo_longitud","varilla_calibre",
      "material_perfil","tuerca_tipo","barras","barra_tipo","barra_diametro","barra_alto","barra_largo","tornillo_diametro_estandar","tornillo_diametro_milimetrico")
    def _onchange_especificaciones(self):
        selection_dict = dict(self._fields['campo_nombre'].selection)
        valor_nombre = selection_dict.get(self.campo_nombre)
        nombre = ""
        medida = ""
        if valor_nombre == 'Lámina':
            result = self.lamina_func()
            nombre = result[0]
            medida = result[1]
        if valor_nombre == 'Perfil':
            result = self.perfil_func()
            nombre = result[0]
            medida = result[1]
        if valor_nombre == 'Ruedas':
            result = self.ruedas_func()
            nombre = result[0]
            medida = result[1]
        if valor_nombre == 'Tornillería':
            result = self.tornilleria_func()
            nombre = result[0]
            medida = result[1]
        if valor_nombre == 'Barras':
            result = self.barras_func()
            nombre = result[0]
            medida = result[1]

        # else:
        #     nombre = valor_nombre if valor_nombre != "Pintura" else f"{valor_nombre} {self.nombre_pintura.nombre if self.nombre_pintura else ''} "
        #     medida = valor_nombre if valor_nombre != "Pintura" else f"{valor_pintura} en {cantidad}"

        self.nombre = nombre
        self.medida = medida

    #Función para tratar las opciones de las lámina
    def lamina_func(self):
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
            nombre = "Lámina"
            if self.material == 'carbon':
                nombre = f"Lámina {valor_material if valor_material else ''} {valor_tipo_carbon if valor_tipo_carbon else ''} {valor_acabado_carbon if valor_acabado_carbon else ''}"
            if self.material == 'inoxidable':
                nombre = f"Lámina {valor_material if valor_material else ''} {valor_tipo_inoxidable if valor_tipo_inoxidable else ''} {valor_acabado_inoxidable if valor_acabado_inoxidable else ''}"
            if self.material == 'aluminio':
                nombre = f"Lámina {valor_material if valor_material else ''} {valor_tipo_aluminio if valor_tipo_aluminio else ''} {valor_acabado_aluminio if valor_acabado_aluminio else ''}"
            if self.material == 'galvanizado':
                nombre = f"Lámina {valor_material if valor_material else ''} "
            medida = f"{valor_largo if valor_largo else ''} x {valor_ancho if valor_ancho else ''} @ {valor_calibre if valor_calibre else ''}"

            return (nombre,medida)
    #Función para tratar las opciones de perfilería
    def perfil_func(self):
            selection_dict = dict(self._fields['perfileria'].selection)
            valor_perfileria = selection_dict.get(self.perfileria)

            selection_dict = dict(self._fields['material_perfil'].selection)
            valor_material = selection_dict.get(self.material_perfil)

            selection_dict = dict(self._fields['calibre'].selection)
            valor_calibre = selection_dict.get(self.calibre_perfil)

            nombre = ""
            medida = ""
            if valor_perfileria == 'Cuadrado' :
                selection_dict = dict(self._fields['seccion_perfil_cuadrado'].selection)
                valor_perfil_cuadrado = selection_dict.get(self.seccion_perfil_cuadrado)

                nombre = f"Perfil {valor_perfileria if valor_perfileria else ''} {valor_material if valor_material else ''}"
                medida = f"{valor_perfil_cuadrado if valor_perfil_cuadrado else ''} @ {valor_calibre if valor_calibre else ''},{self.largo_perfil}"
                self.seccion_perfil_rectangular = None
            if valor_perfileria == 'Rectangular' :
                selection_dict = dict(self._fields['seccion_perfil_rectangular'].selection)
                valor_perfil_rectangular = selection_dict.get(self.seccion_perfil_rectangular)

                nombre = f"Perfil {valor_perfileria if valor_perfileria else ''} {valor_material if valor_material else ''}"
                medida = f"{valor_perfil_rectangular if valor_perfil_rectangular else ''} @ {valor_calibre if valor_calibre else ''},{self.largo_perfil}"
                self.seccion_perfil_cuadrado = None
            if valor_perfileria == 'Redondo' :
                selection_dict = dict(self._fields['tubo_diametro_30'].selection)
                valor_tubo_diametro_30 = selection_dict.get(self.tubo_diametro_30)

                selection_dict = dict(self._fields['tubo_diametro_40'].selection)
                valor_tubo_diametro_40 = selection_dict.get(self.tubo_diametro_40)

                selection_dict = dict(self._fields['tubo_diametro_80'].selection)
                valor_tubo_diametro_80 = selection_dict.get(self.tubo_diametro_80)

                selection_dict = dict(self._fields['tubo_diametro_industrial'].selection)
                valor_tubo_diametro_industrial = selection_dict.get(self.tubo_diametro_industrial)

                selection_dict = dict(self._fields['tubo_cedula'].selection)
                valor_tubo_cedula = selection_dict.get(self.tubo_cedula)

                if valor_tubo_cedula == "30":
                    medida = f" ⌀ {valor_tubo_diametro_30 if valor_tubo_diametro_30 else ''} - {self.largo_perfil}"
                if valor_tubo_cedula == "40" :
                    medida = f" ⌀ {valor_tubo_diametro_40 if valor_tubo_diametro_40 else ''} - {self.largo_perfil}"
                if valor_tubo_cedula == "80" :
                    medida = f" ⌀ {valor_tubo_diametro_80 if valor_tubo_diametro_80 else ''} - {self.largo_perfil}"
                if valor_tubo_cedula == "Industrial":
                    medida = f" ⌀ {valor_tubo_diametro_industrial if valor_tubo_diametro_industrial else ''} - {self.largo_perfil}"
                nombre = f"Perfil {valor_perfileria if valor_perfileria else ''} {valor_material if valor_material else ''} Cédula {valor_tubo_cedula if valor_tubo_cedula else ''}"
                self.seccion_perfil_cuadrado = None
                self.seccion_perfil_rectangular = None
            if valor_perfileria == 'P.T.R.' :
                selection_dict = dict(self._fields['ptr_calibre'].selection)
                valor_ptr_calibre = selection_dict.get(self.ptr_calibre)

                selection_dict = dict(self._fields['ptr_seccion'].selection)
                valor_ptr_seccion = selection_dict.get(self.ptr_seccion)

                nombre = f"{valor_perfileria if valor_perfileria else ''} {valor_material if valor_material else ''}"
                medida = f"{valor_ptr_seccion if valor_ptr_seccion else ''} @ {valor_ptr_calibre if valor_ptr_calibre else ''},{self.largo_perfil}"
            if valor_perfileria == 'Varilla' :
                selection_dict = dict(self._fields['varilla_material'].selection)
                valor_varilla_material = selection_dict.get(self.varilla_material)

                selection_dict = dict(self._fields['varilla_tipo'].selection)
                valor_varilla_tipo = selection_dict.get(self.varilla_tipo)

                selection_dict = dict(self._fields['varilla_calibre'].selection)
                valor_varilla_calibre = selection_dict.get(self.varilla_calibre)

                nombre = f"{valor_perfileria if valor_perfileria else ''} {valor_varilla_material if valor_varilla_material else ''} {valor_varilla_tipo if valor_varilla_tipo else ''}"
                medida = f"⌀ {valor_varilla_calibre if valor_varilla_calibre else ''} - {self.largo_perfil}"

            return (nombre,medida)
    #Función para tratar las opciones de las ruedas
    def ruedas_func(self):
        selection_dict = dict(self._fields['descripcion_rueda'].selection)
        valor_descripcion_rueda = selection_dict.get(self.descripcion_rueda)
        selection_dict = dict(self._fields['material_rueda'].selection)
        valor_material_rueda = selection_dict.get(self.material_rueda)
        selection_dict = dict(self._fields['diametro_rueda'].selection)
        valor_diametro_rueda = selection_dict.get(self.diametro_rueda)
        selection_dict = dict(self._fields['ancho_rueda'].selection)
        valor_ancho_rueda = selection_dict.get(self.ancho_rueda)
        selection_dict = dict(self._fields['balero_rueda'].selection)
        valor_balero_rueda = selection_dict.get(self.balero_rueda)

        nombre = f"Rueda {valor_descripcion_rueda if valor_descripcion_rueda else ''} de {valor_material_rueda if valor_material_rueda else ''} {valor_balero_rueda if valor_balero_rueda else ''}"
        medida = f"{valor_diametro_rueda if valor_diametro_rueda else ''} x {valor_ancho_rueda if valor_ancho_rueda else ''}"
        return (nombre,medida)
    def tornilleria_func(self):
        selection_dict = dict(self._fields['tornilleria'].selection)
        valor_tornilleria = selection_dict.get(self.tornilleria)

        selection_dict = dict(self._fields['tornillo_material'].selection)
        valor_tornillo_material = selection_dict.get(self.tornillo_material)
        selection_dict = dict(self._fields['tornillo_tipo'].selection)
        valor_tornillo_tipo = selection_dict.get(self.tornillo_tipo)
        selection_dict = dict(self._fields['tornillo_diametro_estandar'].selection)
        valor_tornillo_diametro_estandar = selection_dict.get(self.tornillo_diametro_estandar)
        selection_dict = dict(self._fields['tornillo_diametro_milimetrico'].selection)
        valor_tornillo_diametro_milimetrico = selection_dict.get(self.tornillo_diametro_milimetrico)

        nombre = ""
        medida = ""
        if valor_tornilleria=="Tornillo":
            selection_dict = dict(self._fields['tornilleria_tornillo'].selection)
            valor_tornilleria_tornillo = selection_dict.get(self.tornilleria_tornillo)
            selection_dict = dict(self._fields['tornillo_cabeza'].selection)
            valor_tornillo_cabeza = selection_dict.get(self.tornillo_cabeza)
            nombre = f"{valor_tornilleria if valor_tornilleria else ''} de {valor_tornilleria_tornillo if valor_tornilleria_tornillo else ''} {valor_tornillo_cabeza if valor_tornillo_cabeza else ''} {valor_tornillo_material if valor_tornillo_material else ''}"
            if valor_tornillo_tipo == "Estandar":
                medida = f"Ø {valor_tornillo_diametro_estandar if valor_tornillo_diametro_estandar else ''} x {self.tornillo_longitud if self.tornillo_longitud else ''}"
            else:
                medida = f"Ø {valor_tornillo_diametro_milimetrico if valor_tornillo_diametro_milimetrico else ''} x {self.tornillo_longitud if self.tornillo_longitud else ''}"
        if valor_tornilleria=="Tuerca":
            selection_dict = dict(self._fields['tuerca_tipo'].selection)
            valor_tornilleria_tornillo = selection_dict.get(self.tuerca_tipo)
            nombre = f"{valor_tornilleria if valor_tornilleria else ''} {valor_tornillo_material if valor_tornillo_material else ''} {valor_tornilleria_tornillo if valor_tornilleria_tornillo else ''}"
            if valor_tornillo_tipo == "Estandar":
                medida = f"Ø {valor_tornillo_diametro_estandar if valor_tornillo_diametro_estandar else ''}"
            else:
                medida = f"Ø {valor_tornillo_diametro_milimetrico if valor_tornillo_diametro_milimetrico else ''}"
        return (nombre,medida)

    def barras_func(self):
        selection_dict = dict(self._fields['barras'].selection)
        valor_barras = selection_dict.get(self.barras)
        selection_dict = dict(self._fields['material'].selection)
        valor_material = selection_dict.get(self.material)
        selection_dict = dict(self._fields['barra_tipo'].selection)
        valor_tipo = selection_dict.get(self.barra_tipo)

        nombre = ""
        medida = ""
        if valor_barras=="Redonda":
            nombre = f"Barra Redonda {valor_material if valor_material else ''} {valor_tipo if valor_tipo else ''}"
            medida = f"Ø {self.barra_diametro} x {self.barra_largo}"
        if valor_barras=="cuadrada":
            nombre = f"Barra Cuadrada {valor_material if valor_material else ''} {valor_tipo if valor_tipo else ''}"
            medida = f"{self.barra_alto} x {self.ancho} x {self.barra_largo}"
        return (nombre,medida)


    def selection_value(self):
        selection_dict = dict(self._fields['pintura_tipo'].selection)
        valor_pintura = selection_dict.get(self.pintura_tipo)
        cantidad = "Litros" if self.pintura_tipo =="liquida" else "Kilos" if self.pintura_tipo == "polvo" else "Latas"

    def action_limpiar(self):
            self.tornillo_diametro_milimetrico = ""
            self.tornillo_diametro_milimetrico = ""
            self.barras = ""
            self.barra_tipo = ""
            self.barra_diametro = ""
            self.barra_alto = ""
            self.barra_largo = ""
            self.tornilleria = ""
            self.tornillo_material = ""
            self.tornillo_cabeza = ""
            self.tornillo_tipo = ""
            self.tornillo_diametro_estandar = ""
            self.tornillo_longitud = ""
            self.tornilleria_tornillo = ""
            self.calibre_perfil = ""
            self.campo_nombre = ""
            self.material = ""
            self.largo_perfil= ""
            self.material_perfil= ""
            self.seccion_perfil_cuadrado= ""
            self.seccion_perfil_rectangular= ""
            self.perfileria= ""
            self.tubo_cedula= ""
            self.tubo_diametro_30= ""
            self.tubo_diametro_40= ""
            self.tubo_diametro_80= ""
            self.tubo_diametro_industrial= ""
            self.ptr_calibre= ""
            self.ptr_seccion= ""
            self.descripcion_rueda= ""
            self.material_rueda= ""
            self.diametro_rueda= ""
            self.ancho_rueda= ""
            self.balero_rueda = ""
            self.calibre = ""
            self.tipo_carbon = ""
            self.tipo_inoxidable = ""
            self.tipo_aluminio = ""
            self.acabado_carbon = ""
            self.acabado_inoxidable = ""
            self.acabado_aluminio = ""



    @api.depends("cantidad")
    #-----------------------------Saca la cantidad del material que hay disponible---------------
    def _compute_disponible(self):
        for result in self:
            result.disponible = result.cantidad - result.apartado

    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res








