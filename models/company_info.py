# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json

class CompanyInfo(models.Model):
    _name = 'web_company_search.company_info'
    _description = 'Informações da Empresa'

    name = fields.Char(string='Nome da Empresa')
    cnpj = fields.Char(string='CNPJ')
    address = fields.Char(string='Endereço')
    phone = fields.Char(string='Telefone')
    website = fields.Char(string='Website')
    search_request_id = fields.Many2one('web_company_search.search_request', string='Requisição de Pesquisa', ondelete='cascade')

    @api.model
    def _get_webhook_url(self):
        # Configuração dinâmica da URL do webhook a partir de uma configuração do sistema ou campo do modelo,
        # por enquanto definindo uma url padrão.
        return "https://brain.nandus.com.br/webhook/module-odoo-wcs"

    def send_webhook(self):
        """Envia as informações da empresa para o webhook."""
        webhook_url = self._get_webhook_url()
        
        if not webhook_url:
            return {
                'warning': {
                    'title': 'Configuração do Webhook',
                    'message': 'A URL do webhook não está configurada.'
                }
            }

        data = {
            'name': self.name,
            'cnpj': self.cnpj,
            'address': self.address,
            'phone': self.phone,
            'website': self.website,
        }

        headers = {'Content-type': 'application/json'}
        try:
            response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
            response.raise_for_status()  # Lança exceção para status de erro HTTP
            # Log da resposta, se necessário
            self.env['ir.logging'].create({
                'name': 'Webhook Response',
                'type': 'server',
                'level': 'info',
                'message': f'Webhook enviado com sucesso para {webhook_url}. Resposta: {response.text}'
            })
        except requests.exceptions.RequestException as e:
             self.env['ir.logging'].create({
                'name': 'Webhook Error',
                'type': 'server',
                'level': 'error',
                'message': f'Erro ao enviar o webhook para {webhook_url}: {e}'
            })
        return True