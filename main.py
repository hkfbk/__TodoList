import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,project_root)
import simplejson as json
from Task import User_task_list, UserTaskList

from CallBack import add_task, cancle_task, ls_task, quit_exe, mark_finish
COMMAND_MAP:dict = dict()
def init():
    user_name = 'jiang' #input('你的名字是:\n')
    user_id = 'jiang' #input('您的id是:\n')
    User_task_list.set_userinfo(user_name, user_id)
    COMMAND_MAP['add'] = add_task
    COMMAND_MAP['ls'] = ls_task
    COMMAND_MAP['cancle'] = cancle_task
    COMMAND_MAP['mark'] = mark_finish
    COMMAND_MAP['-q'] = quit_exe


def ui():
    print(
    """
    add:    添加任务
    ls:     查看所有任务
    mark:   标记完成
    remove: 删除任务
    cancle: 取消任务
    -q:     退出
    """ )

def task_distribution(task_key:str):
    if task_key in COMMAND_MAP:
        COMMAND_MAP[task_key]()
    else:
        print('error')

def main():
    init()
    from datetime import datetime

    with open('test.json',encoding='utf=8') as f:
        tasks = json.load(f)[User_task_list.name]
        User_task_list.load_task(tasks)
    add_task()
    User_task_list.save()
    print(User_task_list)
    
    # while 1:
    #     ui()
    #     task_distribution(input())
    
    
    
    
    
    
    # d = datetime.now().replace(microsecond=0)
    # sd = str(d)
    # print(sd)
    # print(datetime.fromisoformat(sd))
















if __name__ == '__main__':
    main()