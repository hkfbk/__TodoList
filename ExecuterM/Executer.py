from Task import Task, TaskManager
from datetime import datetime
import threading as thd
import simplejson as json
from net import set_stop, HttpClient

class Executer:

    def __init__(self) -> None:
        self.User_task_list = TaskManager()
        self.Thread_event = thd.Event()
        self.command_map:dict = dict() # type: ignore
        self.http_client = HttpClient(self.User_task_list)
        self.send_thd = thd.Thread(target=self.http_client.run_client, args=(self.Thread_event,))
        
    
    @classmethod
    def init_exe(cls):
        import re
        user_name = input('你的名字是:\n') # 蒋浩祥
        while 1:
            user_id = input('您的邮箱是:\n') # 'jianghaoxiang@kingsoft.com'
            if re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",user_id) is None:
                print('请正确输入邮箱', end=' ')
            else:
                break
        task_list = list()
        try:
            with open('test.json','r',encoding='utf=8') as f:
                task_dict = json.load(f)
                if user_id not in task_dict: # type: ignore
                    task_dict[user_id] = {} # type: ignore
                task_list = task_dict[user_id] # type:ignore
        except FileNotFoundError:
            print('存储文件不存在，存储时将初始化一个新存储文件')
        
        exe = cls()
        exe.User_task_list.load_tasks(task_list) # type: ignore
        exe.User_task_list.set_userinfo(user_name, user_id) # type: ignore
        try:
            exe.send_thd.start()
        except FileNotFoundError as e:
            print(e)
            exe.quit_exe()
        exe.command_map['add'] = exe.add_task
        exe.command_map['ls'] = exe.ls_task
        exe.command_map['cancle'] = exe.cancle_task
        exe.command_map['mark'] = exe.mark_status
        exe.command_map['-q'] = exe.quit_exe
        return exe
    
    def task_distribution(self,task_key:str):
        if task_key in self.command_map:
            self.command_map[task_key]()
        else:
            print('请按照提示正确输入')
        
    def exec(self):
        while 1:
            self.ui()
            arg = input()
            self.task_distribution(arg)
    
    def ui(self):
        print(
        """
        add:    添加任务
        ls:     查看所有任务
        mark:   标记状态
        cancle: 取消任务
        -q:     退出
        """ )
    
    def add_task(self):
        """添加任务"""
        task_content = input('任务内容:\n')
        while 1:
            try:
                end_time_s =  input('任务截止时间,格式(yyyy-mm-dd hh:mm:ss):\n')#'2025-06-12 14:12:12'
                end_time = datetime.strptime(end_time_s,r'%Y-%m-%d %H:%M:%S')
                break
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
                break
            except ValueError:
                print('请根据提示正确输入!!!',end=' ')
        begin_time = datetime.now().replace(microsecond=0)
        task = Task(begin_time, end_time, task_content, stauts, lv) # type: ignore
        self.User_task_list.append_task(task)
        self.User_task_list.save()
        self.Thread_event.set()

    def cancle_task(self):
        """取消任务"""
        task_name = input('想要取消的任务(-q退出):\n')
        if task_name == '-q':
            return
        print(self.User_task_list.cancle_task(task_name=task_name))
        self.User_task_list.save()
        self.Thread_event.set()

    def ls_task(self):
        """查看所有任务"""
        show:int = 0
        while 1:
            try:
                show = int(input('请输入查看方式(1:按完成状态排序, 2:按日期排序, 3:今日任务 0:退出)\n'))
            except ValueError:
                print('请根据提示正确输入!!!',end=' ')
            else:
                match show:
                    case 0:
                        return
                    case 1:
                        return self.User_task_list.show_task_list(True)
                    case 2:
                        return self.User_task_list.show_task_list(False)
                    case 3:
                        return self.User_task_list.show_task_list()
                    case _:
                        print('请按照提示正确输入!!!',end=' ')

    def quit_exe(self):
        """退出程序"""
        if len(self.User_task_list.task_map):
            self.User_task_list.save()
        set_stop(False)
        self.Thread_event.set()
        self.send_thd.join()
        exit()

    def mark_status(self):
        """标记任务状态"""
        task_name:str = ''
        while 1:
            task_name = input('请输入将要标记的任务名(-q退出)\n')
            if task_name == '-q':
                return
            if task_name not in self.User_task_list.task_map:
                print(f'任务{task_name}不存在', end='  ')
                continue
            if self.User_task_list.task_map[task_name].status == '已完成':
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
        self.User_task_list.task_map[task_name].status = status
        self.User_task_list.save()
        self.Thread_event.set()
        print('修改完成')

    
    
    
    
    
