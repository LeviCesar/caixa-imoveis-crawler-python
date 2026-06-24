from pathlib import Path
import http.client


class Caixa:
    states = [
        'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
    ]

    def __init__(self) -> None:
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.url = "https://venda-imoveis.caixa.gov.br"
        self.conn = http.client.HTTPConnection('venda-imoveis.caixa.gov.br')

    def get_spread_sheet(self, state: str) -> bytes:
        self.conn.request(
            'GET', f'/listaweb/Lista_imoveis_{state}.csv?1038721191')
        
        res = self.conn.getresponse()

        assert 300 > res.getcode() > 199

        return res.read().decode('windows-1254')

    def download_spread_sheet(self) -> str:
        for state in self.states:
            file_bytes = self.get_spread_sheet(state)

            p = Path('/csv_files')
            try:

                with p.joinpath(f'Lista_imoveis_{state}.csv').open('wb') as f:
                    f.write(file_bytes)

                assert p.exists()

            except Exception as error:
                print(error)