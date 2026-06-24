from pathlib import Path
import http.client

class CaixaProperties:
    states = [
            'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
        ]
    
    def __init__(self) -> None:
        self.base_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.conn = http.client.HTTPSConnection('venda-imoveis.caixa.gov.br')
    
    def get_spread_sheet(self, state: str) -> str:
        self.conn.request(
            'GET', f'/listaweb/Lista_imoveis_{state}.csv?34743250', headers=self.base_headers)
        
        res = self.conn.getresponse()

        assert 300 > res.getcode() > 199, f'fail to get csv from {state}'

        return res.read().decode('windows-1254')

    def download_spread_sheet(self) -> str:
        for state in self.states:
            file_bytes = self.get_spread_sheet(state)
            
            p = Path('.').joinpath('csv_files/')
            p.mkdir(parents=True, exist_ok=True)
            try:

                with p.joinpath(f'Lista_imoveis_{state}.csv').open('w') as f:
                    f.write(file_bytes)

                assert p.exists(), f'download from state {state} fail!'

            except Exception as error:
                print(error)
    
    def get_town_list(self, state: str) -> list:
        self.conn.request(
            'POST', '/sistema/carregaListaCidades.asp')
        res = self.conn.getresponse()

        assert 300 > res.getcode() > 199

        return res.read().decode('windows-1254')