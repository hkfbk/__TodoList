from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
import simplejson as json

LOCALDATA:str = 'test.json'

class TaskStartus(Enum):
    E_STARTED = '未开始'
    E_START = '进行中'
    E_FINISHED = '已完成'
    E_DELAY = '推迟'

@dataclass
class Task:
    """
    任务数据类型
    """
    create_time:datetime # 任务创建时间
    deadline:datetime    # 截止时间
    task:str        # 任务内容
    status:str     # 状态：未开始， 进行中， 已完成， 推迟
    priority:int    # 优先级

class UserTaskList:
    """
    任务列表
    """
    
    def __init__(self) -> None:
        self.task_list:list[Task] = list() # 任务列表
        self.name:str = None # type: ignore
        self.user_id:str = None # type: ignore
    
    def set_userinfo(self,name:str, user_id:str) -> None:
        self.name = name # 任务负责人
        self.user_id = user_id # 任务负责人id
    
    
    def load_task(self, L:list[dict]):
        for d in L:
            task = Task(d['create_time'], datetime.strptime(d['deadline'],'%Y-%m-%d %H:%M:%S'), 
                        d['task'],d['status'], d['priority'])
            self.task_list.append(task)
    
    def append_task(self, task:Task):
        self.task_list.append(task)
    
    def save(self):
        data_list = list()
        for task in self.task_list:
            # print(task.task)
            data_list.append({'create_time':str(task.create_time), 'deadline':str(task.deadline), 
                              'task':task.task, 'status':str(task.status), 'priority':task.priority})
        with open(LOCALDATA, 'r', encoding='utf-8') as rf:
            json_obj = json.load(rf)
            json_obj[self.name] = data_list
            with open(LOCALDATA, 'w', encoding='utf-8') as wf:
                # print(json_obj)
                json.dump(json_obj,wf,ensure_ascii=False,indent=4)
            
    
    def __str__(self) -> str:
        return f'user:{self.name}, id{self.user_id}, task list{{{self.task_list}}}'

    
    
        


# User_task_list:UserTaskList = UserTaskList()




    

























 