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
    return {k:task[k] for k in task if task[k].status in ('未开始','推迟') and not task[k].reminded}

def check_task_time(today:dict[str,Task])->tuple:
    hour = 3600
    min_time = 86400
    now_time = datetime.now() - TIME
    task_list = list()
    for t in today.values():
        ti = ((t.deadline - TIME) - now_time).total_seconds()
        if ti <= hour:
            task_list.append(t)
        elif ti < min_time:
            min_time = ti - hour
    print(f'暂停{min_time}秒')
    return min_time,task_list

def send_hook(send_task:list[Task]):
    data = {
   "msgtype":"text",
   "text":{
      "content":''
   }}
    at:str = None # type: ignore
    ret_tasks:list = list()
    # content = '任务提醒!!!\n任务{task}\n截止时间:{deadline}\n优先级:{priority}\n状态:{status}\n{at}'
    if User_task_list.name == '-all':
        at = '<at user_id=\"-1\">所有人</at>'
    else:
        at = f'<at email=\"{User_task_list.user_id}\">{User_task_list.name}</at>'
        
    for i in send_task:
        data['text']['content'] = f'任务提醒!!!\n任务{i.task}\n截止时间:{i.deadline}\n优先级:{i.priority}\n状态:{i.status}\n{at}'
        print(data)
        if http.post(URL['url'],json=data):
            i.reminded = True
        else:
            ret_tasks.append(i)
    return ret_tasks
            
def send_failed(tasks:list[Task]):
    task_str = ''
    for t in tasks:
        task_str += t.task
        task_str+='\n'
    print(f'有{len(tasks)}个任务通知失败\n{task_str},服务器未响应')
    

def run_client(event:thd.Event):
    init_url()
    target = True
    today:dict[str,Task] = None # type: ignore
    global Stop
    while Stop:
        if target:
            today = check_today()
        time,send_task_list = check_task_time(today)
        if len(send_task_list) > 0:
            count = 1
            tasks = send_hook(send_task_list)
            while len(tasks) > 0 and count <3:
                tasks = send_hook(tasks)
                count+=1
            if len(tasks) > 0:
                send_failed(tasks)
        if Stop:
            event.clear()
        target = event.wait(time)
    print('client exit')
     