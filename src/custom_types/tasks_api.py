import typing

type TaskSatus = typing.Literal["0", "1", "2"]


class Task(typing.TypedDict):
    id: int
    text: str
    board: str
    status: TaskSatus

