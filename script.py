from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import pyautogui
import time
import os
from datetime import datetime, timedelta

load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Calcular data D-1 (ontem)
data_ontem = datetime.now() - timedelta(days=1)
data_ontem_str = data_ontem.strftime("%d/%m/%Y")

print(f"Processando clientes com data: {data_ontem_str}")

# Ler arquivo Excel com clientes
try:
    # Assumindo que o arquivo Excel tem as colunas: 'Cliente' e 'Data'
    df_clientes = pd.read_excel("clientes.xlsx")
    print(f"Arquivo Excel lido com sucesso. Total de registros: {len(df_clientes)}")
    
    # Converter coluna de data para string no formato dd/mm/yyyy
    df_clientes['Data'] = pd.to_datetime(df_clientes['Data']).dt.strftime("%d/%m/%Y")
    
    # Filtrar apenas clientes com data D-1
    clientes_filtrados = df_clientes[df_clientes['Data'] == data_ontem_str]
    print(f"Clientes encontrados para processar: {len(clientes_filtrados)}")
    
    if len(clientes_filtrados) == 0:
        print("Nenhum cliente encontrado para a data D-1")
        exit()
        
except Exception as e:
    print(f"Erro ao ler arquivo Excel: {e}")
    exit()

# Lista para armazenar todos os dados coletados
todos_dados = []

# Abrir navegador
navegador = webdriver.Chrome()

try:
    # Login
    navegador.get("https://backoffice.omni.chat/#/retailer")
    navegador.maximize_window()
    time.sleep(1)
    user = navegador.find_element(By.XPATH, "//input[@placeholder='Email']")
    user.send_keys(email)
    password_fild = navegador.find_element(By.XPATH, "//input[@formcontrolname='password']")
    password_fild.send_keys(password)
    pyautogui.press("enter")
    time.sleep(5)
    
    # Processar cada cliente
    for index, row in clientes_filtrados.iterrows():
        nome_cliente = row['Cliente']
        data_cliente = row['Data']
        
        print(f"\nProcessando cliente: {nome_cliente} - Data: {data_cliente}")
        
        try:
            # Limpar campo de pesquisa e pesquisar cliente atual
            pesquisa = navegador.find_element(By.XPATH, '//*[@id="search-box"]')
            pesquisa.clear()
            time.sleep(1)
            pesquisa.click()
            time.sleep(1)
            pesquisa.send_keys(nome_cliente)
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(3)

            # Acessar cliente
            selecionar_cliente = navegador.find_element(By.XPATH, '/html/body/app-root/app-menu/mat-sidenav-container/mat-sidenav-content/app-retailers/div/table/tbody/tr/td[1]')
            time.sleep(1)
            selecionar_cliente.click()
            time.sleep(2)

            # Acessar tela de pagamentos
            aba_pagamentos = navegador.find_element(By.XPATH, "//*[text()[normalize-space()='Pagamentos']]")
            time.sleep(2)
            aba_pagamentos.click()
            time.sleep(3)

            # Aguardar tabela carregar
            try:
                WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.mat-mdc-table"))
                )
            except:
                print(f"Tabela não encontrada para cliente: {nome_cliente}")
                continue

            # Extrair dados da tabela
            linhas = navegador.find_elements(By.CSS_SELECTOR, "table.mat-mdc-table tbody tr.mat-mdc-row")

            if len(linhas) > 0:
                # Pegar a primeira linha
                primeira_linha = linhas[0]
                
                # Extrair células
                colunas = primeira_linha.find_elements(By.CSS_SELECTOR, "td.mat-mdc-cell")
                
                # Extrair dados
                dados = [coluna.text.strip() for coluna in colunas]
                
                print(f"Dados brutos encontrados para {nome_cliente}:", dados)
                print(f"Total de colunas: {len(dados)}")
                
                tem_valor_total = len(dados) >= 11  # Se tem todas as colunas esperadas
                              
                # Garantir que temos pelo menos 11 campos
                while len(dados) < 11:
                    dados.append("")
                
                # Vamos mostrar mais informações para debug
                if len(dados) < 11:
                    print(f"ATENÇÃO: Apenas {len(dados)} colunas encontradas para {nome_cliente}")
                
                dados_cliente = [
                    nome_cliente,   # Nome do cliente
                    data_cliente,   # Data
                    dados[0] if len(dados) > 0 else "",       # Id
                    dados[1] if len(dados) > 1 else "",      # Valor total
                    dados[2] if len(dados) > 2 else "",       # Valor líquido
                    dados[3] if len(dados) > 3 else "",       # Método de pagamento
                    dados[4] if len(dados) > 4 else "",       # Status
                    dados[5] if len(dados) > 5 else "",       # Criado em
                    dados[6] if len(dados) > 6 else "",       # Vencimento
                    dados[7] if len(dados) > 7 else "",       # Descrição
                    dados[8] if len(dados) > 8 else "",       # Fatura
                    dados[9] if len(dados) > 9 else "",       # Nota fiscal
                    dados[10] if len(dados) > 10 else ""      # Pagamento
                ]
                
                todos_dados.append(dados_cliente)
                print(f"Dados coletados para {nome_cliente}: {dados_cliente}")
            else:
                print(f"Nenhuma linha encontrada na tabela para {nome_cliente}")
                
            # Voltar para a tela de pesquisa para próximo cliente
            navegador.get("https://backoffice.omni.chat/#/retailer")
            time.sleep(2)
            
        except Exception as e:
            print(f"Erro ao processar cliente {nome_cliente}: {e}")
            # Tentar voltar à tela inicial em caso de erro
            navegador.get("https://backoffice.omni.chat/#/retailer")
            time.sleep(2)
            continue

    # Salvar todos os dados coletados em CSV
    if len(todos_dados) > 0:
        colunas_csv = ["Cliente", "Data", "Id", "Valor_total", "Valor_liquído", "Metodo_pagamento", "Status", 
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       "Criado_em", "Vencimento", "Descricao", "Fatura", "Nota_fiscal", "Pagamento"]
        df_resultado = pd.DataFrame(todos_dados, columns=colunas_csv)
        
        # Nome do arquivo com data atual
        nome_arquivo = f"pagamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_resultado.to_csv(nome_arquivo, index=False, sep=";")
        
        print(f"\n=== RESUMO ===")
        print(f"Total de clientes processados: {len(todos_dados)}")
        print(f"Dados salvos em: {nome_arquivo}")
        print(f"=============")
    else:
        print("Nenhum dado foi coletado")

except Exception as e:
    print(f"Erro geral durante execução: {e}")
    
finally:
    time.sleep(2)
    navegador.quit()
    print("Processo finalizado")