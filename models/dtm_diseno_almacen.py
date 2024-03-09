from odoo import api,fields,models


class Materiales(models.Model):
    _name = "dtm.diseno.almacen"
    _description = "Modelo donde se concentrán todos los materiales disponibles en almacén"
    # _rec_name = "nombre"

    # numero = fields.Integer(string="Número")
    nombre = fields.Char(string="Nombre", readonly=False,compute="_compute_id",store=True, require=True)
    medida = fields.Char(string="Medidas", readonly=False)
    caracteristicas = fields.Char(string="Caracteristicas", readonly=False)
    area = fields.Float(string="Área/Largo")
    cantidad = fields.Integer()

    @api.depends("nombre")
    def _compute_id(self):
        for result in self:
            pass
            # print(result.id)

    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res

    def insertar(self,cantidad,nombre,medida,valor,*args):
            if valor:
                existe =True
            else:
                existe = False
            area = 0
            if args:
                area = args[0]
            if existe:
                self.env.cr.execute("UPDATE dtm_diseno_almacen SET cantidad="+cantidad+", area="+str(area)+" WHERE nombre='"+nombre+"' and medida='"+medida+"'")
            else:
                self.env.cr.execute("INSERT INTO dtm_diseno_almacen ( cantidad, nombre, medida, area) VALUES ("+cantidad+", '"+nombre+"', '"+medida+"',"+str(area)+")")


    def clean_table(self,myset):
        get_info = self.env['dtm.diseno.almacen'].search([])
        no_repeat = set(myset)
        # print(no_repeat)
        for get in get_info:
            # print(get.nombre,get.medida)
            if get.nombre and get.medida:
                if get.nombre+get.medida not in no_repeat:
                    self.env.cr.execute("DELETE FROM dtm_diseno_almacen WHERE nombre='"+get.nombre+"' AND medida='"+get.medida+"'")

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Materiales,self).get_view(view_id, view_type,**options)
        get_lamina = self.env['dtm.materiales'].search([])
        get_angulos = self.env['dtm.materiales.angulos'].search([])
        get_canal = self.env['dtm.materiales.canal'].search([])
        get_perfiles = self.env['dtm.materiales.perfiles'].search([])
        get_pintura = self.env['dtm.materiales.pintura'].search([])
        get_rodamientos = self.env['dtm.materiales.rodamientos'].search([])
        get_solera = self.env['dtm.materiales.solera'].search([])
        get_tornillos = self.env['dtm.materiales.tornillos'].search([])
        get_tubos = self.env['dtm.materiales.tubos'].search([])
        get_varilla = self.env['dtm.materiales.varilla'].search([])
        myset = []
        id = 1

        for lamina in get_lamina:
            # print(lamina.material_id.nombre + " " + str(lamina.largo) + " " + str(lamina.ancho) + " @ " + str(lamina.calibre))
            nombre = "Lámina " + lamina.material_id.nombre + " "
            medida = str(lamina.largo) + " x " + str(lamina.ancho) + " @ " + str(lamina.calibre)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            myset.append(nombre+medida)
            print("Área",lamina.largo,lamina.ancho)
            area = float(lamina.largo) * float(lamina.ancho)
            self.insertar(str(lamina.cantidad),nombre,medida,get_info,area)
            id += 1

        for angulo in get_angulos:
            nombre =  "Ángulo "+ angulo.material_id.nombre
            medida = str(angulo.alto) + " x " + str(angulo.ancho) + " @ " + str(angulo.calibre) +", " + str(angulo.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(angulo.cantidad),nombre,medida,get_info,angulo.largo)
            myset.append(nombre+medida)
            id += 1

        for canal in get_canal:
            nombre = "Canal "+  canal.material_id.nombre
            medida = str(canal.alto) + " x " + str(canal.ancho) + " espesor " + str(canal.espesor) +", " + str(canal.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(canal.cantidad),nombre,medida,get_info,canal.largo)
            myset.append(nombre+medida)
            id += 1

        for perfiles in get_perfiles:
            nombre = "Perfil "+  perfiles.material_id.nombre
            medida = str(perfiles.alto) + " x " + str(perfiles.ancho) + " @ " + str(perfiles.calibre) +", " + str(perfiles.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])

            self.insertar(str(perfiles.cantidad),nombre,medida,get_info,perfiles.largo)
            myset.append(nombre + medida)
            id += 1

        for pintura in get_pintura:
            nombre = "Pintura "+  pintura.material_id.nombre
            medida = str(pintura.cantidades)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(pintura.cantidad),nombre,medida,get_info)
            myset.append(nombre+medida)
            id += 1

        for rodamientos in get_rodamientos:
            nombre = rodamientos.material_id.nombre
            medida = str(rodamientos.descripcion)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(rodamientos.cantidad),nombre,medida,get_info)
            myset.append(nombre+medida)
            id += 1

        for solera in get_solera:
            nombre = "Solera "+  solera.material_id.nombre
            medida = str(solera.largo) + " x " + str(solera.ancho) + " @ " + str(solera.calibre)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(solera.cantidad),nombre,medida,get_info,solera.largo)
            myset.append(nombre+medida)
            id += 1

        for tornillos in get_tornillos:
            nombre = tornillos.material_id.nombre
            medida = str(tornillos.diametro) + " x " + str(tornillos.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(tornillos.cantidad),nombre,medida,get_info)
            myset.append(nombre+medida)
            id += 1

        for tubos in get_tubos:
            nombre = "Tubo "+  tubos.material_id.nombre
            medida = str(tubos.diametro) + " x " + str(tubos.largo) + " @ " + str(tubos.calibre)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(tubos.cantidad),nombre,medida,get_info,tubos.largo)
            myset.append(nombre+medida)
            id += 1

        for varilla in get_varilla:
            nombre = "Varilla "+  varilla.material_id.nombre
            medida = str(varilla.diametro) + " x " + str(varilla.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
            self.insertar(str(varilla.cantidad),nombre,medida,get_info,varilla.largo)
            myset.append(nombre+medida)
            id += 1
        self.clean_table(myset)

        # Carga los materiales del modelo dtm.materials.line que son nuevos (no están en el almacén)

        get_odt = self.env['dtm.materials.line'].search([])
        for get in get_odt:
            get_this = self.env['dtm.diseno.almacen'].search([("nombre","=",get.nombre),("medida","=",get.medida)])
            # print(get_this.id)
            if get_this:
                # print(get_this.id,get_this.nombre,get_this.medida)
                pass
            else:
                # print(get_this)
                # print(get.nombre, get.medida)
                if get.materials_list:# Existe en dtm_materials_line pero no en dtm_diseno_almacen, lo agrega a dtm_diseno_almacen

                    # print("result 2",get.nombre +" "+ get.medida, get.id,get.materials_list.id)
                    get_act = self.env['dtm.diseno.almacen'].search([("id","=",get.materials_list.id)])
                    if not get_act:
                        # print(get_act.id)
                        self.env.cr.execute("INSERT INTO dtm_diseno_almacen (id,nombre,medida,cantidad) VALUES ("+str(get.materials_list.id)+", '"+str(get.nombre)+"','"+str(get.medida)+"', 0)")
                    # self.env.cr.execute("UPDATE dtm_diseno_almacen SET nombre='"+get.nombre+"', medida='"+get.medida+"' WHERE id="+str(get.materials_list.id))
                        act = self.env['dtm.diseno.almacen'].search([("id", "=", get.materials_list.id)])
                        self.env.cr.execute("UPDATE dtm_materials_line SET  nombre='"+act.nombre+"', medida='"+act.medida+"' WHERE materials_list=" + str(get.materials_list.id))
                else:
                    cont = self.env['dtm.diseno.almacen'].search_count([])
                    # print(cont)
                    for iterator in range (1,cont):
                        # print("iterator",iterator)
                        get_id = self.env['dtm.diseno.almacen'].search([("id","=",iterator)])
                        if not get_id:
                            # print("iterator",get_id.nombre)
                            self.env.cr.execute("INSERT INTO dtm_diseno_almacen (id,nombre,medida,cantidad) VALUES ("+str(iterator)+",'"+str(get.nombre)+"','"+str(get.medida)+"', 0)")
                            self.env.cr.execute("UPDATE dtm_materials_line SET materials_list="+str(iterator)+" WHERE id="+str(get.id))
                            break

        return res




