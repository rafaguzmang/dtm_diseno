from odoo import fields,models

class MaterialesDiseno(models.Model):
    _name = "dtm.materiales.diseno"

    material = fields.Char(string="MATERIAL", readonly=True)
    calibre = fields.Char(string="CALIBRE", readonly=True)
    largo = fields.Char(string="LARGO", default="0", readonly=True)
    ancho = fields.Char(string="ANCHO", default="0", readonly=True)
    cantidad = fields.Integer(string="CANTIDAD", readonly=True)



