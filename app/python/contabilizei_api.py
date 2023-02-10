#!/usr/bin/env python

from __future__ import unicode_literals


import sys
import json
import requests
import datetime
from typing import Optional

class ContabilizeiApi(object):
    """
    Class implementing an API client for Contabilizei 
    """

    
    VERBOSE_QUIET = 0
    VERBOSE_NORMAL = 1
    VERBOSE_DEBUG = 2
    VERBOSE_TRACE = 3

    def __init__(self, verbose: Optional[int] = 1, base_url: Optional[str] = "https://appservices.contabilizei.com.br/rest"):
        self.verbose = verbose
        self.base_url = base_url
        
        self.request = requests.Session()
        self.login_data = None
        self.headers = {}
    
    def verbose_print(self, min_verbose_level, msg):
        if self.verbose >= min_verbose_level:
            print(msg)

    def _post(self, url, json={}, data=None, append=True):
        target_url = url
        if append:
            target_url = self.base_url + url
        r = self.request.post(target_url, json=json, data=data, headers=self.headers)
        return self._send_data_helper(r, url)

    def _get(self, url, payload={}, append: Optional[bool] = True):
        target_url = url
        if append:
            target_url = self.base_url + url
        r = self.request.get(target_url, params=payload, headers=self.headers)
        return self._send_data_helper(r, url)

    def _send_data_helper(self, r, url):
        has_error = False
        if r.status_code != requests.codes.ok: # 200
            has_error = True
            print("Error [{}] posting to [{}]".format(r, url))
        if has_error or self.verbose >= self.VERBOSE_TRACE:
            print("status_code: {}".format(r.status_code))
            if "application/json" in r.headers['content-type']:
                rj = r.json()
                print(json.dumps(rj, indent=2, sort_keys=True))
            else:
                print(r.text)
        return r

    def _fixdate(self, ano, mes):
        mes_passado = datetime.datetime.now() - datetime.timedelta(days=30)
        if mes is None:
            mes = mes_passado.month
        if ano is None:
            ano = mes_passado.year
        return ano, mes

    def get_company_details(self):
        url = "https://appservices.contabilizei.com/plataforma/rest/authentication/login"
        data = self.access_token
        resp = self._post(url, data=data, append=False)
        details = json.loads(resp.content)
        self.company_id = details["userId"]
        self.company_name = details["empresa"]["nomeFantasia"]
        self.company_cnpj = details["empresa"]["cnpj"]
        self.company_tax_mode = details["empresa"]["regimeTributario"]
        self.company_raw_details = details
        self.verbose_print(self.VERBOSE_NORMAL, f"Company Details: {self.company_name} | {self.company_cnpj} | {self.company_tax_mode}")

    def login(self, email, password, token: Optional[str] = ""):
        if token == "":
            self.request.auth = (email, password)
            url = 'https://sso.contabilizei.com/login'
            data = {"user": email, "password": password}

            self.login_data = self._post(url, data=data, append=False)
            if self.login_data.is_redirect:
                self.verbose_print(self.VERBOSE_NORMAL, "Received redirect response after login attempt")
            res_url=self.login_data.url
            self.headers["strinfs-token"] = res_url.split("token=")[1]
            self.login_data.headers["token"] = res_url.split("token=")[1]
        else:
            self.headers["strinfs-token"] = token
            self.access_token= token
        
        self.verbose_print(self.VERBOSE_DEBUG, f"Received session token: {self.access_token}")
        self.verbose_print(self.VERBOSE_NORMAL, "Conectado ao contabilizei.com.br como [{}]".format(email))
        self.get_company_details()
        return self

    def impostos_listar_api_1(self, mes=None, ano=None):
        """
        the API used in this method usually only lists the IRRF tax 
        """
        ano, mes = self._fixdate(ano, mes)
        self.verbose_print(self.VERBOSE_NORMAL, "Obtendo lista de impostos para {:04}-{:02}...".format(ano, mes))
        url = "/impostopagar/list/{}/{}".format(mes, ano)
        output = self._get(url).json()
        print(f"Impostos a pagar - part 1: {output}")
        return output
    
    def impostos_listar_api_2(self, mes=None, ano=None):
        """
        the API used in this method usually only lists the INSS + Simples taxes
        """
        ano, mes = self._fixdate(ano, mes)
        self.verbose_print(self.VERBOSE_NORMAL, "Obtendo lista de impostos para {:04}-{:02}...".format(ano, mes))
        url = f"https://impostos.contabilizei.com/guias/api/v1/guia/listGuiasImpostos/{self.company_id}/{ano}?mes={mes}"
        output = self._get(url, append=False).json()
        print(f"Impostos a pagar - part 2: {output}")
        return output


def main():
    if len(sys.argv) < 3:
        print("Syntax: python3 {} username password".format(sys.argv[0]))
        sys.exit(2)
    
    client = ContabilizeiApi(verbose=2).login(sys.argv[1], sys.argv[2], sys.argv[3])
    client.impostos_listar_api_1()
    client.impostos_listar_api_2()


if __name__ == "__main__":
    main()

