import customtkinter  # type: ignore
from CTkMessagebox import CTkMessagebox  # type: ignore
from installer import install_sd, install_sovits, install_yolo

TAB2: str = "Tab 2"
VALUE2: str = "Value 2"
APPEARANCE = {"亮": "light", "暗": "dark", "跟随系统": "system"}

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI 一键配置小工具")
        self.geometry(f"{1100}x{580}")
        
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="功能列表", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_1_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_2_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_3_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_4_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="深暗色切换", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["亮", "暗", "跟随系统"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="界面缩放", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # 主界面
        self.widgets: list[customtkinter.CTkBaseClass] = []  # type: ignore
        self.sidebar_button_1_event()
        
        self.sidebar_button_1.configure(text="欢迎")
        self.sidebar_button_2.configure(text="Stable Diffusion")
        self.sidebar_button_3.configure(text="So-VITS-SVC")
        self.sidebar_button_4.configure(text="YOLO v8")
        self.appearance_mode_optionemenu.set("亮")
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(APPEARANCE[new_appearance_mode])

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_1_event(self):
        self.sidebar_button_event()
        self.welcome_first_label = customtkinter.CTkLabel(self, text="欢迎", font=customtkinter.CTkFont(size=48, weight="bold"))
        self.welcome_first_label.grid(row=2, column=3)
        self.widgets.append(self.welcome_first_label)
        self.tips_first_label = customtkinter.CTkLabel(self, text="请在左侧栏中选择一个你需要部署的功能", font=customtkinter.CTkFont(size=16))
        self.tips_first_label.grid(row=4, column=3)
        self.tips_second_label = customtkinter.CTkLabel(self, text="若是用整合包用户，请在各个功能的路径选择中选择当前目录下的 venv", font=customtkinter.CTkFont(size=16))
        self.tips_second_label.grid(row=5, column=3)
        self.widgets.append(self.tips_first_label)
        self.widgets.append(self.tips_second_label)
        
    def sidebar_button_2_event(self):
        self.sidebar_button_event()
        self.sidebar_button_234_event()
        self.start_installation.configure(command=lambda: install_sd(self.r, self.progress_bar, self.progress_label, self))
    
    def sidebar_button_3_event(self):
        self.sidebar_button_event()
        self.sidebar_button_234_event()
        self.start_installation.configure(command=lambda: install_sovits(self.r, self.progress_bar, self.progress_label, self))
        
    def sidebar_button_4_event(self):
        self.sidebar_button_event()
        self.sidebar_button_234_event()
        self.start_installation.configure(command=lambda: install_yolo(self.r, self.progress_bar, self.progress_label, self))
        
    def sidebar_button_234_event(self):
        self.python_path_tips = customtkinter.CTkLabel(self, text="安装目录：", font=customtkinter.CTkFont(size=16))
        self.python_path_tips.grid(row=0, column=1)
        self.widgets.append(self.python_path_tips)
        self.python_path_label = customtkinter.CTkLabel(self, text="未选择", font=customtkinter.CTkFont(size=16))
        self.python_path_label.grid(row=0, column=2)
        self.widgets.append(self.python_path_label)
        self.python_path_btn = customtkinter.CTkButton(self, text="选择", command=self.get_python_path)
        self.python_path_btn.grid(row=0, column=5)
        self.widgets.append(self.python_path_btn)
        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_label = customtkinter.CTkLabel(self, text="0/0")
        self.start_installation = customtkinter.CTkButton(self, text="开始安装/更新")
        self.start_installation.grid(row=5, column=3)
        self.widgets.append(self.start_installation)

    def sidebar_button_event(self):
        for i in self.widgets:
            i.grid_remove()
            
    def get_python_path(self):
        self.r = customtkinter.filedialog.askdirectory(title="安装位置选取")
        if self.r == "":
            CTkMessagebox(title="错误", message="目录不合法！请重新选择", icon="cancel")
            self.get_python_path()
        else:
            self.python_path_label.configure(text=self.r)
        