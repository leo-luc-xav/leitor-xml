import streamlit as st
import xmltodict
import re

# 1. TÍTULO DA PÁGINA
st.title("Extrator de XML 📄")
st.write("Faça o upload da nota fiscal para extrair e validar os dados.")

# 2. BOTÃO DE UPLOAD (Substitui o 'with open(...)')
# O Streamlit cria um botão de arrastar e soltar na tela
arquivo_xml = st.file_uploader("Selecione o arquivo XML", type=["xml"])

# 3. SÓ RODA O CÓDIGO SE O USUÁRIO ENVIOU O ARQUIVO
if arquivo_xml is not None:
    
    # Lendo o arquivo que o usuário subiu
    xml_content = arquivo_xml.read()
    data = xmltodict.parse(xml_content)

    if 'NFSe' in data or 'infNFSe' in data:
        st.success("Nota de Serviço carregada com Sucesso!")

        info = data['NFSe']['infNFSe']
        corte = r"PCRJ/E/CRE \(\d{7}\)"
        descricao_original = info['DPS']['infDPS']['serv']['cServ']['xDescServ']
        desc_partes = re.split(corte, descricao_original)
    
        informacoes = {
            'numero': info['nNFSe'],
            'data_emissao': info['DPS']['infDPS']['dhEmi'].split('T')[0],
            'valor_servicos': info['valores']['vBC'],
            'descricao_serv': '',
            'nome_escola': '',
            'endereco_escola': ''
        }
    
        if len(desc_partes) > 1:
            informacoes['descricao_serv'] = desc_partes[0].strip()
            resto = desc_partes[1].strip()
            resto_dividido = resto.split('.', 1)
            informacoes['nome_escola'] = resto_dividido[0].strip()
            informacoes['endereco_escola'] = resto_dividido[1].strip() if len(resto_dividido) > 1 else ''
    
    
        st.divider() # Cria uma linha horizontal na tela para separar
        st.subheader("Verifique e edite as informações:")
    
        # 4. CRIANDO O FORMULÁRIO PARA O USUÁRIO EDITAR
        # O 'with st.form' agrupa os campos e só envia os dados quando clicar no botão
        with st.form("form_edicao"):
            
            # st.text_input cria uma caixa de texto. 
            # O segundo parâmetro (value) é o que vem preenchido da sua extração!
            col1, col2, col3 = st.columns(3) # Divide a tela em 3 colunas para ficar bonito
            
            with col1:
                num_editado = st.text_input("Número da Nota", value=informacoes['numero'])
            with col2:
                data_editada = st.text_input("Data de Emissão", value=informacoes['data_emissao'])
            with col3:
                valor_editado = st.text_input("Valor Total (R$)", value=informacoes['valor_servicos'])
    
            # st.text_area é melhor para textos longos
            desc_editada = st.text_area("Descrição do Serviço", value=informacoes['descricao_serv'])
            
            escola_editada = st.text_input("Nome da Escola", value=informacoes['nome_escola'])
            end_editado = st.text_input("Endereço da Escola", value=informacoes['endereco_escola'])
    
            # Botão de salvar
            botao_salvar = st.form_submit_button("Confirmar e Salvar")
    
        # 5. O QUE ACONTECE QUANDO ELE CLICA EM SALVAR?
        if botao_salvar:
            st.success("Dados confirmados com sucesso!")

    elif 'NFe' in data or 'nfeProc' in data:
        st.success("Nota de Produto carregada com Sucesso!")

        #obtem as informações da escola a partir das informaçoes complementares 
        info = data['nfeProc']['NFe']['infNFe']
        pcrj = r"PCRJ/E/CRE \([\d.]+\)"
        corte = 'DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL. NAO GERA DIREITO A CREDITO FISCAL DE ICMS, ISS E IPI'
        infos_escola = re.sub(pcrj, "", info['infAdic']['infCpl']).replace(corte, "")
        nome = infos_escola.split('.', 1)[0]
        endereco = infos_escola.split('.', 1)[1] if len(infos_escola.split('.', 1)) > 1 else ''

        #obtendo informações dos produtos. Caso seja mais de um ele considera lista, para tratar isso estamos verificando se ele é um dicionário, caso seja, transformamos em lista para manter a consistência do código
        detalhes = info['det']
        if type(detalhes) is dict:
            detalhes = [detalhes] 

        #vamos percorrer a lista, armazenando as informações que queremos na lista com os produtos
        lista_produtos = []
        for det in detalhes:
            produto_xml = det['prod']

            produto_limpo = {
                'código': produto_xml['cProd'],
                'descrição': produto_xml['xProd'],
                'quantidade': produto_xml['qCom'],
                'valor_unitário': produto_xml['vUnCom'],
                'valor_total': produto_xml['vProd']
            }
            lista_produtos.append(produto_limpo)



        informacoes = {
            'numero': info['ide']['nNF'],
            'data_emissao': info['ide']['dhEmi'].split('T')[0],
            'valor_servicos': info['total']['ICMSTot']['vNF'],
            'nome_escola': nome,
            'endereco_escola': endereco
        }

        #st.success(informacoes)
        #st.success(lista_produtos)
    
        st.divider() # Cria uma linha horizontal na tela para separar
        st.subheader("Verifique e edite as informações:")
    
        # 4. CRIANDO O FORMULÁRIO PARA O USUÁRIO EDITAR
        # O 'with st.form' agrupa os campos e só envia os dados quando clicar no botão
        with st.form("form_edicao"):
            
            # st.text_input cria uma caixa de texto. 
            # O segundo parâmetro (value) é o que vem preenchido da sua extração!
            col1, col2, col3 = st.columns(3) # Divide a tela em 3 colunas para ficar bonito
            
            with col1:
                num_editado = st.text_input("Número da Nota", value=informacoes['numero'])
            with col2:
                data_editada = st.text_input("Data de Emissão", value=informacoes['data_emissao'])
            with col3:
                valor_editado = st.text_input("Valor Total  (R$)", value=informacoes['valor_servicos'])
    
            col1, col2 = st.columns(2) # Divide a tela em 2 colunas para ficar bonito

            with col1:
                escola_editada = st.text_input("Nome da Escola", value=informacoes['nome_escola'])
            with col2:
                end_editado = st.text_input("Endereço da Escola", value=informacoes['endereco_escola'])

            st.divider()
            st.subheader("Verifique e edite os produtos:")
            st.write("Clique duas vezes em qualquer célula para editar.")

            # O st.data_editor cria a tabela e salva o resultado editado na variável
            produtos_editados = st.data_editor(
                lista_produtos,
                use_container_width=True, # Faz a tabela ocupar toda a largura da tela
                num_rows="dynamic"        # Permite ao usuário adicionar ou excluir linhas!
            )   

            # Botão de salvar
            botao_salvar = st.form_submit_button("Confirmar e Salvar")
        
    
        # 5. O QUE ACONTECE QUANDO ELE CLICA EM SALVAR?
        if botao_salvar:
            st.success("Dados confirmados com sucesso!")

    else:
        st.error("Não foi possível identificar o tipo de nota. Por favor, verifique o arquivo.")
else:
    st.error("Nenhum arquivo foi carregado.")
