import tkinter
from tkinter import filedialog
from tkinter import ttk
import os
import win32com.client
import glob
import shutil
import configparser
import ttkthemes

class copyGUI(tkinter.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("copy-json")    # ウィンドウタイトル
        self.master.geometry("300x200") # ウィンドウサイズ(幅x高さ)

        self.jsonDir = []
        self.btn_list = []

        self.telepotspath = ""

        # ツールバー
        frame_toolbar = tkinter.Frame(self.master, bg = "gray90")

        btn_setfolder = tkinter.Button(frame_toolbar, text = "フォルダ選択", command = self.set_telepotspath)
        btn_reload = tkinter.Button(frame_toolbar, text = "更新", command = self.get_jsonDir)

        btn_setfolder.pack(side = tkinter.LEFT, padx = (5, 0)) # 左側だけ隙間を空ける
        btn_reload.pack(side = tkinter.LEFT) # 左側だけ隙間を空ける

        frame_toolbar.pack(fill=tkinter.X) 

        self.frame_button = tkinter.Frame(self.master)
        self.frame_button.pack()

        frame_Progresslabel = tkinter.Frame(self.master)
        self.Progresstext = tkinter.IntVar(value="")
        Progresslabel = ttk.Label(frame_Progresslabel,textvariable=self.Progresstext)
        Progresslabel.pack()
        frame_Progresslabel.pack()

        self.config_ini = configparser.ConfigParser()
        self.config_ini['CONFIG'] = {'telepots path': self.telepotspath}

        if self.config_ini.read('config.ini'):
            section = self.config_ini['CONFIG']
            self.telepotspath = section.get('telepots path')
        else:
            while self.telepotspath == "":
                self.set_telepotspath()

    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config_ini.write(configfile)

    def set_telepotspath(self):
        dialog = filedialog.askdirectory()
        if not dialog == "":
            self.telepotspath = dialog
            self.config_ini['CONFIG']['telepots path'] = dialog
            self.save_config()
        
    def delete(self):

        if not os.path.exists(self.telepotspath + "/"):
            os.mkdir(self.telepotspath + "/")

        file_list = glob.glob(self.telepotspath + '/*.json')

        self.Progresstext.set(self.telepotspath + " のjsonを削除中")

        for file in file_list:
            os.remove(file)

        self.Progresstext.set(self.telepotspath + " のjsonを削除完了")

    def copy_outer(self, path):
        def copy_inner():
            self.delete()

            file_list = glob.glob(path + '/*.json')

            folder_name = path.split("\\")[-1]
            self.Progresstext.set(folder_name + " をコピー中")

            for file in file_list:
                shutil.copy(file, self.telepotspath)

            self.Progresstext.set(folder_name + " のコピーが完了")

        return copy_inner

    def get_jsonDir(self):
        files = os.listdir()
        self.jsonDir = []

        for f in files:
            
            if os.path.isdir(f):
                self.jsonDir.append(f)

            elif f.split(".")[-1] == "lnk":
                wshell = win32com.client.Dispatch("WScript.Shell") # <COMObject WScript.Shell>
                shortcut = wshell.CreateShortcut(f)
                self.jsonDir.append(shortcut.TargetPath)

        for button in self.btn_list:
            button.destroy()

        self.btn_list = []
        lenmax = 0
        for dir in self.jsonDir:

            path = dir
            button_text = path.split("\\")[-1]
            if len(button_text) > lenmax:
                lenmax = len(button_text)

            func = self.copy_outer(path)
            button = tkinter.Button(self.frame_button, text = button_text, command = func)
            button.pack(expand = True, fill = tkinter.BOTH,ipady = 5, pady = 1)
            self.btn_list.append(button)

        self.Progresstext.set("")
        self.master.geometry(f"{10 * lenmax + 10}x{40 * len(self.jsonDir) + 25}")

if __name__ == "__main__":
    root = tkinter.Tk()
    # root = ttkthemes.ThemedTk(theme="blue")
    app = copyGUI(master = root)
    app.get_jsonDir()
    app.mainloop()
    