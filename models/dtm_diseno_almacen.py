from odoo import api,fields,models


class Materiales(models.Model):
    _name = "dtm.diseno.almacen"
    _description = "Modelo donde se concentrán todos los materiales disponibles en almacén"
    # _rec_name = "nombre"

    nombre = fields.Char(string="Nombre", readonly=False,compute="_compute_id",store=True)
    medida = fields.Char(string="MedidaS", readonly=False)
    caracteristicas = fields.Char(string="Caracteristicas", readonly=False)
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

    def insertar(self,cantidad,nombre,medida,id,valor):
            if valor:
                existe =True
            else:
                existe = False
            if existe:
                self.env.cr.execute("UPDATE dtm_diseno_almacen SET cantidad="+cantidad+", nombre='"+nombre+"', medida='"+medida+"' WHERE id="+id)
            else:
                self.env.cr.execute("INSERT INTO dtm_diseno_almacen (id, cantidad, nombre, medida) VALUES ("+id+", "+cantidad+", '"+nombre+"', '"+medida+"')")

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
        id = 1
        for lamina in get_lamina:
            # print(lamina.material_id.nombre + " " + str(lamina.largo) + " " + str(lamina.ancho) + " @ " + str(lamina.calibre))
            nombre = "Lámina " +lamina.material_id.nombre + " "
            medida = str(lamina.largo) + " x " + str(lamina.ancho) + " @ " + str(lamina.calibre)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])

            self.insertar(str(lamina.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for angulo in get_angulos:
            nombre =  "Ángulo "+ angulo.material_id.nombre
            medida = str(angulo.alto) + " x " + str(angulo.ancho) + " @ " + str(angulo.calibre) +", " + str(angulo.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(angulo.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for canal in get_canal:
            nombre = "Ángulo "+  canal.material_id.nombre
            medida = str(canal.alto) + " x " + str(canal.ancho) + " espesor " + str(canal.espesor) +", " + str(canal.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(canal.cantidad),nombre,medida,str(id),get_info)
            # print(nombre)
            id += 1

        for perfiles in get_perfiles:
            nombre = "Ángulo "+  perfiles.material_id.nombre
            medida = str(perfiles.alto) + " x " + str(perfiles.ancho) + " @ " + str(perfiles.calibre) +", " + str(perfiles.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(perfiles.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for pintura in get_pintura:
            nombre = "Ángulo "+  pintura.material_id.nombre
            medida = str(pintura.cantidades)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(pintura.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for rodamientos in get_rodamientos:
            nombre = rodamientos.material_id.nombre
            medida = str(rodamientos.descripcion)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(rodamientos.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for solera in get_solera:
            nombre = "Solera "+  solera.material_id.nombre
            medida = str(solera.largo) + " x " + str(solera.ancho) + " @ " + str(solera.calibre)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(solera.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for tornillos in get_tornillos:
            nombre = tornillos.material_id.nombre
            medida = str(tornillos.diametro) + " x " + str(tornillos.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(tornillos.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for tubos in get_tubos:
            nombre = "Tubo "+  tubos.material_id.nombre
            medida = str(tubos.diametro) + " x " + str(tubos.largo) + " @ " + str(tubos.calibre)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(tubos.cantidad),nombre,medida,str(id),get_info)
            id += 1

        for varilla in get_varilla:
            nombre = "Varilla "+  varilla.material_id.nombre
            medida = str(varilla.diametro) + " x " + str(varilla.largo)
            get_info = self.env['dtm.diseno.almacen'].search([("id","=",id)])
            self.insertar(str(varilla.cantidad),nombre,medida,str(id),get_info)
            id += 1

        get_info = self.env['dtm.diseno.almacen'].search([])
        id = 1
        for result in get_info:
            if result.id != id:
                print(id)
                self.env.cr.execute("UPDATE dtm_diseno_almacen SET id='"+str(id)+"' WHERE id="+str(result.id))
            id += 1

        return res




