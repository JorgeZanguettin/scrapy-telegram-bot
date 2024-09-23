# TelegramBOT - Scrapy Pipeline Stats for AWS Lambda

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [AWS Deploy](#aws-deploy)
  - [Telegram Settings](#telegram-settings)

## About the Project

**[PT]** Projeto desenvolvido com o propósito de disponibilizar a integração de um projeto Scrapy com um BOT do Telegram, a fim de receber os **stats** das Spiders após a execução.

**[EN]** Project developed with the purpose of providing the integration of a Scrapy project with a Telegram BOT, in order to receive the **stats** of the Spiders after execution.

### Built With

- [Python](https://www.python.org/)
    - [Scrapy](https://docs.scrapy.org/en/latest/)
    - [Requests](https://requests.readthedocs.io/en/latest/)
- [Github Workflows](https://docs.github.com/en/actions)
- [TelegramBOT API](https://core.telegram.org/bots)


### Prerequisites

- Python 3.10
- PIP (Python package manager)

### Installation

1. **[PT]** Clone o repositório: | **[EN]** Clone the repository:
    ```bash
    git clone https://github.com/jorgezanguettin/scrapy-telegram-bot.git
    ```
2. **[PT]** Navegue para o diretório do projeto: | **[EN]**  Navigate to the project directory:
    ```bash
    cd scrapy-telegram-bot
    ```
3. **[PT]** Crie um ambiente virtual: | **[EN]** Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. **[PT]** Instale as dependencias: | **[EN]** Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### AWS Deploy

**[PT]**

Para configurar seu Github, você precisa previamente ter um acesso e credenciais na AWS e também
um ChatBOT criado no Telegram.

1. Crie um fork deste repositório e adicione os seguintes **[secrets](https://docs.github.com/pt/actions/security-guides/using-secrets-in-github-actions)**:
    - **AWS_ACCESS_KEY_ID** - Access Key da sua AWS
    - **AWS_SECRET_ACCESS_KEY** - Secret Key da sua AWS
    - **AWS_REGION** - Regiao da sua AWS
    - **CHAT_ID** - ID do seu CHAT no com o seu ChatBOT do Telegram
    - **TELEGRAM_TOKEN** - Token do seu ChatBOT do Telegram.
2. Execute o Workflow **deploy_lambda.yml**
3. Pronto! O Workflow deve dar conta de configurar o restante.


**[EN]**

To set up your Github, you must first have access and credentials to AWS salso a 
ChatBOT created on Telegram.

1. Fork this repository and add the following **[secrets](https://docs.github.com/pt/actions/security-guides/using-secrets-in-github-actions)**:
    - **AWS_ACCESS_KEY_ID** - Your AWS access key
    - **AWS_SECRET_ACCESS_KEY** - Your AWS secret key
    - **AWS_REGION** - Your AWS region
    - **CHAT_ID** - ID of your CHAT with your Telegram ChatBOT
    - **TELEGRAM_TOKEN** - Token for your Telegram ChatBOT.
2. Run the **deploy_lambda.yml** workflow
3. Done! The Workflow must have a configuration account for the remainder.


### Telegram Settings

**[PT]**

1. Na sua AWS, acesse o AWS Lambda que foi criado pelo Github Workflow e copie sua **invoke url**
2. Configure a Webhook URL do seu TelegramBOT através desta chamada HTTP:
    ```
    https://api.telegram.org/bot{my_bot_token}/setWebhook?url={invoke_url}
    ```
3. Pronto! Seu BOT esta configurado para enviar mensagens utilizando seu Pipeline Scrapy.
4. Em seu projeto Scrapy, adicione o seguinte Pipeline em seu **pipelines.py**
    ``` python
    class TelegramStatsPipeline:
        def close_spider(self, spider):
            stats = spider.crawler.stats.get_stats()

            spider.logger.info('Spider closed: %s' % spider.name)

            requests.post(
                "aws_lambda_invoke_url_here",
                headers={
                    'Content-Type': 'application/json'
                },
                json={
                    "spider": spider.name,
                    "stats": json.dumps(stats, indent=4, sort_keys=True, default=str)
                }
            )
    ```
5. Ative o Pipeline em seu **settings.py**
    ``` python
    ITEM_PIPELINES = {
        "project.pipelines.TelegramStatsPipeline": 300,
    }
    ```
6. Pronto! Agora suas Spiders podem ser monitoradas diretamente pelo Telegram.

**[EN]**

1. On your AWS, access the AWS Lambda that was created by Github Workflow and copy its **invoke url**
2. Configure your TelegramBOT's Webhook URL through this HTTP call:
    ```
    https://api.telegram.org/bot{my_bot_token}/setWebhook?url={invoke_url}
    ```
3. Done! Your BOT is configured to send messages using your Scrapy Pipeline.
4. In your Scrapy project, add the following Pipeline in your **pipelines.py**
    ``` python
    class TelegramStatsPipeline:
        def close_spider(self, spider):
            stats = spider.crawler.stats.get_stats()

            spider.logger.info('Spider closed: %s' % spider.name)

            requests.post(
                "aws_lambda_invoke_url_here",
                headers={
                    'Content-Type': 'application/json'
                },
                json={
                    "spider": spider.name,
                    "stats": json.dumps(stats, indent=4, sort_keys=True, default=str)
                }
            )
    ```
5. Activate Pipeline in your **settings.py**
    ``` python
    ITEM_PIPELINES = {
        "project.pipelines.TelegramStatsPipeline": 300,
    }
    ```
6. Done! Now your Spiders can be monitored directly via Telegram.

