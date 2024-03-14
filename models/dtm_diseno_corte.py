from odoo import api,fields,models
import datetime


class Corte (models.Model):
    _name = "dtm.diseno.corte"
    _description = "Modulo donde se almacenan los cortes para la máquina laser por No. de orden"


    no_orden = fields.Integer(string="PO")
    odt_id = fields.One2many("dtm.diseno.item", "model_id")
    date = fields.Date(string="Fecha" ,default= datetime.datetime.today(), readonly=True)
    notas = fields.Text(string="Notas")


class Item(models.Model):
    _name = "dtm.diseno.item"
    _description = "Modulo donde se almacenan todos los items de las ordenes de trabajo"

    model_id = fields.Many2one("dtm.diseno.corte")
    odt = fields.Integer
    item = fields.Char(string="Item")
    drawingname  = fields.Char(string="DRAWINGNAME")
    cantidad = fields.Char(string="SHEETS")


