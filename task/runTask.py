from .rebuildLLM import TaskLLm
from .task import Task

task = Task()
taskstartllm = TaskLLm()


llmTast:list =[
        {
        "fonction": taskstartllm.lineareregretionTaine,
        "name": "Lineare Regretion Traine",
        "misfire_grace_time": 100,
        "interval": "cron",
        "minutes": 1,
        "activate": True,
        "cron_params": {
            "day": "*",
            "month": "*",
            "hour": "00",
            "minute": "59"
        },
    },
        {
        "fonction": taskstartllm.sgdregretionTaine,
        "name": "sgd Regretion Traine",
        "misfire_grace_time": 100,
        "interval": "cron",
        "minutes": 1,
        "activate": True,
        "cron_params": {
            "day": "*",
            "month": "*",
            "hour": "00",
            "minute": "59"
        },
    },
        {
        "fonction": taskstartllm.retraineKeras,
        "name": "Keras Traine",
        "misfire_grace_time": 100,
        "interval": "cron",
        "minutes": 1,
        "activate": True,
        "cron_params": {
            "day": "*",
            "month": "*",
            "hour": "00",
            "minute": "59"
        },
    },
]

task.add_job(llmTast)

