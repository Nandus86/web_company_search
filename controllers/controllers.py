# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import requests
import json

class WebCompanySearch(http.Controller):
    @http.route('/web/api/search_companies', auth='public', methods=['POST'], csrf=False)
    def search_companies(self, **kw):
        """
        Endpoint para receber os termos de pesquisa e iniciar a busca.
        """
        term = kw.get('term')
        if not term:
            return {
                "status": "error",
                "message": "Termo de pesquisa não fornecido."
            }
        
        search_request = request.env['web_company_search.search_request'].create({'term': term, 'status':'pending'})

        webhook_url = self._get_search_webhook_url()  # Recupera a URL do webhook de pesquisa
        if not webhook_url:
            return {
                "status": "error",
                "message": "URL do webhook de pesquisa não configurada."
            }

        try:
            headers = {'Content-type': 'application/json'}
            payload = {'term': term}
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list):
                for item in data:
                   
                    company_data = {
                        'name': item.get('name', 'N/A'),
                        'cnpj': item.get('cnpj', 'N/A'),
                        'address': item.get('address', 'N/A'),
                        'phone': item.get('phone', 'N/A'),
                        'website': item.get('website', 'N/A'),
                        'search_request_id': search_request.id,
                    }
                    request.env['web_company_search.company_info'].create(company_data)
                
                search_request.write({'status': 'done'})

                return {
                    "status": "success",
                    "message": f"Empresas encontradas para o termo '{term}'.",
                    "results": data
                }
            else:
                 return {
                    "status": "warning",
                    "message": f"Nenhuma empresa encontrada para o termo '{term}'.",
                    "results": []
                }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Erro ao contatar o webhook de pesquisa: {e}"
            }

    def _get_search_webhook_url(self):
         # Configuração dinâmica da URL do webhook a partir de uma configuração do sistema ou campo do modelo,
        # por enquanto definindo uma url padrão.
        return "https://brain.nandus.com.br/webhook/module-odoo-wcs"