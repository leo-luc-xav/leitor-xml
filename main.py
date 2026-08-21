#importando o xmltodict, que é uma biblioteca Python para converter XML em dicionários Python e vice-versa.
import xmltodict
import re
import json

#abrindo o arquivo XML 'teste.xml' e lendo seu conteúdo
with open('teste.xml') as xml_file:
    xml_content = xml_file.read()
    #convertendo o conteúdo XML em um dicionário Python usando a função parse() do xmltodict
    data = xmltodict.parse(xml_content)

#capturando a informação específica do dicionário resultante, acessando a chave 'NFSe' e depois a chave 'infNFSe'
info = data['NFSe']['infNFSe']

#criando o padrão de expressão regular para corresponder à string "PCR/E/CRE (número de 7 dígitos)"
corte = r"PCRJ/E/CRE \(\d{7}\)"
#usando a expressão regular para dividir a descrição do serviço em partes, com base no padrão definido
descricao_original = info['DPS']['infDPS']['serv']['cServ']['xDescServ']
desc_partes = re.split(corte, descricao_original)

#pegando as informações principais do dicionário 'info' e armazenando em um novo dicionário 'informacoes'
informacoes = {
    'numero': info['nNFSe'],
    'data_emissao': info['DPS']['infDPS']['dhEmi'].split('T')[0],
    'valor_servicos': info['valores']['vBC']
}

#as informações adicionais são extraídas da descrição do serviço, se houver mais de uma parte após a divisão
if len(desc_partes) > 1:
    #a descrição do serviço é a primeira parte
    descricao = desc_partes[0].strip()
    #o resto contém o nome da escola e o endereço, que são separados por um ponto
    resto = desc_partes[1].strip()
    #o endereço da escola é obtido dividindo o resto em duas partes, usando o ponto como delimitador
    resto_dividido = resto.split('.', 1)
    nome_escola = resto_dividido[0].strip()
    endereco_escola = resto_dividido[1].strip() if len(resto_dividido) > 1 else ''

    #adicionando as informações extraídas ao dicionário 'informacoes'
    informacoes['descricao_serv'] = descricao
    informacoes['nome_escola'] = nome_escola
    informacoes['endereco_escola'] = endereco_escola

#print(json.dumps(informacoes, indent=2, ensure_ascii=False))

