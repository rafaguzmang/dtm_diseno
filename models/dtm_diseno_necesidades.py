from odoo import fields,models,api

class Nececidades(models.Model):
    _name = "dtm.diseno.necesidades"
    _description = "Modulo para que el o los diseñadores vean las necesidades del cliente"

    no_cotizacion = fields.Char(string="No. De Necesidad", readonly=True)
    cliente = fields.Char(string="Cliente", readonly=True)
    atencion = fields.Char(string="Nombre del requisitor", readonly=True)
    date = fields.Date(string="Fecha", readonly=True)
    telefono = fields.Char(string="Telefono(s)", readonly=True )
    correo = fields.Char(string = "email(s)", readonly=True)
    cotizacion = fields.Boolean(default=False)
    nivel = fields.Char(string="Nivel", readonly=True)
    notes = fields.Text()

    list_materials_ids = fields.One2many('dtm.diseno.list.material', 'model_id',compute="_compute_no_cotizacion",readonly=True)

    def _compute_no_cotizacion(self):
        for result in self:
            get_atencion = self.env['dtm.client.needs'].search([("id","=",result.id)])

            lines = []
            for get in get_atencion.list_materials_ids:
                line =(4,get.id,{})
                lines.append(line)
            result.list_materials_ids = lines


    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Nececidades,self).get_view(view_id, view_type,**options)

        get_info = self.env['dtm.client.needs'].search([])
        self.env.cr.execute("DELETE FROM dtm_diseno_necesidades ")
        for result in get_info:
            id = str(result.id)
            no_cotizacion = result.no_cotizacion
            cliente = str(result.cliente_ids.name)

            date = str(result.date)
            attachment_ids = str(result.attachment_ids)
            telefono = str(result.telefono)
            correo = str(result.correo)
            cotizacion = str(result.cotizacion)
            nivel = str(result.nivel)

            if result.notes:
                notes = str(result.notes)
            else:
                notes = ""

            # print(id,no_cotizacion,cliente,atencion,date,attachment_ids,telefono,correo,cotizacion,nivel)
            get_atencion = self.env['dtm.client.needs'].search([("id","=",id)])
            atencion = ""
            for result in get_atencion:
                # print(result.cliente_ids.name)
                atencion += result.cliente_ids.name
            self.env.cr.execute("INSERT INTO dtm_diseno_necesidades (id, no_cotizacion, cliente, atencion, date, telefono, correo, cotizacion,nivel,notes)" +
                                "VALUES ("+id+",'"+ no_cotizacion + "','" + cliente + "','" + atencion + "','" + date + "','" + telefono +  "','" + correo + "','" + cotizacion + "','" + nivel + "','" + notes +"')")

            get_materials = self.env['cot.list.material'].search([])
            for result in get_materials:
                # print(result.cliente_ids.name)
                id = str(result.id)
                name = str(result.name)
                descripcion = str(result.descripcion)
                cantidad = str(result.cantidad)
                # attachment_ids = str(result.attachment_ids)

                # print(id,name,descripcion,cantidad)
                get_dlm = self.env['dtm.diseno.list.material'].search([("id","=", int(id))])
                if get_dlm:
                    self.env.cr.execute("UPDATE dtm_diseno_list_material SET name='" + name + "', descripcion= '"+descripcion+"', cantidad='"+cantidad+"' "+
                                        "WHERE id="+id)
                else:
                    self.env.cr.execute("INSERT INTO dtm_diseno_list_material (id, name, descripcion, cantidad)" +
                                    "VALUES ("+id+", '"+ name + "','" + descripcion + "'," + cantidad + ")")



        return res


class ListMaterial(models.Model):
    _name = "dtm.diseno.list.material"

    model_id = fields.Many2one("dtm.diseno.necesidades")
    name = fields.Char(string="Producto o servicio", readonly=True)
    descripcion = fields.Text(string="Descripción", readonly=True)
    cantidad = fields.Integer(string="Cantidad", readonly=True)
    attachment_ids = fields.Many2many("dtm.documentos.anexos", compute="_compute_attachment_ids",string="Archivos", readonly=True)

    def _compute_attachment_ids(self):
        for result in self:
            get_anex = self.env['dtm.documentos.anexos'].search([("id","=",result.id)])
            lines = []
            for get in get_anex:
                line =(4,get.id,{})
                lines.append(line)
            result.attachment_ids = lines
