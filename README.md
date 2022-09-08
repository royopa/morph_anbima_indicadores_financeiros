Morph ANBIMA - Indicadores econômicos
-------------------------------------

ANBIMA scraper é um projeto para captura de dados do site da [ANBIMA](https://www.anbima.com.br/informacoes/indicadores/).

## Instalar dependências do projeto

Para instalar as dependências do projeto utilize o comando abaixo:

```sh
> cd anbima_scraper
> pip install -r requirements.txt
```

### Indicadores ANBIMA

SELIC, CDI, IGP-M, IPCA, Dólar, Euro, TR, TBF, FDS

Fonte: https://www.anbima.com.br/informacoes/indicadores/

```sh
> python scraper.py
```

Os arquivos de saída estarão em formato csv na pasta bases.
