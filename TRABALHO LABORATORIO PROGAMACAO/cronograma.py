# --------------- Desenvolvimento de Aplicação CRUD em Python ---------------
# Disciplina: Laboratório de Programação
# Professor: Fábio Oliveira Silva
# Aluna: Bianca dos Santos Gonçalves
# ---------------------------------------------------------------------------

import json
import os

ARQUIVO = 'cronograma.json'

# ---------------- VALIDAÇÕES/REGRAS-------------------

DIAS_SEMANA = {'domingo': 'Domingo',
               'segunda': 'Segunda-feira',
               'terça': 'Terça-feira',
               'quarta': 'Quarta-feira',
               'quinta': 'Quinta-feira',
               'sexta': 'Sexta-feira',
               'sabado': 'Sábado'}


def validar_dia(dia):
    if not dia:
        return None

    dia = dia.strip().lower()
    return DIAS_SEMANA.get(dia)


def validar_hora(hora): #hora somente no formato HH:MM
    try:
        horas, minutos = hora.strip().split(':')
        horas = int(horas)
        minutos = int(minutos)

        if 0 <= horas <= 23 and 0 <= minutos <= 59:
            return f'{horas:02d}:{minutos:02d}'
    except ValueError:
        return None

    return None

def conflito_horario(lista, dia, horario): #se tiver um horário já preenchido não pode adicionar outro no mesmo
    for item in lista:
        if item['dia'] == dia and item['horario'] == horario:
            return True
    return False
# ---------------- JSON/ carregar e salvar -------------------

def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)   
    return []  


def salvar(lista):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
        

# --------------- CRUD --------------------

def listar(lista):
    if not lista:
        print('\nNenhuma atividade cadastrada.\n')
        return

    print('\n=== CRONOGRAMA ===')
    for item in lista:
        print(
            f"ID: {item.get('id')}  |  "     #get para evitar erro ao acessar chave
            f"Dia: {item.get('dia', 'Não informado')}  |  "
            f"Horário: {item.get('horario', 'Não informado')}  |  "
            f"Atividade: {item.get('atividade', 'Não informado')}"
        )
    print()


def criar(lista, dia, horario, atividade): #não permite cadastro com campos vazios
    if not dia or not horario or not atividade: 
        return False

    if conflito_horario(lista, dia, horario):
        print('Erro! Já existe uma atividade nesse dia e horário.')
        return False
    
    novo_id = len(lista) + 1  #obrigatório, criação de id
        
    item = {'id': novo_id, 
            'dia': dia,
            'horario': horario,
            'atividade': atividade}

    lista.append(item)
    return item


def ler(lista, id):
    for item in lista:
        if item.get('id') == id:
            return item
    return None


def atualizar(lista, id, dia = None, horario = None, atividade = None): #att somente os campos informados
    item = ler(lista, id)
    if not item:
        return False   
    if dia:
        item['dia'] = dia
    if horario:
        item['horario'] = horario
    if atividade:
        item['atividade'] = atividade

    return True


def deletar(lista, id):
    item = ler(lista, id)
    if not item:
        return False

    lista.remove(item)
    return True

# -------------- MENU ------------------

def menu():
    lista = carregar()

    while True:
        print('\n=== MENU CRONOGRAMA ===')
        print('1 - Listar')
        print('2 - Criar')
        print('3 - Ler por ID')
        print('4 - Atualizar')
        print('5 - Excluir')
        print('0 - Sair')
        op = input('Escolha uma opção: ').strip()

        if op == '1':
            
            listar(lista)

        elif op == '2':
            
            dia_input= input('Dia da semana: ')
            dia = validar_dia(dia_input)
            if not dia:
                print('Erro! Dia da semana inválido!')
                continue
                
            inicio = validar_hora(input('Hora início (ex: 08:00): '))
            fim = validar_hora(input('Hora fim (ex: 09:00): '))

            if not inicio or not fim:
                print('Erro! Horário inválido.')
                continue

            horario = f'{inicio} - {fim}'
            
            atividade = input('Atividade: ').strip()
                                  
            if criar(lista, dia, horario, atividade):
                salvar(lista)
                print('\nAtividade cadastrada com sucesso!\n') 
                

        elif op == '3':
            try:
                
                id = int(input('Digite o ID: '))
                item = ler(lista, id)
                if item:
                    print(f"\nID: {item['id']}\n"
                          f"Dia: {item['dia']}\n"
                          f"Horário: {item['horario']}\n"
                          f"Atividade: {item['atividade']}\n")
                else:
                    print('ID não encontrado.')
                    
            except ValueError:
                print('Digite um número válido.')  

        elif op == '4':
            try:
                
                id = int(input('Digite o ID para atualizar: '))
                item = ler(lista, id)
                
                if not item:
                    print('ID não encontrado.')
                    continue

                dia_input = input(f"Dia cadastrado: {item.get('dia')} / | → Novo dia (ENTER para manter): ").strip()
                dia = validar_dia(dia_input) if dia_input else None
                
                if dia_input and not dia:
                    print('Dia inválido.')
                    continue

                inicio_input = input('Nova hora início (ex: 08:00, (ENTER para manter)): ').strip()
                fim_input = input('Nova hora fim (ex: 10:00, (ENTER para manter)): ').strip()

                if inicio_input or fim_input:
                    if not (inicio_input and fim_input):
                        print('Informe hora de início e fim.')
                        continue
                    
                    inicio = validar_hora(inicio_input)
                    fim = validar_hora(fim_input)
                    
                    if not inicio or not fim:
                        print('Horário inválido.')
                        continue
                    
                    horario = f'{inicio} - {fim}'
                    
                else:
                    horario = None

                atividade = input(f"Atividade ({item.get('atividade')} (ENTER para manter)): ").strip() or None

                atualizar(lista, id, dia, horario, atividade)
                salvar(lista)
                print('\nAtividade atualizada!')
                
            except ValueError:
                print('Digite um número válido.')

        elif op == '5':
            try:
                id = int(input('Digite o ID para excluir: '))
                
                if deletar(lista, id):
                    salvar(lista)
                    print('\nAtividade excluída!')
                    
                else:
                    print('Erro! ID não encontrado.')
                    
            except ValueError:
                print('Digite um número válido.')

        elif op == '0':
            salvar(lista)
            print('Saindo...')
            break

        else:
            print('Opção inválida.')



if __name__ == '__main__':
    menu()