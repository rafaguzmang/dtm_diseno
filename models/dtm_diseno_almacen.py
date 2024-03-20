from odoo import api,fields,models


class Materiales(models.Model):
    _name = "dtm.diseno.almacen"
    _description = "Modelo donde se concentrán todos los materiales disponibles en almacén"
    # _rec_name = "nombre"

    # numero = fields.Integer(string="Número")
    nombre = fields.Char(string="Nombre", readonly=False,store=True, require=True)
    medida = fields.Char(string="Medidas", readonly=False)
    caracteristicas = fields.Char(string="Caracteristicas", readonly=True)
    notas = fields.Text(string="Notas")
    area = fields.Float(string="Área/Largo")
    cantidad = fields.Integer()

    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res

    def insertar(self,cantidad,nombre,medida,valor,area,caracteristicas):
            if valor:
                existe =True
            else:
                existe = False

            if not caracteristicas:
                caracteristicas = ""

            if existe:
                self.env.cr.execute("UPDATE dtm_diseno_almacen SET cantidad="+cantidad+", area="+str(area)+", caracteristicas='"+caracteristicas+"' WHERE nombre='"+nombre+"' and medida='"+medida+"'")
            else:
                self.env.cr.execute("INSERT INTO dtm_diseno_almacen ( cantidad, nombre, medida, area,caracteristicas) VALUES ("+cantidad+", '"+nombre+"', '"+medida+"',"+str(area)+", '"+ caracteristicas+ "')")


    def clean_table(self,myset):
        get_info = self.env['dtm.diseno.almacen'].search([])
        no_repeat = set(myset)
        # print(no_repeat)
        for get in get_info:
            # print(get.nombre,get.medida)
            if get.nombre and get.medida:
                if get.nombre+get.medida not in no_repeat:
                    self.env.cr.execute("DELETE FROM dtm_diseno_almacen WHERE nombre='"+get.nombre+"' AND medida='"+get.medida+"'")

    def get_view(self, view_id=None, view_type='form', **options):#Carga los items de todos los módulos de Almacén en un solo módulo de diseño
        res = super(Materiales,self).get_view(view_id, view_type,**options)
        # get_lamina = self.env['dtm.materiales'].search([])
        # get_angulos = self.env['dtm.materiales.angulos'].search([])
        # get_canal = self.env['dtm.materiales.canal'].search([])
        # get_perfiles = self.env['dtm.materiales.perfiles'].search([])
        # get_pintura = self.env['dtm.materiales.pintura'].search([])
        # get_rodamientos = self.env['dtm.materiales.rodamientos'].search([])
        # get_solera = self.env['dtm.materiales.solera'].search([])
        # get_tornillos = self.env['dtm.materiales.tornillos'].search([])
        # get_tubos = self.env['dtm.materiales.tubos'].search([])
        # get_varilla = self.env['dtm.materiales.varilla'].search([])
        # myset = []
        # id = 1

        # for lamina in get_lamina:
        #     # print(lamina.material_id.nombre + " " + str(lamina.largo) + " " + str(lamina.ancho) + " @ " + str(lamina.calibre))
        #     nombre = "Lámina " + lamina.material_id.nombre + " "
        #     medida = str(lamina.largo) + " x " + str(lamina.ancho) + " @ " + str(lamina.calibre)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     myset.append(nombre+medida)
        #     area = float(lamina.largo) * float(lamina.ancho)
        #     disponible = lamina.cantidad - lamina.apartado
        #     descripcion = lamina.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,area,descripcion)
        #     id += 1

        # for angulo in get_angulos:
        #     nombre =  "Ángulo "+ angulo.material_id.nombre
        #     medida = str(angulo.alto) + " x " + str(angulo.ancho) + " @ " + str(angulo.calibre) +", " + str(angulo.largo)# Da formato al campo medida
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = angulo.cantidad - angulo.apartado
        #     descripcion = angulo.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,angulo.largo,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for canal in get_canal:
        #     nombre = "Canal "+  canal.material_id.nombre
        #     medida = str(canal.alto) + " x " + str(canal.ancho) + " espesor " + str(canal.espesor) +", " + str(canal.largo)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = canal.cantidad - canal.apartado
        #     descripcion = canal.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,canal.largo,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for perfiles in get_perfiles:
        #     nombre = "Perfil "+  perfiles.material_id.nombre
        #     medida = str(perfiles.alto) + " x " + str(perfiles.ancho) + " @ " + str(perfiles.calibre) +", " + str(perfiles.largo)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     descripcion = perfiles.descripcion
        #     self.insertar(str(perfiles.cantidad),nombre,medida,get_info,perfiles.largo,descripcion)
        #     myset.append(nombre + medida)
        #     id += 1
        #
        # for pintura in get_pintura:
        #     nombre = "Pintura "+  pintura.material_id.nombre
        #     medida = str(pintura.cantidades)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = pintura.cantidad - pintura.apartado
        #     descripcion = pintura.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,0,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for rodamientos in get_rodamientos:
        #     nombre = "Rodamientos "+rodamientos.material_id.nombre
        #     medida = str(rodamientos.descripcion)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = rodamientos.cantidad - rodamientos.apartado
        #     descripcion = rodamientos.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,0,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for solera in get_solera:
        #     nombre = "Solera "+  solera.material_id.nombre
        #     medida = str(solera.largo) + " x " + str(solera.ancho) + " @ " + str(solera.calibre)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = solera.cantidad - solera.apartado
        #     descripcion = solera.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,solera.largo,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for tornillos in get_tornillos:
        #     nombre = "Tornillo "+tornillos.material_id.nombre
        #     medida = str(tornillos.diametro) + " x " + str(tornillos.largo)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = tornillos.cantidad - tornillos.apartado
        #     descripcion = tornillos.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,0,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for tubos in get_tubos:
        #     nombre = "Tubo "+  tubos.material_id.nombre
        #     medida = str(tubos.diametro) + " x " + str(tubos.largo) + " @ " + str(tubos.calibre)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = tubos.cantidad - tubos.apartado
        #     descripcion = tubos.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,tubos.largo,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        #
        # for varilla in get_varilla:
        #     nombre = "Varilla "+  varilla.material_id.nombre
        #     medida = str(varilla.diametro) + " x " + str(varilla.largo)
        #     get_info = self.env['dtm.diseno.almacen'].search([("nombre","=",nombre),("medida","=",medida)])
        #     disponible = varilla.cantidad - varilla.apartado
        #     descripcion = varilla.descripcion
        #     self.insertar(str(disponible),nombre,medida,get_info,varilla.largo,descripcion)
        #     myset.append(nombre+medida)
        #     id += 1
        # self.clean_table(myset)

        # Carga los materiales del modelo dtm.materials.line que son nuevos (no están en el almacén)

        # get_odt = self.env['dtm.materials.line'].search([])
        # for get in get_odt:
        #     get_this = self.env['dtm.diseno.almacen'].search([("nombre","=",get.nombre),("medida","=",get.medida)])
        #     # print(get_this.id)
        #     if get_this:
        #         # print(get_this.id,get_this.nombre,get_this.medida)
        #         pass
        #     else:
        #         # print(get_this)
        #         # print(get.nombre, get.medida)
        #         if get.materials_list:# Existe en dtm_materials_line pero no en dtm_diseno_almacen, lo agrega a dtm_diseno_almacen
        #
        #             # print("result 2",get.nombre +" "+ get.medida, get.id,get.materials_list.id)
        #             get_act = self.env['dtm.diseno.almacen'].search([("id","=",get.materials_list.id)])
        #             if not get_act:
        #                 # print(get_act.id)
        #                 self.env.cr.execute("INSERT INTO dtm_diseno_almacen (id,nombre,medida,cantidad) VALUES ("+str(get.materials_list.id)+", '"+str(get.nombre)+"','"+str(get.medida)+"', 0)")
        #             # self.env.cr.execute("UPDATE dtm_diseno_almacen SET nombre='"+get.nombre+"', medida='"+get.medida+"' WHERE id="+str(get.materials_list.id))
        #                 act = self.env['dtm.diseno.almacen'].search([("id", "=", get.materials_list.id)])
        #                 self.env.cr.execute("UPDATE dtm_materials_line SET  nombre='"+act.nombre+"', medida='"+act.medida+"' WHERE materials_list=" + str(get.materials_list.id))
        #         else:
        #             cont = self.env['dtm.diseno.almacen'].search_count([])
        #             # print(cont)
        #             for iterator in range (1,cont):
        #                 # print("iterator",iterator)
        #                 get_id = self.env['dtm.diseno.almacen'].search([("id","=",iterator)])
        #                 if not get_id:
        #                     # print("iterator",get_id.nombre)
        #                     self.env.cr.execute("INSERT INTO dtm_diseno_almacen (id,nombre,medida,cantidad) VALUES ("+str(iterator)+",'"+str(get.nombre)+"','"+str(get.medida)+"', 0)")
        #                     self.env.cr.execute("UPDATE dtm_materials_line SET materials_list="+str(iterator)+" WHERE id="+str(get.id))
        #                     break

        return res




