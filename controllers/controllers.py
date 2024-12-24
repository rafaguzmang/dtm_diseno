from odoo import http
from odoo.http import request, Response
import json

class DtmOdooController(http.Controller):
    pass
    # @http.route('/web/dtm_odt/almacen', type='http', auth='none', csrf=False)
    # def get_almacen(self, **kwargs):
    #     inventario = request.env['dtm.diseno.almacen'].sudo().search([])
    #     result = [{
    #         'nombre': item.nombre,
    #         'medida': item.medida,
    #         'notas': item.notas,
    #         'localizacion': item.localizacion if item.localizacion else '',
    #         'cantidad': item.cantidad,
    #         'apartado': item.apartado,
    #         'disponible': item.disponible
    #     } for item in inventario]
    #     return request.make_response(
    #         json.dumps(result),
    #         headers={
    #             'Content-Type': 'application/json',
    #             'Access-Control-Allow-Origin': '*',  # Permite solicitudes de cualquier dominio
    #             'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',  # Métodos permitidos
    #             'Access-Control-Allow-Headers': 'Content-Type, Authorization,origin, x-csrftoken, content-type, accep',  # Cabeceras permitidas
    #             'Access-Control-Allow-Credentials': 'true',  # Permitir cookies y credenciales (si es necesario)
    #         }
    #     )
    #
    # @http.route('/cors', type='http', auth='none', methods=['OPTIONS'], csrf=False)
    #  @http.route('/cors', type='http', auth='none', methods=['OPTIONS'], csrf=False)
    # def preflight(self):
    #     # Obtener el origen de la solicitud
    #     origin = request.httprequest.headers.get('Origin')
    #
    #     # Permitir solicitudes desde un origen específico
    #     allowed_origins = ['http://localhost:4200']  # Asegúrate de incluir todos los orígenes permitidos
    #
    #     # Verificar si el origen está permitido
    #     if origin in allowed_origins:
    #         response_origin = origin
    #     else:
    #         response_origin = '*'  # Puedes poner un * para aceptar todos los orígenes si lo deseas (aunque no es recomendado para solicitudes con credenciales)
    #
    #     # Construir la respuesta CORS
    #     response = request.make_response(
    #         json.dumps({'message': 'CORS preflight successful'}),
    #         headers={
    #             'Access-Control-Allow-Origin': response_origin,  # Retornar el origen permitido
    #             'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    #             'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization, talview-odoo-api',
    #             'Access-Control-Allow-Credentials': 'true',  # Permitir credenciales
    #             'Content-Type': 'application/json'
    #         }
    #     )
    #
    #     # Establecer el código de estado HTTP 200
    #     response.status_code = 200
    #     return response
