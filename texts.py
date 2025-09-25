import central as api

class Botoes:
    @staticmethod
    def add_saldo():
        return "💰 ADICIONAR SALDO"

    @staticmethod
    def aguardando_pagamento():
        return "⏰ AGUARDANDO PAGAMENTO"

    @staticmethod
    def comprar_login():
        return "🛒 COMPRAR"

    @staticmethod
    def ccs():
        return "💳 CCs"

    @staticmethod
    def comprar():
        return "📁 LOGINS"

    @staticmethod
    def desenvolvedor():
        return "👨‍💻 DESENVOLVEDOR DO BOT"

    @staticmethod
    def download_historico():
        return "🗂 BAIXAR HISTORICO"

    @staticmethod
    def ggs():
        return "✨ GGs (Geradas)"

    @staticmethod
    def laras():
        return "🍊 Laras"

    @staticmethod
    def perfil():
        return "🔦 PERFIL"

    @staticmethod
    def pix_automatico():
        return "💠 PIX AUTOMATICO"

    @staticmethod
    def pix_manual():
        return "💰 PIX MANUAL"

    @staticmethod
    def suporte():
        return "🎧 SUPORTE"

    @staticmethod
    def servicos():
        return "🛍️ SERVIÇOS"

    @staticmethod
    def trocar_pontos_por_saldo():
        return "🎖 TROCAR PONTOS POR SALDO"

    @staticmethod
    def voltar():
        return "↩️ VOLTAR"

class Textos:
    @staticmethod
    def adicionar_saldo():
        return "<i>Selecione a opção desejada:</i>"

    @staticmethod
    def aprovado_inline(valor, id_pagamento):
        return f"<b>🥳 PAGAMENTO APROVADO!</b>\n<b>├💸 VALOR:</b> R$ {float(valor):.2f}\n<b>└🆔 ID DO PAGAMENTO:</b> <code>{id_pagamento}</code>"

    @staticmethod
    def exibir_servico(message, nome_servico, valor, estoque):
        # Verifica se 'message' é um CallbackQuery ou uma Message
        chat_id = message.message.chat.id if hasattr(message, 'message') else message.chat.id
        saldo_usuario = api.InfoUser.saldo(chat_id)
        
        return f"⚜ <b>LOGIN {nome_servico}</b> ⚜\n\n💰 <b>PREÇO:</b> R${valor}\n💳 <b>SEU SALDO:</b> R${saldo_usuario:.2f}\n📦 <b>ESTOQUE:</b> {estoque}"

    @staticmethod
    def desenvolvedor_info():
        return (
            "<code>============================\n"
            "       BOT DESENVOLVIDO POR:\n"
            "                  @IMPK01\n"
            "============================</code>\n\n"
            "<i>!Faço bots, sites por preço banana, caso tenha interesse entre em contato.</i>"
        )

    @staticmethod
    def giftcard(codigo, quantidade, valor):
        return f"{quantidade} GIFT CARD(s) DE R${float(valor):.2f} GERADO(S)!\n\n{codigo}"

    @staticmethod
    def mensagem_comprou():
        return "🥳 <b>COMPRA REALIZADA COM SUCESSO</b> 🥳\n\n⚜️ <b>{nome}</b> ⚜️\n\n📧 <b>EMAIL:</b> <code>{email}</code>\n🔑 <b>SENHA:</b> <code>{senha}</code>\n\n🌐 <b>SITE:</b> <code>{duracao}</code>\n\n<b>OBRIGADO PELA PREFERÊNCIA!</b>"

    @staticmethod
    def menu_comprar():
        return "🎟️ 𝗟𝗢𝗚𝗜𝗡𝗦 | 𝗖𝗢𝗡𝗧𝗔𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠"

    @staticmethod
    def menu_comprar_cc():
        return "💳 𝗖𝗖𝘀 | 𝗖𝗔𝗥𝗧Õ𝗘𝗦 𝗗𝗘 𝗖𝗥É𝗗𝗜𝗧𝗢"

    @staticmethod
    def menu_comprar_gg():
        return "✨ 𝗚𝗚𝘀 | GERADAS"

    @staticmethod
    def confirmacao_compra_cc(saldo_usuario, valor_cc, nivel, numero, validade, cvv, nome_titular, cpf):
        # Mascara os dados sensíveis para exibição
        numero_mascarado = f"{str(numero)[:6]}{'*' * (len(str(numero)) - 6)}"
        validade_mascarada = '*' * len(str(validade))
        cvv_mascarado = '*' * len(str(cvv))
        primeiro_nome = str(nome_titular).split(' ')[0]
        cpf_mascarado = f"***.{str(cpf)[3:6]}.{str(cpf)[6:9]}-**" if len(str(cpf)) == 11 else '*' * len(str(cpf))
        return f"<b>⚠️ CONFIRME SUA COMPRA ⚠️</b>\n\n<i>Você está prestes a adquirir o seguinte cartão:</i>\n\n<b>💳 NÚMERO:</b> <code>{numero_mascarado}</code>\n<b>👤 TITULAR:</b> <code>{primeiro_nome}</code>\n<b>📄 CPF:</b> <code>{cpf_mascarado}</code>\n<b>📅 VALIDADE:</b> <code>{validade_mascarada}</code>\n<b>🔒 CVV:</b> <code>{cvv_mascarado}</code>\n<b>⭐ NÍVEL:</b> {nivel.upper()}\n\n- - - - - - - - - - - - - - - - - - -\n\n💰 <b>Valor do Cartão:</b> R$ {valor_cc}\n💸 <b>Seu Saldo Atual:</b> R$ {saldo_usuario}\n\n<i>Clique em 'Confirmar Compra' para finalizar.</i>"


    @staticmethod
    def menu_servicos():
        return "<b>🛍️ Nossos Serviços</b>\n\n<i>Selecione uma das categorias abaixo para visualizar os produtos disponíveis.</i>"

    @staticmethod
    def pagamento_aprovado(id_pagamento, saldo):
        return f"✅ <b>Pagamento aprovado</b>\n\n🆔 <b>Id do pagamento:</b> {id_pagamento}\n💸 <b>Saldo atual:</b> R$ {saldo:.2f}"

    @staticmethod
    def pagamento_expirado(id_pagamento):
        return f"⭕ <b>PAGAMENTO EXPIRADO</b>\n\n\n🆔 <b>Id do pagamento:</b> {id_pagamento}\n<i>Gere outro para recarregar!</i>"

    @staticmethod
    def perfil(message):
        # Garante que estamos usando o ID do usuário, não do chat.
        user_id = message.from_user.id

        return f"✨ <b>Suas Informações</b>\n\n<i>- Aqui você pode visualizar os detalhes da sua conta.</i>\n\n\n- 💰 <b>Carteira:</b>\n🆔 <b>ID da carteira:</b> <code>{user_id}</code>\n💸 <b>Saldo:</b> <code>R${api.InfoUser.saldo(user_id):.2f}</code>\n\n\n- 🏆 <b>Indicação:</b>\n🥇 <b>Pontos de indicação:</b> <code>{api.InfoUser.pontos_indicacao(user_id)}</code>\n🏆 <b>Pessoas que você indicou:</b> <code>{api.InfoUser.quantidade_afiliados(user_id)}</code>\n💰 <b>link de indicação:</b> https://t.me/{api.CredentialsChange.user_bot()}?start={user_id}\n\n\n- 🛍 <b>Compras:</b>\n🛒 <b>Logins comprados:</b> <code>{api.InfoUser.total_compras(user_id)}</code>\n💠 <b>Pix inseridos:</b> <code>R${api.InfoUser.pix_inseridos(user_id):.2f}</code>\n🎁 <b>Gifts resgatados:</b> <code>R${api.InfoUser.gifts_resgatados(user_id):.2f}</code>"

    @staticmethod
    def pix_automatico():
        return "💰 <b>Comprar Saldo com pix automático:</b>\n\n⏱ <b>Expira em:</b> <code>{expiracao} min</code>\n💰 <b>Valor:</b> <code>R${valor}</code>\n✨ <b>ID da compra:</b> <code>{id_pagamento}</code>\n\n📃 <b>Este código \"copia e cola\" é valido para apenas 1 pagamento!\nOu seja, se você utilizar ele mais de 1 vez para adicionar saldo, você PERDERAR o saldo e não tem direito a reembolso!</b>\n\n\n💎 <b>Pix copia e cola:</b>\n\n💡 <i>Clique no código para copia-lo.</i>\n\n<code>{pix_copia_cola}</code>\n\n🇧🇷 <b>Após o pagamento ser efetuado, seu saldo será liberado instantaneamente.</b>"

    @staticmethod
    def pix_gerado_inline(id_pagamento, valor, expiracao, pix_copia_cola):
        return f"<b>💠 PIX GERADO! 💠</b>\n\n<b>⚠️ ID DO PAGAMENTO:</b> {id_pagamento}\n<b>💸 VALOR:</b> R$ {float(valor):.2f}\n<b>🚨 EXPIRA EM: {expiracao} minutos</b>\n\n<code>{pix_copia_cola}</code>\n\n<b>💡 Dica: Clique no código para copia-lo 👆</b>"

    @staticmethod
    def pix_manual():
        return "."

    @staticmethod
    def start(first_name, username, id, saldo, pontos_indicacao):
        return f"💟 𝗕𝗲𝗺-𝘃𝗶𝗻𝗱𝗼 a melhor loja de logins do Telegram!! ✨\n\n❗️Caso não tenha o login desejado contate o nosso suporte ☺️\n\n\n\n🧾 <b>Seu perfil:</b>\n├👤 <b>NOME:</b> {first_name}\n├👤 <b>USERNAME:</b> {username}\n├👤 <b>ID:</b> <code>{id}</code>\n├💸 <b>Saldo:</b> R${saldo}\n└🥇 <b>Pontos de indicação:</b> {pontos_indicacao}"