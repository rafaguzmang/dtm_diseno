{
    "name":"Diseño",
    'installable': True,
     'application': False,
    "data":[
        #Security
        'security/ir.model.access.csv',

        #Views
        'views/dtm_diseno_almacen_views.xml',
        'views/dtm_diseno_consumibles_view.xml',
        'views/dtm_herramienta_view.xml',
        'views/dtm_materiales_view.xml',

        #Menú
        'views/menu_item.xml'

    ],
    "depends" : ["base"],
    'license': 'LGPL-3',
}
