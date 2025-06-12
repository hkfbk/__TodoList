import requests as http
from Task import User_task_list, Task
from datetime import datetime
import threading as thd
import simplejson as json

TIME = datetime.now().replace(hour=0, minute=0,second=0,microsecond=0)
Stop = True
def set_stop(b:bool):
    global Stop
    Stop = b
URL:dict[str,str] = None # type: ignore
def init_url():
    with open('url.json',encoding='utf-8') as f:
        global URL
        URL = json.load(f)
def check_today()->dict[str,Task]:
    task:dict[str,Task] = User_task_list.today_task()
    today = {k:task[k] for k in task if task[k].status in ('未开始','推迟')}
    return today

def check_task_time(today:dict[str,Task])->tuple:
    hour = 3600
    min_time = 86400
    now_time = datetime.now() - TIME
    task_list = list()
    for t in today.values():
        ti = ((t.deadline - TIME) - now_time).total_seconds()
        if ti < hour:
            task_list.append(t)
        if ti > hour < min_time:
            min_time = ti    
            
    print(f'暂停{min_time}秒')
    return min_time,task_list







def send_hook(send_task:list[Task]):
    data = {
   "msgtype":"text",
   "text":{
      "content":''
   }}
    at:str = None # type: ignore
    if User_task_list.name == '-all':
        at = '<at user_id=\"-1\">所有人</at>'
    else:
        at = f'<at email=\"{User_task_list.user_id}\">{User_task_list.name}</at>'
    for i in send_task:
        if not i.reminded:
            data['text']['content'] = f'任务提醒!!!\n任务{i.task}\n截止时间:{i.deadline}\n优先级:{i.priority}\n状态:{i.status}\n{at}'
            # print(data)
            i.reminded = True
            http.post(URL['url'],json=data)




def run_client(event:thd.Event):
    init_url()
    target = True
    today:dict[str,Task] = None # type: ignore
    while Stop:
        if target:
            today = check_today()
        time,send_task_list = check_task_time(today)
        if len(send_task_list) > 0:
            send_hook(send_task_list)
        event.clear()
        target = event.wait(time)
            
        
        
        