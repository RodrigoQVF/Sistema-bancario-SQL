"""
Desenvolvedor: Rodrigo Queiroz Vieira Freire            Versão 3.0
Sistema bancário simples acoplado com mysql

=Funções=
-Sistema de sign e login que é armazenado no banco de dados
-Sacar, depositar e transferência (transferência para uma conta existente)
-deletar conta
-Interface amigável
"""
import mysql.connector
import customtkinter
import re

# MUDE A HOST OU BANCO DE DADOS AQUI ex: host='nome da host'
conexao_dados = mysql.connector.connect(
    host='localhost', database='cadastro', user='root', password='')

# Mostra a versao do mysql
info = conexao_dados.get_server_info()
print("Conectado ao Servidor mysql ", info)
cursor = conexao_dados.cursor()

class Usuario:

    @classmethod
    def setUsuario(cls, usuario):
        cls.__usuario = usuario

    @classmethod
    def setSenha(cls, senha):
        cls.__senha = senha

    @classmethod
    def setConfirmaSenha(cls, confirmaSenha):
        cls.__confirmaSenha = confirmaSenha

    @classmethod
    def setValor(cls, valor):
        cls.__valor = valor

    @classmethod
    def setRecebedor(cls, recebedor):
        cls.__recebedor = recebedor

    @classmethod
    def setSaldoFormatado(cls, saldoFormatado):
        cls.__saldoFormatado = saldoFormatado

    @classmethod
    def getSaldoFormatado(cls):
        return cls.__saldoFormatado

    @classmethod
    def getUsuario(cls):
        return cls.__usuario

    @classmethod
    def getSenha(cls):
        return cls.__senha

    @classmethod
    def getConfirmaSenha(cls):
        return cls.__confirmaSenha

    @classmethod
    def getValor(cls):
        return cls.__valor

    @classmethod
    def getRecebedor(cls):
        return cls.__recebedor

    @classmethod
    def ValorFormatado(cls):
        valor_saque_formatado = int(float(cls.getValor()) * 10**2)/10**2
        return valor_saque_formatado

    @classmethod
    def registrar(cls):
        if cls.getUsuario()[0] == " " or len(cls.getUsuario()) <= 3:
            warning_usuario_invalido()
        else:
            add_user = (f"""insert into login
            (id, usuario, senha)
            values (default,'{cls.getUsuario()}', '{cls.getSenha()}')""")
            add_log = (f"""select usuario, senha from login
                where usuario like binary '{cls.getUsuario()}'""")
            cursor.execute(add_log)
            cursor.fetchall()

            if cursor.rowcount == 1:
                warning_login_exist()

            else:
                cursor.execute(add_user)
                warning_login_reg()

    @classmethod
    def logar(cls):
        add_log = (f"""select usuario, senha from login
                where usuario like binary '{cls.getUsuario()}' and senha like binary '{cls.getSenha()}'""")
        cursor.execute(add_log)
        cursor.fetchall()  # busca todas as linhas

        if cursor.rowcount == 1:
            troca_tela()
        else:
            warning_logado()

    @classmethod
    def saque(cls):
        if cls.getConfirmaSenha() == cls.getSenha():
            if apenas_num(cls.getValor()):
                if cls.ValorFormatado() > float(cls.getSaldoFormatado()):
                    warning_saldo_insuficiente(0.4, 0.7)
                else:
                    atualiza_saque = (f"""update login
                    set saldo = saldo - {cls.ValorFormatado()} where usuario like binary '{cls.getUsuario()}'""")
                    cursor.execute(atualiza_saque)
                    mostra_saldo.destroy()
                    atualiza_saldo()
                    warning_saque_confirm()
            else:
                warning_valor_invalido(0.39, 0.7)
        else:
            warning_senha_errada(0.41, 0.7)

    @classmethod
    def deposito(cls):
        if cls.getConfirmaSenha() == cls.getSenha():
            if apenas_num(cls.getValor()):
                atualiza_deposito = (f"""update login
                set saldo = saldo + {cls.ValorFormatado()} where usuario like binary '{cls.getUsuario()}'""")
                cursor.execute(atualiza_deposito)
                mostra_saldo.destroy()
                atualiza_saldo()
                warning_deposito_confirmado()
            else:
                warning_valor_invalido(0.6, 0.7)
        else:
            warning_senha_errada(0.62, 0.7)

    @classmethod
    def transferencia(cls):
        if cls.getConfirmaSenha() == cls.getSenha():
            if apenas_num(cls.getValor()):
                if usuario_exist(cls.getRecebedor()):
                    if cls.ValorFormatado() > float(cls.getSaldoFormatado()):
                        warning_saldo_insuficiente(0.84, 0.78)
                    else:
                        atualiza_saldo_logado = (f"""update login set saldo = saldo + {cls.ValorFormatado()}
                        where usuario like binary '{cls.getRecebedor()}'""")
                        atualiza_saldo_recebedor = (f"""update login set saldo = saldo - {cls.ValorFormatado()}
                        where usuario like binary '{cls.getUsuario()}' """)
                        cursor.execute(atualiza_saldo_logado)
                        cursor.execute(atualiza_saldo_recebedor)
                        mostra_saldo.destroy()
                        atualiza_saldo()
                        warning_transfer_confirmada()
                else:
                    warning_usuario_N_exist()
            else:
                warning_valor_invalido(0.82, 0.78)
        else:
            warning_senha_errada(0.84, 0.78)

customtkinter.set_appearance_mode("Dark")
janela = customtkinter.CTk()
janela.geometry("1280x720")
janela.maxsize(width=1280, height=720)
janela.minsize(width=1280, height=720)

def apenas_num(string):
    padrão_letras = r'^[0-9.]+$'
    resultado = re.search(padrão_letras, string)
    return resultado is not None

def usuario_exist(usuario):
    confere_usuario = (f"""select usuario from login
    where usuario like binary '{usuario}'""")
    cursor.execute(confere_usuario)
    cursor.fetchall()
    if cursor.rowcount == 1:
        return True
    else:
        return False

def warning_logado():
    warning_log = customtkinter.CTkLabel(janela, text="Nome de usuário ou senha incorretos!",
    anchor=customtkinter.W, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_log.place(relx=0.12, rely=0.7)
    warning_log.after(3300, lambda: warning_log.destroy())

def warning_login_exist():
    login_exist = customtkinter.CTkLabel(janela, text="Usuário já registrado!",
    anchor=customtkinter.E, text_color="red", font=reg_fonte, bg_color="grey20")
    login_exist.place(relx=0.69, rely=0.7)
    login_exist.after(2500, lambda: login_exist.destroy())

def warning_login_reg():
    login_exist = customtkinter.CTkLabel(janela, text="Usuário registrado!",
    anchor=customtkinter.E, text_color="green", font=reg_fonte, bg_color="grey20")
    login_exist.place(relx=0.7, rely=0.7)
    login_exist.after(2500, lambda: login_exist.destroy())

def warning_usuario_invalido():
    warning_user_pass = customtkinter.CTkLabel(janela, text="Nome de usuário ou senha inválida(o)\n(Tamanho insuficiente ou espaço ou número no começo)",
    anchor=customtkinter.E, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_user_pass.place(relx=0.62, rely=0.7)
    warning_user_pass.after(3300, lambda: warning_user_pass.destroy())

def warning_mesmo_user():
    warning_mesmoUser = customtkinter.CTkLabel(janela, text="Não é possível transferir\n para si mesmo!",
    anchor=customtkinter.E, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_mesmoUser.place(relx=0.82, rely=0.77)
    warning_mesmoUser.after(3300, lambda: warning_mesmoUser.destroy())

def warning_senha_errada(x, y):
    warning_saque = customtkinter.CTkLabel(
    janela, text="senha incorreta!", anchor=customtkinter.CENTER, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_saque.place(relx=x, rely=y)
    warning_saque.after(2500, lambda: warning_saque.destroy())

def warning_saldo_insuficiente(x, y):
    warning_saldo_menor = customtkinter.CTkLabel(
        janela, text="Saldo insuficiente!", anchor=customtkinter.CENTER, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_saldo_menor.place(relx=x, rely=y)
    warning_saldo_menor.after(2500, lambda: warning_saldo_menor.destroy())

def warning_saque_confirm():
    warning_saque_sucess = customtkinter.CTkLabel(
        janela, text="Saque confirmado!", anchor=customtkinter.CENTER, text_color="green", font=fonte_warning, bg_color="grey20")
    warning_saque_sucess.place(relx=0.4, rely=0.7)
    warning_saque_sucess.after(2500, lambda: warning_saque_sucess.destroy())

def warning_valor_invalido(x, y):
    warning_saque_null = customtkinter.CTkLabel(
        janela, text="Valor inserido inválido!", anchor=customtkinter.CENTER, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_saque_null.place(relx=x, rely=y)
    warning_saque_null.after(2500, lambda: warning_saque_null.destroy())

def warning_deposito_confirmado():
    warning_deposito_sucess = customtkinter.CTkLabel(
        janela, text="Deposito confirmado!", anchor=customtkinter.CENTER, text_color="green", font=fonte_warning, bg_color="grey20")
    warning_deposito_sucess.place(relx=0.61, rely=0.7)
    warning_deposito_sucess.after(
        2500, lambda: warning_deposito_sucess.destroy())

def warning_transfer_confirmada():
    warning_transfer_sucess = customtkinter.CTkLabel(
        janela, text="Transferência\nConfirmada!", anchor=customtkinter.CENTER, text_color="green", font=fonte_warning, bg_color="grey20")
    warning_transfer_sucess.place(relx=0.85, rely=0.77)
    warning_transfer_sucess.after(
        2500, lambda: warning_transfer_sucess.destroy())

def warning_usuario_N_exist():
    warning_usuario_n_existe = customtkinter.CTkLabel(
        janela, text="Usuário não existe!", anchor=customtkinter.CENTER, text_color="red", font=fonte_warning, bg_color="grey20")
    warning_usuario_n_existe.place(relx=0.83, rely=0.78)
    warning_usuario_n_existe.after(
        2500, lambda: warning_usuario_n_existe.destroy())

def atualiza_saldo():
    global mostra_saldo
    saldo_banco = (f"""select saldo from login where usuario like binary '{Usuario().getUsuario()}' and senha like binary '{Usuario().getSenha()}' """)
    cursor.execute(saldo_banco)
    conta = cursor.fetchall()
    for saldo in conta:
        saldo1 = str(saldo)
    remove_char = "(),"
    remove = re.escape(remove_char)
    pad = f"[{remove}]"
    saldo_real = re.sub(pad, "", saldo1)
    saldo_formatado = "{:.2f}".format(float(saldo_real))
    Usuario().setSaldoFormatado(saldo_formatado)
    mostra_saldo = customtkinter.CTkLabel(
        janela, text=f"saldo:{saldo_formatado}R$", anchor=customtkinter.N, font=fonte)
    mostra_saldo.place(relx=0.1, rely=0.1)
    mostra_saldo.after(300)

def troca_tela():
    frame.after(700, lambda: frame.destroy())
    frame_d.after(700, lambda: frame_d.destroy())
    texto.after(700, lambda: texto.destroy())
    texto_reg.after(700, lambda: texto_reg.destroy())
    entry_user.after(700, lambda: entry_user.destroy())
    entry_pass.after(700, lambda: entry_pass.destroy())
    entry_user_reg.after(700, lambda: entry_user_reg.destroy())
    entry_pass_reg.after(700, lambda: entry_pass_reg.destroy())
    button_log.after(700, lambda: button_log.destroy())
    button_registrar.after(700, lambda: button_registrar.destroy())
    logado()

def logado():
    global frame_saque 
    global frame_transfer
    global frame_deposito
    global Nome_banco
    global button_delete
    global button_saque
    global entry_pass_confirm_deposito
    global entry_pass_confirm_saque
    global entry_pass_confirm_transfer
    global entry_valor_saque
    global entry_valor_deposito
    global entry_valor_transfer
    global entry_recebedor
    global button_voltar
    global label_saque
    global label_deposito
    global label_transfer
    global button_deposito
    global button_transfer
    atualiza_saldo()
    frame_saque = customtkinter.CTkFrame(
        janela, width=270, height=600, corner_radius=22, fg_color="grey20", border_color="green", border_width=1, bg_color="transparent")
    frame_saque.place(relx=0.45, rely=0.5, anchor=customtkinter.CENTER)

    frame_deposito = customtkinter.CTkFrame(
        janela, width=270, height=600, corner_radius=22, fg_color="grey20", border_color="purple", border_width=1, bg_color="transparent")
    frame_deposito.place(relx=0.67, rely=0.5, anchor=customtkinter.CENTER)

    frame_transfer = customtkinter.CTkFrame(
        janela, width=270, height=600, corner_radius=22, fg_color="grey20", border_color="yellow", border_width=1, bg_color="transparent")
    frame_transfer.place(relx=0.89, rely=0.5, anchor=customtkinter.CENTER)
    Nome_banco = customtkinter.CTkLabel(
        janela, text="RQ Bank",  anchor=customtkinter.N, font=fonte)
    Nome_banco.place(relx=0.01, rely=0.01)
    Nome_banco.after(800)
    button_delete = customtkinter.CTkButton(
        janela, text="Deletar conta", width=200, height=50, command=deletar_conta, corner_radius=22, fg_color="grey", border_color="red", border_width=1, hover_color="red")
    button_delete.place(relx=0.17, rely=0.98, anchor=customtkinter.SE)

    button_voltar = customtkinter.CTkButton(janela, text="Voltar tela de login", width=200, height=50, command=voltar_tela,corner_radius=22, fg_color="grey", border_color="blue", border_width=1, hover_color="blue")
    button_voltar.place(relx=0.34, rely=0.98, anchor=customtkinter.SE)

    label_saque = customtkinter.CTkLabel(
        janela, text="SAQUE", anchor=customtkinter.CENTER, font=fonte, text_color="green", bg_color="grey20")
    label_saque.place(relx=0.41, rely=0.1)

    label_deposito = customtkinter.CTkLabel(
        janela, text="DEPOSITO", anchor=customtkinter.CENTER, font=fonte, text_color="purple", bg_color="grey20")
    label_deposito.place(relx=0.61, rely=0.1)

    label_transfer = customtkinter.CTkLabel(
        janela, text="TRANSFERÊNCIA", anchor=customtkinter.CENTER, font=fonte, text_color="yellow", bg_color="grey20")
    label_transfer.place(relx=0.8, rely=0.1)

    button_saque = customtkinter.CTkButton(
        janela, text="Confirmar Saque", width=200, height=50, command=saque, corner_radius=22, fg_color="green", border_color="black", border_width=1, hover_color="grey10", bg_color="grey20")
    button_saque.place(relx=0.45, rely=0.87, anchor=customtkinter.CENTER)

    button_deposito = customtkinter.CTkButton(
        janela, text="Confirmar deposito", width=200, height=50, command=deposita, corner_radius=22, fg_color="purple", border_color="black", border_width=1, hover_color="grey10", bg_color="grey20")
    button_deposito.place(relx=0.67, rely=0.87, anchor=customtkinter.CENTER)

    button_transfer = customtkinter.CTkButton(
        janela, text="Confirmar\ntransferência", width=200, height=50, command=transfer, corner_radius=22, fg_color="orange", border_color="black", border_width=1, hover_color="grey10", bg_color="grey20")
    button_transfer.place(relx=0.89, rely=0.87, anchor=customtkinter.CENTER)

    entry_recebedor = customtkinter.CTkEntry(
        janela, placeholder_text="Usuário recebedor", width=200, height=60, border_color="yellow", border_width=1, bg_color="grey20", corner_radius=20)
    entry_recebedor.place(relx=0.89, rely=0.5, anchor=customtkinter.CENTER)

    entry_pass_confirm_saque = customtkinter.CTkEntry(
        janela, placeholder_text="Confirmar senha", show="*", width=200, height=60, border_color="green", border_width=1, bg_color="grey20", corner_radius=20)
    entry_pass_confirm_saque.place(
        relx=0.45, rely=0.5, anchor=customtkinter.CENTER)

    entry_pass_confirm_deposito = customtkinter.CTkEntry(
        janela, placeholder_text="Confirmar senha", show="*", width=200, height=60, border_color="purple", border_width=1, bg_color="grey20", corner_radius=20)
    entry_pass_confirm_deposito.place(
        relx=0.67, rely=0.5, anchor=customtkinter.CENTER)

    entry_pass_confirm_transfer = customtkinter.CTkEntry(
        janela, placeholder_text="Confirmar senha", show="*", width=200, height=60, border_color="yellow", border_width=1, bg_color="grey20", corner_radius=20)
    entry_pass_confirm_transfer.place(
        relx=0.89, rely=0.68, anchor=customtkinter.CENTER)

    entry_valor_saque = customtkinter.CTkEntry(
        janela, placeholder_text="Valor do saque", width=200, height=60, border_color="green", border_width=1, bg_color="grey20", corner_radius=20)
    entry_valor_saque.place(relx=0.45, rely=0.3, anchor=customtkinter.CENTER)

    entry_valor_deposito = customtkinter.CTkEntry(
        janela, placeholder_text="Valor do depósito", width=200, height=60, border_color="purple", border_width=1, bg_color="grey20", corner_radius=20)
    entry_valor_deposito.place(
        relx=0.67, rely=0.3, anchor=customtkinter.CENTER)

    entry_valor_transfer = customtkinter.CTkEntry(
        janela, placeholder_text="Valor da transferência", width=200, height=60, border_color="yellow", border_width=1, bg_color="grey20", corner_radius=20)
    entry_valor_transfer.place(
        relx=0.89, rely=0.3, anchor=customtkinter.CENTER)

def voltar_tela():
    Nome_banco.after(0, lambda: Nome_banco.destroy())
    mostra_saldo.after(0, lambda: mostra_saldo.destroy())
    button_delete.after(0, lambda: button_delete.destroy())
    button_saque.after(0, lambda: button_saque.destroy())
    button_deposito.after(0, lambda: button_deposito.destroy())
    button_transfer.after(0, lambda: button_transfer.destroy())
    frame_deposito.after(0, lambda: frame_deposito.destroy())
    frame_saque.after(0, lambda: frame_saque.destroy())
    frame_transfer.after(0, lambda: frame_transfer.destroy())
    button_voltar.after(0, lambda: button_voltar.destroy())
    label_saque.after(0, lambda: label_saque.destroy())
    label_deposito.after(0, lambda: label_deposito.destroy())
    label_transfer.after(0, lambda: label_transfer.destroy())
    entry_pass_confirm_deposito.after(0, lambda: entry_pass_confirm_deposito.destroy())
    entry_pass_confirm_saque.after(0, lambda: entry_pass_confirm_saque.destroy())
    entry_pass_confirm_transfer.after(0, lambda: entry_pass_confirm_transfer.destroy())
    entry_valor_saque.after(0, lambda: entry_valor_saque.destroy())
    entry_valor_deposito.after(0, lambda: entry_valor_deposito.destroy())
    entry_valor_transfer.after(0, lambda: entry_valor_transfer.destroy())
    entry_recebedor.after(0, lambda: entry_recebedor.destroy())
    tela_inicial()

def deletar_conta():
    delete_account = (f"delete from login where usuario like binary '{
                      Usuario().getUsuario()}'")
    cursor.execute(delete_account)
    voltar_tela()

def saque():
    Usuario().setConfirmaSenha(entry_pass_confirm_saque.get())
    Usuario().setValor(entry_valor_saque.get())
    Usuario().saque()

def deposita():
    Usuario().setConfirmaSenha(entry_pass_confirm_deposito.get())
    Usuario().setValor(entry_valor_deposito.get())
    Usuario().deposito()

def transfer():
    if entry_recebedor.get() == Usuario().getUsuario():
        warning_mesmo_user()
    else:
        Usuario().setConfirmaSenha(entry_pass_confirm_transfer.get())
        Usuario().setValor(entry_valor_transfer.get())
        Usuario().setRecebedor(entry_recebedor.get())
        Usuario().transferencia()

def button_logar():
    if entry_user.get() != "" or entry_pass.get() != "":
        Usuario().setUsuario(entry_user.get())
        Usuario().setSenha(entry_pass.get())
        Usuario().logar()
    else:
        warning_logado()

def button_register():
    if entry_user_reg.get() != "" or entry_pass_reg.get() != "":
        Usuario().setUsuario(entry_user_reg.get())
        Usuario().setSenha(entry_pass_reg.get())
        Usuario().registrar()
    else:
        warning_usuario_invalido()

def tela_inicial():
    global frame
    global frame_d
    global texto
    global texto_reg
    global entry_user
    global entry_pass
    global entry_user_reg
    global entry_pass_reg
    global button_log
    global button_registrar
    global fonte
    global reg_fonte
    global fonte_warning
    fonte = customtkinter.CTkFont(size=30)
    reg_fonte = customtkinter.CTkFont(size=23)
    fonte_warning = customtkinter.CTkFont(size=16)
    frame = customtkinter.CTkFrame(
        janela, width=550, height=550, corner_radius=10, fg_color="grey20", border_color="black", border_width=1, bg_color="transparent")
    frame.place(relx=0.45, rely=0.5, anchor=customtkinter.E)

    frame_d = customtkinter.CTkFrame(
        janela, width=550, height=550, corner_radius=10, fg_color="grey20", border_color="black", border_width=1, bg_color="transparent")
    frame_d.place(relx=0.55, rely=0.5, anchor=customtkinter.W)

    texto = customtkinter.CTkLabel(
        janela, text="Login",  anchor=customtkinter.E, font=fonte)
    texto.place(relx=0.2, rely=0.05)

    texto_reg = customtkinter.CTkLabel(
        janela, text="Registrar",  anchor=customtkinter.W, font=fonte)
    texto_reg.place(relx=0.72, rely=0.05)

    entry_user = customtkinter.CTkEntry(
        janela, placeholder_text="Usuário", width=300, height=60, border_color="black", border_width=1, bg_color="grey20")
    entry_user.place(relx=0.34, rely=0.35, anchor=customtkinter.E)

    entry_pass = customtkinter.CTkEntry(
        janela, placeholder_text="Senha", show="*", width=300, height=60, border_color="black", border_width=1, bg_color="grey20")
    entry_pass.place(relx=0.34, rely=0.58, anchor=customtkinter.E)

    entry_user_reg = customtkinter.CTkEntry(
        janela, placeholder_text="Novo Usuário", width=300, height=60, border_color="black", border_width=1, bg_color="grey20")
    entry_user_reg.place(relx=0.66, rely=0.35, anchor=customtkinter.W)

    entry_pass_reg = customtkinter.CTkEntry(
        janela, placeholder_text="Nova Senha", show="*", width=300, height=60, border_color="black", border_width=1, bg_color="grey20")
    entry_pass_reg.place(relx=0.66, rely=0.58, anchor=customtkinter.W)

    button_log = customtkinter.CTkButton(
        janela, text="Logar", command=button_logar, width=250, height=50, corner_radius=10, border_color="black", border_width=1, bg_color="grey20")
    button_log.place(relx=0.32, rely=0.8, anchor=customtkinter.E)

    button_registrar = customtkinter.CTkButton(
        janela, text="Registrar", command=button_register, fg_color="grey", width=250, height=50, corner_radius=10, border_color="black", border_width=1, bg_color="grey20")
    button_registrar.place(relx=0.68, rely=0.8, anchor=customtkinter.W)

tela_inicial()
janela.mainloop()
"""
=====DOCUMENTAÇÃO=====

===ABREVIAÇÕES DE VARIÁVEIS===
pass = senha
user = usuario
entry = entrada
reg = registro
log = logar
confirm = confirma
num = numero

===LEGENDA===
INFORMAÇÕES ENTRE CHAVES INFORMAM QUE AS FUNÇÕES QUE ESTÃO DENTRO DELA TEM RELAÇÕES DIRETAS
FUNÇÕES DENTRO DE FUNÇÕES INFORMAM QUE ELAS COMPLEMENTAM A OUTRA

{ (Início chaves exemplo) <-- Informa o abrimento das chaves

def exemplo <-- nome da função 23 <-- número que informa a linha que localiza a função
    isso é um exemplo para a legenda
} (Fim chaves exemplo) <-- Informa o fechamento das chaves

CLASSE USUÁRIO
funções getters e setters como método de classe e atributos privados do tipo String.
{
def setUsuario
def setSenha
def setConfirmaSenha
def setValor
def setRecebedor
def setSaldoFormatado
def getSaldoFormatado
def getUsuario
def getSenha
def getConfirmaSenha
def getValor
def getRecebedor
}

{
def ValorFormatado float
    Formatada o valor do saldo para a variavel tornar-se do tipo float.

def registrar
    Onde processa toda a lógica para criar uma conta e inseri-la no banco de dados

def logar
    Processa toda a lógica para logar em uma conta já existente no banco de dados

def saque
    Processa toda a lógica para fazer a operação de saque do usuário logado

def deposito
    Processa toda a lógica para fazer a operação de depositar no saldo do usuário logado e atualizando no banco de dados simultaneamente

def transferencia
    Processa toda a lógica para fazer a operação de transferência de saldo para um usuário existente no banco de dados
}


{ (Início chaves tela_inicial)

def tela_inicial 461
    Inicializa todas as entrys, labels e frames da tela de registrar e logar

def button_register 453 (Botão registrar)
    Chama o método Registrar da classe usuário

def button_logar 445 (botao logar)
    Chama o método Logar da classe usuário
def troca_tela 284
    Apaga todas as entrys, labels e frames da tela inicial para inciar a nova configuração de tela
}(fim chaves tela_inicial)


{ (Início chaves logado)

def logado 297
    Incializa todas as entrys, labels e frames da tela de usuário logado, onde o usuário consegue sacar, depositar e transferir

def atualiza_saldo 266
    Faz a atualização instantânea do saldo disponivel do usuário logado (atualiza quando saca, deposita e transfere)

def apenas_num 176
    Checa se a entry do valor de saque, deposito e transfere tem apenas números

    
{ (início chaves saque)

def saque 426 (botão saque)
    Processa toda a lógica para fazer a operação de saque do usuário logado
} (fim chaves saque)


{ (início chaves deposita)

def deposita 431 (botão de depositar)
    Chama o método deposito da classe usuário
} (fim chaves deposita)


{ (início chaves transfer)

def transfer 436 (botão de transferência) 
    Chama o método transferência da classe usuário
    
    def usuario_exist 181
        Retorna se existe um usuário para fazer a transferêcia de saldo
} (fim chaves transfer)

{ (início chaves voltar_tela)

def voltar_tela 397 (Botão voltar tela)
    Apaga todas as entrys, labels e frames da tela inicial para inciar a nova configuração de tela (tela inicial de logar e registrar)

def deletar_conta 420 (Botão deletar conta)
    apaga a conta do usuário do banco de dados e chama a função voltar_tela
}(fim chaves voltar_tela)


} (fim chaves função logado)
    
!!!TODAS AS FUNÇÕES QUE TEM O NOME "warning_....." SÃO AVISOS PARA GUIAR O USUÁRIO, O NOME DOS WARNINGS SÃO AUTO-EXPLICATIVOS!!!

==EXPLICAÇÕES DIVERSAS==
Todas as variáveis globais são da interface para que consiga fazer as ação de troca de tela dentro de outras funções!
"""
