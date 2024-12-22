# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json

class SearchRequest(models.Model):
    _name = 'web_company_search.search_request'
    _description = 'Requisição de Pesquisa de Empresa'

    term = fields.Char(string='Termo de Pesquisa', required=True)
    search_date = fields.Datetime(string='Data da Pesquisa', default=fields.Datetime.now)
    results = fields.One2many('web_company_search.company_info', 'search_request_id', string='Resultados')
    status = fields.Selection([('pending','Pendente'), ('done','Concluido')], string="Status", default="pending")

    def search_companies_action(self):
          """Envia a requisição para o endpoint de pesquisa."""
          base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
          
          url = f"{base_url}/web/api/search_companies"

          payload = {'term': self.term}
          headers = {'Content-type': 'application/json'}
          try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # Lança exceção para status de erro HTTP
            # Log da resposta, se necessário
            self.env['ir.logging'].create({
                'name': 'Search Companies Response',
                'type': 'server',
                'level': 'info',
                'message': f'Requisição enviada com sucesso para {url}. Resposta: {response.text}'
            })
          except requests.exceptions.RequestException as e:
             self.env['ir.logging'].create({
                'name': 'Search Companies Error',
                'type': 'server',
                'level': 'error',
                'message': f'Erro ao enviar o requisição para {url}: {e}'
            })

          
          return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'title': 'Sucesso',
                'message': 'Pesquisa enviada com sucesso!',
                'type': 'success',
                'sticky': False,
                 }
           }