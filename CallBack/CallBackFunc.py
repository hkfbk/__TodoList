from Task import Task,User_task_list #, TaskStartus
from datetime import datetime
import threading as thd
from net import set_stop


Thread_event = thd.Event()

def add_task():
    """添加任务"""
    task_content = input('任务内容:\n')
    while 1:
        try:
            end_time_s =  input('任务截止时间,格式(yyyy-mm-dd hh:mm:ss):\n')#'2025-06-12 14:12:12'
            end_time = datetime.strptime(end_time_s,r'%Y-%m-%d %H:%M:%S')
        except ValueError:
            print('请根据时间格式正确输入时间!!!',end=' ')
    # print(end_time)
    # stauts = '已完成' #TaskStartus(input('任务状态: 未开始, 进行中,  已完成,  推迟\n'))
    while 1:
        stauts = input('任务状态: 未开始, 进行中,  已完成,  推迟\n')
        if stauts in ('未开始', '进行中',  '已完成',  '推迟'):
            break
        else:
            print('请根据提示正确输入任务状态!!!',end=' ')
    while 1:
        try:
            lv = int(input('优先级, 1,2,3,4,5(数字越小优先级越高)\n'))
        except ValueError:
            print('请根据提示正确输入!!!',end=' ')
    begin_time = datetime.now().replace(microsecond=0)
    task = Task(begin_time, end_time, task_content, stauts, lv) # type: ignore
    User_task_list.append_task(task)
    User_task_list.save()
    Thread_event.set()

def cancle_task():
    """取消任务"""
    task_name = input('想要取消的任务(-q退出):\n')
    if task_name == '-q':
        return
    print(User_task_list.cancle_task(task_name=task_name))
    User_task_list.save()
    Thread_event.set()




def ls_task():
    """查看所有任务"""
    show:int = 0
    while 1:
        try:
            show = int(input('请输入查看方式(1:按完成状态排序, 2:按日期排序, 3:默认, 0:退出)\n'))
        except ValueError:
            print('请根据提示正确输入!!!',end=' ')
        else:
            match show:
                case 0:
                    return
                case 1:
                    return User_task_list.show_task_list(True)
                case 2:
                    return User_task_list.show_task_list(False)
                case 3:
                    return User_task_list.show_task_list()
                case _:
                    print('请按照提示正确输入!!!',end=' ')


def quit_exe():
    """退出程序"""
    User_task_list.save()
    set_stop(False)
    Thread_event.set()
    exit()


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
            print('请正确输入状态', end=' ')
            continue
        break
    User_task_list.task_map[task_name].status = status
    User_task_list.save()
    Thread_event.set()
    print('修改完成')