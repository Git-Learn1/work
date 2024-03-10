from ui import App
import sys

def main() -> None:
    app = App()
    app.mainloop()

if __name__ == "__main__":
    print("请勿关闭此窗口！此为程序日志记录处，若程序卡死请观察此处情况！")
    main()
    sys.exit(0)
