import mercadopago
import json
import string
import telebot
import time
import sys
import uuid
import base64
import re
import os
import html
import datetime
import subprocess
import threading
import random
import signal
import central as api
from os import system
from telebot import types
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from datetime import timezone
from pytz import timezone

# Flag para controle do bot
bot_running = True

def signal_handler(sig, frame):
    global bot_running
    print("\n[INFO] Recebido sinal de parada. Desligando bot...")
    bot_running = False
    try:
        bot.stop_polling()
    except:
        pass
    print("[INFO] Bot desligado com sucesso!")
    sys.exit(0)

# Registra o handler para SIGINT (Ctrl+C) e SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print("🤖 Codigo iniciado...")
print(f"📅 Data/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"🐍 Python: {sys.version}")
print("=" * 50)

# Inicializa o SDK e o Bot no escopo global
try:
    # Lê o token da variável de ambiente 'BOT_TOKEN'. Se não encontrar, usa o do arquivo (para testes locais).
    BOT_TOKEN = os.environ.get('BOT_TOKEN', api.CredentialsChange.token_bot())

    sdk = mercadopago.SDK(api.CredentialsChange.InfoPix.token_mp())
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

    # Obtém informações do bot e armazena o username
    me = bot.get_me()
    BOT_USERNAME = me.username
    print(f"🤖 Bot ID: {me.id}, Username: @{BOT_USERNAME}")
except telebot.apihelper.ApiTelegramException as e:
    print(f"❌ Erro fatal da API do Telegram: {e}")
    print("   Verifique se o token do bot em 'settings/credenciais.json' está correto e não foi revogado.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro fatal ao inicializar o bot: {e}")
    if "timed out" in str(e) or "Connection" in str(e):
        print("   [DICA] Este parece ser um erro de conexão. Verifique sua internet ou se o acesso ao Telegram não está bloqueado.")
    else:
        print("   Verifique as configurações do bot e as dependências.")
    sys.exit(1)

# --- Funções de Verificação e Handlers ---

def ver_se_expirou():
    if api.Admin.verificar_vencimento() == True:
        try:
            bot.send_message(api.CredentialsChange.id_dono(), "OPSS, O PLANO DO SEU BOT VENCEU ELE ESTA INATIVO. RENOVE-O AGORA!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('♻ RENOVAR AGORA', callback_data='renovar_bot')]]))
            bot.send_message(chat_id=int(api.CredentialsChange.id_dono()), text=f'Olá chefe, o bot @{BOT_USERNAME} está vencido!')
        except Exception as e:
            print(f"Erro ao notificar dono sobre vencimento: {e}")


@bot.message_handler(commands=['cancelar'])
def handle_cancelar(message):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.reply_to(message, "ordem cancelada!")
#Painel adm
@bot.message_handler(commands=['admin'])
def painel_admin(message):
    if api.Admin.verificar_admin(message.chat.id) == True or int(message.chat.id) == int(api.CredentialsChange.id_dono()):
        vencimento = "SEU BOT ESTÁ VENCIDO!" if api.Admin.tempo_ate_o_vencimento() <= 0 else f'SEU BOT VENCE EM {api.Admin.tempo_ate_o_vencimento()} DIAS!'
        texto = f'⚙️ <b>PAINEL DE GERENCIAMENTO</b>\n⚠️ <b>{vencimento}</b>⚠️\n🤖 <i>V{api.CredentialsChange.versao_bot()}</i>\n\n📘 <b>Estatísticas:</b>\n📊 Usuarios: {api.Admin.total_users()}\n📈 Receita total: R${api.Admin.receita_total():.2f}\n💠 Receita de hoje: R${api.Admin.receita_hoje():.2f}\n📺 Produtos vendidos: {api.Admin.acessos_vendidos()}\n📲 Produtos vendidos hoje: {api.Admin.acessos_vendidos_hoje()}\n\n🛠 <i>Use os botões abaixo para me configurar</i>'
        bt = InlineKeyboardButton('⚙️ CONFIGURAÇÕES GERAIS ⚙️', callback_data='configuracoes_geral')
        bt2 = InlineKeyboardButton('🖥 CONFIGURAR LOGINS', callback_data='configurar_logins')
        bt3 = InlineKeyboardButton('🕵️ CONFIGURAR ADMINS', callback_data='configurar_admins')
        bt4 = InlineKeyboardButton('👥 CONFIGURAR AFILIADOS', callback_data='configurar_afiliados')
        bt5 = InlineKeyboardButton('👤 CONFIGURAR USUARIOS', callback_data='configurar_usuarios')
        bt6 = InlineKeyboardButton('💠 CONFIGURAR PIX', callback_data='configurar_pix')
        bt7 = InlineKeyboardButton('🛎 NOTIFICAÇÕES FAKE', callback_data='configurar_notificacoes_fake')
        bt8 = InlineKeyboardButton('🎁 GIFT CARD 🎁', callback_data='gift_card')
        bt_ccs = InlineKeyboardButton("💳 CONFIGURAR CC'S", callback_data='configurar_ccs')
        bt_laras = InlineKeyboardButton('🍊 CONFIGURAR LARAS', callback_data='configurar_laras')
        bt_ggs = InlineKeyboardButton('✨ CONFIGURAR GGS', callback_data='configurar_ggs')
        markup = InlineKeyboardMarkup([[bt], [bt2, bt_ccs], [bt_laras, bt_ggs], [bt3, bt4], [bt5, bt6], [bt7, bt8]])
        if message.text != '/admin':
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
            except telebot.apihelper.ApiTelegramException as e:
                if 'message is not modified' not in e.description:
                    raise
        else:
            bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)
    else:
        bot.reply_to(message, "Você não é um adm!")
        return

def configurar_laras(message):
    """Exibe o menu de gerenciamento para o produto 'Laras'."""
    texto = "🍊 <b>Gerenciamento de Laras</b>\n\nSelecione uma das opções abaixo:"
    markup = InlineKeyboardMarkup()
    bt_add = InlineKeyboardButton('➕ ADICIONAR LARA', callback_data='adicionar_lara')
    bt_edit = InlineKeyboardButton('✏️ EDITAR/REMOVER LARA', callback_data='gerenciar_laras')
    bt_voltar = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup.add(bt_add)
    markup.add(bt_edit)
    markup.add(bt_voltar)
    
    # Usamos edit_message_text para manter a navegação fluida
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)

def configurar_ggs(message):
    """Exibe o menu de gerenciamento para o produto 'GGs'."""
    texto = "✨ <b>Gerenciamento de GGs (Geradas)</b>\n\nSelecione uma das opções abaixo:"
    markup = InlineKeyboardMarkup()
    bt_add = InlineKeyboardButton('➕ ADICIONAR GG', callback_data='adicionar_gg')
    bt_edit = InlineKeyboardButton('✏️ EDITAR/REMOVER GG', callback_data='gerenciar_ggs_menu')
    bt_voltar = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup.add(bt_add)
    markup.add(bt_edit)
    markup.add(bt_voltar)
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)

# --- Fluxo de Adição e Gerenciamento de GGs (Admin) ---
def iniciar_adicionar_gg(message):
    """Inicia o processo de adicionar GG, pedindo o número."""
    bot.send_message(message.chat.id, "✨ Qual o <b>número</b> da GG (Gerada)?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_nivel_gg)

def pedir_nivel_gg(message):
    """Pede o nível da GG."""
    numero_gg = message.text
    bot.send_message(message.chat.id, "⭐ Qual o <b>nível</b> da GG? (Ex: Gold, Silver, Bronze)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_valor_gg, numero_gg)

def pedir_valor_gg(message, numero_gg):
    """Pede o valor da GG."""
    nivel_gg = message.text
    bot.send_message(message.chat.id, "💰 Qual o <b>valor</b> de venda da GG?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_validade_gg, numero_gg, nivel_gg)

def pedir_validade_gg(message, numero_gg, nivel_gg):
    """Pede a data de validade."""
    try:
        valor_gg = float(message.text.replace(',', '.'))
    except ValueError:
        bot.reply_to(message, "❌ Valor inválido. Por favor, envie apenas números. O processo foi cancelado.")
        return
    
    bot.send_message(message.chat.id, "📅 Qual a <b>data de validade</b>? (Ex: 02/28)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cvv_gg, numero_gg, nivel_gg, valor_gg)

def pedir_cvv_gg(message, numero_gg, nivel_gg, valor_gg):
    """Pede o nome do titular."""
    validade_gg = message.text
    bot.send_message(message.chat.id, "👤 Qual o <b>nome completo</b> do titular?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cpf_titular_gg, numero_gg, nivel_gg, valor_gg, validade_gg)

def pedir_cpf_titular_gg(message, numero_gg, nivel_gg, valor_gg, validade_gg):
    """Pede o CPF do titular."""
    nome_titular = message.text
    bot.send_message(message.chat.id, "📄 Qual o <b>CPF</b> do titular?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cvv_final_gg, numero_gg, nivel_gg, valor_gg, validade_gg, nome_titular)

def pedir_cvv_final_gg(message, numero_gg, nivel_gg, valor_gg, validade_gg, nome_titular):
    """Pede o CVV e chama a função final."""
    cpf_titular = message.text
    bot.send_message(message.chat.id, "🔒 Qual o <b>CVV/código de segurança</b>?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, finalizar_adicao_gg, numero_gg, nivel_gg, valor_gg, validade_gg, nome_titular, cpf_titular)

def finalizar_adicao_gg(message, numero_gg, nivel_gg, valor_gg, validade_gg, nome_titular, cpf_titular):
    """Adiciona a GG ao banco de dados e informa o admin."""
    cvv_gg = message.text
    try:
        # A estrutura é a mesma da CC: nome=número, email=número, senha=validade, duracao=cvv
        api.Admin.ControleGGs.add_gg(nome=numero_gg, valor=valor_gg, descricao=nivel_gg, email=numero_gg, senha=validade_gg, duracao=cvv_gg, titular=nome_titular, cpf=cpf_titular)
        bot.reply_to(message, f"✅ <b>GG adicionada com sucesso!</b>\n\n<b>Número:</b> <code>{numero_gg}</code>\n<b>Nível:</b> {nivel_gg}\n<b>Valor:</b> R$ {valor_gg:.2f}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ocorreu um erro ao adicionar a GG: {e}")

def gerenciar_ggs_menu(call):
    """Exibe os níveis de GGs disponíveis para gerenciamento."""
    niveis = api.Admin.ControleGGs.pegar_niveis_unicos()
    markup = InlineKeyboardMarkup()

    if not niveis:
        bot.answer_callback_query(call.id, "Nenhum nível de GG encontrado no estoque.", show_alert=True)
        return

    for nivel in niveis:
        markup.add(InlineKeyboardButton(f"Nível: {nivel.upper()}", callback_data=f"listar_ggs_do_nivel {nivel}"))
    
    markup.add(InlineKeyboardButton("↩️ Voltar", callback_data="configurar_ggs"))
    texto = "🗂️ Selecione um <b>nível</b> para ver ou remover as GGs:"
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def listar_ggs_do_nivel(call, nivel):
    """Lista todas as GGs de um nível específico com opções de gerenciamento."""
    ggs_do_nivel = api.Admin.ControleGGs.pegar_ggs_por_nivel(nivel)
    markup = InlineKeyboardMarkup()
    
    texto = f"✨ <b>GGs do Nível: {nivel.upper()}</b>\n\n"

    if not ggs_do_nivel:
        texto += "Não há GGs neste nível."
    else:
        for gg in ggs_do_nivel:
            numero = gg.get("nome")
            email_id = gg.get("email") # Identificador único
            texto_gg = f"<code>{numero[:6]}...{numero[-4:]}</code> - R${gg.get('valor'):.2f}"
            markup.add(InlineKeyboardButton(texto_gg, callback_data="noop"), InlineKeyboardButton("✏️", callback_data=f"editar_gg_menu {numero}|{email_id}"), InlineKeyboardButton("❌", callback_data=f"remover_gg_especifico {numero}|{email_id}"))

    markup.add(InlineKeyboardButton(f"🗑️ Remover TODAS de {nivel.upper()}", callback_data=f"confirmar_remover_nivel_gg {nivel}"))
    markup.add(InlineKeyboardButton("↩️ Voltar aos Níveis", callback_data="gerenciar_ggs_menu"))

    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def confirmar_remover_nivel_gg(call, nivel):
    """Pede confirmação para remover todas as GGs de um nível."""
    texto = f"⚠️ <b>ATENÇÃO</b> ⚠️\n\nVocê tem certeza que deseja remover <b>TODAS</b> as GGs do nível <b>{nivel.upper()}</b>?\n\nEsta ação não pode ser desfeita."
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"✅ Sim, remover todas", callback_data=f"remover_nivel_gg_confirmado {nivel}")],
        [InlineKeyboardButton("❌ Não, cancelar", callback_data=f"listar_ggs_do_nivel {nivel}")]
    ])
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def remover_nivel_gg_confirmado(call, nivel):
    """Remove todas as GGs de um nível e atualiza a visualização."""
    if api.Admin.ControleGGs.remover_por_nivel(nivel):
        bot.answer_callback_query(call.id, f"Todas as GGs do nível '{nivel.upper()}' foram removidas.", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Erro ao remover as GGs ou nenhuma GG encontrada.", show_alert=True)
    gerenciar_ggs_menu(call)

def editar_gg_menu(call, gg_identifier):
    """Exibe o menu de edição para uma GG específica."""
    try:
        numero, email = gg_identifier.split('|')
    except ValueError:
        bot.answer_callback_query(call.id, "Erro: Identificador de GG inválido.", show_alert=True)
        return

    gg_data = api.ControleGGs.entregar_gg(numero, email)
    if not gg_data:
        bot.answer_callback_query(call.id, "Erro: GG não encontrada.", show_alert=True)
        return

    texto = (
        f"✏️ <b>Editando GG</b>\n\n"
        f"<b>Número:</b> <code>{gg_data.get('nome', 'N/A')}</code>\n"
        f"<b>Nível:</b> {gg_data.get('descricao', 'N/A')}\n"
        f"<b>Valor:</b> R$ {float(gg_data.get('valor', 0)):.2f}\n"
        f"<b>Validade:</b> <code>{gg_data.get('senha', 'N/A')}</code>\n"
        f"<b>CVV:</b> <code>{gg_data.get('duracao', 'N/A')}</code>\n"
        f"<b>Titular:</b> {gg_data.get('titular', 'N/A')}\n"
        f"<b>CPF:</b> <code>{gg_data.get('cpf', 'N/A')}</code>\n\n"
        "Selecione o campo que deseja editar:"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💰 Editar Valor", callback_data=f"editar_campo_gg valor|{numero}"))
    markup.add(InlineKeyboardButton("⭐ Editar Nível", callback_data=f"editar_campo_gg nivel|{numero}"))
    markup.add(InlineKeyboardButton("👤 Editar Titular", callback_data=f"editar_campo_gg titular|{numero}"))
    markup.add(InlineKeyboardButton("📄 Editar CPF", callback_data=f"editar_campo_gg cpf|{numero}"))
    markup.add(InlineKeyboardButton("↩️ Voltar", callback_data=f"listar_ggs_do_nivel {gg_data.get('descricao')}"))

    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def solicitar_novo_valor_campo_gg(call, campo, numero_gg):
    """Pede ao admin o novo valor para um campo específico da GG."""
    mapa_campos = {
        'valor': 'o novo valor', 'nivel': 'o novo nível',
        'titular': 'o novo nome do titular', 'cpf': 'o novo CPF'
    }
    prompt = f"Digite {mapa_campos.get(campo, 'o novo valor')} para a GG <code>{numero_gg}</code>:"
    bot.send_message(call.message.chat.id, prompt, parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(call.message, salvar_campo_gg_editado, campo, numero_gg)

def salvar_campo_gg_editado(message, campo, numero_gg):
    """Salva o valor editado do campo da GG no banco de dados."""
    novo_valor = message.text.strip()
    sucesso = False
    
    try:
        if campo == 'valor':
            sucesso = api.Admin.ControleGGs.mudar_valor_gg(numero_gg, novo_valor)
        elif campo == 'nivel':
            sucesso = api.Admin.ControleGGs.mudar_nivel_gg(numero_gg, novo_valor)
        elif campo == 'titular':
            sucesso = api.Admin.ControleGGs.mudar_titular_gg(numero_gg, novo_valor)
        elif campo == 'cpf':
            sucesso = api.Admin.ControleGGs.mudar_cpf_gg(numero_gg, novo_valor)

        if sucesso:
            bot.reply_to(message, f"✅ O campo '{campo}' da GG foi atualizado com sucesso!")
        else:
            bot.reply_to(message, "❌ Erro: Não foi possível atualizar a GG.")

    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao processar a alteração: {e}")

# --- Fluxo de Adição de Laras ---
def iniciar_adicionar_lara(message):
    """Inicia o processo de adicionar Lara, pedindo o e-mail."""
    bot.send_message(message.chat.id, "📧 Qual o <b>e-mail</b> da conta?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_senha_email_lara)

def pedir_senha_email_lara(message):
    """Pede a senha do e-mail."""
    email = message.text
    bot.send_message(message.chat.id, "🔑 Qual a <b>senha do e-mail</b>?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_senha_lara, email)

def pedir_senha_lara(message, email):
    """Pede a senha da 'Lara'."""
    senha_email = message.text
    bot.send_message(message.chat.id, "🍊 Qual a <b>senha da Lara</b>?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_sexo_lara, email, senha_email)

def pedir_sexo_lara(message, email, senha_email):
    """Pede o sexo."""
    senha_lara = message.text
    bot.send_message(message.chat.id, "♀️♂️ Qual o <b>sexo</b>? (Feminino/Masculino)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_nome_lara, email, senha_email, senha_lara)

def pedir_nome_lara(message, email, senha_email, senha_lara):
    """Pede o nome completo."""
    sexo = message.text
    bot.send_message(message.chat.id, "👤 Qual o <b>nome completo</b>?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cpf_lara, email, senha_email, senha_lara, sexo)

def pedir_cpf_lara(message, email, senha_email, senha_lara, sexo):
    """Pede o CPF."""
    nome = message.text
    bot.send_message(message.chat.id, "📄 Qual o <b>CPF</b>?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_banco_lara, email, senha_email, senha_lara, sexo, nome)

def pedir_banco_lara(message, email, senha_email, senha_lara, sexo, nome):
    """Pede o banco da Lara."""
    cpf = message.text
    bot.send_message(message.chat.id, "🏦 Qual o <b>banco</b> da Lara?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_valor_lara, email, senha_email, senha_lara, sexo, nome, cpf)

def pedir_valor_lara(message, email, senha_email, senha_lara, sexo, nome, cpf):
    """Pede o valor de venda."""
    banco = message.text
    bot.send_message(message.chat.id, "💰 Qual o <b>valor de venda</b> do produto?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, finalizar_adicao_lara, email, senha_email, senha_lara, sexo, nome, cpf, banco)

def finalizar_adicao_lara(message, email, senha_email, senha_lara, sexo, nome, cpf, banco):
    """Finaliza a adição da Lara, salvando no banco de dados."""
    try:
        valor = float(message.text.replace(',', '.'))
        api.ControleLaras.add_lara(email, senha_email, senha_lara, sexo, nome, cpf, valor, banco)
        bot.reply_to(message, f"✅ <b>Produto 'Lara' adicionado com sucesso!</b>\n\n<b>E-mail:</b> <code>{email}</code>\n<b>Nome:</b> {nome}\n<b>Banco:</b> {banco}\n<b>Valor:</b> R$ {valor:.2f}", parse_mode='HTML')
    except ValueError:
        bot.reply_to(message, "❌ Valor inválido. Por favor, envie apenas números. O processo foi cancelado.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ocorreu um erro ao adicionar o produto: {e}")

# --- Fluxo de Gerenciamento de Laras ---
def gerenciar_laras_menu(call):
    """Exibe a lista de Laras disponíveis para gerenciamento."""
    laras = api.ControleLaras.pegar_todas_laras()
    markup = InlineKeyboardMarkup()
    
    texto = "🍊 <b>Gerenciar Laras</b>\n\nSelecione uma para editar ou remover:\n\n"

    if not laras:
        texto += "Não há 'Laras' no estoque."
    else:
        for lara in laras:
            email = lara.get("email")
            valor = lara.get("valor", 0)
            texto_lara = f"<code>{email}</code> - R${valor:.2f}"
            # Adiciona botões de Editar e Remover para cada Lara
            markup.add(
                InlineKeyboardButton(texto_lara, callback_data="noop"),
                InlineKeyboardButton("✏️", callback_data=f"editar_lara_menu {email}"),
                InlineKeyboardButton("❌", callback_data=f"remover_lara_confirma {email}")
            )

    markup.add(InlineKeyboardButton('↩ VOLTAR', callback_data='configurar_laras'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

def remover_lara_confirma(call, email):
    """Pede confirmação para remover uma Lara."""
    texto = f"⚠️ <b>ATENÇÃO</b> ⚠️\n\nVocê tem certeza que deseja remover a Lara com o e-mail:\n<code>{email}</code>?\n\nEsta ação não pode ser desfeita."
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Sim, remover", callback_data=f"remover_lara_executa {email}")],
        [InlineKeyboardButton("❌ Não, cancelar", callback_data="gerenciar_laras")]
    ])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

def remover_lara_executa(call, email):
    """Executa a remoção da Lara."""
    if api.ControleLaras.remover_lara(email):
        bot.answer_callback_query(call.id, "Lara removida com sucesso!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Erro: Lara não encontrada.", show_alert=True)
    # Volta para o menu de gerenciamento
    gerenciar_laras_menu(call)

def editar_lara_menu(call, email):
    """Exibe o menu de edição para uma Lara específica."""
    lara = api.ControleLaras.pegar_lara_por_email(email)
    if not lara:
        bot.answer_callback_query(call.id, "Erro: Lara não encontrada.", show_alert=True)
        return

    texto = (
        f"✏️ <b>Editando Lara:</b> <code>{lara.get('email')}</code>\n\n"
        f"<b>Senha E-mail:</b> <code>{lara.get('senha_email', 'N/A')}</code>\n"
        f"<b>Senha Lara:</b> <code>{lara.get('senha_lara', 'N/A')}</code>\n"
        f"<b>Sexo:</b> {lara.get('sexo', 'N/A')}\n"
        f"<b>Nome:</b> {lara.get('nome', 'N/A')}\n"
        f"<b>CPF:</b> <code>{lara.get('cpf', 'N/A')}</code>\n"
        f"<b>Banco:</b> {lara.get('banco', 'N/A')}\n"
        f"<b>Valor:</b> R$ {float(lara.get('valor', 0)):.2f}\n\n"
        "Selecione o campo que deseja editar:"
    )
    markup = InlineKeyboardMarkup()
    campos = ["email", "senha_email", "senha_lara", "sexo", "nome", "cpf", "banco", "valor"]
    
    for campo in campos:
        markup.add(InlineKeyboardButton(f"Editar {campo.replace('_', ' ').title()}", callback_data=f"editar_campo_lara {email}|{campo}"))

    markup.add(InlineKeyboardButton("↩️ Voltar", callback_data="gerenciar_laras"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

def solicitar_novo_valor_lara(call, email, campo):
    """Pede ao admin o novo valor para um campo da Lara."""
    prompt = f"Digite o novo valor para <b>{campo.replace('_', ' ')}</b> da Lara <code>{email}</code>:"
    bot.send_message(call.message.chat.id, prompt, parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(call.message, salvar_campo_lara_editado, email, campo)

def salvar_campo_lara_editado(message, email, campo):
    """Salva o valor editado do campo da Lara."""
    novo_valor = message.text.strip()
    
    # Converte para float se o campo for 'valor'
    if campo == 'valor':
        try:
            novo_valor = float(novo_valor.replace(',', '.'))
        except ValueError:
            bot.reply_to(message, "❌ Valor inválido. Por favor, envie apenas números para o campo 'valor'.")
            return

    if api.ControleLaras.editar_campo_lara(email, campo, novo_valor):
        bot.reply_to(message, f"✅ O campo '{campo}' foi atualizado com sucesso!")
        # Idealmente, aqui voltaríamos para o menu de edição, mas como perdemos o 'call',
        # o admin pode voltar manualmente pelo painel.
    else:
        bot.reply_to(message, "❌ Erro: Não foi possível atualizar a Lara.")

# --- Fluxo de Compra de Laras (Cliente) ---
def servicos_laras_menu(message):
    """Exibe a lista de Laras disponíveis para compra."""
    laras = api.ControleLaras.pegar_todas_laras()
    markup = InlineKeyboardMarkup()
    
    texto = "🍊 <b>Laras Disponíveis</b>\n\nSelecione uma das opções abaixo para ver os detalhes e comprar:\n\n"

    if not laras:
        texto += "Não há 'Laras' disponíveis no momento."
        markup.add(InlineKeyboardButton('↩ VOLTAR', callback_data='menu_servicos'))
    else:
        for lara in laras:
            email = lara.get("email")
            banco = lara.get("banco", "N/A")
            valor = float(lara.get("valor", 0))
            markup.add(InlineKeyboardButton(f"🏦 {banco.title()} - R$ {valor:.2f}", callback_data=f"exibir_lara {email}"))
        markup.add(InlineKeyboardButton('↩ VOLTAR', callback_data='menu_servicos'))

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

def exibir_lara_compra(call, email):
    """Exibe os detalhes de uma Lara para confirmação de compra."""
    lara = api.ControleLaras.pegar_lara_por_email(email)
    if not lara:
        bot.answer_callback_query(call.id, "Esta Lara não está mais disponível.", show_alert=True)
        servicos_laras_menu(call.message)
        return

    saldo_usuario = api.InfoUser.saldo(call.from_user.id)
    valor = float(lara.get("valor", 0))

    # Mascarar dados para exibição
    nome_mascarado = lara.get('nome', 'N/A').split(' ')[0]
    cpf_mascarado = f"***.{lara.get('cpf', '***********')[3:6]}.***-**"

    texto = (
        f"<b>⚠️ CONFIRME SUA COMPRA ⚠️</b>\n\n"
        f"<i>Você está prestes a adquirir a seguinte Lara:</i>\n\n"
        f"🏦 <b>Banco:</b> {lara.get('banco', 'N/A').title()}\n"
        f"👤 <b>Nome:</b> <code>{nome_mascarado}</code>\n"
        f"📄 <b>CPF:</b> <code>{cpf_mascarado}</code>\n"
        f"♀️♂️ <b>Sexo:</b> {lara.get('sexo', 'N/A').title()}\n"
        f"- - - - - - - - - - - - - - - - - - -\n\n"
        f"💰 <b>Valor do Produto:</b> R$ {valor:.2f}\n"
        f"💸 <b>Seu Saldo Atual:</b> R$ {saldo_usuario:.2f}\n\n"
        f"<i>Clique em 'Confirmar Compra' para finalizar.</i>"
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('✅ Confirmar Compra', callback_data=f"comprar_lara {email}")],
        [InlineKeyboardButton('↩️ Voltar', callback_data='servicos_laras')]
    ])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

def entregar_lara(call, email):
    """Processa a compra e entrega da Lara."""
    lara = api.ControleLaras.pegar_lara_por_email(email)
    if not lara:
        bot.answer_callback_query(call.id, "Esta Lara não está mais disponível.", show_alert=True)
        return

    valor = float(lara.get("valor", 0))
    if api.InfoUser.saldo(call.from_user.id) < valor:
        bot.answer_callback_query(call.id, "Saldo insuficiente!", show_alert=True)
        return

    api.InfoUser.tirar_saldo(call.from_user.id, valor)
    api.ControleLaras.remover_lara(email)
    api.MudancaHistorico.add_compra_lara(call.from_user.id, lara)

    texto_entrega = f"🥳 <b>COMPRA REALIZADA COM SUCESSO</b> 🥳\n\n<b>Detalhes da sua Lara:</b>\n\n📧 <b>E-mail:</b> <code>{lara.get('email')}</code>\n🔑 <b>Senha E-mail:</b> <code>{lara.get('senha_email')}</code>\n🍊 <b>Senha Lara:</b> <code>{lara.get('senha_lara')}</code>\n🏦 <b>Banco:</b> {lara.get('banco')}\n👤 <b>Nome:</b> {lara.get('nome')}\n📄 <b>CPF:</b> <code>{lara.get('cpf')}</code>\n♀️♂️ <b>Sexo:</b> {lara.get('sexo')}\n\n<b>OBRIGADO PELA PREFERÊNCIA!</b>"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto_entrega, parse_mode='HTML')

# --- Fluxo de Compra de GGs (Cliente) ---
def servicos_ggs_menu(message):
    """Exibe a lista de NÍVEIS de GGs disponíveis para compra."""
    niveis = api.Admin.ControleGGs.pegar_niveis_unicos()
    markup = InlineKeyboardMarkup()

    if not niveis:
        markup.add(InlineKeyboardButton('❌ NÃO HÁ GGs DISPONÍVEIS ❌', callback_data='menu_servicos'))
    else:
        for nivel in niveis:
            markup.add(InlineKeyboardButton(f"⭐ Nível {nivel.upper()}", callback_data=f"ver_gg_do_nivel {nivel}|0"))
    
    markup.add(InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_servicos'))
    texto = api.Textos.menu_comprar_gg()
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def ver_gg_do_nivel(call, nivel, index):
    """Exibe uma GG de um nível específico com base no índice."""
    ggs_do_nivel = api.Admin.ControleGGs.pegar_ggs_por_nivel(nivel)

    if not ggs_do_nivel:
        bot.answer_callback_query(call.id, "Não há mais GGs neste nível.", show_alert=True)
        servicos_ggs_menu(call.message)
        return

    index = int(index) % len(ggs_do_nivel)
    gg_atual = ggs_do_nivel[index]

    numero_gg = gg_atual.get("nome")
    valor = float(gg_atual.get("valor", 0))
    
    saldo_usuario = api.InfoUser.saldo(call.from_user.id)

    # Usa a mesma função de texto da CC, pois a estrutura é idêntica
    texto = api.Textos.confirmacao_compra_cc(
        saldo_usuario=f"{saldo_usuario:.2f}", valor_cc=f"{valor:.2f}", nivel=nivel,
        numero=numero_gg, validade=gg_atual.get("senha"), cvv=gg_atual.get("duracao"),
        nome_titular=gg_atual.get("titular", "N/A"), cpf=gg_atual.get("cpf", "N/A")
    )

    total_ggs = len(ggs_do_nivel)
    proximo_index = (index + 1) % total_ggs
    anterior_index = (index - 1 + total_ggs) % total_ggs

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('✅ Confirmar Compra', callback_data=f'comprar_gg {numero_gg}|{numero_gg}')],
        [InlineKeyboardButton('◀️ Anterior', callback_data=f'ver_gg_do_nivel {nivel}|{anterior_index}'),
         InlineKeyboardButton('▶️ Próxima', callback_data=f'ver_gg_do_nivel {nivel}|{proximo_index}')],
        [InlineKeyboardButton('↩️ Voltar aos Níveis', callback_data='servicos_ggs')]
    ])
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def entregar_produto_generico(call, produto_data, funcao_remover, funcao_historico):
    """Função genérica para processar a compra e entrega de produtos (CC, GG)."""
    if not produto_data:
        bot.answer_callback_query(call.id, "Erro: Produto não encontrado. Pode já ter sido vendido.", show_alert=True)
        return

    valor = float(produto_data['valor'])
    if api.InfoUser.saldo(call.from_user.id) < valor:
        bot.answer_callback_query(call.id, "Saldo insuficiente!", show_alert=True)
        return

    api.InfoUser.tirar_saldo(call.from_user.id, valor)
    # 'nome' é o número/id, 'email' também é o número/id na estrutura original
    funcao_remover(produto_data['nome'], produto_data['email'])
    funcao_historico(call.from_user.id, produto_data)
    
    # Formata a mensagem de entrega para o usuário
    texto_entrega = f"🥳 <b>COMPRA REALIZADA COM SUCESSO</b> 🥳\n\n⚜️ <b>{produto_data['descricao'].upper()}</b> ⚜️\n\n<b>NÚMERO:</b> <code>{produto_data['nome']}</code>\n<b>VALIDADE:</b> <code>{produto_data['senha']}</code>\n<b>CVV:</b> <code>{produto_data['duracao']}</code>\n<b>NOME:</b> <code>{produto_data['titular']}</code>\n<b>CPF:</b> <code>{produto_data['cpf']}</code>\n\n<b>OBRIGADO PELA PREFERÊNCIA!</b>"
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto_entrega, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise


def entregar_gg(call, nome_gg, numero_gg):
    """Processa a compra e entrega da GG."""
    gg_data = api.ControleGGs.entregar_gg(nome_gg, numero_gg)
    # O resto da lógica é idêntica à de entregar_cc, então podemos reutilizar
    entregar_produto_generico(call, gg_data, api.ControleGGs.remover_gg, api.MudancaHistorico.add_compra_gg)

#Menu Geral
def configuracoes_geral(message):
    texto = f'<i>Use os botões abaixo para configurar seu bot:</i>\n📬 DESTINO DAS LOG\'S: {api.CredentialsChange.id_dono()}\n👤 <b>LINK DO SUPORTE ATUAL: {api.CredentialsChange.SuporteInfo.link_suporte()}</b>\n✂️ SEPARADOR: {api.CredentialsChange.separador()}\n<i>separador é o caractér que separa as informações quando você vai alterar algo no bot. Ele é muito importante, então escolha um caractér que você não usa com frequencia para que o bot não fique confuso na hora de separar</i>\n<b>EX DO SEPARADOR EM AÇÃO:</b> NOME{api.CredentialsChange.separador()}VALOR'
    bt = InlineKeyboardButton('🔴 MANUTENÇÃO (off)', callback_data='manutencao')
    if api.CredentialsChange.status_manutencao() == True:
        bt = InlineKeyboardButton('🟢 MANUTENÇÃO (on)', callback_data='manutencao')
    bt2 = InlineKeyboardButton('🎧 MUDAR SUPORTE', callback_data='suporte')
    bt3 = InlineKeyboardButton('✂️ MUDAR SEPARADOR', callback_data='mudar_separador')
    bt4 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, text=texto, message_id=message.message_id, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def trocar_suporte(message, idcall):
    """Atualiza o link de suporte e notifica o admin."""
    api.CredentialsChange.SuporteInfo.mudar_link_suporte(str(message.text))
    bot.answer_callback_query(idcall, text="Suporte alterado com sucesso!", show_alert=True)

def mudar_separador(message, callid):
    """Atualiza o caractere separador e notifica o admin."""
    api.CredentialsChange.mudar_separador(message.text)
    bot.answer_callback_query(callid, "Separador alterado com sucesso!", show_alert=True)

# --- Novo fluxo passo a passo para adicionar Login ---
def iniciar_adicionar_login(message):
    """Inicia o processo de adicionar login, pedindo o nome do serviço."""
    bot.send_message(message.chat.id, "📁 Qual o <b>nome do serviço</b>? (Ex: Netflix, Spotify)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_valor_login)

def pedir_valor_login(message):
    """Pede o valor de venda do login."""
    nome_servico = message.text
    bot.send_message(message.chat.id, "💰 Qual o <b>valor de venda</b> do login?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_descricao_login, nome_servico)

def pedir_descricao_login(message, nome_servico):
    """Pede a descrição do login."""
    try:
        valor_login = float(message.text.replace(',', '.'))
    except ValueError:
        bot.reply_to(message, "❌ Valor inválido. Por favor, envie apenas números. O processo foi cancelado.")
        return
    bot.send_message(message.chat.id, "📝 Qual a <b>descrição</b> do produto? (Ex: Tela Privada, Plano Família)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_email_login, nome_servico, valor_login)

def pedir_email_login(message, nome_servico, valor_login):
    """Pede o email/usuário do login."""
    descricao_login = message.text
    bot.send_message(message.chat.id, "📧 Qual o <b>email ou usuário</b> da conta?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_senha_login, nome_servico, valor_login, descricao_login)

def pedir_senha_login(message, nome_servico, valor_login, descricao_login):
    """Pede a senha do login."""
    email_login = message.text
    bot.send_message(message.chat.id, "🔑 Qual a <b>senha</b> da conta?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_duracao_login, nome_servico, valor_login, descricao_login, email_login)

def pedir_duracao_login(message, nome_servico, valor_login, descricao_login, email_login):
    """Pede a duração ou informação extra."""
    senha_login = message.text
    bot.send_message(message.chat.id, "⏳ Qual a <b>duração ou informação extra</b>? (Ex: 30 dias, site.com)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, finalizar_adicao_login, nome_servico, valor_login, descricao_login, email_login, senha_login)

def finalizar_adicao_login(message, nome_servico, valor_login, descricao_login, email_login, senha_login):
    """Salva o login no banco de dados e informa o admin."""
    duracao_login = message.text
    try:
        api.ControleLogins.add_login(nome=nome_servico, valor=valor_login, descricao=descricao_login, email=email_login, senha=senha_login, duracao=duracao_login)
        bot.reply_to(message, f"✅ <b>Login adicionado com sucesso!</b>\n\n<b>Serviço:</b> {nome_servico}\n<b>Valor:</b> R$ {valor_login:.2f}\n<b>Email:</b> <code>{email_login}</code>", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ocorreu um erro ao adicionar o login: {e}")

def remover_login(message):
    separador = api.CredentialsChange.separador()
    try:
        stri = message.text.strip().split(f'{separador}')
        api.ControleLogins.remover_login(nome=stri[0], email=stri[1])
        bot.reply_to(message, "Removido com sucesso do estoque!")
    except:
        bot.reply_to(message, "Erro ao remover o login.")
def remover_por_plataforma(message):
    plat = message.text
    try:
        api.ControleLogins.remover_por_nome(plat)
        bot.reply_to(message, f"Todos os logins de {plat} foram removidos com sucesso!")
    except:
        bot.reply_to(message, 'Erro ao remover os logins...')
def mudar_valor_servico(message):
    try:
        sep = api.CredentialsChange.separador()
        txt = message.text.strip().split(f'{sep}')
        servico = txt[0]
        valor = txt[1]
        api.ControleLogins.mudar_valor_por_nome(servico, valor)
        bot.reply_to(message, f"O servico {servico} teve seu valor mudado para R${float(valor):.2f}")
    except:
        bot.reply_to(message, 'Falha ao mudar os valores.')
def mudar_valor_todos(message):
    try:
        valor = message.text
        api.ControleLogins.mudar_valor_de_todos(valor)
        bot.reply_to(message, "Valores alterados com sucesso")
    except:
        bot.reply_to(message, "Erro ao alterar valores.")
def configurar_logins(message):
    texto = f'📦 <b>LOGINS NO ESTOQUE: {api.ControleLogins.estoque_total()}</b>\n\n<i>Selecione uma das opções abaixo para gerenciar o estoque de logins.</i>'
    bt = InlineKeyboardButton('📮 ADICIONAR LOGIN', callback_data='adicionar_login')
    bt_gerenciar = InlineKeyboardButton('✏️ EDITAR / REMOVER LOGIN', callback_data='gerenciar_logins_menu')
    bt_voltar = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt_gerenciar], [bt_voltar]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, text=texto, message_id=message.message_id, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

# --- Novo fluxo de Gerenciamento de Logins ---
def gerenciar_logins_menu(call):
    """Exibe a lista de logins disponíveis para gerenciamento."""
    logins = api.ControleLogins.pegar_todos_logins()
    markup = InlineKeyboardMarkup()
    texto = "✏️ <b>Gerenciar Logins</b>\n\nSelecione um para editar ou remover:\n\n"

    if not logins:
        texto += "Não há logins no estoque."
    else:
        for i, login in enumerate(logins):
            nome = login.get("nome")
            email = login.get("email")
            valor = login.get("valor", 0)
            texto_login = f"{nome} - <code>{email}</code> - R${valor:.2f}"
            # Usamos o índice (i) como identificador único para esta sessão
            markup.add(
                InlineKeyboardButton(f"{nome} - R${valor:.2f}", callback_data=f"editar_login_menu {i}"),
                InlineKeyboardButton("❌", callback_data=f"remover_login_especifico {i}")
            )

    markup.add(InlineKeyboardButton('↩ VOLTAR', callback_data='configurar_logins'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

def editar_login_menu(call, login_index):
    """Exibe o menu de edição para um login específico."""
    try:
        login_index = int(login_index)
        login_data = api.ControleLogins.pegar_login_por_indice(login_index)
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Erro: Login não encontrado.", show_alert=True)
        return

    if not login_data:
        bot.answer_callback_query(call.id, "Erro: Login não encontrado.", show_alert=True)
        gerenciar_logins_menu(call)
        return

    texto = (
        f"✏️ <b>Editando Login</b>\n\n"
        f"<b>Serviço:</b> {login_data.get('nome', 'N/A')}\n"
        f"<b>Valor:</b> R$ {float(login_data.get('valor', 0)):.2f}\n"
        f"<b>Descrição:</b> {login_data.get('descricao', 'N/A')}\n"
        f"<b>Email/User:</b> <code>{login_data.get('email', 'N/A')}</code>\n"
        f"<b>Senha:</b> <code>{login_data.get('senha', 'N/A')}</code>\n"
        f"<b>Info Extra:</b> <code>{login_data.get('duracao', 'N/A')}</code>\n\n"
        "Selecione o campo que deseja editar:"
    )

    markup = InlineKeyboardMarkup()
    campos = ['nome', 'valor', 'descricao', 'email', 'senha', 'duracao']
    for campo in campos:
        markup.add(InlineKeyboardButton(f"Editar {campo.title()}", callback_data=f"editar_campo_login {login_index}|{campo}"))
    
    markup.add(InlineKeyboardButton("↩️ Voltar", callback_data="gerenciar_logins_menu"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')

#Menu CCs
def remover_cc(message):
    separador = api.CredentialsChange.separador()
    try:
        stri = message.text.strip().split(f'{separador}')
        api.Admin.ControleCCs.remover_cc(nome=stri[0], email=stri[1])
        bot.reply_to(message, "Removido com sucesso do estoque!")
    except:
        bot.reply_to(message, "Erro ao remover a CC.")
def remover_cc_por_banco(message):
    plat = message.text
    try:
        api.Admin.ControleCCs.remover_por_nome(plat)
        bot.reply_to(message, f"Todas as CCs do banco/bin {plat} foram removidas com sucesso!")
    except:
        bot.reply_to(message, 'Erro ao remover as CCs...')
def mudar_valor_cc(message):
    try:
        sep = api.CredentialsChange.separador()
        txt = message.text.strip().split(f'{sep}')
        servico = txt[0]
        valor = txt[1]
        api.Admin.ControleCCs.mudar_valor_por_nome(servico, valor)
        bot.reply_to(message, f"A CC {servico} teve seu valor mudado para R${float(valor):.2f}")
    except:
        bot.reply_to(message, 'Falha ao mudar os valores.')
def mudar_valor_todas_ccs(message):
    try:
        valor = message.text
        api.Admin.ControleCCs.mudar_valor_de_todos(valor)
        bot.reply_to(message, "Valores alterados com sucesso")
    except:
        bot.reply_to(message, "Erro ao alterar valores.")
def configurar_ccs(call):
    texto = f"""💳 <b>Gerenciamento de CC's</b>\n\n<b>Estoque atual:</b> {api.Admin.ControleCCs.estoque_total()} unidades.\n\n<i>Selecione uma das opções abaixo para gerenciar o estoque.</i>"""
    bt = InlineKeyboardButton("📮 ADICIONAR CC'S", callback_data='adicionar_cc')
    bt2 = InlineKeyboardButton("✏️ EDITAR / REMOVER CC", callback_data='gerenciar_ccs_por_nivel')
    bt3 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3]])
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def gerenciar_ccs_por_nivel(call):
    """Exibe os níveis de CCs disponíveis para gerenciamento."""
    niveis = api.Admin.ControleCCs.pegar_niveis_unicos()
    markup = InlineKeyboardMarkup()

    if not niveis:
        bot.answer_callback_query(call.id, "Nenhum nível de CC encontrado no estoque.", show_alert=True)
        return

    for nivel in niveis:
        markup.add(InlineKeyboardButton(f"Nível: {nivel.upper()}", callback_data=f"listar_ccs_do_nivel {nivel}"))
    
    markup.add(InlineKeyboardButton("↩️ Voltar", callback_data="configurar_ccs"))
    texto = "🗂️ Selecione um <b>nível</b> para ver ou remover os cartões:"
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def listar_ccs_do_nivel(call, nivel):
    """Lista todos os CCs de um nível específico com opções de remoção."""
    ccs_do_nivel = api.Admin.ControleCCs.pegar_ccs_por_nivel(nivel)
    markup = InlineKeyboardMarkup()
    
    texto = f"💳 <b>Cartões do Nível: {nivel.upper()}</b>\n\n"

    if not ccs_do_nivel:
        texto += "Não há cartões neste nível."
    else:
        for cc in ccs_do_nivel:
            numero = cc.get("nome")
            # O 'email' também é o número do cartão na sua estrutura
            email_id = cc.get("email") 
            texto_cc = f"<code>{numero[:6]}...{numero[-4:]}</code> - R${cc.get('valor'):.2f}"
            markup.add(InlineKeyboardButton(texto_cc, callback_data="noop"), InlineKeyboardButton("✏️", callback_data=f"editar_cc_menu {numero}|{email_id}"), InlineKeyboardButton("❌", callback_data=f"remover_cc_especifico {numero}|{email_id}"))

    markup.add(InlineKeyboardButton(f"🗑️ Remover TODOS de {nivel.upper()}", callback_data=f"confirmar_remover_nivel {nivel}"))
    markup.add(InlineKeyboardButton("↩️ Voltar aos Níveis", callback_data="gerenciar_ccs_por_nivel"))

    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def confirmar_remover_nivel(call, nivel):
    """Pede confirmação para remover todos os CCs de um nível."""
    texto = f"⚠️ <b>ATENÇÃO</b> ⚠️\n\nVocê tem certeza que deseja remover <b>TODOS</b> os cartões do nível <b>{nivel.upper()}</b>?\n\nEsta ação não pode ser desfeita."
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"✅ Sim, remover todos", callback_data=f"remover_nivel_confirmado {nivel}")],
        [InlineKeyboardButton("❌ Não, cancelar", callback_data=f"listar_ccs_do_nivel {nivel}")]
    ])
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def remover_nivel_confirmado(call, nivel):
    """Remove todos os CCs de um nível e atualiza a visualização."""
    if api.Admin.ControleCCs.remover_por_nivel(nivel):
        bot.answer_callback_query(call.id, f"Todos os cartões do nível '{nivel.upper()}' foram removidos.", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Erro ao remover os cartões ou nenhum cartão encontrado.", show_alert=True)
    
    # Volta para a lista de níveis
    gerenciar_ccs_por_nivel(call)

def editar_cc_menu(call, cc_identifier):
    """Exibe o menu de edição para um CC específico."""
    try:
        numero, email = cc_identifier.split('|')
    except ValueError:
        bot.answer_callback_query(call.id, "Erro: Identificador de CC inválido.", show_alert=True)
        return

    cc_data = api.ControleCCs.entregar_cc(numero, email)
    if not cc_data:
        bot.answer_callback_query(call.id, "Erro: Cartão não encontrado.", show_alert=True)
        return

    texto = (
        f"✏️ <b>Editando Cartão</b>\n\n"
        f"<b>Número:</b> <code>{cc_data.get('nome', 'N/A')}</code>\n"
        f"<b>Nível:</b> {cc_data.get('descricao', 'N/A')}\n"
        f"<b>Valor:</b> R$ {float(cc_data.get('valor', 0)):.2f}\n"
        f"<b>Validade:</b> <code>{cc_data.get('senha', 'N/A')}</code>\n"
        f"<b>CVV:</b> <code>{cc_data.get('duracao', 'N/A')}</code>\n"
        f"<b>Titular:</b> {cc_data.get('titular', 'N/A')}\n"
        f"<b>CPF:</b> <code>{cc_data.get('cpf', 'N/A')}</code>\n\n"
        "Selecione o campo que deseja editar:"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💰 Editar Valor", callback_data=f"editar_campo_cc valor|{numero}"))
    markup.add(InlineKeyboardButton("⭐ Editar Nível", callback_data=f"editar_campo_cc nivel|{numero}"))
    markup.add(InlineKeyboardButton("👤 Editar Titular", callback_data=f"editar_campo_cc titular|{numero}"))
    markup.add(InlineKeyboardButton("📄 Editar CPF", callback_data=f"editar_campo_cc cpf|{numero}"))
    markup.add(InlineKeyboardButton("↩️ Voltar", callback_data=f"listar_ccs_do_nivel {cc_data.get('descricao')}"))

    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def solicitar_novo_valor_campo(call, campo, numero_cc):
    """Pede ao admin o novo valor para um campo específico."""
    mapa_campos = {
        'valor': 'o novo valor',
        'nivel': 'o novo nível',
        'titular': 'o novo nome do titular',
        'cpf': 'o novo CPF'
    }
    prompt = f"Digite {mapa_campos.get(campo, 'o novo valor')} para o cartão <code>{numero_cc}</code>:"
    bot.send_message(call.message.chat.id, prompt, parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(call.message, salvar_campo_editado, campo, numero_cc)

def salvar_campo_editado(message, campo, numero_cc):
    """Salva o valor editado do campo no banco de dados."""
    novo_valor = message.text.strip()
    sucesso = False
    
    try:
        if campo == 'valor':
            sucesso = api.Admin.ControleCCs.mudar_valor_cc(numero_cc, novo_valor)
        elif campo == 'nivel':
            sucesso = api.Admin.ControleCCs.mudar_nivel_cc(numero_cc, novo_valor)
        elif campo == 'titular':
            sucesso = api.Admin.ControleCCs.mudar_titular_cc(numero_cc, novo_valor)
        elif campo == 'cpf':
            sucesso = api.Admin.ControleCCs.mudar_cpf_cc(numero_cc, novo_valor)

        if sucesso:
            bot.reply_to(message, f"✅ O campo '{campo}' foi atualizado com sucesso!")
            # Para voltar ao menu de edição, precisamos do call object.
            # Como não o temos aqui, podemos instruir o usuário a voltar manualmente ou
            # simplesmente confirmar a ação. Por simplicidade, vamos apenas confirmar.
            # Para uma melhor UX, seria necessário reestruturar para passar o 'call' ou 'message_id'.
        else:
            bot.reply_to(message, "❌ Erro: Não foi possível atualizar o cartão.")

    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao processar a alteração: {e}")

# --- Novo fluxo passo a passo para adicionar CC ---
def iniciar_adicionar_cc(message):
    """Inicia o processo de adicionar CC, pedindo o número do cartão."""
    bot.send_message(message.chat.id, "💳 Qual o <b>número</b> do cartão?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_nivel_cc)

def pedir_nivel_cc(message):
    """Pede o nível do cartão."""
    numero_cc = message.text
    bot.send_message(message.chat.id, "⭐ Qual o <b>nível</b> do cartão? (Ex: infinity, black, platinum)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_valor_cc, numero_cc)

def pedir_valor_cc(message, numero_cc):
    """Pede o valor do cartão."""
    nivel_cc = message.text
    bot.send_message(message.chat.id, "💰 Qual o <b>valor</b> de venda do cartão?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_validade_cc, numero_cc, nivel_cc)

def pedir_validade_cc(message, numero_cc, nivel_cc):
    """Pede a data de validade do cartão."""
    try:
        valor_cc = float(message.text.replace(',', '.'))
    except ValueError:
        bot.reply_to(message, "❌ Valor inválido. Por favor, envie apenas números. O processo foi cancelado.")
        return
    
    bot.send_message(message.chat.id, "📅 Qual a <b>data de validade</b>? (Ex: 02/28)", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cvv_cc, numero_cc, nivel_cc, valor_cc)

def pedir_cvv_cc(message, numero_cc, nivel_cc, valor_cc):
    """Pede o CVV e finaliza a adição."""
    validade_cc = message.text
    bot.send_message(message.chat.id, "👤 Qual o <b>nome completo</b> do titular do cartão?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cpf_titular_cc, numero_cc, nivel_cc, valor_cc, validade_cc)

def pedir_cpf_titular_cc(message, numero_cc, nivel_cc, valor_cc, validade_cc):
    """Pede o CPF do titular."""
    nome_titular = message.text
    bot.send_message(message.chat.id, "📄 Qual o <b>CPF</b> do titular do cartão?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, pedir_cvv_final_cc, numero_cc, nivel_cc, valor_cc, validade_cc, nome_titular)

def pedir_cvv_final_cc(message, numero_cc, nivel_cc, valor_cc, validade_cc, nome_titular):
    """Pede o CVV e chama a função final."""
    cpf_titular = message.text
    bot.send_message(message.chat.id, "🔒 Qual o <b>CVV</b> do cartão?", parse_mode='HTML', reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, finalizar_adicao_cc, numero_cc, nivel_cc, valor_cc, validade_cc, nome_titular, cpf_titular)

def finalizar_adicao_cc(message, numero_cc, nivel_cc, valor_cc, validade_cc, nome_titular, cpf_titular):
    """Adiciona o CC ao banco de dados e informa o admin."""
    cvv_cc = message.text
    try:
        # No seu sistema, o 'nome' e 'email' do CC são o número do cartão.
        # 'senha' é a validade e 'duracao' é o CVV.
        api.Admin.ControleCCs.add_cc(nome=numero_cc, valor=valor_cc, descricao=nivel_cc, email=numero_cc, senha=validade_cc, duracao=cvv_cc, titular=nome_titular, cpf=cpf_titular)
        bot.reply_to(message, f"✅ <b>Cartão adicionado com sucesso!</b>\n\n<b>Número:</b> <code>{numero_cc}</code>\n<b>Nível:</b> {nivel_cc}\n<b>Valor:</b> R$ {valor_cc:.2f}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Ocorreu um erro ao adicionar o cartão: {e}")

#Menu admin
def configurar_admins(message):
    texto = f'🅰️ <b>PAINEL CONFIGURAR ADMIN</b>\n\n👮 Administradores: {api.Admin.quantidade_admin()}\n<i>Use os botões abaixo para fazer as alterações necessárias</i>'
    bt = InlineKeyboardButton('➕ ADICIONAR ADM', callback_data='adicionar_adm')
    bt2 = InlineKeyboardButton('🚮 REMOVER ADM', callback_data='remover_adm')
    bt3 = InlineKeyboardButton('📃 LISTA DE ADM', callback_data='lista_adm')
    bt4 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    bot.edit_message_text(chat_id=message.chat.id, text=texto, message_id=message.message_id, parse_mode='HTML', reply_markup=markup)
def adicionar_adm(message):
    try:
        id_admin = message.text
        api.Admin.add_admin(id_admin)
        bot.reply_to(message, f"O usuario: {id_admin} foi feito admin!")
    except:
        bot.reply_to(message, "Erro ao promover para adm.")
def remover_adm(message):
    try:
        id = message.text
        api.Admin.remover_admin(id)
        bot.reply_to(message, f"Adm {id} foi feito um usuario comum novamente.")
    except:
        bot.reply_to(message, "Falha ao remover o adm.")
#Menu afiliados
def configurar_afiliados(message):
    texto = f'🔻 <b>PONTOS MINIMO PRA SALDO: {api.AfiliadosInfo.minimo_pontos_pra_saldo()}</b>✖️\n<b>MULTIPLICADOR: {api.AfiliadosInfo.multiplicador_pontos()}</b>\n\n\n◎ ══════ ❈ ══════ ◎\n👥 <b>SISTEMA DE INDICAÇÃO</b>\n◎ ══════ ❈ ══════ ◎\nAo clicar, altera o status do sistema de indicação. Se estiver OFF os usuários não poderão trocar seus pontos por saldo.\nVERDE = On\nVERMELHO = Off\n┕━━━━╗✹╔━━━━┙\n\n\n◎ ══════ ❈ ══════ ◎\n🗞 <b>PONTOS POR RECARGA</b>\n◎ ══════ ❈ ══════ ◎\nEssa é a quantidade de pontos que o usuário ganha cada vez que o seu afiliado fizer uma recarga.\n┕━━━━╗✹╔━━━━┙\n\n\n◎ ══════ ❈ ══════ ◎\n🔻 <b>PONTOS MINIMO PARA CONVERTER</b>\n◎ ══════ ❈ ══════ ◎\nIsso é a quantidade mínima de pontos que o usuário precisa para converter seus pontos em saldo.\n┕━━━━╗✹╔━━━━┙\n\n\n◎ ══════ ❈ ══════ ◎\n✖️ <b>MULTIPLICADOR PARA CONVERTER</b>\n◎ ══════ ❈ ══════ ◎\nIsso é o multiplicador de pontos para saldo na hora de converter.\n<b>EX:</b> <i>Se o multiplicador for 0.01 e o usuário tiver 500 pontos, quando ele converter ele ficará com 5,00 de saldo.\nSe o multiplicador for 0.50 e o usuario tiver com 20 pontos, quando ele converter ele ficará com 10,00 de saldo.</i>\n┕━━━━╗✹╔━━━━┙'
    bt = InlineKeyboardButton('🔴 SISTEMA DE INDICAÇÃO(off)', callback_data='mudar_status_afiliados')
    if api.AfiliadosInfo.status_afiliado() == True:
        bt = InlineKeyboardButton('🟢 SISTEMA DE INDICAÇÃO(off)', callback_data='mudar_status_afiliados')
    bt2 = InlineKeyboardButton('🗞 PONTOS POR RECARGA', callback_data='pontos_por_recarga')
    bt3 = InlineKeyboardButton('🔻 PONTOS MINIMO PARA CONVERTER', callback_data='pontos_minimo_converter')
    bt4 = InlineKeyboardButton('✖️ MULTIPLICADOR PARA CONVERTER', callback_data='multiplicador_para_converter')
    bt5 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4], [bt5]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def pontos_por_recarga(message):
    try:
        pontos = message.text
        api.AfiliadosInfo.mudar_pontos_por_recarga(pontos)
        bot.reply_to(message, f"Alterado com sucesso! Agora toda vez que um usuário recarregar, quem indicou ele ganhará {pontos} pontos.")
    except:
        bot.reply_to(message, "Falha ao alterar a quantidade de pontos, verifique se enviou um número aceitavel.")
def pontos_minimo_converter(message):
    try:
        min = message.text
        api.AfiliadosInfo.trocar_minimo_pontos_pra_saldo(min)
        bot.reply_to(message, f"Feito! Agora os usuarios precisam ter {min} pontos para poder converter em saldo.")
    except:
        bot.reply_to(message, f"Erro ao alterar a quantidade de pontos, verifique se enviou um número aceitavel.")
def multiplicador_para_converter(message):
    try:
        mult = message.text
        api.AfiliadosInfo.trocar_multiplicador_pontos(mult)
        bot.reply_to(message, "Multiplicador alterado com sucesso!")
    except:
        bot.reply_to(message, "Falha ao alterar o multiplicador, verifique se enviou um número aceitavel.")
#Menu usuarios
def configurar_usuarios(message):
    texto = f'◎ ══════ ❈ ══════ ◎\n📪 <b>TRANSMITIR A TODOS</b>\n◎ ══════ ❈ ══════ ◎\nEnvia uma mensagem para todos os usuários registrados no bot. 📬✉️\nApós clicar, envie o texto que quer transmitir ou a foto. Para enviar uma foto com texto, basta colocar o texto na legenda da imagem. 📷🖋️\n┕━━━━╗✹╔━━━━┙\n\n\n◎ ══════ ❈ ══════ ◎\n🔎 <b>PESQUISAR USUÁRIO</b>\n◎ ══════ ❈ ══════ ◎\nSe este usuário estiver registrado no bot, vai abrir as configurações de edição desse usuário. 💼🔧\nVocê poderá editar o saldo, ver o histórico de compras, e todas as informações dele. 📈📋\n┕━━━━╗✹╔━━━━┙'
    bt = InlineKeyboardButton('📫 TRANSMITIR A TODOS', callback_data='transmitir_todos')
    bt2 = InlineKeyboardButton('🔎 PESQUISAR USUARIO', callback_data='pesquisar_usuario')
    bt3 = InlineKeyboardButton('🗑 ZERAR VENDAS', callback_data='zerar_vendas')
    bt4 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    try:
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
        except telebot.apihelper.ApiTelegramException as e:
            if 'message is not modified' not in e.description:
                raise
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def transmitir_todos(message):
    api.FuncaoTransmitir.zerar_infos()
    bt = InlineKeyboardButton('➕ ADD BOTAO ➕', callback_data='add_botao')
    bt2 = InlineKeyboardButton('✅ CONFIRMAR ENVIO', callback_data='confirmar_envio')
    markup = InlineKeyboardMarkup([[bt], [bt2]])
    if message.content_type == 'photo':
        photo = message.photo[0].file_id
        api.FuncaoTransmitir.adicionar_foto(photo)
        api.FuncaoTransmitir.adicionar_texto(message.caption)
        api.FuncaoTransmitir.adicionar_entitie(message.caption_entities)
        bot.send_photo(message.chat.id, photo=photo, caption=message.caption, caption_entities=message.entities, reply_markup=markup)
    elif message.content_type == 'text':
        api.FuncaoTransmitir.adicionar_texto(message.text)
        api.FuncaoTransmitir.adicionar_entitie(message.entities)
        bot.send_message(message.chat.id, text=message.text, entities=message.entities, reply_markup=markup)
    else:
        bot.reply_to(message, "Este tipo de mensagem ainda não está disponível para transmitir.")
def add_botao(message):
    try:
        text = message.text
        s = text.split('\n')
        markup = InlineKeyboardMarkup()
        for elemento in s:
            botoes = []
            separar = elemento.split('&&')
            for botao in separar:
                sep = botao.split('-')
                nome = sep[0].strip()
                url = sep[1].strip()
                botoes.append(InlineKeyboardButton(f'{nome}', url=f'{url}'))
            markup.row(*botoes)
        api.FuncaoTransmitir.adicionar_markup(markup)
        bt2 = InlineKeyboardButton('✅ CONFIRMAR ENVIO', callback_data='confirmar_envio')
        markup.row(bt2)
        if markup != None:
            texto = api.FuncaoTransmitir.pegar_texto()
            photo = api.FuncaoTransmitir.pegar_foto()
            entities = api.FuncaoTransmitir.pegar_entities()
            telebot_entities = []
            for entity in entities:
                telebot_entity = telebot.types.MessageEntity(
                    type=entity['type'],
                    offset=entity['offset'],
                    length=entity['length'],
                    url=entity['url'],
                    user=entity['user'],
                    language=entity['language'],
                    custom_emoji_id=entity['custom_emoji_id']
                )
                telebot_entities.append(telebot_entity)
            if texto != None and photo == None:
                bot.send_message(message.chat.id, texto, entities=telebot_entities, reply_markup=markup)
            elif photo != None and texto == None:
                bot.send_photo(message.chat.id, photo, caption_entities=telebot_entities, reply_markup=markup)
            elif photo != None and texto != None:
                bot.send_photo(message.chat.id, photo, caption=texto, caption_entities=telebot_entities, reply_markup=markup)
            else:
                bot.reply_to(message, "Error!")
    except Exception as e:
        bot.reply_to(message, "Ocorreu um erro ao processar, verifique se enviou o nome e a URL no formato correto.")
        print(e)
def disparar_transmissao(tipo, texto, photo, entities):
    markup1 = api.FuncaoTransmitir.pegar_markup()
    markup =InlineKeyboardMarkup()
    for b in markup1:
        botoes = []
        for item in b:
            botoes.append(InlineKeyboardButton(f'{item["text"]}', url=f'{item["url"]}'))
        markup.row(*botoes)
    print(markup)
    with open('database/users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for user in data.get("users", []):
        try:
            if tipo == 1:
                bot.send_message(user["id"], texto, entities=entities)
            elif tipo == 2:
                bot.send_message(user["id"], texto, entities=entities, reply_markup=markup)
            elif tipo == 3:
                bot.send_photo(user["id"], photo, caption=texto, caption_entities=entities)
            elif tipo == 4:
                bot.send_photo(user["id"], photo, caption=texto, caption_entities=entities, reply_markup=markup)
            elif tipo == 5:
                bot.send_photo(user["id"], photo, caption=texto, caption_entities=entities, reply_markup=markup)
        except Exception as e:
            print(f"Erro ao enviar mensagem para o usuário {user['id']}: {str(e)}")

    bot.send_message(api.CredentialsChange.id_dono(), "Transmissão finalizada!")
def confirmar_envio(message):
    entities_prim = api.FuncaoTransmitir.pegar_entities()
    entities = []
    markup = InlineKeyboardMarkup(api.FuncaoTransmitir.pegar_markup())
    for entity in entities_prim:
        telebot_entity = telebot.types.MessageEntity(
            type=entity['type'],
            offset=entity['offset'],
            length=entity['length'],
            url=entity['url'],
            user=entity['user'],
            language=entity['language'],
            custom_emoji_id=entity['custom_emoji_id']
        )
        entities.append(telebot_entity)
    print(entities)
    texto = api.FuncaoTransmitir.pegar_texto()
    photo = api.FuncaoTransmitir.pegar_foto()

    if texto != None and photo == None:
        if markup != None:
            disparar_transmissao(2, texto, photo, entities)
        else:
            disparar_transmissao(1, texto, photo, entities)
    elif photo != None and texto == None:
        if markup != None:
            disparar_transmissao(4, texto, photo, entities)
        else:
            disparar_transmissao(3, texto, photo, entities)
    elif photo != None and texto != None:
        if markup != None:
            disparar_transmissao(5, texto, photo, entities)
    else:
        bot.reply_to(message, "Error!")
def pesquisar_usuario(message):
    id = message.text
    if api.InfoUser.verificar_usuario(id) == True:
        texto = f'🔎 <b>USUÁRIO ENCONTRADO</b> ✅\n\n🕵️ <b>INFORMAÇÕES</b> 🕵️\n📛 <b>ID:</b> <code>{id}</code>\n💰 <b>SALDO:</b> <code>{api.InfoUser.saldo(id):.2f}</code>\n🛒 <b>ACESSOS COMPRADOS:</b> <code>{api.InfoUser.total_compras(id)}</code>\n💠 <b>PIX INSERIDOS:</b> <code>R${api.InfoUser.pix_inseridos(id):.2f}</code>\n👥 <b>INDICADOS:</b> <code>{api.InfoUser.quantidade_afiliados(id)}</code>\n🎁 <b>GIFT RESGATADO:</b> <code>R${api.InfoUser.gifts_resgatados(id):.2f}</code>'
        bt = InlineKeyboardButton('🧑‍⚖️ Banir', callback_data=f'banir {id}')
        bt2 = InlineKeyboardButton('💰 MUDAR SALDO', callback_data=f'mudar_saldo {id}')
        bt3 = InlineKeyboardButton('📥 BAIXAR HISTORICO', callback_data=f'baixar_historico {id}')
        markup = InlineKeyboardMarkup([[bt], [bt2], [bt3]])
        if api.InfoUser.verificar_ban(id) == True:
            bt = InlineKeyboardButton('🧑‍⚖️ DESBANIR', callback_data=f'banir {id}')
            markup = InlineKeyboardMarkup([[bt]])
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
    else:
        bot.reply_to(message, "Usuario não foi encontrado.")
def mudar_saldo(message, id):
    saldo = message.text
    try:
        api.InfoUser.mudar_saldo(id, saldo)
        bot.reply_to(message, "Saldo alterado com sucesso!")
    except:
        bot.reply_to(message, "Falha ao alterar, verifique se enviou um valor valido.")
#Menu Pix
def configurar_pix(message):
    texto = (
        f'🔑 <b>TOKEN MERCADO PAGO:</b> <code>{api.CredentialsChange.InfoPix.token_mp()}</code>\n'
        f'🔑 <b>CHAVE PIX MANUAL:</b> <code>{api.CredentialsChange.InfoPix.chave_pix_manual()}</code>\n'
        f'🔻 <b>DEPÓSITO MÍNIMO:</b> <code>R${api.CredentialsChange.InfoPix.deposito_minimo_pix():.2f}</code>\n'
        f'❗️ <b>DEPÓSITO MÁXIMO:</b> <code>R${api.CredentialsChange.InfoPix.deposito_maximo_pix():.2f}</code>\n'
        f'🔶 <b>BÔNUS DE DEPÓSITO:</b> <code>{api.CredentialsChange.BonusPix.quantidade_bonus()}%</code>\n'
        f'🔷 <b>DEPÓSITO MÍNIMO PARA GANHAR O BÔNUS:</b> R${api.CredentialsChange.BonusPix.valor_minimo_para_bonus():.2f}'
    )
    bt = InlineKeyboardButton('🔴 PIX MANUAL', callback_data='trocar_pix_manual')
    bt2 = InlineKeyboardButton('🔴 PIX AUTOMATICO', callback_data='trocar_pix_automatico')
    if api.CredentialsChange.StatusPix.pix_manual() == True:
        bt = InlineKeyboardButton('🟢 PIX MANUAL', callback_data='trocar_pix_manual')
    if api.CredentialsChange.StatusPix.pix_auto() == True:
        bt2 = InlineKeyboardButton('🟢 PIX AUTOMATICO', callback_data='trocar_pix_automatico')
    bt3 = InlineKeyboardButton('🔑 MUDAR TOKEN MP', callback_data='mudar_token')
    bt_chave_manual = InlineKeyboardButton('🔑 MUDAR CHAVE PIX MANUAL', callback_data='mudar_chave_pix_manual')
    bt4 = InlineKeyboardButton('🔻 MUDAR DEPOSITO MIN', callback_data='mudar_deposito_minimo')
    bt5 = InlineKeyboardButton('❗️ MUDAR DEPOSITO MAX', callback_data='mudar_deposito_maximo')
    bt6 = InlineKeyboardButton('🔶 MUDAR BONUS', callback_data='mudar_bonus')
    bt7 = InlineKeyboardButton('🔷 MUDAR MIN PARA BONUS', callback_data='mudar_min_bonus')
    bt8 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt, bt2], [bt3], [bt_chave_manual], [bt4], [bt5], [bt6], [bt7], [bt8]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def mudar_token(message):
    try:
        token = message.text
        api.CredentialsChange.InfoPix.mudar_tokenmp(token)
        bot.reply_to(message, "Alterado com sucesso")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_chave_pix_manual(message):
    try:
        chave = message.text
        api.CredentialsChange.InfoPix.mudar_chave_pix_manual(chave)
        bot.reply_to(message, "Chave PIX manual alterada com sucesso!")
    except Exception as e:
        bot.reply_to(message, f"Falha ao alterar a chave: {e}")
def mudar_deposito_minimo(message):
    try:
        min = message.text
        api.CredentialsChange.InfoPix.trocar_deposito_minimo_pix(min)
        bot.reply_to(message, "Alterado com sucesso!")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_deposito_maximo(message):
    try:
        max = message.text
        api.CredentialsChange.InfoPix.trocar_deposito_maximo_pix(max)
        bot.reply_to(message, "Alterado com sucesso")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_expiracao(message):
    if message.text.isdigit() == True:
        expiracao = int(message.text)
        if expiracao < 15:
            bot.reply_to(message, "O tempo de expiracao deve ser maior do que 15 minutos!")
            return
        api.CredentialsChange.InfoPix.mudar_expiracao(expiracao)
        bot.reply_to(message, "Alterado com sucesso!")
    else:
        bot.reply_to(message, "Envie apenas digitos!")
def mudar_bonus(message):
    try:
        p = message.text
        p = p.replace('%', '')
        p = p.strip()
        api.CredentialsChange.BonusPix.mudar_quantidade_bonus(p)
        bot.reply_to(message, "Alterado com sucesso!")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_min_bonus(message):
    try:
        min = message.text
        api.CredentialsChange.BonusPix.mudar_valor_minimo_para_bonus(min)
        bot.reply_to(message, "Alterado com sucesso")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
# Menu notificações
def configurar_notificacoes(message):
    quantidade_servico = api.Notificacoes.quantidade_de_servicos_pra_sortear()
    texto = f'🎯 <b>GRUPO ALVO:</b> {api.Notificacoes.id_grupo()}\n\n\n🛎 <b>NOTIFICAÇÕES FAKES CONFIGURAÇÕES</b> ⚙️\n\n💰 <b>NOTIFICAÇÃO DE RECARGA:</b>\n⌛️ <b>Tempo de espera:</b> selecionando entre {api.Notificacoes.tempo_minimo_saldo()} e {api.Notificacoes.tempo_maximo_saldo()} segundos\n📦 <b>Selecionando aleatoriamente entre: R${api.Notificacoes.min_max_saldo()[0]:.2f} e R${api.Notificacoes.min_max_saldo()[1]:.2f} de saldo.</b>\n\n\n🛒 <b>NOTIFICAÇÕES DE COMPRA:</b>\n📔 <b>Quantidade de serviços para selecionar:</b> {quantidade_servico}\n⌛️ <b>Tempo de espera:</b> selecionando entre {api.Notificacoes.tempo_minimo_compras()} e {api.Notificacoes.tempo_maximo_compras()} segundos'
    bt = InlineKeyboardButton('🔴 NOTIFICACOES', callback_data='status_notificacoes')
    if api.Notificacoes.status_notificacoes() == True:
        bt = InlineKeyboardButton('🟢 NOTIFICACOES', callback_data='status_notificacoes')
    bt2 = InlineKeyboardButton('🎯 MUDAR GP ALVO', callback_data='mudar_grupo_alvo')
    bt3 = InlineKeyboardButton('⌛️ TEMPO MIN SALDO', callback_data='tempo_min_saldo')
    bt4 = InlineKeyboardButton('⌛️ TEMPO MAX SALDO', callback_data='tempo_max_saldo')
    bt5 = InlineKeyboardButton('📃 TROCAR TEXTO', callback_data='trocar_texto_saldo')
    bt6 = InlineKeyboardButton('💰 TROCAR MIN MAX SALDO', callback_data='trocar_min_max_saldo')
    bt7 = InlineKeyboardButton('━━━━━━━━━━━━━━━━━━', callback_data='poooo')
    bt8 = InlineKeyboardButton('⌛️ TEMPO MIN COMPRAS', callback_data='tempo_min_compra')
    bt9 = InlineKeyboardButton('⌛️ TEMPO MAX COMPRAS', callback_data='tempo_max_compra')
    bt10 = InlineKeyboardButton('📃 TROCAR TEXTO', callback_data='trocar_texto_compra')
    bt11 = InlineKeyboardButton('🔖 TROCAR SERVICOS', callback_data='trocar_servicos')
    bt12 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4], [bt5], [bt6], [bt7], [bt8],[bt9], [bt10], [bt11], [bt12]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def tempo_min_saldo(message):
    min = message.text
    api.Notificacoes.trocar_tempo_minimo_saldo(min)
    bot.reply_to(message, "Alterado com sucesso!")
def tempo_max_saldo(message):
    max = message.text
    api.Notificacoes.trocar_tempo_maximo_saldo(max)
    bot.reply_to(message, "Alterado com sucesso!")
def tempo_min_compra(message):
    min = message.text
    api.Notificacoes.trocar_tempo_minimo_compras(min)
    bot.reply_to(message, "Alterado com sucesso!")
def tempo_max_compra(message):
    max = message.text
    api.Notificacoes.trocar_tempo_maximo_compras(max)
    bot.reply_to(message, "Alterado com sucesso!")
def mudar_grupo_alvo(message):
    gp = message.text
    api.Notificacoes.trocar_id_grupo(gp)
    bot.reply_to(message, "Alterado com sucesso.")
def trocar_texto_saldo(message):
    txt = message.text
    api.Notificacoes.mudar_texto_saldo(txt)
    bot.reply_to(message, "Alterado com sucesso!")
def trocar_min_max_saldo(message):
    separador = api.CredentialsChange.separador()
    separar = message.text.strip().split(f'{separador}')
    min = separar[0].strip()
    max = separar[1].strip()
    api.Notificacoes.trocar_min_max_saldo(min, max)
    bot.reply_to(message, "Alterado com sucesso!")
def trocar_texto_compra(message):
    api.Notificacoes.mudar_texto_compra(message.text)
    bot.reply_to(message, "Alterado com sucesso!")
def trocar_servicos(message):
    lista = message.text
    api.Notificacoes.mudar_servicos_random(lista)
    bot.reply_to(message, "Alterado com sucesso")
def enviar_notificacao_saldo():
    while True:
        time.sleep(60)
        if api.Notificacoes.status_notificacoes() == True:
            minimo = int(api.Notificacoes.tempo_minimo_saldo())
            maximo = int(api.Notificacoes.tempo_maximo_saldo())
            texto = api.Notificacoes.texto_notificacao_saldo()
            gp = int(api.Notificacoes.id_grupo())
            try:
                bot.send_message(chat_id=gp, text=texto, parse_mode='HTML')
            except Exception as e:
                print(e)
                pass
            delay = random.randint(minimo, maximo)
            time.sleep(delay)
        else:
            time.sleep(200)
def enviar_notificacao_compra():
    while True:
        time.sleep(300)
        if api.Notificacoes.status_notificacoes() == True:
            minimo = int(api.Notificacoes.tempo_minimo_compras())
            maximo = int(api.Notificacoes.tempo_maximo_compras())
            texto = api.Notificacoes.texto_notificacao_compra()
            gp = int(api.Notificacoes.id_grupo())
            try:
                bot.send_message(chat_id=gp, text=texto, parse_mode='HTML')
            except Exception as e:
                print(e)
                pass
            delay = random.randint(minimo, maximo)
            time.sleep(delay)
        else:
            time.sleep(700)
#Menu gift card
def gift_card(message):
    bt = InlineKeyboardButton('🎁 GERAR GIFT CARD', switch_inline_query_current_chat='CREATEGIFT 1')
    bt2 = InlineKeyboardButton('🎁 GERAR VARIOS GIFT 🎁', switch_inline_query_current_chat='CREATEGIFT 1 10')
    bt4 = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt4]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='<i>Selecione a opção desejada:</i>', parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
@bot.inline_handler(lambda query: query.query.startswith('CREATEGIFT '))
def create_gift_card(inline_query):
    print(inline_query)
    if api.Admin.verificar_admin(inline_query.from_user.id) == False and int(api.CredentialsChange.id_dono()) != int(inline_query.from_user.id):
        return
    if len(inline_query.query.split()) == 2:
        value = inline_query.query.split(' ')[1]
        valor, codigo = gerar_gift_card(value)
        txt = api.Textos.giftcard(codigo=codigo, quantidade=1, valor=valor)
        title = f"Criar gift card de {value}"
        description = f"Clique aqui para criar um gift card de {value}."
        reply_markup = telebot.types.InlineKeyboardMarkup()
        button_text = "📝 Resgatar agora"
        button = telebot.types.InlineKeyboardButton(button_text, callback_data=f'resgatar {codigo}')
        reply_markup.add(button)
        result_id = '1'
        result = telebot.types.InlineQueryResultArticle(
            id=result_id, title=title, description=description, 
            input_message_content=telebot.types.InputTextMessageContent(txt, parse_mode='HTML'), 
            reply_markup=reply_markup, 
            thumbnail_url='https://cdn-icons-png.flaticon.com/512/612/612886.png'
        )
        bot.answer_inline_query(inline_query.id, [result], cache_time=0)
    else:
        value = inline_query.query.split(' ')[1]
        quantidade = inline_query.query.split(' ')[2]
        codigo = gerar_muito_gift(quantidade, value)
        txt = api.Textos.giftcard(codigo=codigo, quantidade=quantidade, valor=value)
        title = f"Criar {quantidade} gifts cards de R${float(value):.2f}"
        description = f"Clique aqui para criar {quantidade} gift card de R${float(value):.2f}."
        result_id = '3'
        result = telebot.types.InlineQueryResultArticle(id=result_id, title=title, description=description, input_message_content=telebot.types.InputTextMessageContent(txt, parse_mode='HTML'), thumbnail_url='https://cdn-icons-png.flaticon.com/512/1261/1261149.png')
        bot.answer_inline_query(inline_query.id, [result])
def gerar_muito_gift(quantidade, valor):
    codigos = ''
    for i in range(int(quantidade)):
        while True:
            codigo = random.choices(string.ascii_uppercase + string.digits, k=9)
            codigo = ''.join(codigo)
            if api.GiftCard.validar_gift(codigo)[0] == False:
                api.GiftCard.create_gift(codigo, float(valor))
                codigos += f'\n{codigo}'
                break
            else:
                continue
    return codigos
def gerar_gift_card(valor):
    while True:
        codigo = random.choices(string.ascii_uppercase + string.digits, k=9)
        codigo = ''.join(codigo)
        if api.GiftCard.validar_gift(codigo)[0] == False:
            api.GiftCard.create_gift(codigo, float(valor))
            break
        else:
            continue
    return valor, codigo
@bot.inline_handler(lambda query: query.query.startswith('CREATEPIX '))
def create_pix(query):
    if api.Admin.verificar_admin(query.from_user.id) == False and int(api.CredentialsChange.id_dono()) != int(query.from_user.id):
        return
    valor = query.query.split(' ')[1]
    payment = api.CriarPix.gerar(valor, "inline")
    id_pag = payment['response']['id']
    pix_copia_cola = payment['response']['point_of_interaction']['transaction_data']['qr_code']
    txt = api.Textos.pix_gerado_inline(
        id_pagamento=id_pag,
        valor=valor,
        expiracao=api.CredentialsChange.InfoPix.expiracao(),
        pix_copia_cola=pix_copia_cola
    )
    title = f'Criar um pix de R${float(valor):.2f}'
    descricao = f'Clique aqui para gerar um pix de R${float(valor):.2f}'
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.aguardando_pagamento()}', callback_data='aguardando')]])
    result = types.InlineQueryResultArticle(
        id='9', 
        title=title, 
        description=descricao, 
        input_message_content=types.InputTextMessageContent(txt, parse_mode='HTML'), 
        thumbnail_url='https://devtools.com.br/img/pix/logo-pix-png-icone-520x520.png', 
        reply_markup=markup)
    bot.answer_inline_query(query.id, [result], cache_time=0)
    verificar_inline_payment(id_pag, valor, query.from_user.id)
def verificar_inline_payment(id_pag, valor, id):
    while True:
        time.sleep(5)
        result = sdk.payment().get(id_pag)
        payment = result["response"]
        status_pag = payment['status']
        if 'approved' in status_pag:
            txt = api.Textos.aprovado_inline(valor=valor, id_pagamento=id_pag)
            bot.send_message(chat_id=id, text=txt, parse_mode='HTML')
            break
        elif 'pending' in status_pag:
            continue
        elif 'cancelled' in status_pag:
            bot.send_message(chat_id=id, text=api.Textos.pagamento_expirado(id_pagamento=id_pag), parse_mode='HTML')
            break
@bot.message_handler(commands=['resgatar'])
def redeem_gift(message):
    msg = message.text.strip().split()
    if len(msg) != 2:
        bot.reply_to(message, "Erro, envie no formato correto.\nex: /resgatar 1isjue")
        return
    codigo = msg[1]
    processar_resgate(message.chat.id, codigo)
def processar_resgate(id, codigo):
    verif, valor = api.GiftCard.validar_gift(codigo)
    if verif == True:
        api.GiftCard.del_gift(codigo)
        api.MudancaHistorico.mudar_gift_resgatado(id, float(valor))
        api.InfoUser.add_saldo(id, valor)
        bot.send_message(int(id), f'🎉 <b>Parabéns!</b>\nVocê resgatou o Gift Card com sucesso ✅\n\n💰 <b>Valor:</b> {valor:.2f}\n📔 <b>Código: </b>{codigo}', parse_mode='HTML')
        bot.send_message(int(api.CredentialsChange.id_dono()), f'⚠️ <b>GIFT CARD RESGATADO</b> 🙋\nUsuario: {id} acabou de resgatar o gift card: {codigo} e obteve um saldo de R${valor:.2f}', parse_mode='HTML')
    else:
        bot.send_message(id, "Gift card invalido ou ja resgatado!")
        return
@bot.message_handler(commands=['format'])
def formatar_msg(message):
    txt = message.text
    txt = txt.replace('\n', '\\n').split()[1:]
    txt = ' '.join(txt)
    print(txt)
    bot.send_message(message.chat.id, txt)
@bot.message_handler(commands=['adicionar_texto'])
def handle_adicionar_texto(message):
    msg = message.text
    msg = msg.replace('/adicionar_texto', '')
    if len(msg.split(f'{api.CredentialsChange.separador()}')) != 3:
        bot.reply_to(message, f'Formato incorreto! A mensagem deve estar no formato:\nTEXTO{api.CredentialsChange.separador()}NOME DO BOTÃO{api.CredentialsChange.separador()}URL DO BOTÃO')
        return
    with open('mensagem_transmissora.txt', 'w') as f:
        f.write(msg)
    bot.reply_to(message, "Alterado com sucesso!")
@bot.inline_handler(lambda query: query.query.startswith('MENSAGEM'))
def inline_message(query):
    if api.Admin.verificar_admin(query.from_user.id) == False and int(api.CredentialsChange.id_dono()) != int(query.from_user.id):
        return
    try:
        with open('mensagem_transmissora.txt',  'r') as f:
            data = f.read()
    except:
        with open('mensagem_transmissora.txt',  'w') as f:
            f.write('')
        with open('mensagem_transmissora.txt',  'r') as f:
            data = f.read()
    print(len(data))
    if len(data) <= 1:
        try:
            result = types.InlineQueryResultArticle(id='110', title='Defina uma mensagem!', description='Você não tem nenhuma mensagem registrada, clique aqui e veja as instruções.', input_message_content=types.InputTextMessageContent(f"Para definir uma mensagem você deve usar o seguinte comando neste formato:\n\n<code>/adicionar_texto TEXTO{api.CredentialsChange.separador()}NOME BOTÃO{api.CredentialsChange.separador()}URL BOTÃO</code>\n\nVocê pode usar <a href=\"http://telegram.me/MDtoHTMLbot?start=html\">HTML.</a> Após definir o seu texto, basta dar o mesmo comando inline <code>@{api.CredentialsChange.user_bot()} MENSAGEM</code> - Isso você pode utilizar em qualquer chat, para enviar uma mensagem com botão apartir do seu perfil. E para redefinir a mensagem, basta dar o mesmo comando", parse_mode='HTML'), thumbnail_url='https://compras.wiki.ufsc.br/images/5/56/Erro.png')
        except:
            result = types.InlineQueryResultArticle(id='110', title='Defina uma mensagem!', description='Você não tem nenhuma mensagem registrada, clique aqui e veja as instruções.', input_message_content=types.InputTextMessageContent(f"Para definir uma mensagem você deve usar o seguinte comando neste formato:\n\n<code>/adicionar_texto TEXTO{api.CredentialsChange.separador()}NOME BOTÃO{api.CredentialsChange.separador()}URL BOTÃO</code>\n\nVocê pode usar <a href=\"http://telegram.me/MDtoHTMLbot?start=html\">HTML.</a> Após definir o seu texto, basta dar o mesmo comando inline <code>@{api.CredentialsChange.user_bot()} MENSAGEM</code> - Isso você pode utilizar em qualquer chat, para enviar uma mensagem com botão apartir do seu perfil. E para redefinir a mensagem, basta dar o mesmo comando", parse_mode='HTML'), thumb_url='https://compras.wiki.ufsc.br/images/5/56/Erro.png')
    else:
        p = data.replace('/adicionar_texto', '')
        p = p.split(f'{api.CredentialsChange.separador()}')
        text = p[0]
        nome_botao = p[1]
        url_botao = p[2]
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'{nome_botao}', url=f'{url_botao}')]])
        title = 'Enviar mensagem'
        description = 'Clique aqui para enviar uma mensagem com botão!'
        try:
            result = types.InlineQueryResultArticle(id=str(random.randint(1, 99999)), title=title, description=description, input_message_content=types.InputTextMessageContent(f'{text}', parse_mode='HTML'), reply_markup=markup, thumbnail_url='https://png.pngtree.com/png-vector/20190217/ourlarge/pngtree-vector-send-message-icon-png-image_558846.jpg')
        except:
            result = types.InlineQueryResultArticle(id=str(random.randint(1, 99999)), title=title, description=description, input_message_content=types.InputTextMessageContent(f'{text}', parse_mode='HTML'), reply_markup=markup, thumb_url='https://png.pngtree.com/png-vector/20190217/ourlarge/pngtree-vector-send-message-icon-png-image_558846.jpg')
    bot.answer_inline_query(query.id, [result], cache_time=0)

@bot.message_handler(commands=['start'])
def handle_start(message, edit_message=False):
    # Ignora comandos de start em grupos que não são direcionados explicitamente ao bot
    if message.chat.type != 'private' and f'@{BOT_USERNAME}' not in message.text and not message.text.strip() == '/start':
        return

    bot.clear_step_handler_by_chat_id(message.chat.id)
    if api.Admin.verificar_vencimento():
        bot.reply_to(message, "Desculpe, o bot está temporariamente indisponível por questões administrativas.")
        return
    if len(message.text.split()) == 2:
        if message.text.split()[1].isdigit():
            if message.text.split()[1] != str(message.from_user.id):
                api.InfoUser.novo_afiliado(message.from_user.id, message.text.split()[1])
    if api.InfoUser.verificar_usuario(message.from_user.id) == False:
        api.InfoUser.novo_usuario(message.from_user.id)
        try:
            bot.send_message(chat_id=api.CredentialsChange.id_dono(), text=api.Log.log_registro(message), parse_mode='HTML')
        except Exception as e:
            bot.send_message(api.CredentialsChange.id_dono(), f"Log não enviada!\nMotivo: {e}")
            pass
    if api.InfoUser.verificar_ban(message.from_user.id) == True:
        bot.reply_to(message, "Você está banido neste bot e não pode utiliza-lo!")
        return

    if api.CredentialsChange.status_manutencao():
        # Se a manutenção estiver LIGADA, bloqueia usuários normais e permite que admins continuem.
        if not api.Admin.verificar_admin(message.from_user.id) and api.CredentialsChange.id_dono() != int(message.from_user.id):
            bot.reply_to(message, "O bot esta em manutenção, voltaremos em breve!")
            return

    # Acessa o nome do usuário de forma segura
    first_name = html.escape(message.from_user.first_name) if message.from_user.first_name else "Usuário"
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
    
    # Usa a função centralizada de textos para a mensagem de start, passando os argumentos corretos
    texto = api.Textos.start(
        first_name=first_name,
        username=username,
        id=message.from_user.id,
        saldo=f"{api.InfoUser.saldo(message.from_user.id):.2f}",
        pontos_indicacao=api.InfoUser.pontos_indicacao(message.from_user.id)
    )

    bt_servicos = InlineKeyboardButton(f'{api.Botoes.servicos()}', callback_data='menu_servicos')
    bt2 = InlineKeyboardButton(f'{api.Botoes.perfil()}', callback_data='perfil')
    bt3 = InlineKeyboardButton(f'{api.Botoes.add_saldo()}', callback_data='addsaldo')
    bt_dev = InlineKeyboardButton(f'{api.Botoes.desenvolvedor()}', callback_data='desenvolvedor')
    
    suporte_link = api.CredentialsChange.SuporteInfo.link_suporte()
    if suporte_link and suporte_link.startswith('@'):
        suporte_link = f'https://t.me/{suporte_link.lstrip("@")}'
    bt4 = InlineKeyboardButton(f'{api.Botoes.suporte()}', url=suporte_link)
    markup = InlineKeyboardMarkup([[bt_servicos], [bt2, bt3], [bt_dev]])
    markup.row(bt4)

    if edit_message:
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            if 'message is not modified' not in e.description:
                raise
    else:
        try:
            bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            if 'message is not modified' not in e.description:
                raise



@bot.message_handler(commands=['kay'])
def handle_kay(message):
    bot.reply_to(message, "OI MEU AMOOOOOOOOOOOOOOOOOOOOOOOOOOR EU TE AMO MUITOO escreve /carta ai pra vose ve")

@bot.message_handler(commands=['carta'])
def handle_carta(message):
    texto_carta = """oi meu amor, fiz uma pequena cartinha pra você em quanto eu mexia nos códigos pq eu tinha tido essa ideia e falei "pq não", eu queria te agradecer por sempre estar ao meu lado independente das circunstancias e desafios que passamos, sou grato por você sempre confiar em mim e espero retribuir isso algum dia nem que seja comprando a joia mais cara desse mundo (ou te dando a merda de um fiat500 rosa), espero que algum dia você consiga se ver da forma que eu te vejo, se isso acontecer tenho certeza que vc nunca mais vai querer suas coxas separadas e nem tirar o umbigo pra eu parar de enfiar o dedo. eu te amo demais meu amor """
    url_musica = "https://open.spotify.com/intl-pt/track/2Z5wXgysowvzl0nKGNGU0t?si=4ef7a6a8b74c4b6c"
    
    markup = InlineKeyboardMarkup()
    botao_musica = InlineKeyboardButton("uma das primeira musicas que ouvi pensando em voce", url=url_musica)
    markup.add(botao_musica)
    
    bot.reply_to(message, texto_carta, reply_markup=markup)

def menu_servicos(message):
    texto = api.Textos.menu_servicos()
    
    # Botões para as categorias de serviços
    bt_logins = InlineKeyboardButton(f'{api.Botoes.comprar()}', callback_data='servicos')
    bt_ccs = InlineKeyboardButton(f'{api.Botoes.ccs()}', callback_data='servicos_ccs')
    # O botão TC foi removido e substituído por Laras a pedido.
    bt_laras = InlineKeyboardButton(f'{api.Botoes.laras()}', callback_data='servicos_laras')
    bt_ggs = InlineKeyboardButton(f'{api.Botoes.ggs()}', callback_data='servicos_ggs')
    
    # Botão para voltar ao menu principal
    bt_voltar = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')
    
    markup = InlineKeyboardMarkup([[bt_logins, bt_ccs], [bt_laras, bt_ggs], [bt_voltar]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def servicos_ccs(message):
    """Exibe a lista de NÍVEIS de CCs disponíveis para compra."""
    niveis = api.Admin.ControleCCs.pegar_niveis_unicos()
    markup = InlineKeyboardMarkup()

    if not niveis:
        markup.add(InlineKeyboardButton('❌ NÃO HÁ CCs DISPONÍVEIS ❌', callback_data='menu_servicos'))
    else:
        for nivel in niveis:
            # O callback agora chama a nova função de visualização, começando pelo primeiro cartão (índice 0)
            markup.add(InlineKeyboardButton(f"⭐ Nível {nivel.upper()}", callback_data=f"ver_cartao_do_nivel {nivel}|0"))
    
    markup.add(InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_servicos'))
    texto = api.Textos.menu_comprar_cc()
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def ver_cartao_do_nivel(call, nivel, index):
    """Exibe um cartão de um nível específico com base no índice."""
    cartoes_do_nivel = api.Admin.ControleCCs.pegar_ccs_por_nivel(nivel)

    if not cartoes_do_nivel:
        bot.answer_callback_query(call.id, "Não há mais cartões neste nível.", show_alert=True)
        servicos_ccs(call.message) # Volta para a seleção de níveis
        return

    # Garante que o índice seja cíclico
    index = int(index) % len(cartoes_do_nivel)
    cartao_atual = cartoes_do_nivel[index]

    # Extrai os dados do cartão selecionado
    numero_cartao = cartao_atual.get("nome")
    valor = float(cartao_atual.get("valor", 0))
    validade = cartao_atual.get("senha")
    cvv = cartao_atual.get("duracao")
    nome_titular = cartao_atual.get("titular", "N/A")
    cpf_titular = cartao_atual.get("cpf", "N/A")
    
    saldo_usuario = api.InfoUser.saldo(call.from_user.id)

    texto = api.Textos.confirmacao_compra_cc(
        saldo_usuario=f"{saldo_usuario:.2f}",
        valor_cc=f"{valor:.2f}",
        nivel=nivel,
        numero=numero_cartao,
        validade=validade,
        cvv=cvv,
        nome_titular=nome_titular,
        cpf=cpf_titular
    )

    # Calcula os índices anterior e próximo para navegação
    total_cartoes = len(cartoes_do_nivel)
    proximo_index = (index + 1) % total_cartoes
    anterior_index = (index - 1 + total_cartoes) % total_cartoes

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('✅ Confirmar Compra', callback_data=f'comprar_cc {numero_cartao}|{numero_cartao}')],
        [InlineKeyboardButton('◀️ Cartão Anterior', callback_data=f'ver_cartao_do_nivel {nivel}|{anterior_index}'),
         InlineKeyboardButton('▶️ Próximo Cartão', callback_data=f'ver_cartao_do_nivel {nivel}|{proximo_index}')],
        [InlineKeyboardButton('↩️ Voltar aos Níveis', callback_data='servicos_ccs')]
    ])
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise # Re-raise the exception if it's not the one we're expecting

def show_developer_info(message):
    """Exibe a mensagem com informações do desenvolvedor."""
    texto = api.Textos.desenvolvedor_info()
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup, disable_web_page_preview=True)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def descricoes_logins(message):
    servicos = api.ControleLogins.pegar_servicos()
    
    texto_final = "<b>ℹ️ Descrição dos Logins Disponíveis</b>\n\n"
    
    nomes_unicos = []
    for servico in servicos:
        nome = servico.get("nome")
        if nome and nome not in nomes_unicos:
            nomes_unicos.append(nome)
            
    if not nomes_unicos:
        texto_final += "Nenhum login com descrição disponível no momento."
    else:
        for nome in sorted(nomes_unicos):
            info = api.ControleLogins.pegar_info(nome)
            if info:
                descricao = info[2]
                if descricao and descricao.strip():
                     texto_final += f"<b>{nome}:</b>\n<code>{html.escape(descricao)}</code>\n\n"
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto_final, parse_mode='HTML', reply_markup=markup, disable_web_page_preview=True)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def perfil(message):
    markup = InlineKeyboardMarkup()
    bt = InlineKeyboardButton(f'{api.Botoes.download_historico()}', callback_data=f'baixar_historico {message.chat.id}')
    markup.add(bt)
    if api.AfiliadosInfo.status_afiliado() == True:
        bt2 = InlineKeyboardButton(f'{api.Botoes.trocar_pontos_por_saldo()}', callback_data=f'trocar_pontos')
        markup.add(bt2)
    bt3 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')
    markup.add(bt3)
    texto = api.Textos.perfil(message)
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def servicos(message):
    servicos = api.ControleLogins.pegar_servicos()
    markup = InlineKeyboardMarkup()
    ja_foram = []
    lista = []
    for servico in servicos:
        if servico["nome"] not in ja_foram:
            nome = servico["nome"]
            valor = servico["valor"]
            try:
                # Tenta converter o valor para float. Se falhar, ignora este item.
                valor_float = float(valor)
                lista.append((nome, InlineKeyboardButton(f'{nome} R${valor_float:.2f}', callback_data=f'exibir_servico {nome}')))
                ja_foram.append(nome)
            except (ValueError, TypeError):
                # Imprime um erro no console para o admin saber que há um item com defeito
                print(f"[AVISO] O serviço '{nome}' foi ignorado na lista por ter um valor inválido: '{valor}'")
                pass # Pula para o próximo item do loop
    lista = sorted(lista, key=lambda x: x[0])
    if len(ja_foram) == 0:
        bt = InlineKeyboardButton('❌ NÃO HÁ LOGINS DISPONÍVEIS ❌', callback_data='oookk')
        markup.add(bt)
    for _, button in lista:
        markup.add(button)
    bt3 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')
    markup.add(bt3)
    texto = api.Textos.menu_comprar()
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def exibir_servico(message, servico):
    # Pega as informações do primeiro item disponível para obter o email/identificador único
    info_servico = api.ControleLogins.pegar_info(servico)
    if not info_servico:
        bot.answer_callback_query(message.id, "Este serviço não está mais disponível.", show_alert=True)
        servicos(message.message) # Volta para a lista de serviços
        return

    _, valor, _, _, email = info_servico
    estoque = api.ControleLogins.pegar_estoque(servico)
    
    texto = api.Textos.exibir_servico(message, servico, f"{valor:.2f}", estoque)

    bt = InlineKeyboardButton(f'{api.Botoes.comprar_login()}', callback_data=f'comprar {servico}|{email}')
    bt2 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='servicos')
    markup = InlineKeyboardMarkup([[bt], [bt2]])
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def entregar(message, nome, valor, email, senha, descricao, duracao):
    texto = api.Textos.mensagem_comprou()
    api.ControleLogins.remover_login(nome, email)
    api.MudancaHistorico.add_compra(message.chat.id, nome, valor, email, senha)
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
    try:
        texto_adm = api.Log.log_compra(message, nome, email, senha, valor, descricao)
        bot.send_message(chat_id=api.CredentialsChange.id_dono(), text=texto_adm, parse_mode='HTML')
    except Exception as e:
        bot.send_message(api.CredentialsChange.id_dono(), f'Falha ao enviar a log!\nMotivo: {e}')
        pass

def entregar_cc(message, nome_cc, numero_cc):
    """Processa a compra e entrega do CC."""
    cc_data = api.ControleCCs.entregar_cc(nome_cc, numero_cc)
    if not cc_data:
        bot.answer_callback_query(message.id, "Erro: CC não encontrado. Pode já ter sido vendido.", show_alert=True)
        return

    valor = float(cc_data['valor'])
    if api.InfoUser.saldo(message.from_user.id) < valor:
        bot.answer_callback_query(message.id, "Saldo insuficiente!", show_alert=True)
        return

    api.InfoUser.tirar_saldo(message.from_user.id, valor)
    api.ControleCCs.remover_cc(nome_cc, numero_cc)
    
    # Formata a mensagem de entrega para o usuário
    texto_entrega = f"🥳 <b>COMPRA REALIZADA COM SUCESSO</b> 🥳\n\n⚜️ <b>{cc_data['descricao'].upper()}</b> ⚜️\n\n<b>NÚMERO:</b> <code>{cc_data['nome']}</code>\n<b>VALIDADE:</b> <code>{cc_data['senha']}</code>\n<b>CVV:</b> <code>{cc_data['duracao']}</code>\n<b>NOME:</b> <code>{cc_data['titular']}</code>\n<b>CPF:</b> <code>{cc_data['cpf']}</code>\n\n<b>OBRIGADO PELA PREFERÊNCIA!</b>"
    try:
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=texto_entrega, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise

def addsaldo(message):
    markup = InlineKeyboardMarkup()
    if api.CredentialsChange.StatusPix.pix_auto() == True and api.CredentialsChange.StatusPix.pix_manual() == True:
        bt = InlineKeyboardButton(f'{api.Botoes.pix_automatico()}', callback_data='pix_auto')
        bt2 = InlineKeyboardButton(f'{api.Botoes.pix_manual()}', callback_data='pix_manu')
        markup.add(bt2, bt)
    if api.CredentialsChange.StatusPix.pix_auto() == True and api.CredentialsChange.StatusPix.pix_manual() == False:
        bt = InlineKeyboardButton(f'{api.Botoes.pix_automatico()}', callback_data='pix_auto')
        markup.add(bt)
    if api.CredentialsChange.StatusPix.pix_auto() == False and api.CredentialsChange.StatusPix.pix_manual() == True:
        bt = InlineKeyboardButton(f'{api.Botoes.pix_manual()}', callback_data='pix_manu')
        markup.add(bt)
    if api.CredentialsChange.StatusPix.pix_auto() == False and api.CredentialsChange.StatusPix.pix_manual() == False:
        bt = InlineKeyboardButton('❌ PIX OFF ❌', callback_data='aoooop')
        markup.add(bt)
    bt3 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')
    markup.add(bt3)
    texto = api.Textos.adicionar_saldo()
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message is not modified' not in e.description:
            raise
def pix_auto(message):
    token_mp = api.CredentialsChange.InfoPix.token_mp()
    if not token_mp or token_mp.strip() == "":
        bot.reply_to(message, "Desculpe, o pagamento automático está temporariamente indisponível. Por favor, contate o suporte.")
        try:
            bot.send_message(api.CredentialsChange.id_dono(), "⚠️ <b>ALERTA DE CONFIGURAÇÃO</b> ⚠️\n\nUm usuário tentou fazer uma recarga via PIX automático, mas a operação falhou porque o <b>Token do Mercado Pago</b> não está configurado no painel de administração.", parse_mode='HTML')
        except Exception as log_error:
            print(f"Erro ao notificar admin sobre token MP ausente: {log_error}")
        return

    valor = message.text
    valor = valor.replace('R$', '').replace('R', '').replace('$', '').replace(',',  '.').replace(' ', '')
    try:
        valor = float(valor)
    except ValueError:
        bot.send_message(message.chat.id, "Digite um número válido!\n\n<b>Ex:</b> 10.00 ou 15", parse_mode='HTML')
        return
    if float(valor) >= float(api.CredentialsChange.InfoPix.deposito_minimo_pix()) and float(valor) <= float(api.CredentialsChange.InfoPix.deposito_maximo_pix()):
        try:
            payment = api.CriarPix.gerar(float(valor), message.chat.id)
            if not payment or 'response' not in payment or 'id' not in payment['response']:
                raise Exception(f"Falha ao gerar PIX. Resposta da API: {payment}")
            id_pag = payment['response']['id']
            pix_copia_cola = payment['response']['point_of_interaction']['transaction_data']['qr_code']
            chat_id = message.chat.id
            texto = api.Textos.pix_automatico(message, pix_copia_cola, 15, id_pag, f'{float(valor):.2f}')
            message1 = bot.send_message(chat_id=chat_id, text=texto, parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.aguardando_pagamento()}', callback_data='aguardando')]]))
            threading.Thread(target=verificar_pagamento, args=(message1, id_pag, valor)).start()
        except Exception as e:
            print(e)
            bot.reply_to(message, "Ocorreu um erro ao tentar gerar o pagamento. Por favor, tente novamente mais tarde ou contate o suporte.")
            bot.send_message(api.CredentialsChange.id_dono(), f"⚠️ <b>ERRO NA GERAÇÃO DE PIX</b> ⚠️\n\nOcorreu um erro ao tentar gerar um PIX para o usuário <code>{message.chat.id}</code>.\n\n<b>Erro:</b>\n<code>{html.escape(str(e))}</code>", parse_mode='HTML')
            return
    else:
        bot.reply_to(message, f"Valor invalido! Digite um valor entre R${float(api.CredentialsChange.InfoPix.deposito_minimo_pix()):.2f} e R${float(api.CredentialsChange.InfoPix.deposito_maximo_pix()):.2f}")
        return
def verificar_pagamento(message, id_pag, valor):
    time.sleep(5)
    while True:
        time.sleep(5)
        result = sdk.payment().get(id_pag)
        payment = result["response"]
        status_pag = payment['status']
        if 'approved' in status_pag:
            print(payment)
            if float(valor) >= float(api.CredentialsChange.BonusPix.valor_minimo_para_bonus()):
                bonus = api.CredentialsChange.BonusPix.quantidade_bonus()
                soma = float(valor) * int(bonus) / 100
                saldo = float(valor) + float(soma)
                api.InfoUser.add_saldo(message.chat.id, saldo)
                api.MudancaHistorico.add_pagamentos(message.chat.id, valor, id_pag)
            else:
                api.InfoUser.add_saldo(message.chat.id, valor)
                api.MudancaHistorico.add_pagamentos(message.chat.id, valor, id_pag)
            try:
                texto_adm = api.Log.log_recarga(message, id_pag, valor)
                id = api.CredentialsChange.id_dono()
                bot.send_message(chat_id=id, text=texto_adm, parse_mode='HTML')
            except Exception as e:
                bot.send_message(api.CredentialsChange.id_dono(), f'Falha ao enviar a log!\nMotivo: {e}')
                print(e)
                pass
            texto = api.Textos.pagamento_aprovado(id_pagamento=id_pag, saldo=api.InfoUser.saldo(message.chat.id))
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML')
            except telebot.apihelper.ApiTelegramException as e:
                if 'message is not modified' not in e.description:
                    raise
            break
        elif 'cancelled' in status_pag:
            texto = api.Textos.pagamento_expirado(id_pagamento=id_pag)
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML')
            except telebot.apihelper.ApiTelegramException as e:
                if 'message is not modified' not in e.description:
                    raise
            break
        elif 'pending' in status_pag:
            continue
        else:
            continue


@bot.message_handler(commands=['get_id'])
def get_id(message):
    bot.reply_to(message, f'{message.chat.id}')

@bot.message_handler(commands=['criador'])
def handle_criador(message):
    if message.from_user.id == int(api.CredentialsChange.id_dono()):
        b = InlineKeyboardButton('➕ ADD EM GRUPO ➕', url=f'https://t.me/{api.CredentialsChange.user_bot()}?startgroup=start')
        bt = InlineKeyboardButton('🔃 REINICIAR BOT', callback_data='reiniciar_bot')
        bt1 = InlineKeyboardButton('👮‍♀️ PEGAR ADMIN', callback_data='pegar_admin_creator')
        bt2 = InlineKeyboardButton('🔑 MUDAR TOKEN BOT', callback_data='mudar_token_bot')
        bt3 = InlineKeyboardButton('🤖 MUDAR USER DO BOT', callback_data='mudar_user_bot')
        bt4 = InlineKeyboardButton('💼 MUDAR DONO DO BOT', callback_data='mudar_dono_bot')
        bt43 = InlineKeyboardButton('👨‍💻 MUDAR VERSÃO DO BOT', callback_data='mudar_versao_bot')
        bt5 = InlineKeyboardButton('⏰ CONFIGURAR VENCIMENTO', callback_data='configurar_vencimento')
        markup = InlineKeyboardMarkup([[b], [bt], [bt1], [bt2], [bt3], [bt4], [bt43], [bt5]])
        txt = f'🧑‍💻 <b>PAINEL DE CONFIGURAÇÕES DEV</b>\n\n🎫 <b>Tipo de bot:</b> <i>Acessos e logins</i>\n🤖 <b>Versão:</b> <i>{api.CredentialsChange.versao_bot()}</i>\n👤 <b>Bot:</b> @{api.CredentialsChange.user_bot()}\n👥 <b>Dono:</b> <code>{api.CredentialsChange.id_dono()}</code>\n🔑 <b>Token:</b> <code>{api.CredentialsChange.token_bot()}</code>\n⏳ <b>Vencimento:</b> <code>{api.Admin.data_vencimento()} faltam {api.Admin.tempo_ate_o_vencimento()} dias!</code>'
        if message.text == '/criador':
            bot.send_message(chat_id=message.chat.id, text=txt, parse_mode='HTML', reply_markup=markup)
        else:
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
            except telebot.apihelper.ApiTelegramException as e:
                if 'message is not modified' not in e.description:
                    raise
def trocar_token(message):
    api.CredentialsChange.mudar_token_bot(message.text)
    bot.reply_to(message, "Alterado com sucesso! Reiniciando...")
    sys.exit(0) # Usa sys.exit para uma saída mais limpa
def trocar_user(message):
    api.CredentialsChange.mudar_user_bot(message.text)
    bot.reply_to(message, "Alterado!")
    message.text = '/criador'
    handle_criador(message)
def mudar_dono_bot(message):
    api.CredentialsChange.mudar_dono(message.text)
    bot.reply_to(message, "Alterado!")
    message.text = '/criador'
    handle_criador(message)
def mudar_dias_vencimento(message, tipo):
    if tipo == 'mais':
        api.Admin.aumentar_vencimento(message.text)
    else:
        api.Admin.diminuir_vencimento(message.text)
    bot.reply_to(message, 'Alterado!')
    message.text = '/criador'
    handle_criador(message)
def mudar_versao_bot(message):
    versao = message.text
    api.CredentialsChange.mudar_versao_bot(versao)
    bot.reply_to(message, "Alterado com sucesso!")
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'mudar_token_bot':
        bot.send_message(call.message.chat.id, "Envie o novo token do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_token)
        return
    if call.data == 'pegar_admin_creator':
        if api.Admin.verificar_admin(call.message.chat.id) == False:
            api.Admin.add_admin(call.message.chat.id)
            bot.answer_callback_query(call.id, "Feito!", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Você já é um admin!", show_alert=True)
    if call.data == 'mudar_user_bot':
        bot.send_message(call.message.chat.id, "Me envie o novo @ do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_user)
        return
    if call.data == 'mudar_dono_bot':
        bot.send_message(call.message.chat.id, "Digite o id do novo dono:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_dono_bot)
        return
    if call.data == 'configurar_vencimento':
        txt = '<i>Selecione abaixo a opção desejada:</i>'
        bt = InlineKeyboardButton('➕ AUMENTAR DIAS', callback_data='modificar_dias mais')
        bs = InlineKeyboardButton('➖ DIMINUIR DIAS', callback_data='modificar_dias menos')
        bp = InlineKeyboardButton('⭕ ZERAR DIAS', callback_data='parar_dias_creator')
        vo = InlineKeyboardButton('↩ VOLTAR', callback_data='voltar_painel_creator')
        markup = InlineKeyboardMarkup([[bt], [bs], [bp], [vo]])
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            if 'message is not modified' not in e.description:
                raise
        return
    if call.data == 'parar_dias_creator':
        api.Admin.zerar_vencimento()
        bot.reply_to(call.message, "Os dias foram zerados!")
        return
    if call.data.split()[0] == 'modificar_dias':
        tipo = call.data.split()[1]
        bot.send_message(call.message.chat.id, "Digite a quantidade de dias:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_dias_vencimento, tipo)
        return
    if call.data == 'mudar_versao_bot':
        bot.send_message(call.message.chat.id, "Digite a nova versão do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_versao_bot)
    if call.data == 'voltar_painel_creator':
        handle_criador(call.message)
        return
    try:
        if api.InfoUser.verificar_ban(call.message.chat.id) == True:
            bot.reply_to(call.message, "Você está banido neste bot e não pode utiliza-lo!")
            return
    except:
        if api.InfoUser.verificar_ban(call.from_user.id) == True:
            bot.reply_to(call.message, "Você está banido neste bot e não pode utiliza-lo!")
            return
    if api.CredentialsChange.status_manutencao() == True:
        if api.Admin.verificar_admin(call.message.chat.id) == False:
            if api.CredentialsChange.id_dono() != int(call.message.chat.id):
                bot.answer_callback_query(call.id, "O bot esta em manutenção, voltaremos em breve!", show_alert=True)
                return
    if api.Admin.verificar_vencimento():
        bot.answer_callback_query(call.id, "Desculpe, o bot está temporariamente indisponível por questões administrativas.", show_alert=True)
    # Voltar painel adm
    if call.data == 'voltar_paineladm':
        painel_admin(call.message)
    # Menu inicial
    if call.data == 'perfil':
        perfil(call.message)
    if call.data == 'servicos':
        servicos(call.message)
    if call.data == 'servicos_ccs':
        servicos_ccs(call.message)
    if call.data == 'menu_servicos':
        menu_servicos(call.message)
    if call.data == 'desenvolvedor':
        show_developer_info(call.message)
    if call.data == 'addsaldo':
        addsaldo(call.message)
    #Menu pix
    if call.data == 'pix_manu':
        if api.CredentialsChange.StatusPix.pix_manual() == True:
            pix_key = html.escape(api.CredentialsChange.InfoPix.chave_pix_manual())
            texto = f"Para fazer a recarga, use a seguinte chave PIX para realizar o pagamento:\n\n<code>{pix_key}</code>\n\nApós o pagamento, envie o comprovante para o suporte ({api.CredentialsChange.SuporteInfo.link_suporte()}) para que seu saldo seja adicionado manualmente."
            markup = InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='addsaldo')]])
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
            except telebot.apihelper.ApiTelegramException as e:
                if 'message is not modified' not in e.description:
                    raise
        else:
            return
    if call.data == 'pix_auto':
        if api.CredentialsChange.StatusPix.pix_auto() == True:
            bot.send_message(chat_id=call.message.chat.id, text=f"Digite o valor que deseja recarregar!\nmínimo: R${api.CredentialsChange.InfoPix.deposito_minimo_pix():.2f}\nmáximo: R${api.CredentialsChange.InfoPix.deposito_maximo_pix():.2f}", reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, pix_auto)
    # Menu serviços
    if call.data.split()[0] == 'exibir_servico':
        nome = call.data.split()[1:]
        nome = ' '.join(nome)
        exibir_servico(call.message, nome)
    if call.data.startswith('ver_cartao_do_nivel'):
        try:
            partes = ' '.join(call.data.split()[1:]).split('|')
            nivel, index = partes[0], int(partes[1])
            ver_cartao_do_nivel(call, nivel, index)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao carregar cartão.", show_alert=True)
    if call.data.split()[0] == 'comprar_cc':
        try:
            # Usamos '|' como separador para evitar problemas com nomes de bancos/bins que contêm espaços
            nome_cc, numero_cc = ' '.join(call.data.split()[1:]).split('|') # nome_cc e numero_cc são os mesmos
            entregar_cc(call, nome_cc, numero_cc) # A função entregar_cc agora usa o 'call'
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar a compra. Tente novamente.", show_alert=True)
    if call.data.split()[0] == 'comprar':
        try:
            # O formato agora é 'comprar NOME_SERVICO|EMAIL'
            dados_compra = ' '.join(call.data.split()[1:])
            servico, email_compra = dados_compra.split('|')
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar a compra. Tente novamente.", show_alert=True)
            return

        nome, valor, email, senha, descricao, duracao = api.ControleLogins.entregar_acesso(servico, email_compra)
        if float(api.InfoUser.saldo(call.message.chat.id)) < float(valor):
            falta = float(api.InfoUser.saldo(call.message.chat.id)) - float(valor)
            bot.answer_callback_query(call.id, f"Saldo insuficiente! Faltam R${float(valor) - float(api.InfoUser.saldo(call.message.chat.id)):.2f} faça uma recarga e tente novamente.", show_alert=True)
            return
        else:
            api.InfoUser.tirar_saldo(call.message.chat.id, valor)
            entregar(call.message, nome, valor, email, senha, descricao, duracao)
    # Menu perfil
    if call.data == 'trocar_pontos':
        if api.AfiliadosInfo.status_afiliado() == True:
            if int(api.InfoUser.pontos_indicacao(call.message.chat.id)) >= int(api.AfiliadosInfo.minimo_pontos_pra_saldo()):
                somar = float(api.InfoUser.pontos_indicacao(call.message.chat.id)) * float(api.AfiliadosInfo.multiplicador_pontos())
                pts = int(api.InfoUser.pontos_indicacao(call.message.chat.id))
                api.MudancaHistorico.zerar_pontos(call.message.chat.id)
                api.InfoUser.add_saldo(call.message.chat.id, int(somar))
                bot.answer_callback_query(call.id, f"Troca concluida!\nVocê trocou seus {pts} pontos e obteve um saldo de R${somar:.2f}", show_alert=True)
                return
            else:
                necessario = int(api.AfiliadosInfo.minimo_pontos_pra_saldo()) - api.InfoUser.pontos_indicacao(call.message.chat.id)
                bot.answer_callback_query(call.id, f"Pontos insuficientes!\nVocê precisa de mais {necessario} pontos para converter.", show_alert=True)
    if call.data == 'menu_start':
        handle_start(call.message, edit_message=True)
    # Configurações gerais
    if call.data == 'reiniciar_bot':
        bot.answer_callback_query(call.id, "Reiniciando...", show_alert=True)
        sys.exit(0)
    if call.data == 'configuracoes_geral':
        configuracoes_geral(call.message)
    if call.data == 'manutencao':
        api.CredentialsChange.mudar_status_manutencao()
        bot.answer_callback_query(call.id, "Status de manutenção atualizado com sucesso!", show_alert=True)
        configuracoes_geral(call.message)
    if call.data == 'suporte':
        bot.send_message(chat_id=call.message.chat.id, text="Me envie o novo link do suporte:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_suporte, call.id)
    if call.data == 'mudar_separador':
        bot.send_message(call.message.chat.id, "Digite o novo separador:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_separador, call.id)
    # Configurações de login
    if call.data == 'configurar_logins':
        configurar_logins(call.message)
    if call.data == 'adicionar_login':
        # Inicia o novo fluxo passo a passo para adicionar logins
        iniciar_adicionar_login(call.message)
    if call.data == 'gerenciar_logins_menu':
        gerenciar_logins_menu(call)
    # Configurações de CCs
    if call.data == 'configurar_ccs':
        configurar_ccs(call)
    if call.data == 'adicionar_cc':
        # Inicia o novo fluxo passo a passo
        iniciar_adicionar_cc(call.message)
    if call.data == 'remover_cc':
        # Esta callback agora é para remover um CC específico, mas o fluxo antigo ainda está aqui.
        # O novo fluxo de remoção começa em 'gerenciar_ccs_por_nivel'.
        # Vou manter o handler antigo para o caso de ser usado em outro lugar, mas o ideal seria removê-lo.
        bot.send_message(call.message.chat.id, f"Envie a CC que deseja remover, envie o banco/bin e o número, separados por {api.CredentialsChange.separador()}\nEx: ITAU{api.CredentialsChange.separador()}40028922...", parse_mode='HTML', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, remover_cc)
    if call.data == 'gerenciar_ccs_por_nivel':
        gerenciar_ccs_por_nivel(call)
    if call.data.startswith('listar_ccs_do_nivel'):
        nivel = ' '.join(call.data.split()[1:])
        listar_ccs_do_nivel(call, nivel)
    if call.data.startswith('remover_cc_especifico'):
        try:
            nome, email = ' '.join(call.data.split()[1:]).split('|')
            if api.Admin.ControleCCs.remover_cc(nome, email):
                bot.answer_callback_query(call.id, "Cartão removido com sucesso!")
                # Atualiza a lista daquele nível
                nivel = api.ControleCCs.pegar_info(nome)[2] # Pega o nível do cartão removido para recarregar a tela
                listar_ccs_do_nivel(call, nivel)
            else:
                bot.answer_callback_query(call.id, "Erro: Cartão não encontrado.", show_alert=True)
        except Exception as e:
            bot.answer_callback_query(call.id, f"Erro ao processar: {e}", show_alert=True)
    if call.data.startswith('confirmar_remover_nivel'):
        nivel = ' '.join(call.data.split()[1:])
        confirmar_remover_nivel(call, nivel)
    if call.data.startswith('remover_nivel_confirmado'):
        nivel = ' '.join(call.data.split()[1:])
        remover_nivel_confirmado(call, nivel)
    if call.data.startswith('editar_cc_menu'):
        cc_identifier = ' '.join(call.data.split()[1:])
        editar_cc_menu(call, cc_identifier)
    if call.data.startswith('editar_campo_cc'):
        try:
            campo, numero_cc = ' '.join(call.data.split()[1:]).split('|')
            solicitar_novo_valor_campo(call, campo, numero_cc)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar a edição.", show_alert=True)
    if call.data == 'remover_cc_por_banco':
        bot.send_message(call.message.chat.id, "Envie o nome do banco/bin que deseja remover do estoque:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, remover_cc_por_banco)
    if call.data == 'zerar_estoque_cc':
        try:
            api.Admin.ControleCCs.zerar_estoque()
            bot.answer_callback_query(call.id, text="Estoque de CCs zerado com sucesso!", show_alert=True)
        except:
            bot.answer_callback_query(call.id, text="Falha ao zerar o estoque de CCs.", show_alert=True)
    if call.data == 'mudar_valor_cc':
        bot.send_message(call.message.chat.id, f"Digite o banco/bin que terá seu valor mudado e o novo valor, separados por {api.CredentialsChange.separador()}\nEx: ITAU{api.CredentialsChange.separador()}100", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_valor_cc)
    if call.data == 'mudar_valor_todas_ccs':
        bot.send_message(call.message.chat.id, "Me envie o novo valor das CCs:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_valor_todas_ccs)
    # Configurações de adms
    if call.data == 'configurar_admins':
        configurar_admins(call.message)
    if call.data == 'adicionar_adm':
        bot.send_message(call.message.chat.id, "Digite o id do novo adm:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, adicionar_adm)
    if call.data == 'remover_adm':
        bot.send_message(call.message.chat.id, "Digite o id o admin que será removido:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, remover_adm)
    if call.data == 'lista_adm':
            try:
                lista = api.Admin.listar_admins()
                bot.send_message(call.message.chat.id, text=lista, parse_mode='HTML')
            except:
                bot.send_message(call.message.chat.id, "Erro ao buscar lista de admin")
    # Configurações dos afiliados
    if call.data == 'configurar_afiliados':
        configurar_afiliados(call.message)
    if call.data == 'mudar_status_afiliados':
        try:
            api.AfiliadosInfo.mudar_status_afiliado()
            bot.answer_callback_query(call.id, "Status alterado com sucesso!", show_alert=True)
            configurar_afiliados(call.message)
        except:
            bot.answer_callback_query(call.id, "Falha ao mudar o status.", show_alert=True)
    if call.data == 'pontos_por_recarga':
        bot.send_message(call.message.chat.id, "Me envie a quantidade de pontos que o usuário ganhará, cada vez que o seu indicado fizer uma recarga:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, pontos_por_recarga)
    if call.data == 'pontos_minimo_converter':
        bot.send_message(call.message.chat.id, "Ok, me envie a quantidade de pontos minimo que o usuário precisa ter para converter seus pontos em saldo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, pontos_minimo_converter)
    if call.data == 'multiplicador_para_converter':
        bot.send_message(call.message.chat.id, "Me envie o novo multiplicador:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, multiplicador_para_converter)
    # Configurações de usuarios
    if call.data == 'configurar_usuarios':
        configurar_usuarios(call.message)
    if call.data == 'transmitir_todos':
        api.FuncaoTransmitir.zerar_infos()
        bot.send_message(call.message.chat.id, "Me envie a mensagem que deseja transmitir:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, transmitir_todos)
    if call.data == 'mudar_bonus_registro':
        bot.send_message(call.message.chat.id, "Digite agora o novo bônus de registro:")
        bot.register_next_step_handler(call.message, mudar_bonus_registro)
    if call.data == 'add_botao':
        bot.send_message(call.message.chat.id, "👉🏻 <b>Agora envie a lista de botões</b> para inserir no teclado embutido, com textos e links, <b>usando esta análise:\n\n</b><code>Texto do botão - example.com\nTexto do botão - example.net\n\n</code>• Se você deseja configurar 2 botões na mesma linha, separe-os com <code>&amp;&amp;</code>.\n\n<b>Exemplo:\n</b><code>Grupo - t.me/username &amp;&amp; Canal - t.me/username\nSuporte - t.me/username\nWhatsapp - wa.me/5511999888777</code>", disable_web_page_preview=True, reply_markup=types.ForceReply(), parse_mode='HTML')
        bot.register_next_step_handler(call.message, add_botao)
    if call.data == 'confirmar_envio':
        confirmar_envio(call.message)
    if call.data == 'pesquisar_usuario':
        bot.send_message(call.message.chat.id, "Digite o id do usuario:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, pesquisar_usuario)
    if call.data == 'zerar_vendas':
        try:
            api.Admin.zerar_acessos_vendidos()
            bot.answer_callback_query(call.id, "Todos os registros de vendas foram zerados com sucesso!", show_alert=True)
        except Exception as e:
            bot.answer_callback_query(call.id, f"Ocorreu um erro ao zerar as vendas: {e}", show_alert=True)
    if call.data.split()[0] == 'banir':
        id = call.data.split()[1]
        if api.InfoUser.verificar_ban(id) == True:
            api.InfoUser.tirar_ban(id)
            bot.answer_callback_query(call.id, "Usuario desbanido!", show_alert=True)
            return
        else:
            api.InfoUser.dar_ban(id)
            bot.answer_callback_query(call.id, "Usuario banido!", show_alert=True)
            return
    if call.data.split()[0] == 'mudar_saldo':
        id = call.data.split()[1]
        bot.send_message(call.message.chat.id, f"Digite o novo saldo do usuario {id}:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_saldo, id)
    if call.data.split()[0] == 'baixar_historico':
        id = call.data.split()[1]
        api.InfoUser.fazer_txt_do_historico(id)
        with open(f'historicos/{id}.txt', 'rb') as file:
            bot.send_document(call.message.chat.id, document=file)
    # Configurações pix
    if call.data == 'configurar_pix':
        configurar_pix(call.message)
    if call.data == 'trocar_pix_manual':
        api.CredentialsChange.ChangeStatusPix.change_pix_manual()
        bot.answer_callback_query(call.id, "Alterado!", show_alert=True)
        configurar_pix(call.message)
    if call.data == 'trocar_pix_automatico':
        api.CredentialsChange.ChangeStatusPix.change_pix_auto()
        bot.answer_callback_query(call.id, "Alterado!", show_alert=True)
        configurar_pix(call.message)
    if call.data == 'mudar_token':
        bot.send_message(call.message.chat.id, "Me envie o novo token do mercado pago:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_token)
    if call.data == 'mudar_chave_pix_manual':
        bot.send_message(call.message.chat.id, "Me envie a nova chave PIX manual (pode ser CPF/CNPJ, celular, e-mail ou chave aleatória):", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_chave_pix_manual)
    if call.data == 'mudar_expiracao':
        bot.send_message(call.message.chat.id, f'Digite agora o novo tempo de expiração (EM MINUTOS)', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_expiracao)
    if call.data == 'mudar_deposito_minimo':
        bot.send_message(call.message.chat.id, "Digite o novo valor minimo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_deposito_minimo)
    if call.data == 'mudar_deposito_maximo':
        bot.send_message(call.message.chat.id, "Envie o novo deposito maximo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_deposito_maximo)
    if call.data == 'mudar_bonus':
        bot.send_message(call.message.chat.id, 'Me envie a porcentagem de bonus que o usuario ganhará por cada depósito:\n\nPor favor, envie sem o caractér (%)', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_bonus)
    if call.data == 'mudar_min_bonus':
        bot.send_message(call.message.chat.id, "Digite o valor mínimo que o usuário precisa depositar para ganhar o bônus:", reply_markup=types.ForceReply())
    # Configurações notificação
    if call.data == 'configurar_notificacoes_fake':
        configurar_notificacoes(call.message)
    if call.data == 'status_notificacoes':
        api.Notificacoes.mudar_status_notificacoes()
        configurar_notificacoes(call.message)
    if call.data == 'mudar_grupo_alvo':
        bot.send_message(call.message.chat.id, 'Me envie o id do novo grupo:', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_grupo_alvo)
    if call.data == 'tempo_min_saldo':
        bot.send_message(call.message.chat.id, "Digite o novo tempo mínimo das notificações (em segundos):", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, tempo_min_saldo)
    if call.data == 'tempo_max_saldo':
        bot.send_message(call.message.chat.id, "Digite o novo tempo máximo das notificações (em segundos):", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, tempo_max_saldo)
    if call.data == 'trocar_texto_saldo':
        bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de notificação de saldo!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID aleatório\n• <code>{saldo}</code> = saldo aleatorio', parse_mode='HTML', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_texto_saldo)
    if call.data == 'trocar_min_max_saldo':
        bot.send_message(call.message.chat.id, f"Envie o minimo e o maximo se saldo que as notificações escolherão, lembre-se de separa-los com um {api.CredentialsChange.separador()}\n<b>Ex:</b> 5{api.CredentialsChange.separador()}20", reply_markup=types.ForceReply(), parse_mode='HTML')
        bot.register_next_step_handler(call.message, trocar_min_max_saldo)
    if call.data == 'tempo_min_compra':
        bot.send_message(call.message.chat.id, "Digite o novo tempo mínimo das notificações (em segundos):", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, tempo_min_compra)
    if call.data == 'tempo_max_compra':
        bot.send_message(call.message.chat.id, "Digite o novo tempo máximo das notificações (em segundos):", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, tempo_max_compra)
    if call.data == 'trocar_texto_compra':
        bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de start!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML (http://telegram.me/MDtoHTMLbot?start=html)</a> e:\n\n• <code>{id}</code> = ID aleatório\n• <code>{servico}</code> = serviço aleatório\n• <code>{valor}</code> = valor do serviço aleatório', parse_mode='HTML', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_texto_compra)
    if call.data == 'trocar_servicos':
        bot.send_message(call.message.chat.id, "Digite a lista dos serviços que serão sorteados nas notificações fakes, lembre-se de enviar o valor na frente no serviço com 'R$' e pular uma linha para que o bot não faça confusão.\n\nEx:\nnetflix R$9,00\nglobo play + premiere R$9,00", parse_mode='HTML', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_servicos)
    if call.data == 'mudar_tipo_servico':
        api.Notificacoes.mudar_modo_servico()
        configurar_notificacoes(call.message)
    # Configurações gift card
    if call.data == 'gift_card':
        gift_card(call.message)
    if 'resgatar' in call.data.strip().split()[0]:
        id = call.from_user.id
        codigo = call.data.strip().split()[1]
        processar_resgate(int(id), codigo)
    if call.data == 'listar_tcs':
        bot.answer_callback_query(call.id, "Esta funcionalidade ainda não foi implementada.", show_alert=True)
    if call.data == 'servicos_laras':
        servicos_laras_menu(call.message)
    if call.data == 'configurar_laras':
        configurar_laras(call.message)
    if call.data == 'adicionar_lara':
        iniciar_adicionar_lara(call.message)
    if call.data == 'gerenciar_laras':
        gerenciar_laras_menu(call)
    if call.data.startswith('remover_lara_confirma'):
        email = ' '.join(call.data.split()[1:])
        remover_lara_confirma(call, email)
    if call.data.startswith('remover_lara_executa'):
        email = ' '.join(call.data.split()[1:])
        remover_lara_executa(call, email)
    if call.data.startswith('editar_lara_menu'):
        email = ' '.join(call.data.split()[1:])
        editar_lara_menu(call, email)
    if call.data.startswith('editar_campo_lara'):
        try:
            email, campo = ' '.join(call.data.split()[1:]).split('|')
            solicitar_novo_valor_lara(call, email, campo)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar a edição.", show_alert=True)
    if call.data.startswith('exibir_lara'):
        email = ' '.join(call.data.split()[1:])
        exibir_lara_compra(call, email)
    if call.data.startswith('comprar_lara'):
        email = ' '.join(call.data.split()[1:])
        entregar_lara(call, email)
    if call.data == 'configurar_ggs':
        configurar_ggs(call.message)
    if call.data == 'adicionar_gg':
        iniciar_adicionar_gg(call.message)
    if call.data == 'gerenciar_ggs_menu':
        gerenciar_ggs_menu(call)
    if call.data.startswith('listar_ggs_do_nivel'):
        nivel = ' '.join(call.data.split()[1:])
        listar_ggs_do_nivel(call, nivel)
    if call.data.startswith('remover_gg_especifico'):
        try:
            nome, email = ' '.join(call.data.split()[1:]).split('|')
            if api.Admin.ControleGGs.remover_gg(nome, email):
                bot.answer_callback_query(call.id, "GG removida com sucesso!")
                gg_data = api.ControleGGs.entregar_gg(nome, email)
                nivel = gg_data.get('descricao') if gg_data else 'default'
                listar_ggs_do_nivel(call, nivel)
            else:
                bot.answer_callback_query(call.id, "Erro: GG não encontrada.", show_alert=True)
        except Exception as e:
            bot.answer_callback_query(call.id, f"Erro ao processar: {e}", show_alert=True)
    if call.data.startswith('confirmar_remover_nivel_gg'):
        nivel = ' '.join(call.data.split()[1:])
        confirmar_remover_nivel_gg(call, nivel)
    if call.data.startswith('remover_nivel_gg_confirmado'):
        nivel = ' '.join(call.data.split()[1:])
        remover_nivel_gg_confirmado(call, nivel)
    if call.data.startswith('editar_gg_menu'):
        gg_identifier = ' '.join(call.data.split()[1:])
        editar_gg_menu(call, gg_identifier)
    if call.data.startswith('editar_campo_gg'):
        try:
            campo, numero_gg = ' '.join(call.data.split()[1:]).split('|')
            solicitar_novo_valor_campo_gg(call, campo, numero_gg)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar a edição.", show_alert=True)
    if call.data == 'servicos_ggs':
        servicos_ggs_menu(call.message)
    if call.data.startswith('ver_gg_do_nivel'):
        try:
            partes = ' '.join(call.data.split()[1:]).split('|')
            nivel, index = partes[0], int(partes[1])
            ver_gg_do_nivel(call, nivel, index)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao carregar GG.", show_alert=True)
    if call.data.startswith('comprar_gg'):
        try:
            nome_gg, numero_gg = ' '.join(call.data.split()[1:]).split('|')
            entregar_gg(call, nome_gg, numero_gg)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar a compra. Tente novamente.", show_alert=True)

    # --- Handlers para Gerenciamento de Logins ---
    if call.data.startswith('remover_login_especifico'):
        try:
            login_index = int(call.data.split()[1])
            if api.ControleLogins.remover_login_por_indice(login_index):
                bot.answer_callback_query(call.id, "Login removido com sucesso!")
                gerenciar_logins_menu(call) # Atualiza a lista
            else:
                bot.answer_callback_query(call.id, "Erro: Login não encontrado.", show_alert=True)
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar remoção.", show_alert=True)

    if call.data.startswith('editar_login_menu'):
        login_index = call.data.split()[1]
        editar_login_menu(call, login_index)

    if call.data.startswith('editar_campo_login'):
        try:
            identificador, campo = call.data.split()[1].split('|')
            login_index = int(identificador)
            prompt = f"Digite o novo valor para <b>{campo}</b>:"
            bot.send_message(call.message.chat.id, prompt, parse_mode='HTML', reply_markup=types.ForceReply())
            # Precisamos de uma função para salvar o campo editado
            # bot.register_next_step_handler(call.message, salvar_campo_login_editado, login_index, campo)
            bot.answer_callback_query(call.id, "Funcionalidade de edição de campo de login em desenvolvimento.")
        except (ValueError, IndexError):
            bot.answer_callback_query(call.id, "Erro ao processar edição de login.", show_alert=True)


def iniciar_verificacao():
    global bot_running
    while bot_running:
        try:
            time.sleep(240)
            if bot_running:
                ver_se_expirou()
            time.sleep(43200)
        except:
            break

def main():
    global bot_running
    
    print("🚀 Iniciando threads de verificação...")
    
    # Inicia threads de verificação
    verification_thread = threading.Thread(target=iniciar_verificacao, daemon=True)
    notification_saldo_thread = threading.Thread(target=enviar_notificacao_saldo, daemon=True)
    notification_compra_thread = threading.Thread(target=enviar_notificacao_compra, daemon=True)
    
    verification_thread.start()
    notification_saldo_thread.start()
    notification_compra_thread.start()
    
    print("✅ Threads iniciadas com sucesso!")
    print("🤖 Bot online e funcionando...")
    print("🛑 Para parar o bot, use Ctrl+C ou execute stop_bot.bat")
    
    try:
        bot.send_message(chat_id=api.CredentialsChange.id_dono(), text='🤖 <b>SEU BOT FOI REINICIADO!</b> 🤖', parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔧 PAINEL ADM', callback_data='voltar_paineladm')]]))
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível enviar a mensagem de reinicialização. Erro: {e}")

    print("=" * 50)    
    
    # Loop de polling robusto para lidar com erros de conexão
    while bot_running:
        try:
            # O timeout e long_polling_timeout ajudam a não ficar "preso".
            # O signal_handler vai chamar bot.stop_polling() para sair do loop.
            bot.infinity_polling(timeout=20, long_polling_timeout=15)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print(f"⚠️ Erro de conexão detectado: {e}")
            print("   Tentando reconectar em 15 segundos...")
            time.sleep(15)
        except KeyboardInterrupt:
            print("\n[INFO] Interrupção manual detectada.")
            bot_running = False
        except Exception as e:
            print(f"❌ Erro inesperado no polling: {e}")
            print("   Reiniciando em 30 segundos...")
            time.sleep(30)

    print("🛑 Finalizando bot...")
    bot.stop_polling()

if __name__ == "__main__":
    main()
