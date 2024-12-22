# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import json
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class WebScrapingModel(models.Model):
    _name = 'webscraping.model'
    _description = 'Web Scraping Model'

    name = fields.Char(string='Text Field', required=True)
    webhook_url = fields.Char(string='Webhook URL', 
                            default='https://brain.nandus.com.br/webhook-test/verifica-html',
                            config_parameter='webscraping_v1.webhook_url')

    def send_webhook(self):
        """Send data to webhook"""
        self.ensure_one()
        webhook_url = self.env['ir.config_parameter'].sudo().get_param('webscraping_v1.webhook_url')
        
        if not webhook_url:
            raise UserError(_('Please configure the webhook URL in System Parameters'))

        payload = {
            'dado': self.name
        }

        try:
            response = requests.post(webhook_url, 
                                  json=payload,
                                  headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _('Data sent successfully!'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            raise UserError(_('Failed to send data: %s') % str(e))