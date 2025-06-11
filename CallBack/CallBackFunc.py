from Task import Task, TaskStartus,User_task_list
from datetime import datetime

def add_task():
    """添加任务"""
    task_content = input('任务内容:\n')
    end_time_s = input('任务截止时间,格式(yyyy-mm-dd hh:mm:ss):\n')
    end_time = datetime.strptime(end_time_s,'%Y-%m-%d %H:%M:%S')
    stauts = TaskStartus(input('任务状态: 未开始, 进行中,  已完成,  推迟'))
    lv = int(input('优先级, 1,2,3,4,5'))
    begin_time = datetime.now().replace(microsecond=0)
    task = Task(begin_time, end_time, task_content, stauts, lv)
    User_task_list.append_task(task)
    
    print('add')

def cancle_task():
    """取消任务"""
    print('cancle')

def ls_task():
    """查看所有任务"""
    print('all')


def quit_exe():
    """退出程序"""
    print('quit')


def mark_finish():
    """标记已完成"""
    print('finish')