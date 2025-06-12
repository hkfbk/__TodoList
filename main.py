import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,project_root)
import simplejson as json
from Task import User_task_list
from net import run_client
import threading as thd
from time import sleep
from CallBack import add_task, cancle_task, ls_task, quit_exe, mark_status,Thread_event
COMMAND_MAP:dict = dict() # type: ignore



def init():
    user_name = '蒋浩祥'#input('你的名字是:\n')
    user_id = 'jianghaoxiang@kingsoft.com'#input('您的id是:\n')
    User_task_list.set_userinfo(user_name, user_id)
    with open('test.json',encoding='utf=8') as f:
        tasks = json.load(f)[User_task_list.user_id]
        User_task_list.load_task(tasks)
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
        return

def main():
    init()
    send_thd = thd.Thread(target=run_client, args=(Thread_event,))
    send_thd.start()
    while 1:
        ui()
        arg = input()
        if arg not in ('add','ls','cancle','mark','-q'):
            print('请根据提示正确输入')
            sleep(1)
            continue
        task_distribution(arg)
    send_thd.join()
















if __name__ == '__main__':
    main()