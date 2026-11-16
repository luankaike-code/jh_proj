# PROJ_JH

O backend para o projeto escolar para a escola José Henrique de Paula e Silva.

Esse backend conta com uma API e banco de dados para gerenciamento de login, biblioteca e achados-e-perdidos

## Requisitos

- ter o poetry e python instalados
- ter um banco de dados compativel com o MariaDB 13.2.0 rodando na porta 3306.
	- por padrão, os requisitos abaixo devem ser cumpridos. Você pode mudar-los em `./src/db/.env`
		- ter um banco de dados nomeado como "jh_db"
		- possuir um usuário chamado "user", com sua senha sendo "password"

## Preparar o ambiente

`poetry install`

## rodar o programa

`poetry run python src/proj_jh`