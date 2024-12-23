{
    'name': 'Contatos Webhook',
    'version': '16.0.1.0.0',
    'summary': 'Módulo para receber contatos via webhook e gerenciar envios',
    'description': '''
        Módulo para gerenciamento de contatos recebidos via webhook.
        Funcionalidades:
        - Recebimento de contatos via webhook
        - Gerenciamento de mensagens
        - Envio personalizado de mensagens
        - Integração com res.partner
    ''',
    'category': 'Tools',
    'author': 'Fernando Dias - v.1.0.2',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/contatos_webhook_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_views.xml',
        'views/webscraping_view.xml',
        'data/config_parameter.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}