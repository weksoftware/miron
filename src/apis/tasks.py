import aiohttp

from custom_types import (
    Task,
    TaskSatus,
)

API_URL = "https://api.weksoftware.ru/tools/tasks"


class ForbiddenError(Exception):
    pass


class BadRequestError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class IAmATeapotError(Exception):
    pass


class TasksAPIManager:
    @staticmethod
    def raise_error(response: aiohttp.ClientResponse):
        if response.status == 403:
            raise ForbiddenError()
        elif response.status == 400:
            raise BadRequestError()
        elif response.status == 401:
            raise UnauthorizedError()
        elif response.status == 418:
            raise IAmATeapotError()
        
    @staticmethod
    async def get_users_tasks(api_token: str, user_id: int) -> list[Task]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api.php?id={user_id}&token={api_token}") as response:
                TasksAPIManager.raise_error(response)
                
                return await response.json()

    @staticmethod
    async def create_task(api_token: str, user_id: int, text: str, board: str, status: TaskSatus) -> Task: 
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/new.php?user={user_id}&text={text}&board={board}&status={status}&token={api_token}") as response:
                TasksAPIManager.raise_error(response)
                
                return await response.json()

    @staticmethod
    async def update_task_status(api_token: str, user_id: int, task_id: int, status: TaskSatus) -> Task:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/upd.php?user={user_id}&task={task_id}&status={status}&token={api_token}") as response:
                TasksAPIManager.raise_error(response)
                
                return await response.json()

    @staticmethod
    async def delete_task(api_token: str, user_id: int, task_id: int) -> Task:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/del.php?user={user_id}&id={task_id}&token={api_token}") as response:
                TasksAPIManager.raise_error(response)
                
                return await response.json()

