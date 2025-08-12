from odoo import fields,api,models

class Consumibles(models.Model):
    _name = 'dtm.diseno.consumibles'
    _description = 'Modelo para llevar el conteo de los consumibles'

    fecha = fields.Date(string='Fecha')
    codigo = fields.Integer(string="ID")
    nombre = fields.Char(string="Nombre")
    cantidad = fields.Integer(string="Stock", default=0)
    entregado = fields.Char(string="Entregado")
    recibe = fields.Char(string="Recibe")
    notas = fields.Text(string="Notas")




