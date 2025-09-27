import time
import argparse
import sys
from central import Admin, ler_json

# --- Funções de Cor para o Console ---
def print_color(text, color_code):
    """Imprime texto colorido no console."""
    print(f"\033[{color_code}m{text}\033[0m")

def green(text):
    print_color(text, "92")

def red(text):
    print_color(text, "91")

def yellow(text):
    print_color(text, "93")

def cyan(text):
    print_color(text, "96")

def main():
    """Função principal para executar o checker de CCs via linha de comando."""
    parser = argparse.ArgumentParser(description="Checker de CCs via linha de comando.")
    parser.add_argument(
        "--level",
        type=str,
        help="Verifica apenas os CCs de um nível específico."
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=2,
        help="Atraso em segundos entre cada verificação para evitar bloqueios de API. Padrão: 2s."
    )
    args = parser.parse_args()

    cyan("=====================================")
    cyan("=       CHECKER DE CCs - CLI        =")
    cyan("=====================================")
    print("\n")

    if args.level:
        yellow(f"[*] Verificando cartões do nível: {args.level.upper()}")
        ccs_para_checar = Admin.ControleCCs.pegar_ccs_por_nivel(args.level)
    else:
        yellow("[*] Verificando TODOS os cartões em estoque.")
        all_data = ler_json(Admin.ControleCCs._ccs_path)
        ccs_para_checar = all_data.get("ccs", [])

    if not ccs_para_checar:
        red("[!] Nenhum cartão encontrado para verificação.")
        sys.exit(1)

    total = len(ccs_para_checar)
    lives = []
    deads = []
    erros = []

    for i, cc_data in enumerate(ccs_para_checar):
        numero_cc = cc_data.get("nome", "N/A")
        print(f"[*] Checando [{i+1}/{total}]: {numero_cc[:6]}...{numero_cc[-4:]}", end='\r')

        status, motivo = Admin.ControleCCs.check_cc(cc_data)

        if status == "LIVE":
            lives.append(f"{numero_cc} | {cc_data.get('senha')} | {cc_data.get('duracao')} -> {motivo}")
        elif status == "DEAD":
            deads.append(f"{numero_cc} -> {motivo}")
        else: # ERRO
            erros.append(f"{numero_cc} -> {motivo}")

        time.sleep(args.delay)

    print("\n\n" + "="*20 + " RESULTADOS " + "="*20)
    if lives:
        green(f"\n--- ✅ LIVES ({len(lives)}) ---")
        for live in lives: green(live)
    if deads:
        red(f"\n--- ❌ DEADS ({len(deads)}) ---")
        for dead in deads: red(dead)
    if erros:
        yellow(f"\n--- ⚠️ ERROS ({len(erros)}) ---")
        for erro in erros: yellow(erro)

if __name__ == "__main__":
    main()