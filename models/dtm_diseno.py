from odoo import api,fields,models

class DisenoMateriales(models.Model):
    _name = 'dtm.diseno'
    _description = "Modulo del área de diseño"

    drawingname  = fields.Char(string="DRAWINGNAME")
    sheets = fields.Char(string="SHEETS")
    material_id = fields.Many2one('dtm.materiales')
    @api.onchange("sheets")
    def _onchange_apartado(self):
        if self.material_id.id:
            self.env.cr.execute("UPDATE dtm_materiales SET apartado = "+ str(self.sheets) +" WHERE id = " + str(self.material_id.id))

class Realizados(models.Model):
    _name = "dtm.diseno.realizados"
    _description = "Lleva el listado de todo el material cortado en la Laser"
    drawingname  = fields.Char(string="DRAWINGNAME")
    sheets = fields.Char(string="SHEETS")
    material_id = fields.Char(string="MATERIALES")

class Materiales(models.Model):
    _name = "dtm.diseno.materiales"
    _description = "Carga la tabla de materiales del Modulo dtm_materiales para uso del diseñador"
    material = fields.Char(string="MATERIAL")
    calibre = fields.Float(string="CALIBRE")
    largo = fields.Float(string="LARGO")
    ancho = fields.Float(string="ANCHO")
    area = fields.Float(string="AREA")
    cantidad = fields.Integer(string="STOCK")
    apartado = fields.Integer(string="APARTADO")
    disponible = fields.Integer(string="DISPONIBLE")

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Materiales,self).get_view(view_id, view_type,**options)

        get_info = self.env['dtm.materiales'].search([])

        self.env.cr.execute("DELETE FROM dtm_diseno_materiales ")
        for result in get_info:
            id = str(result.id)
            material = str(result.material_id.nombre)
            calibre = str(result.calibre)
            largo = str(result.largo)
            ancho = str(result.ancho)
            area = str(result.area)
            disponible = str(result.disponible)
            self.env.cr.execute("INSERT INTO dtm_diseno_materiales (id, material, calibre, largo, ancho, area, disponible)" +
                                "VALUES ("+id+",'"+ material + "','" + calibre + "','" + largo + "','" + ancho + "','" + area +  "','" + disponible +"')")
        return res



