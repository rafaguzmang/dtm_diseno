from odoo import api,fields,models
from odoo.exceptions import ValidationError
import re



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

    # @api.onchange("nombre")
    # def _action_nombre(self):
    #     if self.nombre:
    #         txt = self.nombre
    #         txt = re.sub(".*[lL][aAáÁ][mM][iI][nN][aA][sS].*", "Lámina", txt)
    #         txt = re.sub(".*[cC][aA][rR][bB][oOóÓ][nN].*", "Lámina Acero al carbón", txt)
    #         txt = re.sub(".*[nN][eE][gG][rR][aA].*", "Lámina Acero al carbón", txt)
    #         self.nombre = txt
    #
    #
    # @api.onchange("medida")
    # def _action_medida(self):
    #     if self.medida:
    #         txt = self.medida
    #         ntxt = ""
    #         for num in txt:
    #             if not num.isdecimal():
    #                 num = " " + num + " "
    #             ntxt = ntxt + num
    #         ntxt = re.sub("^\s+","", ntxt)
    #         ntxt = re.sub("\s+$","", ntxt)
    #         ntxt = re.sub("\s+"," ", ntxt)
    #
    #         ntxtList = ntxt.split(" ")
    #         ftxt = ""
    #         for num in ntxtList:
    #             if re.match("\d",num):
    #                 num = str(float(num))
    #             ftxt = ftxt +" " + num
    #         ftxt = re.sub("\s+$","", ftxt)
    #         self.medida = ftxt

    def name_get(self):#--------------------------------Arreglo para cuando usa este modulo como Many2one--------------------
        res = []
        for result in self:
            res.append((result.id,f'{result.id}-  {result.nombre} {result.medida}'))
        return res



    def get_view(self, view_id=None, view_type='form', **options):#Carga los items de todos los módulos de Almacén en un solo módulo de diseño
        res = super(Materiales,self).get_view(view_id, view_type,**options)
        return res

    @api.model
    def create(self,vals):
        res = super(Materiales, self).create(vals)

        get_info = self.env['dtm.diseno.almacen'].search([])

        mapa ={}
        for info in get_info:
            nombre = info.nombre
            medida = info.medida

            cadena = nombre,medida

            if mapa.get(cadena):
                info.unlink()
                raise ValidationError("Material Duplicado")
            else:
                mapa[cadena] = 1
        return res




