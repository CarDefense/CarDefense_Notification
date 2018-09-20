# CarDefense Notification

![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Django Rest](https://img.shields.io/badge/django--rest--framework-3.7.7-orange.svg)
![Python](https://img.shields.io/badge/python-3.6-ff69b4.svg)

## Microsserviço de gerenciamento de notificações

O microsserviço de notificações é utilizado no aplicativo CarDefense para gerenciar o envio e recebimento de notificações dentro da aplicação.

## Instalação 

### Requisitos 
Para instalação do projeto você deve ter instalado:
* Docker
* Docker Compose

### Como instalar

1 - Clone o repositório

2 - Entre na pasta do projeto

3 - Rode o comando:
```
sudo docker-compose up
```
4 - Acesse localhost:8000

Para acessar o container da aplicação use o seguinte comando:
```
sudo docker exec -it cardefensenotification_web_1 bash
```

Para ver todos os containers rodando na sua máguina use o seguinte comando:

```
sudo docker ps
```

## Outros microsserviços 
* [CarDefense Profile](https://github.com/CarDefense/CarDefense_Profile)
* [CarDefense Cars](https://github.com/CarDefense/CarDefense_Cars)
* [CarDefense Gamification](https://github.com/CarDefense/CarDefense_Gamification)