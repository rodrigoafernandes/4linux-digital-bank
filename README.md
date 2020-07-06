# 4linux-digital-bank
Repositório para o exercício final do curso Python Fundamentals<br/>

## Descrição da solução
### Problema do Caixa Eletrônico

#### Administração
[cadastro de usuarios](https://github.com/rodrigoafernandes/4linux-digital-bank/issues/3)<br/>
[reset de senhas](https://github.com/rodrigoafernandes/4linux-digital-bank/issues/5)<br/>
[desbloqueio](https://github.com/rodrigoafernandes/4linux-digital-bank/issues/6) <- errou 3 vezes, block<br/>
#--------------------------#
#### Usuário
redefinir senha<br/>
consulta de saldo<br/>
saque<br/>
deposito<br/>
transferencia entre contas <br/>

#### login
[Login da aplicação](https://github.com/rodrigoafernandes/4linux-digital-bank/issues/8)<br/>

#### Menu
[menu administração](https://github.com/rodrigoafernandes/4linux-digital-bank/issues/7)<br/>
menu usuário comum <br/>

###### requisito 
[usar o banco de dados](https://github.com/rodrigoafernandes/4linux-digital-bank/issues/4)<br/>


#################################

## Milestones 

### Menu 

 -> funções <br/>


##### Versão de Admin 
(issues)    - cadastrar usuario -> comportamento/acao<br/>
            - resetar senha -><br/>
            - desbloquear usuario -><br/>
##### Versão de cliente
(issues)    - redefinir senha<br/>
            - consultar saldo<br/>
            - saque<br/>
            - transferência<br/>
            - depósito<br/>

como enquadrar como um problema de orientação à objetos <br/>

## Conexão com o Banco de Dados MariaDB
<code>docker container run -d --name mariadb-4LDB --restart always -p 3306:3306 -e MYSQL_ROOT_PASSWORD=admin123 -e MYSQL_DATABASE=4LDBKDEV01 -e MYSQL_USER=USR_4LDBK -e MYSQL_PASSWORD=USR_4LDBK mariadb</code>

## Execução de testes unitários e coverage
<code>python -m coverage run --source=modulos test/test.py<br/>python -m coverage json --pretty-print<br/>COVERAGE=$(cat coverage.json | jq -r '.totals.percent_covered')</code>