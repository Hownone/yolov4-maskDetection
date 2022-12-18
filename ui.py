import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk
from torchvision import transforms as transforms
import os
import cv2
from yolo import YOLO
from PIL import Image
from matplotlib import pyplot as plt
yolo = YOLO()
import tkinter as tk
from tkinter import messagebox as messagebox
import threading
from time import strftime


# 设置图片保存路径
outfile = './out_pic'
video_tmp = "video/video_tmp.jpg"
img_path = video_tmp

# 创建一个界面窗口
win = tkinter.Tk()
win.title("口罩识别")
win.geometry("1280x650")
str="output"+strftime("%Y%m%d%H%M")+".avi"
# 设置全局变量
original = Image.new('RGB', (360, 480))
save_img = Image.new('RGB', (360, 480))
count = 0
img2 = tkinter.Label(win)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(str, fourcc, 13.0, (802, 414))  # 保存视频 ,13为帧率，可以进行修改改为生成的视频与拍摄的视频时间基本一致，802, 414为视频的分辨率可以根据不同的视频进行修改
select_file = ""


# 实现在本地电脑选择图片
def choose_file():
    global select_file
    select_file = tkinter.filedialog.askopenfilename(title='选择图片')
    e.set(select_file)
    load = Image.open(select_file)
    load = transforms.Resize((360, 480))(load)
    # 声明全局变量
    global original
    original = load
    render = ImageTk.PhotoImage(load)

    img = tkinter.Label(win, image=render)
    img.image = render
    img.place(x=100, y=100)

    e.set(select_file)
    img = select_file
    try:
        image = Image.open(img)
    except:
        messagebox.showinfo('提示', '未选择图片')
    else:
        r_image = yolo.detect_image(image)
        r_image = r_image.convert("RGB")
        r_image.save("out_pic/mask.jpg")
        maskimg = cv2.imread("out_pic/mask.jpg", 1)
        maskimg = cv2.cvtColor(maskimg, cv2.COLOR_BGR2RGB)
        maskimg = cv2.resize(maskimg, (480, 360))
        # # cv2.imshow("gray", gray)
        maskimg = Image.fromarray(maskimg)  # 将图像转换成Image对象
        render = ImageTk.PhotoImage(maskimg)
        global img2
        img2.destroy()
        img2 = tkinter.Label(win, image=render)
        img2.image = render
        img2.place(x=700, y=100)


movieLabel = tkinter.Label(win)  # 创建一个用于播放视频的label容器
movieLabel.place(x=100, y=100)

movieLabelimg2 = tkinter.Label(win)  # 创建一个用于播放视频的label容器
movieLabelimg2.place(x=700, y=100)


def open_cam():
    global button_num
    button_num = 3
    video_tmp = "video/video_tmp.jpg"  # 加载路径，导入对象 ，相机采集的照片的临时存储，Yolo对此照片进行识别，
    str = "video/output" + strftime("%Y%m%d%H%M") + ".avi"
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    img_path = video_tmp
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(str, fourcc, 15.0, (640, 480))  # 保存视频 ,16为帧率，可以进行修改改为生成的视频与拍摄的视频时间基本一致
    while (button_num == 3):
        ret, frame = cap.read()
        ##############################################################
        if ret == True:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # 转换颜色使播放时保持原有色彩

            cv2.imwrite(video_tmp, frame)  # 保存相机采集的实时图像图像信息

            img_o = Image.open(img_path)

            img_o = yolo.detect_image(img_o)

            img_o.save("out_pic/result.jpg")
            img2 = cv2.imread("out_pic/result.jpg")
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)  # 转换颜色使播放时保持原有色彩

            out.write(cv2.imread("out_pic/result.jpg"))  # 写入视频

            current_image = Image.fromarray(img).resize((480, 360))  # 将图像转换成Image对象

            current_image2 = Image.fromarray(img2).resize((480, 360))  # 将图像转换成Image对象

            imgtk = ImageTk.PhotoImage(image=current_image)
            movieLabel.imgtk = imgtk
            movieLabel.config(image=imgtk)

            imgtk2 = ImageTk.PhotoImage(image=current_image2)
            movieLabelimg2.imgtk = imgtk2
            movieLabelimg2.config(image=imgtk2)

            cv2.waitKey(15)
            movieLabel.update()  # 每执行以此只显示一张图片，需要更新窗口实现视频播放
            movieLabelimg2.update()  # 每执行以此只显示一张图片，需要更新窗口实现视频播放
        #############################################################

        out.write(cv2.imread("result.jpg"))  # 写入视频

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 显示路径
e = tkinter.StringVar()


# 设置标签分别为原图像和修改后的图像
label1 = tkinter.Label(win, text="原始图像")
label1.place(x=300, y=50)

label2 = tkinter.Label(win, text="识别图像")
label2.place(x=900, y=50)

def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

# 设置选择图片的按钮
button1 = tkinter.Button(win, text="识别图像", command=choose_file,height=1, width=12)
button1.place(x=400, y=530)


# 设置打开摄像头并识别
button3 = tkinter.Button(win, text="打开摄像头并识别", command=lambda: thread_it(open_cam))
button3.place(x=610, y=530)

# 设置退出按钮
button0 = tkinter.Button(win, text="退出", command=win.quit,height=1, width=12)
button0.place(x=810, y=530)
win.mainloop()
