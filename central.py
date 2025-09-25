import mercadopago
import json
import time
import datetime
import random
import html
import pytz
import os
from datetime import timezone
from pytz import timezone

# --- Funções Utilitárias para JSON ---
def ler_json(caminho_arquivo):
    """Lê um arquivo JSON e retorna seu conteúdo, ou um dicionário/lista padrão em caso de erro."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Retorna uma estrutura padrão se o arquivo não existir ou estiver corrompido
        if 'users' in caminho_arquivo:
            return {"users": []}
        if 'acessos' in caminho_arquivo:
            return {"acessos": []}
        if 'admins' in caminho_arquivo:
            return {"admins": []}
        if 'ccs' in caminho_arquivo:
            return {"ccs": []}
        if 'laras' in caminho_arquivo:
            return {"laras": []}
        if 'ggs' in caminho_arquivo:
            return {"ggs": []}
        if 'gift' in caminho_arquivo:
            return {"gift": []}
        return {}

def escrever_json(caminho_arquivo, dados):
    """Escreve dados em um arquivo JSON."""
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4)

class ViewTime():
    @staticmethod
    def data_atual():
        data_e_hora_atuais = datetime.datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
        return data_e_hora_em_texto
    
    @staticmethod
    def hora_atual():
        data_e_hora_atuais = datetime.datetime.now()
        fuso_horario_sp = timezone('America/Sao_Paulo')
        hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario_sp)
        return hora_sao_paulo.strftime('%H:%M:%S')

class CredentialsChange():
    _credenciais_path = 'settings/credenciais.json'

    @staticmethod
    def user_bot():
        data = ler_json(CredentialsChange._credenciais_path)
        return str(data.get("user_bot", ""))

    @staticmethod
    def mudar_user_bot(user):
        data = ler_json(CredentialsChange._credenciais_path)
        data["user_bot"] = str(user)
        escrever_json(CredentialsChange._credenciais_path, data)

    @staticmethod
    def token_bot():
        data = ler_json(CredentialsChange._credenciais_path)
        return str(data.get("api-bot", ""))

    @staticmethod
    def mudar_token_bot(token):
        data = ler_json(CredentialsChange._credenciais_path)
        data["api-bot"] = str(token)
        escrever_json(CredentialsChange._credenciais_path, data)

    @staticmethod
    def versao_bot():
        data = ler_json(CredentialsChange._credenciais_path)
        return str(data.get("version", "N/A"))

    @staticmethod
    def mudar_versao_bot(version):
        data = ler_json(CredentialsChange._credenciais_path)
        data["version"] = version
        escrever_json(CredentialsChange._credenciais_path, data)

    @staticmethod
    def separador():
        data = ler_json(CredentialsChange._credenciais_path)
        return str(data.get("separador", "|"))

    @staticmethod
    def mudar_separador(separador):
        data = ler_json(CredentialsChange._credenciais_path)
        data["separador"] = separador
        escrever_json(CredentialsChange._credenciais_path, data)

    @staticmethod
    def status_manutencao():
        data = ler_json(CredentialsChange._credenciais_path)
        return str(data.get("maintance", "off")).lower() == 'on'
    
    @staticmethod
    def mudar_status_manutencao():
        data = ler_json(CredentialsChange._credenciais_path)
        data["maintance"] = "off" if str(data.get("maintance")).lower() == "on" else "on"
        escrever_json(CredentialsChange._credenciais_path, data)

    @staticmethod
    def id_dono():
        data = ler_json(CredentialsChange._credenciais_path)
        return int(data.get("id_dono", 0))

    @staticmethod
    def mudar_dono(id):
        data = ler_json(CredentialsChange._credenciais_path)
        data["id_dono"] = int(id)
        escrever_json(CredentialsChange._credenciais_path, data)

    class SuporteInfo():
        @staticmethod
        def link_suporte():
            data = ler_json(CredentialsChange._credenciais_path)
            return str(data.get("link_suporte", ""))

        @staticmethod
        def mudar_link_suporte(link):
            data = ler_json(CredentialsChange._credenciais_path)
            data["link_suporte"] = str(link)
            escrever_json(CredentialsChange._credenciais_path, data)

    class StatusPix():
        @staticmethod
        def pix_manual():
            data = ler_json(CredentialsChange._credenciais_path)
            return str(data.get("status_pix_manu", "off")).lower() == 'on'

        @staticmethod
        def pix_auto():
            data = ler_json(CredentialsChange._credenciais_path)
            return str(data.get("status_pix_auto", "off")).lower() == 'on'

    class ChangeStatusPix():
        @staticmethod
        def change_pix_manual():
            data = ler_json(CredentialsChange._credenciais_path)
            data["status_pix_manu"] = "off" if str(data.get("status_pix_manu")).lower() == "on" else "on"
            escrever_json(CredentialsChange._credenciais_path, data)

        @staticmethod
        def change_pix_auto():
            data = ler_json(CredentialsChange._credenciais_path)
            data["status_pix_auto"] = "off" if str(data.get("status_pix_auto")).lower() == "on" else "on"
            escrever_json(CredentialsChange._credenciais_path, data)

    class BonusPix():
        @staticmethod
        def quantidade_bonus():
            data = ler_json(CredentialsChange._credenciais_path)
            return int(data.get("bonus_pix", 0))

        @staticmethod
        def mudar_quantidade_bonus(porcentagem):
            data = ler_json(CredentialsChange._credenciais_path)
            data["bonus_pix"] = int(porcentagem)
            escrever_json(CredentialsChange._credenciais_path, data)

        @staticmethod
        def valor_minimo_para_bonus():
            data = ler_json(CredentialsChange._credenciais_path)
            return int(data.get("bonus_pix_min", 0))

        @staticmethod
        def mudar_valor_minimo_para_bonus(valor_min):
            data = ler_json(CredentialsChange._credenciais_path)
            data["bonus_pix_min"] = int(valor_min)
            escrever_json(CredentialsChange._credenciais_path, data)

    class BonusRegistro():
        @staticmethod
        def bonus():
            data = ler_json(CredentialsChange._credenciais_path)
            return float(data.get("bonus_registro", 0.0))

        @staticmethod
        def mudar_bonus(novo_bonus):
            data = ler_json(CredentialsChange._credenciais_path)
            data["bonus_registro"] = float(novo_bonus)
            escrever_json(CredentialsChange._credenciais_path, data)

    class InfoPix():
        @staticmethod
        def token_mp():
            data = ler_json(CredentialsChange._credenciais_path)
            return str(data.get("token_mp", ""))

        @staticmethod
        def mudar_tokenmp(token):
            data = ler_json(CredentialsChange._credenciais_path)
            data["token_mp"] = str(token)
            escrever_json(CredentialsChange._credenciais_path, data)

        @staticmethod
        def chave_pix_manual():
            data = ler_json(CredentialsChange._credenciais_path)
            return str(data.get("chave_pix_manual", "Nenhuma chave configurada"))

        @staticmethod
        def mudar_chave_pix_manual(chave):
            data = ler_json(CredentialsChange._credenciais_path)
            data["chave_pix_manual"] = str(chave)
            escrever_json(CredentialsChange._credenciais_path, data)
            return True

        @staticmethod
        def deposito_minimo_pix():
            data = ler_json(CredentialsChange._credenciais_path)
            return float(data.get("min_pix", 1.0))

        @staticmethod
        def trocar_deposito_minimo_pix(min_val):
            data = ler_json(CredentialsChange._credenciais_path)
            data["min_pix"] = float(min_val)
            escrever_json(CredentialsChange._credenciais_path, data)

        @staticmethod
        def deposito_maximo_pix():
            data = ler_json(CredentialsChange._credenciais_path)
            return float(data.get("max_pix", 1000.0))

        @staticmethod
        def trocar_deposito_maximo_pix(max_val):
            data = ler_json(CredentialsChange._credenciais_path)
            data["max_pix"] = float(max_val)
            escrever_json(CredentialsChange._credenciais_path, data)

        @staticmethod
        def expiracao():
            data = ler_json(CredentialsChange._credenciais_path)
            return int(data.get("expiracao_pix", 15))

        @staticmethod
        def mudar_expiracao(minutes):
            data = ler_json(CredentialsChange._credenciais_path)
            data["expiracao_pix"] = int(minutes)
            escrever_json(CredentialsChange._credenciais_path, data)
            return True

class AfiliadosInfo():
    _credenciais_path = 'settings/credenciais.json'

    @staticmethod
    def status_afiliado():
        data = ler_json(AfiliadosInfo._credenciais_path)
        return str(data.get("afiliados", "off")).lower() == 'on'

    @staticmethod
    def mudar_status_afiliado():
        data = ler_json(AfiliadosInfo._credenciais_path)
        data["afiliados"] = "off" if str(data.get("afiliados")).lower() == "on" else "on"
        escrever_json(AfiliadosInfo._credenciais_path, data)

    @staticmethod
    def pontos_por_recarga():
        data = ler_json(AfiliadosInfo._credenciais_path)
        return int(data.get("pontos_by_indicate_buy", 0))

    @staticmethod
    def mudar_pontos_por_recarga(pontos):
        data = ler_json(AfiliadosInfo._credenciais_path)
        data["pontos_by_indicate_buy"] = int(pontos)
        escrever_json(AfiliadosInfo._credenciais_path, data)

    @staticmethod
    def minimo_pontos_pra_saldo():
        data = ler_json(AfiliadosInfo._credenciais_path)
        return int(data.get("min_points_saldo", 0))

    @staticmethod
    def trocar_minimo_pontos_pra_saldo(min_val):
        data = ler_json(AfiliadosInfo._credenciais_path)
        data["min_points_saldo"] = int(min_val)
        escrever_json(AfiliadosInfo._credenciais_path, data)

    @staticmethod
    def multiplicador_pontos():
        data = ler_json(AfiliadosInfo._credenciais_path)
        return float(data.get("multiplicador_pontos", 0.0))

    @staticmethod
    def trocar_multiplicador_pontos(multiplicador):
        data = ler_json(AfiliadosInfo._credenciais_path)
        data["multiplicador_pontos"] = float(multiplicador)
        escrever_json(AfiliadosInfo._credenciais_path, data)

class Notificacoes():
    _notify_path = 'settings/notify.json'

    @staticmethod
    def modo_servico():
        data = ler_json(Notificacoes._notify_path)
        return int(data.get("tipo_texto", 0))

    @staticmethod
    def mudar_modo_servico():
        data = ler_json(Notificacoes._notify_path)
        data["tipo_texto"] = 1 if data.get("tipo_texto", 0) == 0 else 0
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def status_notificacoes():
        data = ler_json(Notificacoes._notify_path)
        return str(data.get("status_notify", "off")).lower() == 'on'

    @staticmethod
    def mudar_status_notificacoes():
        data = ler_json(Notificacoes._notify_path)
        data["status_notify"] = "off" if str(data.get("status_notify")).lower() == 'on' else 'on'
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def id_grupo():
        data = ler_json(Notificacoes._notify_path)
        return int(data.get("id_grupo", 0))

    @staticmethod
    def trocar_id_grupo(id_grupo):
        data = ler_json(Notificacoes._notify_path)
        data["id_grupo"] = int(id_grupo)
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def tempo_minimo_compras():
        data = ler_json(Notificacoes._notify_path)
        return int(data.get("time_min_compras", 120))
    
    @staticmethod
    def trocar_tempo_minimo_compras(min_val):
        data = ler_json(Notificacoes._notify_path)
        data["time_min_compras"] = int(min_val)
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def tempo_maximo_compras():
        data = ler_json(Notificacoes._notify_path)
        return int(data.get("time_max_compras", 700))

    @staticmethod
    def trocar_tempo_maximo_compras(max_val):
        data = ler_json(Notificacoes._notify_path)
        data["time_max_compras"] = int(max_val)
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def tempo_minimo_saldo():
        data = ler_json(Notificacoes._notify_path)
        return int(data.get("time_min_saldo", 400))

    @staticmethod
    def trocar_tempo_minimo_saldo(min_val):
        data = ler_json(Notificacoes._notify_path)
        data["time_min_saldo"] = int(min_val)
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def tempo_maximo_saldo():
        data = ler_json(Notificacoes._notify_path)
        return int(data.get("time_max_saldo", 1200))

    @staticmethod
    def trocar_tempo_maximo_saldo(max_val):
        data = ler_json(Notificacoes._notify_path)
        data["time_max_saldo"] = int(max_val)
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def min_max_saldo():
        data = ler_json(Notificacoes._notify_path)
        return float(data.get("saldo_min", 1.0)), float(data.get("saldo_max", 20.0))

    @staticmethod
    def trocar_min_max_saldo(min_val, max_val):
        data = ler_json(Notificacoes._notify_path)
        data["saldo_min"] = float(min_val)
        data["saldo_max"] = float(max_val)
        escrever_json(Notificacoes._notify_path, data)

    @staticmethod
    def quantidade_de_servicos_pra_sortear():
        try:
            with open('settings/notificacao/servicos.txt', 'r', encoding='utf-8') as f:
                servicos = f.read().strip().split('\n')
            return len([s for s in servicos if s])
        except FileNotFoundError:
            return 0

    @staticmethod
    def pegar_servico_random():
        try:
            with open('settings/notificacao/servicos.txt', 'r', encoding='utf-8') as f:
                servicos = [s for s in f.read().splitlines() if s]
            if not servicos: return None, None
            servico_escolhido = random.choice(servicos)
            partes = servico_escolhido.strip().split('R$')
            return partes[0].strip(), f'R${partes[1].strip()}'
        except (FileNotFoundError, IndexError):
            return None, None

    @staticmethod
    def pegar_servicos_disponiveis():
        data = ler_json('database/acessos.json')
        nomes = [{"nome": a["nome"], "valor": a["valor"]} for a in data.get("acessos", [])]
        if not nomes: return None, None
        sort = random.choice(nomes)
        return sort["nome"], f'R${sort["valor"]:.2f}'

    @staticmethod
    def mudar_servicos_random(lista):
        with open('settings/notificacao/servicos.txt', 'w', encoding='utf-8') as f:
            f.write(lista)

    @staticmethod
    def pegar_texto_saldo():
        try:
            with open('settings/notificacao/saldo.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Usuário {id} adicionou R${saldo} de saldo!"

    @staticmethod
    def mudar_texto_saldo(texto):
        with open('settings/notificacao/saldo.txt', 'w', encoding='utf-8') as f:
            f.write(texto)

    @staticmethod
    def pegar_texto_compra():
        try:
            with open('settings/notificacao/compra.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Usuário {id} comprou {servico} por {valor}!"

    @staticmethod
    def mudar_texto_compra(texto):
        with open('settings/notificacao/compra.txt', 'w', encoding='utf-8') as f:
            f.write(texto)

    @staticmethod
    def texto_notificacao_saldo():
        texto = Notificacoes.pegar_texto_saldo()
        id_rand = random.randint(898012903, 4290812093)
        saldo_min, saldo_max = Notificacoes.min_max_saldo()
        saldo = random.randint(int(saldo_min), int(saldo_max))
        return texto.replace('{id}', str(id_rand)).replace('{saldo}', str(saldo))

    @staticmethod
    def texto_notificacao_compra():
        texto = Notificacoes.pegar_texto_compra()
        id_rand = random.randint(898012903, 4290812093)
        if Notificacoes.modo_servico() == 0:
            servico, valor = Notificacoes.pegar_servico_random()
        else:
            servico, valor = Notificacoes.pegar_servicos_disponiveis()
        if servico and valor:
            return texto.replace('{id}', str(id_rand)).replace('{servico}', servico).replace('{valor}', valor)
        return None

class InfoUser():
    _users_path = 'database/users.json'

    @staticmethod
    def _get_user(id):
        data = ler_json(InfoUser._users_path)
        for user in data.get("users", []):
            if int(user.get("id", 0)) == int(id):
                return user, data
        return None, data

    @staticmethod
    def verificar_usuario(id):
        user, _ = InfoUser._get_user(id)
        return user is not None

    @staticmethod
    def novo_afiliado(usuario_id, indicador_id):
        data = ler_json(InfoUser._users_path)
        indicador_encontrado = None
        usuario_encontrado = None

        for user in data.get("users", []):
            if int(user.get("id", 0)) == int(indicador_id):
                indicador_encontrado = user
            if int(user.get("id", 0)) == int(usuario_id):
                usuario_encontrado = user
        
        if indicador_encontrado and usuario_encontrado:
            if usuario_encontrado.get("afiliado_por", 0) == 0:
                usuario_encontrado["afiliado_por"] = int(indicador_id)
                
                afiliados_ids = [af.get("id_afiliado") for af in indicador_encontrado.get("afiliados", [])]
                if int(usuario_id) not in afiliados_ids:
                    indicador_encontrado["afiliacoes"] = indicador_encontrado.get("afiliacoes", 0) + 1
                    indicador_encontrado.setdefault("afiliados", []).append({"id_afiliado": int(usuario_id)})
                    
                    escrever_json(InfoUser._users_path, data)

    @staticmethod
    def novo_usuario(id):
        if InfoUser.verificar_usuario(id):
            return
        data = ler_json(InfoUser._users_path)
        new_user = {
            "id": int(id), "banned": "False", "afiliado_por": 0, "saldo": 0.0,
            "gift_redeemed": 0.0, "total_compras": 0, "compras": [],
            "total_pagos": 0, "pagamentos": [], "pontos_indicado": 0,
            "afiliacoes": 0, "afiliados": []
        }
        data.setdefault("users", []).append(new_user)
        escrever_json(InfoUser._users_path, data)

    @staticmethod
    def verificar_ban(id):
        user, _ = InfoUser._get_user(id)
        if user:
            return str(user.get("banned", "False")).lower() == 'true'
        return False

    @staticmethod
    def dar_ban(id):
        user, data = InfoUser._get_user(id)
        if user:
            user["banned"] = "True"
            escrever_json(InfoUser._users_path, data)

    @staticmethod
    def tirar_ban(id):
        user, data = InfoUser._get_user(id)
        if user:
            user["banned"] = "False"
            escrever_json(InfoUser._users_path, data)

    @staticmethod
    def saldo(id):
        user, _ = InfoUser._get_user(id)
        return float(user.get("saldo", 0.0)) if user else 0.0

    @staticmethod
    def add_saldo(id, novo_saldo):
        user, data = InfoUser._get_user(id)
        if user:
            user["saldo"] = user.get("saldo", 0.0) + float(novo_saldo)
            escrever_json(InfoUser._users_path, data)

    @staticmethod
    def tirar_saldo(id, valor):
        user, data = InfoUser._get_user(id)
        if user:
            user["saldo"] = user.get("saldo", 0.0) - float(valor)
            escrever_json(InfoUser._users_path, data)

    @staticmethod
    def mudar_saldo(id, novo_saldo):
        user, data = InfoUser._get_user(id)
        if user:
            user["saldo"] = float(novo_saldo)
            escrever_json(InfoUser._users_path, data)

    @staticmethod
    def gifts_resgatados(id):
        user, _ = InfoUser._get_user(id)
        return float(user.get("gift_redeemed", 0.0)) if user else 0.0

    @staticmethod
    def total_compras(id):
        user, _ = InfoUser._get_user(id)
        return int(user.get("total_compras", 0)) if user else 0

    @staticmethod
    def pix_inseridos(id):
        user, _ = InfoUser._get_user(id)
        if user:
            return sum(float(p.get("valor", 0.0)) for p in user.get("pagamentos", []))
        return 0.0

    @staticmethod
    def pontos_indicacao(id):
        user, _ = InfoUser._get_user(id)
        return int(user.get("pontos_indicado", 0)) if user else 0

    @staticmethod
    def trocar_pontos(id):
        user, data = InfoUser._get_user(id)
        if user and int(user.get("pontos_indicado", 0)) >= int(AfiliadosInfo.minimo_pontos_pra_saldo()):
            somar = int(user["pontos_indicado"]) * AfiliadosInfo.multiplicador_pontos()
            user["pontos_indicado"] = 0
            user["saldo"] = user.get("saldo", 0.0) + float(somar)
            escrever_json(InfoUser._users_path, data)
            return True
        return False

    @staticmethod
    def fazer_txt_do_historico(id):
        user, _ = InfoUser._get_user(id)
        if not user: return False
        
        historico = f'HISTORICO DETALHADO @{CredentialsChange.user_bot()}\n_______________________\n\nCOMPRAS:'
        for compra in user.get("compras", []):
            historico += f'\nServiço: {compra.get("servico")}\nValor: {compra.get("valor")}\nEmail: {compra.get("email")}\nSenha: {compra.get("senha")}\nData: {compra.get("data")}'
        
        historico += '\n_______________________\n\nPAGAMENTOS:'
        for pagamento in user.get("pagamentos", []):
            historico += f'\nId pagamento: {pagamento.get("id_pagamento")}\nValor: {pagamento.get("valor")}\nData: {pagamento.get("data")}'
        
        os.makedirs('historicos', exist_ok=True)
        with open(f'historicos/{id}.txt', 'w', encoding='utf-8') as f:
            f.write(historico)
        return True

    @staticmethod
    def quantidade_afiliados(id):
        user, _ = InfoUser._get_user(id)
        return int(user.get("afiliacoes", 0)) if user else 0

class MudancaHistorico():
    _users_path = 'database/users.json'

    @staticmethod
    def mudar_gift_resgatado(id, valor):
        user, data = InfoUser._get_user(id)
        if user:
            user["gift_redeemed"] = user.get("gift_redeemed", 0.0) + float(valor)
            escrever_json(MudancaHistorico._users_path, data)

    @staticmethod
    def add_compra(id, servico, valor, email, senha):
        user, data = InfoUser._get_user(id)
        if user:
            user["total_compras"] = user.get("total_compras", 0) + 1
            user.setdefault("compras", []).append({
                "servico": servico, "valor": valor, "email": email, "senha": senha,
                "data": f"{ViewTime.data_atual()} as {ViewTime.hora_atual()}"
            })
            escrever_json(MudancaHistorico._users_path, data)

    @staticmethod
    def add_compra_lara(id, lara_data):
        """Adiciona uma compra de 'Lara' ao histórico do usuário."""
        user, data = InfoUser._get_user(id)
        if user:
            user["total_compras"] = user.get("total_compras", 0) + 1
            compra_info = lara_data.copy() # Cria uma cópia para não modificar o original
            compra_info["data_compra"] = f"{ViewTime.data_atual()} as {ViewTime.hora_atual()}"
            user.setdefault("compras", []).append(compra_info)
            escrever_json(MudancaHistorico._users_path, data)

    @staticmethod
    def add_compra_gg(id, gg_data):
        """Adiciona uma compra de 'GG' ao histórico do usuário."""
        user, data = InfoUser._get_user(id)
        if user:
            user["total_compras"] = user.get("total_compras", 0) + 1
            compra_info = gg_data.copy()
            compra_info["tipo_produto"] = "GG" # Identifica o tipo de produto
            compra_info["data_compra"] = f"{ViewTime.data_atual()} as {ViewTime.hora_atual()}"
            user.setdefault("compras", []).append(compra_info)
            escrever_json(MudancaHistorico._users_path, data)

    @staticmethod
    def add_pagamentos(id, valor, id_pag):
        user, data = InfoUser._get_user(id)
        if not user: return

        afiliado_por = user.get("afiliado_por", 0)
        user["total_pagos"] = user.get("total_pagos", 0) + 1
        user.setdefault("pagamentos", []).append({
            "id_pagamento": id_pag, "valor": valor,
            "data": f"{ViewTime.data_atual()} as {ViewTime.hora_atual()}"
        })
        escrever_json(MudancaHistorico._users_path, data)

        if AfiliadosInfo.status_afiliado() and int(afiliado_por) != 0:
            indicador, data_indicador = InfoUser._get_user(afiliado_por)
            if indicador:
                indicador["pontos_indicado"] = indicador.get("pontos_indicado", 0) + int(AfiliadosInfo.pontos_por_recarga())
                escrever_json(MudancaHistorico._users_path, data_indicador)

    @staticmethod
    def zerar_pontos(id):
        user, data = InfoUser._get_user(id)
        if user:
            user["pontos_indicado"] = 0
            escrever_json(MudancaHistorico._users_path, data)

class GiftCard():
    _gift_path = "database/gift_card.json"

    @staticmethod
    def validar_gift(codigo):
        data = ler_json(GiftCard._gift_path)
        for gift in data.get('gift', []):
            if gift.get("codigo") == codigo:
                return True, float(gift.get("valor", 0.0))
        return False, 0

    @staticmethod
    def listar_gift():
        data = ler_json(GiftCard._gift_path)
        return ''.join([f'<code>{g.get("codigo")}</code> R${float(g.get("valor", 0.0)):.2f}\n' for g in data.get("gift", [])])

    @staticmethod
    def create_gift(codigo, valor):
        data = ler_json(GiftCard._gift_path)
        data.setdefault("gift", []).append({"codigo": codigo, "valor": float(valor)})
        escrever_json(GiftCard._gift_path, data)
        return True

    @staticmethod
    def del_gift(codigo):
        data = ler_json(GiftCard._gift_path)
        gifts_restantes = [g for g in data.get("gift", []) if g.get("codigo") != codigo]
        if len(gifts_restantes) < len(data.get("gift", [])):
            data["gift"] = gifts_restantes
            escrever_json(GiftCard._gift_path, data)
            return True
        return False

class FuncaoTransmitir():
    _transmitir_path = 'database/info_transmitir.json'

    @staticmethod
    def pegar_foto():
        return ler_json(FuncaoTransmitir._transmitir_path).get("photo")

    @staticmethod
    def pegar_texto():
        return ler_json(FuncaoTransmitir._transmitir_path).get("texto")

    @staticmethod
    def pegar_entities():
        return ler_json(FuncaoTransmitir._transmitir_path).get("entities")

    @staticmethod
    def pegar_markup():
        return ler_json(FuncaoTransmitir._transmitir_path).get("markup")

    @staticmethod
    def adicionar_foto(photo):
        data = ler_json(FuncaoTransmitir._transmitir_path)
        data["photo"] = photo
        escrever_json(FuncaoTransmitir._transmitir_path, data)

    @staticmethod
    def adicionar_texto(txt):
        data = ler_json(FuncaoTransmitir._transmitir_path)
        data["texto"] = txt
        escrever_json(FuncaoTransmitir._transmitir_path, data)

    @staticmethod
    def adicionar_entitie(ent):
        data = ler_json(FuncaoTransmitir._transmitir_path)
        entities = [e.to_dict() for e in ent] if isinstance(ent, list) else None
        data["entities"] = entities
        escrever_json(FuncaoTransmitir._transmitir_path, data)

    @staticmethod
    def adicionar_markup(markup):
        data = ler_json(FuncaoTransmitir._transmitir_path)
        if markup:
            data["markup"] = [
                [{'text': but.text, 'url': but.url} for but in row]
                for row in markup.keyboard
            ]
        else:
            data["markup"] = None
        escrever_json(FuncaoTransmitir._transmitir_path, data)

    @staticmethod
    def zerar_infos():
        escrever_json(FuncaoTransmitir._transmitir_path, {"texto": None, "photo": None, "entities": None, "markup": None})

class ControleLogins():
    _acessos_path = 'database/acessos.json'

    @staticmethod
    def add_login(nome, valor, descricao, email, senha, duracao):
        data = ler_json(ControleLogins._acessos_path)
        data.setdefault("acessos", []).append({
            "nome": nome, "valor": valor, "descricao": descricao,
            "email": email, "senha": senha, "duracao": duracao
        })
        escrever_json(ControleLogins._acessos_path, data)
        return True

    @staticmethod
    def remover_login(nome, email):
        data = ler_json(ControleLogins._acessos_path)
        acessos_restantes = [a for a in data.get("acessos", []) if not (a.get("nome") == nome and a.get("email") == email)]
        if len(acessos_restantes) < len(data.get("acessos", [])):
            data["acessos"] = acessos_restantes
            escrever_json(ControleLogins._acessos_path, data)
            return True
        return False

    @staticmethod
    def pegar_servicos():
        data = ler_json(ControleLogins._acessos_path)
        return [{"nome": a.get("nome"), "valor": a.get("valor")} for a in data.get("acessos", [])]

    @staticmethod
    def estoque_total():
        data = ler_json(ControleLogins._acessos_path)
        return len(data.get("acessos", []))

    @staticmethod
    def pegar_estoque(nome):
        data = ler_json(ControleLogins._acessos_path)
        return sum(1 for a in data.get("acessos", []) if a.get("nome") == nome)

    @staticmethod
    def pegar_estoque_detalhado():
        data = ler_json(ControleLogins._acessos_path)
        estoque = {}
        for acesso in data.get("acessos", []):
            nome = acesso.get("nome")
            if nome:
                estoque[nome] = estoque.get(nome, 0) + 1
        
        logins = ''.join([f'\n{nome}: {quantidade}' for nome, quantidade in estoque.items()])
        return f"<b>ACESSOS EM ESTOQUE:</b>\n\n<code>{logins}</code>"

    @staticmethod
    def criar_estoque_detalhado():
        data = ler_json(ControleLogins._acessos_path)
        mensagem = "ACESSOS EM ESTOQUE:\n"
        for acesso in data.get("acessos", []):
            mensagem += f'\n\nNome: {acesso.get("nome")}\nValor: {acesso.get("valor")}\nDescricao: {acesso.get("descricao")}\nEmail: {acesso.get("email")}\nSenha: {acesso.get("senha")}\nDuracao: {acesso.get("duracao")}'
        
        os.makedirs('historicos', exist_ok=True)
        with open('historicos/estoque_detalhado.txt', 'w', encoding='utf-8') as f:
            f.write(mensagem)
        return True

    @staticmethod
    def arquivo_estoque_detalhado():
        return open('historicos/estoque_detalhado.txt', 'rb')

    @staticmethod
    def remover_por_nome(nome):
        data = ler_json(ControleLogins._acessos_path)
        data["acessos"] = [a for a in data.get("acessos", []) if str(a.get("nome")) != str(nome)]
        escrever_json(ControleLogins._acessos_path, data)
        return True

    @staticmethod
    def zerar_estoque():
        escrever_json(ControleLogins._acessos_path, {"acessos": []})
        return True

    @staticmethod
    def mudar_valor_por_nome(nome, novo_valor):
        data = ler_json(ControleLogins._acessos_path)
        for acesso in data.get("acessos", []):
            if acesso.get("nome") == nome:
                acesso["valor"] = float(novo_valor)
        escrever_json(ControleLogins._acessos_path, data)

    @staticmethod
    def mudar_valor_de_todos(valor):
        data = ler_json(ControleLogins._acessos_path)
        for acesso in data.get("acessos", []):
            acesso["valor"] = float(valor)
        escrever_json(ControleLogins._acessos_path, data)

    @staticmethod
    def pegar_info(nome):
        data = ler_json(ControleLogins._acessos_path)
        for acesso in data.get("acessos", []):
            if acesso.get("nome") == nome:
                try:
                    valor = float(acesso.get("valor"))
                    return (
                        acesso.get("nome", "N/A"), valor,
                        acesso.get("descricao", "N/A"), acesso.get("duracao", "N/A"),
                        acesso.get("email")
                    )
                except (ValueError, TypeError, AttributeError):
                    continue
        return None

    @staticmethod
    def entregar_acesso(nome, email):
        data = ler_json(ControleLogins._acessos_path)
        for acesso in data.get("acessos", []):
            if acesso.get("nome") == nome and acesso.get("email") == email:
                return (
                    acesso.get("nome"), acesso.get("valor"), acesso.get("email"),
                    acesso.get("senha"), acesso.get("descricao"), acesso.get("duracao")
                )
        return None, None, None, None, None, None

    @staticmethod
    def pegar_info_entrega(nome, email):
        data = ler_json(ControleLogins._acessos_path)
        for acesso in data.get("acessos", []):
            if acesso.get("nome") == nome and acesso.get("email") == email:
                return acesso
        return None

class ControleLaras():
    _laras_path = 'database/laras.json'

    @staticmethod
    def add_lara(email, senha_email, senha_lara, sexo, nome, cpf, valor, banco):
        """Adiciona uma nova 'Lara' ao banco de dados."""
        data = ler_json(ControleLaras._laras_path)
        data.setdefault("laras", []).append({
            "email": email, "senha_email": senha_email, "senha_lara": senha_lara,
            "sexo": sexo, "nome": nome, "cpf": cpf, "valor": valor, "banco": banco
        })
        escrever_json(ControleLaras._laras_path, data)
        return True

    @staticmethod
    def pegar_todas_laras():
        """Retorna uma lista de todas as 'Laras' no banco de dados."""
        data = ler_json(ControleLaras._laras_path)
        return data.get("laras", [])

    @staticmethod
    def pegar_lara_por_email(email):
        """Busca uma 'Lara' específica pelo email."""
        laras = ControleLaras.pegar_todas_laras()
        for lara in laras:
            if lara.get("email") == email:
                return lara
        return None

    @staticmethod
    def remover_lara(email):
        """Remove uma 'Lara' do banco de dados pelo email."""
        data = ler_json(ControleLaras._laras_path)
        laras_originais = data.get("laras", [])
        laras_restantes = [lara for lara in laras_originais if lara.get("email") != email]
        if len(laras_restantes) < len(laras_originais):
            data["laras"] = laras_restantes
            escrever_json(ControleLaras._laras_path, data)
            return True
        return False

    @staticmethod
    def editar_campo_lara(email, campo, novo_valor):
        """Função genérica para editar um campo de uma 'Lara' específica."""
        data = ler_json(ControleLaras._laras_path)
        for lara in data.get("laras", []):
            if lara.get("email") == email:
                lara[campo] = novo_valor
                escrever_json(ControleLaras._laras_path, data)
                return True
        return False

class ControleGGs():
    _ggs_path = 'database/ggs.json'

    @staticmethod
    def pegar_servicos():
        """Lista todos os tipos de GGs disponíveis (nível)."""
        data = ler_json(ControleGGs._ggs_path)
        return [{"nome": gg.get("nome"), "valor": gg.get("valor"), "descricao": gg.get("descricao")} for gg in data.get("ggs", [])]

    @staticmethod
    def pegar_info(nome):
        """Pega as informações do primeiro GG disponível de um determinado tipo."""
        data = ler_json(ControleGGs._ggs_path)
        for gg in data.get("ggs", []):
            if gg.get("nome") == nome:
                try:
                    valor = float(gg.get("valor"))
                    return (
                        gg.get("nome"), valor, gg.get("descricao"), gg.get("senha"),
                        gg.get("duracao"), gg.get("titular"), gg.get("cpf")
                    )
                except (ValueError, TypeError, AttributeError):
                    continue
        return None

    @staticmethod
    def pegar_estoque(nome):
        """Calcula o estoque para um tipo específico de GG."""
        data = ler_json(ControleGGs._ggs_path)
        return sum(1 for gg in data.get("ggs", []) if gg.get("nome") == nome)

    @staticmethod
    def entregar_gg(nome, numero_gg):
        """Busca um GG específico pelo nome (nível) e número para entrega."""
        data = ler_json(ControleGGs._ggs_path)
        for gg in data.get("ggs", []):
            # 'email' na estrutura original é usado para o número do cartão/gg
            if gg.get("nome") == nome and gg.get("email") == numero_gg:
                return gg
        return None

    @staticmethod
    def remover_gg(nome, numero_gg):
        """Remove um GG do estoque após a compra."""
        data = ler_json(ControleGGs._ggs_path)
        # 'email' na estrutura original é usado para o número do cartão/gg
        ggs_restantes = [gg for gg in data.get("ggs", []) if not (gg.get("nome") == nome and gg.get("email") == numero_gg)]
        if len(ggs_restantes) < len(data.get("ggs", [])):
            data["ggs"] = ggs_restantes
            escrever_json(ControleGGs._ggs_path, data)
            return True
        return False



class ControleCCs():
    _ccs_path = 'database/ccs.json'

    @staticmethod
    def pegar_servicos():
        """Lista todos os tipos de CCs disponíveis (banco/bin)."""
        data = ler_json(ControleCCs._ccs_path)
        lista = []
        for cc in data.get("ccs", []):
            lista.append({"nome": cc.get("nome"), "valor": cc.get("valor"), "descricao": cc.get("descricao")})
        return lista

    @staticmethod
    def pegar_info(nome):
        """Pega as informações do primeiro CC disponível de um determinado tipo."""
        data = ler_json(ControleCCs._ccs_path)
        for cc in data.get("ccs", []):
            if cc.get("nome") == nome:
                try:
                    valor = float(cc.get("valor"))
                    # Retorna as informações necessárias para a tela de exibição e compra
                    return (
                        cc.get("nome"),
                        valor,
                        cc.get("descricao"), # Nível (ex: infinity)
                        cc.get("senha"),     # Validade (ex: 02/28)
                        cc.get("duracao"),   # CVV (ex: 123)
                        cc.get("titular"),   # Nome do Titular
                        cc.get("cpf")        # CPF do Titular
                    )
                except (ValueError, TypeError, AttributeError):
                    continue # Pula item com valor inválido
        return None

    @staticmethod
    def pegar_estoque(nome):
        """Calcula o estoque para um tipo específico de CC."""
        data = ler_json(ControleCCs._ccs_path)
        quantidade = 0
        for cc in data.get("ccs", []):
            if cc.get("nome") == nome:
                quantidade += 1
        return quantidade

    @staticmethod
    def entregar_cc(nome, numero_cc):
        """Busca um CC específico pelo nome (banco/bin) e número para entrega."""
        data = ler_json(ControleCCs._ccs_path)
        for cc in data.get("ccs", []):
            if cc.get("nome") == nome and cc.get("email") == numero_cc:
                return cc # Retorna o dicionário completo do CC
        return None

    @staticmethod
    def remover_cc(nome, numero_cc):
        """Remove um CC do estoque após a compra."""
        data = ler_json(ControleCCs._ccs_path)
        ccs_restantes = [cc for cc in data.get("ccs", []) if not (cc.get("nome") == nome and cc.get("email") == numero_cc)]
        if len(ccs_restantes) < len(data.get("ccs", [])):
            data["ccs"] = ccs_restantes
            escrever_json(ControleCCs._ccs_path, data)
            return True
        return False
class Admin():
    class ControleGGs():
        _ggs_path = 'database/ggs.json'

        @staticmethod
        def add_gg(nome, valor, descricao, email, senha, duracao, titular, cpf):
            data = ler_json(Admin.ControleGGs._ggs_path)
            data.setdefault("ggs", []).append({
                "nome": nome, "valor": valor, "descricao": descricao, "email": email, 
                "senha": senha, "duracao": duracao, "titular": titular, "cpf": cpf
            })
            escrever_json(Admin.ControleGGs._ggs_path, data)
            return True
        
        @staticmethod
        def pegar_niveis_unicos():
            """Retorna uma lista de todos os níveis (descrições) de GGs únicos."""
            data = ler_json(Admin.ControleGGs._ggs_path)
            niveis = {gg.get("descricao").strip() for gg in data.get("ggs", []) if gg.get("descricao")}
            return sorted(list(niveis))

        @staticmethod
        def pegar_ggs_por_nivel(nivel):
            """Retorna todos os GGs que pertencem a um determinado nível."""
            data = ler_json(Admin.ControleGGs._ggs_path)
            return [gg for gg in data.get("ggs", []) if gg.get("descricao") == nivel]

        @staticmethod
        def remover_gg(nome, email):
            data = ler_json(Admin.ControleGGs._ggs_path)
            ggs_restantes = [gg for gg in data.get("ggs", []) if not (gg.get("nome") == nome and gg.get("email") == email)]
            if len(ggs_restantes) < len(data.get("ggs", [])):
                data["ggs"] = ggs_restantes
                escrever_json(Admin.ControleGGs._ggs_path, data)
                return True
            return False
        
        @staticmethod
        def remover_por_nome(nome):
            data = ler_json(Admin.ControleGGs._ggs_path)
            ggs_mantidos = [gg for gg in data["ggs"] if str(gg.get("nome")) != str(nome)]
            data["ggs"] = ggs_mantidos
            escrever_json(Admin.ControleGGs._ggs_path, data)
            return True
        
        @staticmethod
        def _editar_campo_gg(numero_gg, campo, novo_valor):
            """Função genérica para editar um campo de um GG específico."""
            data = ler_json(Admin.ControleGGs._ggs_path)
            gg_encontrado = False
            for gg in data.get("ggs", []):
                if gg.get("nome") == numero_gg:
                    gg[campo] = novo_valor
                    gg_encontrado = True
                    break
            if gg_encontrado:
                escrever_json(Admin.ControleGGs._ggs_path, data)
            return gg_encontrado

        @staticmethod
        def mudar_valor_gg(numero_gg, novo_valor):
            return Admin.ControleGGs._editar_campo_gg(numero_gg, 'valor', float(novo_valor))

        @staticmethod
        def mudar_nivel_gg(numero_gg, novo_nivel):
            return Admin.ControleGGs._editar_campo_gg(numero_gg, 'descricao', novo_nivel)

        @staticmethod
        def mudar_titular_gg(numero_gg, novo_titular):
            return Admin.ControleGGs._editar_campo_gg(numero_gg, 'titular', novo_titular)

        @staticmethod
        def mudar_cpf_gg(numero_gg, novo_cpf):
            return Admin.ControleGGs._editar_campo_gg(numero_gg, 'cpf', novo_cpf)

        @staticmethod
        def remover_por_nivel(nivel):
            data = ler_json(Admin.ControleGGs._ggs_path)
            ggs_mantidos = [gg for gg in data.get("ggs", []) if gg.get("descricao") != nivel]
            if len(ggs_mantidos) < len(data.get("ggs", [])):
                data["ggs"] = ggs_mantidos
                escrever_json(Admin.ControleGGs._ggs_path, data)
                return True
            return False
        
        @staticmethod
        def estoque_total():
            data = ler_json(Admin.ControleGGs._ggs_path)
            return len(data.get("ggs", []))
        
        @staticmethod
        def zerar_estoque():
            escrever_json(Admin.ControleGGs._ggs_path, {"ggs": []})
            return True

    _credenciais_path = 'settings/credenciais.json'

    class ControleCCs():
        _ccs_path = 'database/ccs.json'

        @staticmethod
        def add_cc(nome, valor, descricao, email, senha, duracao, titular, cpf):
            data = ler_json(Admin.ControleCCs._ccs_path)
            data.setdefault("ccs", []).append({
                "nome": nome, "valor": valor, "descricao": descricao, "email": email, 
                "senha": senha, "duracao": duracao, "titular": titular, "cpf": cpf
            })
            escrever_json(Admin.ControleCCs._ccs_path, data)
            return True
        
        @staticmethod
        def pegar_niveis_unicos():
            """Retorna uma lista de todos os níveis (descrições) de CCs únicos."""
            data = ler_json(Admin.ControleCCs._ccs_path)
            niveis = {cc.get("descricao").strip() for cc in data.get("ccs", []) if cc.get("descricao")}
            return sorted(list(niveis))

        @staticmethod
        def pegar_ccs_por_nivel(nivel):
            """Retorna todos os CCs que pertencem a um determinado nível."""
            data = ler_json(Admin.ControleCCs._ccs_path)
            return [cc for cc in data.get("ccs", []) if cc.get("descricao") == nivel]

        @staticmethod
        def remover_cc(nome, email):
            data = ler_json(Admin.ControleCCs._ccs_path)
            ccs_restantes = [cc for cc in data.get("ccs", []) if not (cc.get("nome") == nome and cc.get("email") == email)]
            if len(ccs_restantes) < len(data.get("ccs", [])):
                data["ccs"] = ccs_restantes
                escrever_json(Admin.ControleCCs._ccs_path, data)
                return True
            return False
        
        @staticmethod
        def remover_por_nome(nome):
            data = ler_json(Admin.ControleCCs._ccs_path)
            ccs_mantidos = [cc for cc in data["ccs"] if str(cc.get("nome")) != str(nome)]
            data["ccs"] = ccs_mantidos
            escrever_json(Admin.ControleCCs._ccs_path, data)
            return True
        
        @staticmethod
        def _editar_campo_cc(numero_cc, campo, novo_valor):
            """Função genérica para editar um campo de um CC específico."""
            data = ler_json(Admin.ControleCCs._ccs_path)
            cc_encontrado = False
            for cc in data.get("ccs", []):
                if cc.get("nome") == numero_cc:
                    cc[campo] = novo_valor
                    cc_encontrado = True
                    break
            if cc_encontrado:
                escrever_json(Admin.ControleCCs._ccs_path, data)
            return cc_encontrado

        @staticmethod
        def mudar_valor_cc(numero_cc, novo_valor):
            """Muda o valor de um CC específico."""
            return Admin.ControleCCs._editar_campo_cc(numero_cc, 'valor', float(novo_valor))

        @staticmethod
        def mudar_nivel_cc(numero_cc, novo_nivel):
            """Muda o nível (descrição) de um CC específico."""
            return Admin.ControleCCs._editar_campo_cc(numero_cc, 'descricao', novo_nivel)

        @staticmethod
        def mudar_titular_cc(numero_cc, novo_titular):
            """Muda o nome do titular de um CC específico."""
            return Admin.ControleCCs._editar_campo_cc(numero_cc, 'titular', novo_titular)

        @staticmethod
        def mudar_cpf_cc(numero_cc, novo_cpf):
            """Muda o CPF do titular de um CC específico."""
            return Admin.ControleCCs._editar_campo_cc(numero_cc, 'cpf', novo_cpf)

        @staticmethod
        def remover_por_nivel(nivel):
            data = ler_json(Admin.ControleCCs._ccs_path)
            ccs_mantidos = [cc for cc in data.get("ccs", []) if cc.get("descricao") != nivel]
            if len(ccs_mantidos) < len(data.get("ccs", [])):
                data["ccs"] = ccs_mantidos
                escrever_json(Admin.ControleCCs._ccs_path, data)
                return True
            return False
        
        @staticmethod
        def mudar_valor_por_nome(nome, novo_valor):
            data = ler_json(Admin.ControleCCs._ccs_path)
            for cc in data["ccs"]:
                if cc["nome"] == nome:
                    cc["valor"] = float(novo_valor)
            escrever_json(Admin.ControleCCs._ccs_path, data)
        
        @staticmethod
        def mudar_valor_de_todos(valor):
            data = ler_json(Admin.ControleCCs._ccs_path)
            for cc in data["ccs"]:
                cc["valor"] = float(valor)
            escrever_json(Admin.ControleCCs._ccs_path, data)
        
        @staticmethod
        def estoque_total():
            data = ler_json(Admin.ControleCCs._ccs_path)
            return len(data.get("ccs", []))
        
        @staticmethod
        def zerar_estoque():
            escrever_json(Admin.ControleCCs._ccs_path, {"ccs": []})
            return True

    @staticmethod
    def total_users():
        data = ler_json('database/users.json')
        return len(data.get("users", []))

    @staticmethod
    def verificar_vencimento():
        time = Admin.tempo_ate_o_vencimento()
        return int(time) <= 0
    
    @staticmethod
    def data_vencimento():
        data = ler_json(Admin._credenciais_path)
        return str(data.get("vencimento_bot", "N/A"))

    @staticmethod
    def tempo_ate_o_vencimento():
        try:
            data = ler_json(Admin._credenciais_path)
            data_vencimento_str = data.get('vencimento_bot', '01/01/1970')
            data_vencimento = datetime.datetime.strptime(data_vencimento_str, '%d/%m/%Y').date()
            return (data_vencimento - datetime.date.today()).days
        except (ValueError, KeyError):
            return -999

    @staticmethod
    def _modificar_vencimento(dias):
        data = ler_json(Admin._credenciais_path)
        vencimento_str = data.get('vencimento_bot', '01/01/1970')
        vencimento_bot = datetime.datetime.strptime(vencimento_str, '%d/%m/%Y')
        nova_data = vencimento_bot + datetime.timedelta(days=int(dias))
        data["vencimento_bot"] = nova_data.strftime('%d/%m/%Y')
        escrever_json(Admin._credenciais_path, data)
        return True

    @staticmethod
    def aumentar_vencimento(dias):
        return Admin._modificar_vencimento(dias)

    @staticmethod
    def diminuir_vencimento(dias):
        return Admin._modificar_vencimento(-int(dias))

    @staticmethod
    def zerar_vencimento():
        data = ler_json(Admin._credenciais_path)
        data["vencimento_bot"] = '01/01/2023'
        escrever_json(Admin._credenciais_path, data)

    @staticmethod
    def receita_total():
        data = ler_json('database/users.json')
        return sum(float(p.get("valor", 0.0)) for u in data.get("users", []) for p in u.get("pagamentos", []))

    @staticmethod
    def receita_hoje():
        data = ler_json('database/users.json')
        today = ViewTime.data_atual()
        return sum(float(p.get("valor", 0.0)) for u in data.get("users", []) for p in u.get("pagamentos", []) if str(p.get('data', '').split(' ')[0]) == str(today))

    @staticmethod
    def acessos_vendidos():
        data = ler_json('database/users.json')
        return sum(u.get("total_compras", 0) for u in data.get("users", []))

    @staticmethod
    def acessos_vendidos_hoje():
        data = ler_json('database/users.json')
        today = ViewTime.data_atual()
        return sum(1 for u in data.get("users", []) for c in u.get("compras", []) if str(c.get("data", "").split(" ")[0]) == str(today))

    @staticmethod
    def zerar_acessos_vendidos():
        data = ler_json('database/users.json')
        for user in data.get("users", []):
            user["total_compras"] = 0
            user["compras"] = []
            user["total_pagos"] = 0
            user["pagamentos"] = []
        escrever_json('database/users.json', data)

    @staticmethod
    def verificar_admin(id):
        data = ler_json('database/admins.json')
        return any(int(admin.get("id", 0)) == int(id) for admin in data.get("admins", []))

    @staticmethod
    def add_admin(id):
        data = ler_json('database/admins.json')
        if not any(int(a.get("id", 0)) == int(id) for a in data.get("admins", [])):
            data.setdefault("admins", []).append({"id": int(id)})
            escrever_json('database/admins.json', data)
        return True

    @staticmethod
    def quantidade_admin():
        data = ler_json('database/admins.json')
        return len(data.get("admins", []))

    @staticmethod
    def listar_admins():
        data = ler_json('database/admins.json')
        adm_list = '<b>👮 LISTA DE ADMINS:</b> 🚨\n\n'
        adm_list += '\n'.join([f'<b>ADMIN ID:</b> <code>{admin.get("id")}</code>' for admin in data.get("admins", [])])
        return adm_list

    @staticmethod
    def remover_admin(id):
        data = ler_json('database/admins.json')
        admins_restantes = [a for a in data.get("admins", []) if int(a.get("id", 0)) != int(id)]
        if len(admins_restantes) < len(data.get("admins", [])):
            data["admins"] = admins_restantes
            escrever_json('database/admins.json', data)
            return True
        return False
import texts

class Textos(texts.Textos):
    pass

class Botoes(texts.Botoes):
    pass
class Log():
    _credenciais_path = 'settings/credenciais.json'

    @staticmethod
    def id_log_destino():
        data = ler_json(Log._credenciais_path)
        return data.get("destino_log")

    @staticmethod
    def mudar_destino_logs(id):
        data = ler_json(Log._credenciais_path)
        data["destino_log"] = id
        escrever_json(Log._credenciais_path, data)

    @staticmethod
    def _formatar_log(caminho_template, message, **kwargs):
        try:
            with open(caminho_template, 'r', encoding='utf-8') as f:
                txt = f.read()
        except FileNotFoundError:
            return f"Template de log não encontrado: {caminho_template}"
        
        if message is None: return txt

        replacements = {
            '{id}': str(message.chat.id),
            '{name}': str(message.chat.first_name),
            '{username}': f'@{message.chat.username}' if message.chat.username else 'N/A',
            '{link}': f'https://t.me/{message.chat.username}' if message.chat.username else 'N/A',
            '{data}': ViewTime.data_atual(),
            '{hora}': ViewTime.hora_atual(),
            '{saldo}': f'{InfoUser.saldo(message.chat.id):.2f}',
            '\\n': '\n'
        }
        replacements.update({f'{{{k}}}': str(v) for k, v in kwargs.items()})

        for key, value in replacements.items():
            txt = txt.replace(key, value)
        return txt

    @staticmethod
    def log_registro(message):
        return Log._formatar_log('log/registro.txt', message)

    @staticmethod
    def log_compra(message, servico, email, senha, valor, descricao):
        return Log._formatar_log('log/compra.txt', message, servico=servico, email=email, senha=senha, valor=f'{float(valor):.2f}', descricao=descricao)

    @staticmethod
    def log_recarga(message, id_pagamento, valor):
        return Log._formatar_log('log/recarga.txt', message, id_pagamento=id_pagamento, valor=f'{float(valor):.2f}')

class MudarLog():
    @staticmethod
    def _escrever_log(caminho, txt):
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(txt)

    @staticmethod
    def log_registro(txt):
        MudarLog._escrever_log('log/registro.txt', txt)

    @staticmethod
    def log_compra(txt):
        MudarLog._escrever_log('log/compra.txt', txt)

    @staticmethod
    def log_recarga(txt):
        MudarLog._escrever_log('log/recarga.txt', txt)

class CriarPix():
    @staticmethod
    def gerar(valor, id):
        sdk = mercadopago.SDK(str(CredentialsChange.InfoPix.token_mp()))
        expiracao_time = CredentialsChange.InfoPix.expiracao()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(expiracao_time))
        # Formato correto para a API do Mercado Pago
        expire = expire.strftime("%Y-%m-%dT%H:%M:%S.000-03:00")
        payment_data = {
            "transaction_amount": float(valor),
            "description":f'Recarga de {valor} para {id}',
            "payment_method_id": 'pix',
            "date_of_expiration": f'{expire}',
            "payer": {
                "email": 'maxwilliam.saraiva@outlook.com'
            }
        }
        result = sdk.payment().create(payment_data)
        return result
