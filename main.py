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

print(desc_partes)

informacoes = {
    'numero': info['nNFSe'],
    'data_emissao': info['DPS']['infDPS']['dhEmi'].split('T')[0],
    'valor_servicos': info['valores']['vBC']
}

if len(desc_partes) > 1:
    descricao = desc_partes[0].strip()
    resto = desc_partes[1].strip()
    resto_dividido = resto.split('.', 1)
    nome_escola = resto_dividido[0].strip()
    endereco_escola = resto_dividido[1].strip() if len(resto_dividido) > 1 else ''

    informacoes['descricao_serv'] = descricao
    informacoes['nome_escola'] = nome_escola
    informacoes['endereco_escola'] = endereco_escola

print(json.dumps(informacoes, indent=2, ensure_ascii=False))

