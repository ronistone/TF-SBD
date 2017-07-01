Para instalar e executar, siga os seguintes passos:  

1. Clone o repositório  
        ```
        $ git clone https://github.com/ronistone/TF-SBD.git
        ```
2. Entre no repositório  
        ```
        $ cd TF-SBD
        ```
3. Instale o virtualenv  
        ```
        $ sudo pip install virtualenv
        ```
4. Crie um novo virtualenv  
        ```
        $ virtualenv -p python3 flask
        ```
5. Execute o virtualenv  
        ```
        $ . flask/bin/activate
        ```
6. Caso já não tenha, instale o PostgreSQL e o pacote python3-dev  
        ```
        $ sudo apt install postgresql postgresql-contrib postgresql-server-dev-9.5
        ```  
        ```
        $ sudo apt install python3-dev
        ```  
7. Crie um usuário no PostgreSQL com o seu nome de usuário  
        ```
        $ sudo -i -u postgres
        ```   
        ```
        # psql  
        ```  
        CREATE USER nomedousuario SUPERUSER INHERIT CREATEDB CREATEROLE PASSWORD 'qualquerSenha'; 
        ```  
        Para sair utilize ``` \q ``` ou pressione Ctrl+D
8. Crie o banco de dados *agencia* no seu PostgreSQL local   
        ```
        $ sudo -u <usuario> createdb agencia
        ```
9. Instale as dependências  
        ```
        $ flask/bin/pip3 install -r requirements.txt
        ```
10. Realizar a criação do banco de dados  
        ```
        $ flask initdb  
        ```  
11. Execute o programa   
        ```
        $ python3 run.py  
        ```  
12. Para parar a execução, basta pressionar CTRL+C  
13. Para sair do *virtualenv*  
        ```
        $ deactivate
        ```

Certifique-se de sempre realizar os passos 5 e 10 novamente em execuções futuras.
