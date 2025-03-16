# Miron bot
> Discord bot that works with stuff from tools.weksoftware

## Features
- Tasks management

## Usage
### With uv
1. Install [uv](https://github.com/astral-sh/uv/)
2. Clone this repo
3. Copy `.env.example` to `.env` and fill it with your data
4. Launch bot with `uv run start`

### With docker compose
1. Install [docker](https://docs.docker.com/get-started/get-docker/)
2. Clone this repo
3. Copy `.env.example` to `.env` and fill it with your data
4. Launch bot with `docker compose up`

## Commands
### tasks
#### view
**Usage:** `tasks view [user:user] [--private=yes] [--board=board]`\
**Description:** Shows tasks for user. Available only to bot owners (OWNER_IDS in .env)

#### my
**Usage:** `tasks my [--private=yes] [--board=board]`\
**Description:** Shows your tasks.

#### create
**Usage:** `tasks create [text:string] [board:string] [status:string]`\
**Description:** Creates task.

#### update
**Usage:** `tasks update [task_id:integer] [status:string]`\
**Description:** Updates task.

#### delete
**Usage:** `tasks delete [task_id:integer]`\
**Description:** Deletes task.

### ping
**Usage:** `ping`\
**Description:** Shows bot latency and memory usage.

