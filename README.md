# Web XPL Bot

Bot de reconhecimento de informações para Discord, desenvolvido em Python como projeto acadêmico de Cybersecurity.

## Objetivo

O projeto tem como objetivo automatizar algumas etapas básicas de reconhecimento, permitindo que ferramentas e serviços de consulta sejam utilizados diretamente por meio de comandos no Discord.

O bot recebe comandos enviados pelos usuários, processa os parâmetros informados, executa a ferramenta ou consulta correspondente e retorna os resultados de forma organizada no Discord.

As consultas devem ser utilizadas somente em domínios, endereços IP e hosts para os quais o usuário tenha autorização para realizar testes.

## Arquitetura

O projeto é dividido em três partes principais:

- `bot.py`: responsável pela inicialização do bot, registro dos comandos e comunicação com o Discord.
- `commands/`: contém os módulos responsáveis pela execução de cada funcionalidade de reconhecimento.
- `tests/`: contém scripts utilizados para testar individualmente os módulos durante o desenvolvimento.

O fluxo básico de execução é:

1. O usuário envia um comando no Discord.
2. O `bot.py` recebe o comando e seus parâmetros.
3. O comando realiza validações básicas dos dados recebidos.
4. O módulo correspondente em `commands/` executa a consulta ou ferramenta.
5. O resultado é processado pelo bot.
6. O resultado é enviado de volta ao usuário no Discord.

### Fluxo simplificado

```text
Usuário
   │
   │ Comando /parâmetro
   ▼
Discord
   │
   ▼
bot.py
   │
   ├── ipinfo.py ──► ipinfo.io
   │
   ├── gau.py ─────► GAU
   │
   ├── nmap.py ────► Nmap
   │
   ├── whois.py ───► WHOIS
   │
   └── crt.py ─────► crt.sh (módulo implementado, não integrado)
   │
   ▼
Resultado formatado
   │
   ▼
Discord
```

## Tecnologias utilizadas

### Linguagem

- **Python 3.14.4**: linguagem utilizada no desenvolvimento do bot e dos módulos de integração.

### Bibliotecas Python

- **discord.py**: utilizada para criar o bot, registrar os comandos slash e interagir com a API do Discord.
- **python-dotenv**: utilizada para carregar variáveis de ambiente armazenadas no arquivo `.env`.
- **aiohttp**: utilizada para realizar requisições HTTP assíncronas aos serviços externos.

### Ferramentas externas

- **Nmap**: utilizado para realizar uma varredura básica de portas e serviços.
- **GAU (GetAllUrls)**: utilizado para coletar URLs públicas associadas a um domínio.
- **WHOIS**: utilizado para consultar informações de registro de domínios.

### Serviços externos

- **ipinfo.io**: utilizado para consultar informações relacionadas a endereços IP.
- **crt.sh**: utilizado pelo módulo `crt.py` para consulta de certificados e identificação de possíveis subdomínios.
- **Discord**: plataforma utilizada como interface para interação com o bot.

## Estrutura do projeto

```text
web-xpl-bot/
├── bot.py
├── commands/
│   ├── crt.py
│   ├── gau.py
│   ├── ipinfo.py
│   ├── nmap.py
│   └── whois.py
├── tests/
│   ├── test_cert_module.py
│   ├── test_crt.py
│   ├── test_gau.py
│   ├── test_ipinfo.py
│   └── test_whois.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```
### Arquivos principais

- `bot.py`: arquivo principal responsável pela inicialização do bot e definição dos comandos Discord.
- `commands/ipinfo.py`: realiza consultas de informações sobre endereços IP utilizando o serviço ipinfo.io.
- `commands/gau.py`: executa o GAU para coletar URLs públicas associadas a um domínio.
- `commands/nmap.py`: executa uma varredura básica utilizando o Nmap.
- `commands/whois.py`: executa consultas WHOIS e processa as informações retornadas.
- `commands/crt.py`: módulo desenvolvido para consultar certificados no crt.sh; implementado, porém não integrado aos comandos finais do bot devido à indisponibilidade do serviço durante os testes.
- `tests/`: contém scripts utilizados durante o desenvolvimento para validar individualmente as funcionalidades.
- `.env`: armazena o token do Discord e outras informações de configuração que não devem ser incluídas no código-fonte.
- `.gitignore`: define arquivos e diretórios que não devem ser versionados.
- `requirements.txt`: lista as dependências Python utilizadas pelo projeto.
- `README.md`: documentação do projeto.

## Instalação e configuração

### Pré-requisitos

O projeto foi desenvolvido e testado em uma máquina virtual com Ubuntu 26.04 LTS.

São necessários:

* Python 3.14 ou superior;
* `pip`;
* `venv`;
* Go;
* Nmap;
* WHOIS;
* uma aplicação/bot criado no Discord;
* token do bot e ID do servidor Discord.

### 1. Criar o ambiente Python

Após criar ou obter o projeto, entre no diretório:

```bash
cd ~/web-xpl-bot
```

Crie um ambiente virtual Python:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

As bibliotecas Python utilizadas são instaladas automaticamente a partir do arquivo `requirements.txt`.

### 2. Instalar as ferramentas externas

O projeto utiliza algumas ferramentas externas que não são instaladas pelo `pip`.

#### Nmap

O Nmap pode ser instalado utilizando o gerenciador de pacotes do Ubuntu:

```bash
sudo apt update
sudo apt install nmap
```

Após a instalação, é possível verificar a versão instalada:

```bash
nmap --version
```

#### WHOIS

O utilitário WHOIS também pode ser instalado pelo gerenciador de pacotes:

```bash
sudo apt install whois
```

A instalação pode ser verificada com:

```bash
whois --version
```

#### Go

O Go é necessário para instalar o GAU. Após instalar o Go, verifique a versão:

```bash
go version
```

#### GAU

Com o Go configurado, o GAU pode ser instalado utilizando:

```bash
go install github.com/lc/gau/v2/cmd/gau@latest
```

Após a instalação, verifique se o executável está disponível:

```bash
~/go/bin/gau --version
```
Caso o diretório ~/go/bin esteja configurado no PATH, também é possível utilizar:

gau --version

O módulo commands/gau.py tenta localizar automaticamente o executável gau pelo PATH. Caso não seja encontrado, utiliza o diretório padrão ~/go/bin/gau.

Dessa forma, o código não depende de um caminho absoluto específico ou do nome do usuário utilizado no sistema.

### 3. Configurar o Discord

Para utilizar o bot, é necessário criar uma aplicação no Discord Developer Portal, adicionar um bot à aplicação e instalá-lo no servidor desejado.

O bot deve possuir as permissões necessárias para:

* enviar mensagens;
* utilizar comandos slash.

O projeto utiliza duas variáveis de ambiente:

* `DISCORD_TOKEN`: token de autenticação do bot;
* `GUILD_ID`: ID do servidor Discord onde os comandos serão sincronizados.

Crie o arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN=SEU_TOKEN_AQUI
GUILD_ID=SEU_ID_DO_SERVIDOR
```

O arquivo `.env` não deve ser compartilhado ou versionado, pois contém informações de configuração sensíveis. Ele está incluído no `.gitignore` do projeto.

Após configurar o arquivo `.env`, o bot pode ser iniciado com:

```bash
python3 bot.py
```

Se a configuração estiver correta, o terminal exibirá os comandos sincronizados e o bot ficará disponível no servidor Discord configurado.

## Comandos disponíveis

O bot disponibiliza os seguintes comandos no Discord:

### `/ping`

Verifica se o bot está funcionando corretamente.

```text
/ping
```

Resposta esperada:

```text
Pong! 🏓
```

### `/ipinfo`

Consulta informações relacionadas a um endereço IP utilizando o serviço `ipinfo.io`.

```text
/ipinfo 8.8.8.8
```

O resultado pode apresentar informações como:

* endereço IP;
* hostname;
* organização;
* cidade;
* região;
* país;
* timezone.

O comando realiza uma validação básica para verificar se o valor informado possui formato válido de endereço IP.

### `/gau`

Executa o GAU para coletar URLs públicas associadas a um domínio.

```text
/gau example.com
```

O comando apresenta a quantidade de URLs encontradas e exibe parte dos resultados diretamente no Discord.

O módulo utiliza o provedor `urlscan` para realizar a consulta.

### `/nmap`

Executa uma varredura básica utilizando o Nmap.

```text
/nmap 127.0.0.1
```

O resultado apresenta as informações retornadas pelo Nmap, incluindo portas e serviços identificados durante a varredura.

### `/whois`

Realiza uma consulta WHOIS para obter informações de registro de um domínio.

```text
/whois example.com
```

O comando processa as informações retornadas e apresenta dados como:

* domínio;
* registrador;
* data de criação;
* data de atualização;
* data de expiração;
* DNSSEC;
* servidores DNS.

### `/crt`

O projeto possui um módulo para consulta de certificados utilizando o `crt.sh`.

Entretanto, durante os testes finais, o serviço externo apresentou indisponibilidade e retornou respostas HTTP `502`. Por esse motivo, o módulo `crt.py` foi mantido no projeto, mas o comando não foi integrado à versão final do bot.

## Tratamento de erros

O bot possui validações e tratamento básico de erros para evitar que entradas inválidas ou falhas externas interrompam sua execução.

Entre os casos tratados estão:

* endereço IP inválido no comando `/ipinfo`;
* domínio inválido no comando `/gau`;
* host não encontrado ou inacessível durante uma consulta com `/nmap`;
* falha na execução de ferramentas externas;
* ausência de resultados em consultas;
* indisponibilidade de serviços externos.

Quando uma entrada não é válida ou uma consulta não pode ser realizada, o bot retorna uma mensagem informando o problema ao usuário em vez de encerrar sua execução.

Algumas operações que podem levar mais tempo, como `/gau`, `/nmap` e `/whois`, utilizam respostas assíncronas do Discord para evitar que o usuário fique sem retorno enquanto a consulta está sendo processada.

Além disso, operações externas possuem limites de tempo em determinadas consultas, evitando que processos demorados permaneçam executando indefinidamente.

## Testes

Durante o desenvolvimento, os módulos foram testados individualmente antes da integração com o bot do Discord.

Os testes estão organizados no diretório `tests/`:

* `test_ipinfo.py`: valida a consulta de informações de endereços IP.
* `test_gau.py`: valida a execução do GAU e o tratamento dos resultados.
* `test_whois.py`: valida a execução e o processamento das respostas WHOIS.
* `test_crt.py`: utilizado para validar a consulta ao `crt.sh`.
* `test_cert_module.py`: utilizado durante os testes do módulo de certificados.

Após os testes individuais, os comandos integrados ao bot foram testados diretamente no Discord.

Foram validados:

```text
/ping
/ipinfo 8.8.8.8
/gau example.com
/nmap 127.0.0.1
/whois example.com
```

Também foram realizadas consultas com entradas inválidas para verificar o comportamento do tratamento de erros.


