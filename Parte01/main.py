from requests import get
from bs4 import BeautifulSoup
from zipfile import ZipFile

def main():
    #Coletando página
    urlRes = get("https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude")

    #Criando objeto BeautifulSoup
    soup = BeautifulSoup(urlRes.content, "html.parser")

    #Buscando e armazenando uma lista de links cujo texto do hyperlink contém a palavra "Anexo"
    links = soup.select('a')
    linksAnexos = [link.get("href") for link in links if "Anexo" in link.text]

    #Armazenando nome dos arquivos
    nomeArquivos = [linksAnexos[i].split('/')[-1] for i in range(len(linksAnexos))]

    #Baixando arquivos
    for i, link in enumerate(linksAnexos):
        download(nomeArquivos[i], link)
    
    #Comprimindo arquivos
    zipMultiArqs("anexos.zip", nomeArquivos)

#Função para zipar arquivos 
#Parâmetros: Nome desejado do arquivo zip, lista dos arquivos que serão zipados
def zipMultiArqs(nomeZip, nomeArquivos):
    with ZipFile(nomeZip, 'w') as zipper:
        for nomeArq in nomeArquivos:
            zipper.write(nomeArq)

#Função para realizar o download de um arquivo
#Parâmetros: Nome desejado do arquivo, url do arquivo
def download(nomeArq, url):
    urlRes = get(url, stream = True)
    open(nomeArq, "wb").write(urlRes.content)

if __name__ == "__main__":
    main()