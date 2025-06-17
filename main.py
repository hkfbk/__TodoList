import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,project_root)
from ExecuterM import Executer



def main():
    app = Executer.init_exe()
    app.exec()

























if __name__ == '__main__':
    main()