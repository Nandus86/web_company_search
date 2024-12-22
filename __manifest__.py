# -*- coding: utf-8 -*-
{
    'name': "Pesquisar Empresas Web",
    'summary': """
        Módulo para pesquisar empresas via web scraping e enviar informações para webhooks.""",
    'description': """
        Este módulo permite pesquisar informações de empresas através de um webhook externo e gerenciar esses dados no Odoo.
        Além disso, permite o envio de informações para um webhook específico.
    """,
    'author': "Fernando Dias - v.1.0.2",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}