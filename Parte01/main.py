from requests import get
from bs4 import BeautifulSoup
from zipfile import ZipFile

def main():
    #Coletando página
    urlRes = get("https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude")

    #Criando objeto BeautifulSoup
    soup = BeautifulSoup(urlRes.content, "html.parser")

    #Armazenando lista de hyperlinks da página
    hlinks = soup.select('a')

    #Buscando e armazenando links, juntamente com o nome de seus arquivos, em que o texto do hyperlink contém a palavra "Anexo"
    anexos = []
    for hlink in hlinks:
        if "Anexo" in hlink.text:
            anexos.append({
                "link": hlink.get("href"),
                "nome": hlink.get("href").split('/')[-1]
            })

    #Baixando arquivos
    for anexo in anexos:
        download(anexo.get("link"), anexo.get("nome"))
    
    #Comprimindo arquivos
    zipMultiArqs("anexos.zip", [anexo.get("nome") for anexo in anexos])

#Função para realizar o download de um arquivo
#Parâmetros: Url do arquivo, nome do arquivo
def download(url, nomeArq):
    urlRes = get(url, stream = True)
    open(nomeArq, "wb").write(urlRes.content)

#Função para zipar arquivos 
#Parâmetros: Nome desejado do arquivo zip, lista dos arquivos que serão zipados
def zipMultiArqs(nomeZip, nomeArquivos):
    with ZipFile(nomeZip, 'w') as zipper:
        for nomeArq in nomeArquivos:
            zipper.write(nomeArq)

if __name__ == "__main__":
    main()
