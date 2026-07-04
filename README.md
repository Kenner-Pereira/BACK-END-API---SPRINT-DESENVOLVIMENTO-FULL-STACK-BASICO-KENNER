## Como executar a API do cadastro de usuários da papelaria


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```

--- Para criar o ambiente virtual execute o comando abaixo no terminal CMD

python -m venv venv

--- Depois de instalado , para ativar o ambiente virtual utilize esse comando: 
Quando o ambiente virtual for ativado aparecerá no inicio do endereço do terminal o escrito " (venv) "


venv\Scripts\activate.bat

--- Utilize o comando abaixo para instalar as dependências/bibliotecas, descritas no arquivo `requirements.txt`.


pip install -r requirements.txt

```

Para executar a API  basta executar:

```
flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
flask run --host 0.0.0.0 --port 5000 --reload

```

Abra o [http://localhost:5000/#/] (http://localhost:5000/#/) no navegador para verificar o status da API em execução.
