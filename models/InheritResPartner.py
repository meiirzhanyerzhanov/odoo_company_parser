# -*- coding: utf-8 -*-
# Copyright <2017> <Tenovar Ltd>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields
import xmlrpc.client
from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool

class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    region = fields.Char(string='Регион')
    nas_punkt = fields.Char(string='Населенный пункт')
    url = fields.Char(string='URL address')
    vid_deyatelnosti = fields.Char(string='Вид деятельности')
    ur_address = fields.Char(string='Юридический адрес')
    fact_address = fields.Char(string='Фактический адрес')
    sector_econ = fields.Char(string='Сектор экономики')
    org_right_form = fields.Char(string='Организационно-правовая форма')
    form_sobs = fields.Char(string='Форма собственности')
    status_pred = fields.Char(string='Статус предприятия')
    bin = fields.Char(string='БИН')
    year_form = fields.Char(string='Год образования')
    status_platelshik = fields.Char(string='Статус плательщика')
    klaster = fields.Char(string='Кластер')
    otrasl = fields.Selection([
        ('0', 'Строительство зданий и жилых помещений'),
        ('1', 'Финансовые услуги'),
        ('2', 'Дизайн и Архитектура')
    ], default='0', index=True, string="Отрасль компании")

    def create_company_odoo(self, data):

        val = self.sudo().search([['url', '=', self.url]])
        if len(val) > 0:
            val.region = data.get('Регион:', 'default value')
            val.nas_punkt = data.get('Населенный пункт:', 'default value')
            val.vid_deyatelnosti = data.get('Вид деятельности:', 'default value')
            val.ur_address = data.get('Юридический адрес:', 'default value')
            val.fact_address = data.get('Фактический адрес:', 'default value')
            val.sector_econ = data.get('Сектор экономики:', 'default value')
            val.org_right_form = data.get('Организационно-правовая форма:', 'default value')
            val.form_sobs = data.get('Форма собственности:', 'default value')
            val.status_pred = data.get('Статус предприятия:', 'default value')
            val.bin = data.get('БИН:', 'default value')
            val.year_form = data.get('Год образования:', 'default value')
            val.status_platelshik = data.get('Статус плательщика:', 'default value')
            val.klaster = data.get('Кластер:', 'default value')
            val.otrasl = '0'

    def get_company_data(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, 'html.parser')
        soup = soup.find('table', id='reestr_items').find_all('td')
        data = {}
        for i in range(len(soup)):
            if i % 2 == 0:
                data[soup[i].text] = soup[i + 1].text
        self.create_company_odoo(data)
    def simple_method(self):
        print("Hello")





    def get_company_data2(self, pair):
        url, name = pair
        print(url, name)
        name = str(name).replace('ТОВАРИЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', 'ТОО')
        name = str(name).replace('ТОВАРИЩЕСТВА С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', 'ТОО')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', id='reestr_items')
        if table is not None:
            data = {
                'Наименование:': name
            }
            for tr in table.find_all('tr'):
                td = [td.text.strip() for td in tr.find_all('td')]
                data[td[0]] = td[1]

            val = self.sudo().search([['url', '=', url]])
            if len(val) == 0:

                self.env['res.partner'].sudo().create({
                    'name': data.get('Наименование:', 'default value'), 'display_name': data.get('Наименование:', 'default value'),
                    'url': url,
                    'is_company': 'company',
                    'region': data.get('Регион:', 'default value'),
                    'nas_punkt': data.get('Населенный пункт:', 'default value'),
                    'vid_deyatelnosti': data.get('Вид деятельности:', 'default value'),
                    'ur_address': data.get('Юридический адрес:', 'default value'),
                    'fact_address': data.get('Фактический адрес:', 'default value'),
                    'sector_econ': data.get('Сектор экономики:', 'default value'),
                    'org_right_form': data.get('Организационно-правовая форма:', 'default value'),
                    'form_sobs': data.get('Форма собственности:', 'default value'),
                    'status_pred': data.get('Статус предприятия:', 'default value'),
                    'bin': data.get('БИН:', 'default value'),
                    'year_form': data.get('Год образования:', 'default value'),
                    'status_platelshik': data.get('Статус плательщика:', 'default value'),
                    'klaster': data.get('Кластер:', 'default value'),
                    'otrasl': '0',
                })

    def get_all_url(self, url, i):
        if i >= 2:
            return []
        data = []
        r = requests.get(url + str(i) + '&SIZEN_1=100')
        soup = BeautifulSoup(r.content, 'html.parser')
        for a in soup.find('tbody').find_all('a'):
            if a.text != 'Подробнее':
                data.append(('http://businessnavigator.kz' + a['href'], a.text))

        if soup.find('a', title='Следующая страница') is None:
            return data
        else:
            data.extend(self.get_all_url(url, i + 1))
        return data

    def data_collector(self):
        base_urls = {
            'Финансовые услуги': 'http://businessnavigator.kz/ru/branch/?OKED_5=&lang=ru&BIN=&NAME=&KATO_1%5B0%5D=467773'
                                 '&OKED_2%5B0%5D=468074&submit-map=&search=%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8%D1'
                                 '%82%D1%8C&PAGEN_1=',
            'Строительство зданий': 'http://businessnavigator.kz/ru/branch/?OKED_5=&lang=ru&BIN=&NAME=&KATO_1%5B0%5D'
                                    '=467773&OKED_2%5B0%5D=468055&submit-map=&search=%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D0%BD'
                                    '%D0%B8%D1%82%D1%8C&PAGEN_1=',
            'Дизайн': 'http://businessnavigator.kz/ru/branch/?OKED_5=&lang=ru&BIN=&NAME=&KATO_1%5B0%5D'
                      '=467773&OKED_2%5B0%5D=468080&submit-map=&search=%D0%9F%D1%80%D0%B8%D0%BC%D0%B5'
                      '%D0%BD%D0%B8%D1%82%D1%8C&PAGEN_1='

        }
        all_url = []
        all_url.extend(self.get_all_url(base_urls['Финансовые услуги'], 1))
        all_url.extend(self.get_all_url(base_urls['Строительство зданий'], 1))
        all_url.extend(self.get_all_url(base_urls['Дизайн'], 1))

        for i in all_url:
            self.get_company_data2(i)

