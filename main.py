import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,project_root)
import simplejson as json
from Task import User_task_list
from net import run_client
import threading as thd
from CallBack import add_task, cancle_task, ls_task, quit_exe, mark_status,Thread_event
COMMAND_MAP:dict = dict() # type: ignore



def init():
    import re
    user_name = input('你的名字是:\n') # 蒋浩祥
    while 1:
        user_id = input('您的邮箱是:\n') # 'jianghaoxiang@kingsoft.com'
        if re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",user_id) is None:
            print('请正确输入邮箱', end=' ')
        else:
            break
    User_task_list.set_userinfo(user_name, user_id) # type: ignore
    try:
        with open('test.json','r',encoding='utf=8') as f:
            task_dict = json.load(f)
            if user_id not in task_dict: # type: ignore
                task_dict[user_id] = {} # type: ignore
            User_task_list.load_tasks(task_dict[user_id]) # type: ignore
    except FileNotFoundError:
        print('存储文件不存在，将初始化一个新存储文件')
    COMMAND_MAP['add'] = add_task
    COMMAND_MAP['ls'] = ls_task
    COMMAND_MAP['cancle'] = cancle_task
    COMMAND_MAP['mark'] = mark_status
    COMMAND_MAP['-q'] = quit_exe


def ui():
    print(
    """
    add:    添加任务
    ls:     查看所有任务
    mark:   标记状态
    cancle: 取消任务
    -q:     退出
    """ )

def task_distribution(task_key:str):
    if task_key in COMMAND_MAP:
        COMMAND_MAP[task_key]()
    else:
        print('请按照提示正确输入')

def main():
    init()
    send_thd = thd.Thread(target=run_client, args=(Thread_event,))
    send_thd.start()
    while 1:
        ui()
        arg = input()
        task_distribution(arg)
    send_thd.join()
















if __name__ == '__main__':
    main()