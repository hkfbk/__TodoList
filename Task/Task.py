from dataclasses import dataclass
from datetime import datetime
# from enum import Enum
import simplejson as json
import threading as thd

LOCALDATA:str = 'test.json'

# class TaskStartus(Enum):
#     E_STARTED = '未开始'
#     E_START = '进行中'
#     E_FINISHED = '已完成'
#     E_DELAY = '推迟'

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
    reminded:bool = False
    
    def __str__(self) -> str:
        return f'''
    创建时间:{self.create_time},截止时间:{self.deadline},
    内容:{self.task}, 
    执行状态:{self.status}, 优先级:{self.priority}
    '''

class UserTaskList:
    """
    任务列表
    """
    
    def __init__(self) -> None:
        self.task_map:dict[str,Task] = dict() # 任务列表
        self.name:str = None # type: ignore
        self.user_id:str = None # type: ignore
        self.lock = thd.Lock() # 与发送通知的的线程存在竞争访问，加锁保护
    
    def set_userinfo(self,name:str, user_id:str) -> None:
        self.name = name # 任务负责人
        self.user_id = user_id # 任务负责人id
    
    
    def load_task(self, L:list[dict]):
        for d in L:
            task = Task(d['create_time'],
                         datetime.strptime(d['deadline'],r'%Y-%m-%d %H:%M:%S'), 
                        d['task'],d['status'], d['priority'])
            # print(task)
            self.task_map[d['task']] = task
    
    def append_task(self, task:Task):
        with self.lock:
            self.task_map[task.task] = task
        
    
    def cancle_task(self, task_name:str)->str | None:
        if task_name not in self.task_map:
            return f'任务:{task_name}不存在'
        if self.task_map[task_name].status in ('已完成','进行中'):
            return '该任务正在进行中或已完成'
        with self.lock:
            del self.task_map[task_name]
            return '成功取消'

    
    def today_task(self):
        today = datetime.now().date()
        with self.lock:
            return {k:self.task_map[k] for k in self.task_map if self.task_map[k].deadline.date() == today}
    def show_task_list(self, show_way:bool = None): # type: ignore
        """展示任务列表, show_way控制展示方式

        Args:
            show_way (bool, optional):  True为按完成状态排序;\n
                                        False为按日期排序;\n
                                        None为按优先级排序,优先级相等时即将结束的任务优先. \n
                                        默认为 None.\n
        """
        pre = None
        if show_way is None:
            pre = lambda task:(task[1].priority, task[1].deadline)
        elif show_way:
            pre = lambda task:task[1].status
        else:
            pre = lambda task:task[1].deadline
        today_task = self.today_task()
        new_list = sorted(today_task.items(), key=pre)
        for L in new_list:
            print(L[1])
    
    
    
    
    
    
    def save(self):
        data_list = list()
        # data_list.append({'user_name':self.name})
        for task in self.task_map.values():
            # print(task.task)
            data_list.append({'create_time':str(task.create_time), 
                              'deadline':str(task.deadline), 
                              'task':task.task, 'status':str(task.status), 
                              'priority':task.priority})
        try:
            with open(LOCALDATA, 'r', encoding='utf-8') as rf:
                json_obj = json.load(rf)
                json_obj[self.user_id] = data_list
        except FileNotFoundError:
            json_obj = dict()
            json_obj[self.user_id] = data_list
        with open(LOCALDATA, 'w', encoding='utf-8') as wf:
            # print(json_obj)
            json.dump(json_obj,wf,ensure_ascii=False,indent=4)
            
    
    def __str__(self) -> str:
        return f'user:{self.name}, id{self.user_id}, task list{{{self.task_map}}}'

    
    
        


User_task_list:UserTaskList = UserTaskList()




    

























 