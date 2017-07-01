Para instalar e executar, siga os seguintes passos:  

1. Clone o repositório  
        ```
        $ git clone https://github.com/lctheodoro/LibraryFree.git
        ```
2. Entre no repositório  
        ```
        $ cd LibraryFree
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
        # createuser <usuario>
        ```  
        Para sair utilize ``` exit ``` ou pressione Ctrl+D
8. Crie o banco de dados *libraryfree* no seu PostgreSQL local   
        ```
        $ sudo -u <usuario> createdb libraryfree
        ```
9. Instale as dependências  
        ```
        $ flask/bin/pip3 install -r requirements.txt
        ```
10. Aplique as variáveis de ambiente  
        ```
        $ export APP_SETTINGS=config.DevelopmentConfig  
        ```    
        ```
        $ export LIBRARYFREE_DB_URI="postgres:///libraryfree"  
        ```
11. Realizar as *migrations* do banco de dados  
        ```
        $ python3 run.py db init
        ```  
        ```
        $ python3 run.py db migrate
        ```  
        ```
        $ python3 run.py db upgrade  
        ```  
        ```
        $ python3 run.py admin  
        ```  
12. Execute o programa   
        ```
        $ python3 run.py runserver
        ```  
13. Execute o servidor de notificações em outro terminal  
        ```
        $ python3 run.py notify
        ```  
14. Para parar a execução, basta pressionar CTRL+C  
15. Para sair do *virtualenv*  
        ```
        $ deactivate
        ```

Certifique-se de sempre realizar os passos 5 e 10 novamente em execuções futuras.