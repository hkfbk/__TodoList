import requests as http
from Task import  Task
from datetime import datetime
import threading as thd
import simplejson as json

DATE = datetime.now().replace(hour=0, minute=0,second=0,microsecond=0)
Stop = True
def set_stop(b:bool):
    global Stop
    Stop = b
URL:dict[str,str] = None # type: ignore
def init_url():
    try:
        with open('url.json',encoding='utf-8') as f:
            global URL
            URL = json.load(f)
    except FileNotFoundError:
        set_stop(False)
        raise FileNotFoundError('url.json config file not found')

class HttpClient:
    def __init__(self, user_task_list) -> None:
        self.User_task_list = user_task_list
    
    def run_client(self,event:thd.Event):
        init_url()
        target = True
        today:dict[str,Task] = None # type: ignore
        global Stop
        while Stop:
            if target:
                today = self.check_today()
            time,send_task_list = self.check_task_time(today)
            if len(send_task_list) > 0:
                count = 1
                tasks = self.send_hook(send_task_list)
                while len(tasks) > 0 and count <3:
                    tasks = self.send_hook(tasks)
                    count+=1
                if len(tasks) > 0:
                    self.send_failed(tasks)
            if Stop:
                event.clear()
            target = event.wait(time)
        print('client exit')
    
    def send_failed(self,tasks:list[Task]):
        task_str = ''
        for t in tasks:
            task_str += t.task
            task_str+='\n'
        print(f'有{len(tasks)}个任务通知失败\n{task_str}服务器未响应')

    def send_hook(self,send_task:list[Task]):
        data = {
    "msgtype":"text",
    "text":{
        "content":''
    }}
        at:str = None # type: ignore
        ret_tasks:list = list()
        if self.User_task_list.name == '-all':
            at = '<at user_id=\"-1\">所有人</at>'
        else:
            at = f'<at email=\"{self.User_task_list.user_id}\">{self.User_task_list.name}</at>'
            
        for i in send_task:
            data['text']['content'] = f'任务提醒!!!\n任务{i.task}\n截止时间:{i.deadline}\n优先级:{i.priority}\n状态:{i.status}\n{at}'
            # print(data) # 测试用
            if http.post(URL['url'],json=data):
                i.reminded = True
            else:
                ret_tasks.append(i)
        return ret_tasks

    def check_task_time(self,today:dict[str,Task])->tuple:
        hour = 3600
        min_time = 86400
        now_time = datetime.now() - DATE
        task_list = list()
        for t in today.values():
            ti = ((t.deadline - DATE) - now_time).total_seconds()
            if 0 < ti <= hour:
                task_list.append(t)
            elif ti < min_time:
                min_time = ti - hour
        min_time = min_time if min_time < hour else hour
        print(f'暂停{min_time}秒')
        return min_time,task_list

    def check_today(self)->dict[str,Task]:
        task:dict[str,Task] = self.User_task_list.today_tasks()
        return {k:task[k] for k in task if task[k].status in ('未开始','推迟') and not task[k].reminded}



