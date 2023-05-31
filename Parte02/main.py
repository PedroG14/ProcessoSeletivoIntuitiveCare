import tabula, sys
import pandas as pd
from zipfile import ZipFile

def main():
    #Nome do arquivo PDF
    pdfNome = "Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536_RN537_RN538_RN539_RN541_RN542_RN544_546_571_577.pdf"

    #Armazenando caminho da pasta do PDF
    caminho = sys.argv[0] #Pegando o caminho do módulo a ser executado
    caminho = caminho.replace(caminho.split('/')[-1], '') #Removendo o nome do módulo, mantendo só o caminho da pasta

    #Concatenando caminho + nome do arquivo
    pdfCaminho = caminho + pdfNome

    #Extraindo tabelas do PDF
    tabelas = tabula.read_pdf(pdfCaminho, pages = "all", lattice = True)

    #Criando objeto "tabelaFinal" para então armazenar a concatenação de todas as tabelas extraídas, exceto as vazias
    tabelaFinal = pd.DataFrame()
    for tabela in tabelas:
        if not tabela.empty:
            tabelaFinal = pd.concat([tabelaFinal, tabela], ignore_index = True)

    #Removendo quebra de linha do nome das colunas e dos dados
    #Caso não seja removido, a quebra de linha pode interferir na organização do arquivo csv final
    tabelaFinal.columns = tabelaFinal.columns.str.replace('\r', ' ', regex = True)
    tabelaFinal = tabelaFinal.replace('\r', ' ', regex = True)

    #EXTRA: Substituindo os dados abreviados das colunas OD e AMB
    tabelaFinal.columns = tabelaFinal.columns.str.replace("^OD$", "Seg. Odontológica", regex = True).str.replace("^AMB$", "Seg. Ambulatorial", regex = True)
    tabelaFinal = tabelaFinal.replace("^OD$", "Seg. Odontológica", regex = True).replace("^AMB$", "Seg. Ambulatorial", regex = True)

    #Variável do caminho do arquivo csv
    caminhoCsv = pdfCaminho + ".csv"
    
    #Salvando tabela csv
    tabelaFinal.to_csv(caminhoCsv, index = False)

    #Variável do nome do arquivo zip final
    caminhoZip = caminho + "Teste_Pedro_Gabriel_de_Morais_Ribeiro.zip"

    #Zipando arquivo csv gerado
    zipArquivo(caminhoZip, caminhoCsv)

#Função para zipar arquivo 
#Parâmetros: Caminho/nome desejado do arquivo zip, arquivo que será zipado
def zipArquivo(nomeZip, caminhoArquivo):
    with ZipFile(nomeZip, 'w') as zipper:
        zipper.write(caminhoArquivo)

if __name__ == "__main__":
    main()
