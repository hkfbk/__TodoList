from Task import Task, TaskStartus,User_task_list
from datetime import datetime

def add_task():
    """添加任务"""
    task_content = input('任务内容:\n')
    end_time_s = '2025-12-12 12:12:12' #input('任务截止时间,格式(yyyy-mm-dd hh:mm:ss):\n')
    end_time = datetime.strptime(end_time_s,r'%Y-%m-%d %H:%M:%S')
    print(end_time)
    stauts = '已完成' #TaskStartus(input('任务状态: 未开始, 进行中,  已完成,  推迟\n'))
    lv = int('1') #int(input('优先级, 1,2,3,4,5\n'))
    begin_time = datetime.now().replace(microsecond=0)
    task = Task(begin_time, end_time, task_content, stauts, lv)
    User_task_list.append_task(task)

def cancle_task():
    """取消任务"""
    task_name = input('想要取消的任务(-q退出):\n')
    if task_name == '-q':
        return
    print(User_task_list.cancle_task(task_name=task_name))




def ls_task():
    """查看所有任务"""
    print('all')


def quit_exe():
    """退出程序"""
    User_task_list.save()
    exit()
    print('quit')


def mark_status():
    """标记任务状态"""
    task_name:str = ''
    while 1:
        task_name = input('请输入将要标记的任务名(-q退出)\n')
        if task_name == '-q':
            return
        if task_name not in User_task_list.task_map:
            print(f'任务{task_name}不存在', end='  ')
            continue
        if User_task_list.task_map[task_name].status == '已完成':
            print(f'任务{task_name}已完成')
            return
        break
    status:str = ''
    while 1:
        status = input('任务类型:进行中, 已完成, 推迟  (-q退出)\n')
        if status == '-q':
            return
        if status not in ('进行中', '已完成', '推迟'):
            print('请正确输入状态', end='  ')
            continue
        break
    User_task_list.task_map[task_name].status = status
    print('修改完成')