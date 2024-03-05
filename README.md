====PROPRIETÁRIO: Rodrigo Queiroz Vieira Freire=====<br/>
Sistema Bancário Simples em Python com CRUD em MySQL<br/>

Este sistema bancário é desenvolvido em Python, utilizando um banco de dados MySQL para armazenamento das informações dos clientes.<br/>
O sistema abrange as funcionalidades principais de um banco, incluindo registro de contas, login, saque, depósito, transferência e excluir contas.<br/>

===INSTRUÇÕES PARA UTILIZAR NA SUA MÁQUINA===<br/>
-Certifique-se de ter o VSCode (COMPILADOR), o WAMP Server (LOCALHOST) e o MySQL Workbench (DATABASE) instalados.<br/>
-Inicialize o servidor local do WAMP Server e abra o MySQL Workbench e conecte-se ao servidor local.<br/>
(Use as configurações padrão (host: localhost, porta: 3306, usuário: root, senha: em branco))<br/>
-Selecione a opção para importar um arquivo SQL (cadastro-login).<br/> 
você encontrará essa opção na seção "SERVER",logo após verá a opção "Data Import".<br/>
-No VScode, instale as bibliotecas usadas no código (mysql-connector, re, customtkinter)<br/>
-Após realizada todas as etapas, compile o código "Banco_SQL.py" no compilador (VScode) que começará funcionar normalmente.<br/>

===FUNCIONALIDADES===<br/>

REGISTRO DA CONTA<br/>
Os usuários podem registrar suas contas fornecendo seu nome e senha.<br/>
Os dados da conta são armazenados em uma tabela MySQL chamada login, que contém campos para o identificador do id, usuario, senha e saldo.<br/>

LOGIN<br/>
Após o registro, os clientes podem fazer login fornecendo seus nomes.<br/>
O sistema verifica se o nome fornecido corresponde a uma conta registrada no banco de dados.<br/>

SAQUE<br/>
Os usuários podem sacar dinheiro de suas contas, desde que tenham saldo suficiente.<br/>
O saldo da conta é atualizado no banco de dados após o saque.<br/>
A funcão saque é apenas a subtração do dinheiro, não o movendo para outra localidade.<br/>

DEPÓSITO<br/>
Os usuários podem depositar dinheiro em suas contas.<br/>
O saldo da conta é atualizado no banco de dados após o depósito.<br/>
A funcão depósito é apenas a adição do dinheiro, não o movendo para outra localidade.<br/>

TRANSFERÊNCIA<br/>
Os usuários podem transferir dinheiro de sua conta para outra conta registrada no sistema, desde que essa conta exista.<br/>
O sistema verifica se há saldo suficiente antes de realizar a transferência.<br/>
O saldo das contas envolvidas na transferência é atualizada no banco de dados.<br/>

EXCLUSÃO DE CONTAS<br/>
Os usuários têm a opção de excluir suas contas do sistema.<br/>
Ao apertar no botão deletar conta, todas as informações da conta são removidas do banco de dados.<br/>

IMPLEMENTAÇÃO<br/>
O sistema utiliza a biblioteca mysql-connector para conectar e interagir com o banco de dados MySQL.<br/>
As operações CRUD são realizadas dependendo da função chamada ao interagir com a interface simples.<br/>
Este sistema bancário oferece uma solução simples e funcional para gerenciar contas bancárias, permitindo que os clientes realizem transações básicas de forma segura e eficiente.<br/>

===INFORMAÇÕES ADICIONAIS SOBRE O FUNCIONAMENTO DO CÓDIGO===<br/>
A lib "Pandas" também funciona para a manipulação e análise de dados, porém a lib utilizada (mysql-connector) tem a sintaxe e princípios similares ao Pandas para a manipulação de dados no database mysql.<br/>
Caso queira modificar o nome do database ou host, modifique no código na seguinte parte:<br/>

conexao_dados = mysql.connector.connect(
    host='nome_da_host', database='nome_do_database', user='root', password='')
    
(USE CTRL + F E ESCREVA O NOME "conexao_dados" PARA ENCONTRA-LA NO CÓDIGO)<br/>
As entradas de valores do saque, deposito e transferência não contam números após a 2 casa decimal<br/>
EX: 10.90809 == 10.90<br/>
PARA ENTRADAS COM PONTO FLUTUANTE SÓ É PERMITIDO UTILIZANDO "."<br/>


===MELHORIAS CONSIDERADAS===<br/>
-Aceitar ',' para utilizar como ponto flutuante<br/>
-Interface recursiva<br/>
-Otimização do código explorando melhor conceitos de Clean Code e SOLID.<br/>
-Melhorar as condições para restringir alguns tipos específicos de nomes de usuários na função de registro.
