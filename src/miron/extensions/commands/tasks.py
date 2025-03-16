import os
import disnake
from disnake.ext import commands

from custom_types import (
    AnyBot,
    Task,
    TaskSatus
)
from apis import (
    TasksAPIManager,
    ForbiddenError,
    BadRequestError,
    IAmATeapotError,
)
from utils import EmbedHelper

STATUS_EMOJIES: dict[TaskSatus, str] = {
    "0": "<:utka_secret:1082255548923252746>",
    "1": "<:olegi_matrix:1116274001329799200>",
    "2": "<:utka:1081946997222809610>"
}
STATUS_MEANINGS: dict[TaskSatus, str] = {
    "0": "Существует",
    "1": "В работе",
    "2": "Сделано"
}
STATUS_CHOICES: dict[str, TaskSatus] = {
    "Существует": "0",
    "В работе": "1",
    "Сделано": "2",
}


class TasksCommand(commands.Cog):
    def __init__(self, bot: AnyBot):
        self.bot = bot
        self.tasks_api_token = os.environ["TASKS_API_TOKEN"]
    
    def format_task(self, task: Task) -> str:
        return (
            f"### {STATUS_EMOJIES[task['status']]} {task['text']}\n"
            f"**Доска**: `{task['board']}`\n"
            f"**Статус**: `{STATUS_MEANINGS[task['status']]}`\n"
            f"**ID**: {task['id']}"
        )

    @commands.slash_command(name="tasks")
    async def tasks(self, _inter: disnake.AppCmdInter):
        pass
    
    @tasks.sub_command(
        name="view",
        description="Показать чужие задачи",
        options=[
            disnake.Option(
                name="user",
                description="Пользователь",
                type=disnake.OptionType.user,
                required=True,
            ),
            disnake.Option(
                name="private",
                description="Отправить приватное сообщение?",
                choices=[
                    disnake.OptionChoice(name="Да", value="yes"),
                    disnake.OptionChoice(name="Нет", value="no"),
                ],
                required=False,
                type=disnake.OptionType.string,
            ),
            disnake.Option(
                name="board",
                description="Название доски",
                type=disnake.OptionType.string,
                max_length=255,
                required=False,
            ),
        ]
    )
    async def view_tasks(
        self,
        inter: disnake.AppCmdInter,
        user: disnake.User,
        private: str = "yes",
        board: str | None = None,
    ):
        if inter.author.id not in inter.bot.owner_ids:
            await inter.send(
                embed=disnake.Embed(
                    color=EmbedHelper.red_color(),
                    title="🚫 Ошибка",
                    description="Эта команда доступна только для администраторов бота",
                ),
                ephemeral=True
            )
            return
        
        bool_private = private == "yes"
        
        await inter.response.defer(ephemeral=bool_private)
        
        try:
            tasks = await TasksAPIManager.get_users_tasks(self.tasks_api_token, user.id)
        except Exception as e:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Ошибка при получении задач: {e}")
            return
        
        if board is not None:
            tasks = [task for task in tasks if task["board"] == board]
        
        if len(tasks) == 0 and board is not None:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> У {user.name} нет задач на доске `{board}`")
            return
        elif len(tasks) == 0:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> У {user.name} нет задач")
            return
        
        embed_title = f"🦆 Задачи {user.name}"
        
        if len(tasks) <= 15:
            embed = disnake.Embed(
                color=EmbedHelper.transparent_color(),
                title=embed_title,
                description="\n\n".join([self.format_task(task) for task in tasks]),
            )
            await inter.edit_original_response(embed=embed)
            return

        for i in range(0, len(tasks), 15):
            embed = disnake.Embed(
                color=EmbedHelper.transparent_color(),
                title=embed_title,
                description="\n\n".join([self.format_task(task) for task in tasks[i:i+15]]),
            )
            
            if i == 0:
                await inter.edit_original_response(embed=embed)
                continue
            
            await inter.send(embed=embed, ephemeral=bool_private)
    
    @tasks.sub_command(
        name="my",
        description="Показать задачи",
        options=[
            disnake.Option(
                name="private",
                description="Отправить приватное сообщение?",
                choices={"Да": "yes", "Нет": "no"}, 
                required=False,
            ),
            disnake.Option(
                name="board",
                description="Название доски",
                type=disnake.OptionType.string,
                max_length=255,
                required=False,
            ),
        ]
    )
    async def my_tasks(
        self,
        inter: disnake.AppCmdInter,
        private: str = "yes",
        board: str | None = None,
    ):
        bool_private = private == "yes"
        
        await inter.response.defer(ephemeral=bool_private)
        
        try:
            tasks = await TasksAPIManager.get_users_tasks(self.tasks_api_token, inter.user.id)
        except Exception as e:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Ошибка при получении задач: {e}")
            return
        
        if board is not None:
            tasks = [task for task in tasks if task["board"] == board]

        if len(tasks) == 0 and board is not None:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> У тебя нет задач на доске `{board}`")
            return
        elif len(tasks) == 0:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> У тебя нет задач")
        
        embed_title = f"🦆 Задачи {inter.author.name}"
        
        if len(tasks) <= 15:
            embed = disnake.Embed(
                color=EmbedHelper.transparent_color(),
                title=embed_title,
                description="\n\n".join([self.format_task(task) for task in tasks]),
            )
            await inter.edit_original_response(embed=embed)
            return

        for i in range(0, len(tasks), 15):
            embed = disnake.Embed(
                color=EmbedHelper.transparent_color(),
                title=embed_title,
                description="\n\n".join([self.format_task(task) for task in tasks[i:i+15]]),
            )
            
            if i == 0:
                await inter.edit_original_response(embed=embed)
                continue
            
            await inter.send(embed=embed, ephemeral=bool_private)

    @tasks.sub_command(
        name="create",
        description="Создать задачу",
        options=[
            disnake.Option(
                name="text",
                description="Текст задачи",
                type=disnake.OptionType.string,
                max_length=255,
                required=True,
            ),
            disnake.Option(
                name="board",
                description="Название доски",
                type=disnake.OptionType.string,
                max_length=255,
                required=True,
            ),
            disnake.Option(
                name="status",
                description="Статус задачи",
                choices=STATUS_CHOICES,
                required=True,
            ),
        ]
    )
    async def create_task(
        self,
        inter: disnake.AppCmdInter,
        text: str,
        board: str,
        status: TaskSatus,
    ):
        await inter.response.defer(ephemeral=True)
        
        try:
            task = await TasksAPIManager.create_task(self.tasks_api_token, inter.user.id, text, board, status)
        except Exception as e:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Ошибка при создании задачи: {e}")
            return
        
        embed = disnake.Embed(
            color=EmbedHelper.transparent_color(),
            title="🦆 Задача создана!",
            description=self.format_task({ "id": task["id"], "text": task["text"], "board": task["board"], "status": task["status"] }),
        )
        
        await inter.edit_original_response(embed=embed)
    
    @tasks.sub_command(
        name="update",
        description="Обновить задачу",
        options=[
            disnake.Option(
                name="task_id",
                description="ID задачи",
                type=disnake.OptionType.integer,
                min_value=1,
                required=True,
            ),
            disnake.Option(
                name="status",
                description="Новый статус задачи",
                choices=STATUS_CHOICES,
                required=True,
            ),
        ]
    )
    async def update_task(
        self,
        inter: disnake.AppCmdInter,
        task_id: int,
        status: TaskSatus,
    ):
        await inter.response.defer(ephemeral=True)
        
        try:
            task = await TasksAPIManager.update_task_status(self.tasks_api_token, inter.user.id, task_id, status)
        except BadRequestError:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Задачи с ID `{task_id}` не существует")
            return
        except ForbiddenError:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Вы не можете обновлять чужие задачи!")
            return
        except IAmATeapotError:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> У данной задачи уже указан статус `{STATUS_MEANINGS[status]}`")
            return
        except Exception as e:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Ошибка при обновлении задачи: {e}")
            return
        
        embed = disnake.Embed(
            color=EmbedHelper.transparent_color(),
            title="🦆 Задача обновлена!",
            description=self.format_task({ "id": task["id"], "text": task["text"], "board": task["board"], "status": task["status"] }),
        )
        
        await inter.edit_original_response(embed=embed)
    
    @tasks.sub_command(
        name="delete",
        description="Удалить задачу",
        options=[
            disnake.Option(
                name="task_id",
                description="ID задачи",
                type=disnake.OptionType.integer,
                min_value=1,
                required=True,
            ),
        ]
    )
    async def delete_task(
        self,
        inter: disnake.AppCmdInter,
        task_id: int,
    ):
        await inter.response.defer(ephemeral=True)
        
        try:
            task = await TasksAPIManager.delete_task(self.tasks_api_token, inter.user.id, task_id)
        except BadRequestError:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Задачи с ID `{task_id}` не существует")
            return
        except ForbiddenError:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Вы не можете удалять чужие задачи!")
            return
        except Exception as e:
            await inter.edit_original_response(f"<:utka_zloj:1110624872687747102> Ошибка при удалении задачи: {e}")
            return
        
        embed = disnake.Embed(
            color=EmbedHelper.transparent_color(),
            title="🦆 Задача удалена!",
            description=self.format_task({ "id": task["id"], "text": task["text"], "board": task["board"], "status": task["status"] }),
        )
        
        await inter.edit_original_response(embed=embed)


def setup(bot: commands.InteractionBot):
    bot.add_cog(TasksCommand(bot))
