====PROPRIETÁRIO: Rodrigo Queiroz Vieira Freire=====
Sistema Bancário Simples em Python com CRUD em MySQL

Este sistema bancário é desenvolvido em Python, utilizando um banco de dados MySQL para armazenamento das informações dos clientes. 
O sistema abrange as funcionalidades principais de um banco, incluindo registro de contas, login, saque, depósito, transferência e excluir contas.

===INSTRUÇÕES PARA UTILIZAR NA SUA MÁQUINA===
-Certifique-se de ter o VSCode (COMPILADOR), o WAMP Server (LOCALHOST) e o MySQL Workbench (DATABASE) instalados.
-Inicialize o servidor local do WAMP Server e abra o MySQL Workbench e conecte-se ao servidor local.
(Use as configurações padrão (host: localhost, porta: 3306, usuário: root, senha: em branco))
-Selecione a opção para importar um arquivo SQL (cadastro-login). 
você encontrará essa opção na seção "SERVER",logo após verá a opção "Data Import".
-No VScode, instale as bibliotecas usadas no código (mysql-connector, re, customtkinter)
-Após realizada todas as etapas, compile o código "Banco_SQL.py" no compilador (VScode) que começará funcionar normalmente.

===FUNCIONALIDADES===

REGISTRO DA CONTA
Os usuários podem registrar suas contas fornecendo seu nome e senha.
Os dados da conta são armazenados em uma tabela MySQL chamada login, que contém campos para o identificador do id, usuario, senha e saldo.

LOGIN
Após o registro, os clientes podem fazer login fornecendo seus nomes.
O sistema verifica se o nome fornecido corresponde a uma conta registrada no banco de dados.

SAQUE
Os usuários podem sacar dinheiro de suas contas, desde que tenham saldo suficiente.
O saldo da conta é atualizado no banco de dados após o saque.
A funcão saque é apenas a subtração do dinheiro, não o movendo para outra localidade.

DEPÓSITO
Os usuários podem depositar dinheiro em suas contas.
O saldo da conta é atualizado no banco de dados após o depósito.
A funcão depósito é apenas a adição do dinheiro, não o movendo para outra localidade.

TRANSFERÊNCIA
Os usuários podem transferir dinheiro de sua conta para outra conta registrada no sistema, desde que essa conta exista.
O sistema verifica se há saldo suficiente antes de realizar a transferência.
O saldo das contas envolvidas na transferência é atualizada no banco de dados.

EXCLUSÃO DE CONTAS
Os usuários têm a opção de excluir suas contas do sistema.
Ao apertar no botão deletar conta, todas as informações da conta são removidas do banco de dados.

IMPLEMENTAÇÃO
O sistema utiliza a biblioteca mysql-connector para conectar e interagir com o banco de dados MySQL.
As operações CRUD são realizadas dependendo da função chamada ao interagir com a interface simples.
Este sistema bancário oferece uma solução simples e funcional para gerenciar contas bancárias, permitindo que os clientes realizem transações básicas de forma segura e eficiente.

===INFORMAÇÕES ADICIONAIS SOBRE O FUNCIONAMENTO DO CÓDIGO===
A lib "Pandas" também funciona para a manipulação e análise de dados, porém a lib utilizada (mysql-connector) tem a sintaxe e princípios similares ao Pandas para a manipulação de dados no database mysql.
Caso queira modificar o nome do database ou host, modifique no código na seguinte parte:

conexao_dados = mysql.connector.connect(
    host='nome_da_host', database='nome_do_database', user='root', password='')
    
(USE CTRL + F E ESCREVA O NOME "conexao_dados" PARA ENCONTRA-LA NO CÓDIGO)
As entradas de valores do saque, deposito e transferência não contam números após a 2 casa decimal 
EX: 10.90809 == 10.90
PARA ENTRADAS COM PONTO FLUTUANTE SÓ É PERMITIDO UTILIZANDO "."


===MELHORIAS CONSIDERADAS===
-Aceitar ',' para utilizar como ponto flutuante
-Interface recursiva
-Otimização do código explorando melhor conceitos de Clean Code e SOLID.
