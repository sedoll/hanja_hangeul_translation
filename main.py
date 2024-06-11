import easyocr # 문자 인식 라이브러리
import hanja # 한자 to 한글 번역 라이브러리
import tkinter.messagebox as msgbox # 메세지 박스
import tkinter as tk # 파이썬 gui
from tkinter import ttk
from tkinter import filedialog
from tkinter import Text
from tkinter import Radiobutton

# 파일 경로를 저장할 전역 변수
file_path = ""

def info():
    msgbox.showinfo("알림", "번역이 완료되었습니다.")

def warn():
    msgbox.showwarning("경고", "파일을 선택해주세요")

def error():
    msgbox.showerror("에러", "에러가 발생했습니다.")

def select_file():
    global file_path
    
    # 파일 다이얼로그를 통해 파일 선택
    file_path = filedialog.askopenfilename()
    if file_path:
        # 파일 경로를 출력
        print(f"Selected file: {file_path}")
        # 파일 경로를 라벨에 표시
        file_label.config(text=f"{file_path}")
    else:
        # 파일을 선택하지 않았을 때
        print("No file selected.")
        file_label.config(text="No file selected")
        file_path = ""
    return file_path

def button_disabled():
    select_button.config(state="disabled")  # 버튼 비활성화
    translate_button.config(state="disabled")  # 버튼 비활성화

def button_normal():
    select_button.config(state="normal")  # 버튼 활성화
    translate_button.config(state="normal")  # 버튼 비활성화

def ocr(img_url):
    button_disabled()
    
    if(img_url == ''):
        warn()
        button_normal()
        return False
    try:
        # 어떤 텍스트를 추출할 건지 선언
        # https://www.jaided.ai/easyocr/
        reader = None

        # False CPU, True GPU
        if gpu_choice.get() == 0:
            gpu = False
        else:
            gpu = True
        
        reader = easyocr.Reader(['ch_tra', 'en'], gpu) # 중국어 번체, 영어
        run_label.config(text='20')
        
        # 이미지 내의 텍스트를 list 형태로 추출
        with open(img_url, "rb") as f:
            img = f.read()
        run_label.config(text='40')
        
        # 추출된 정보중에 글자만 한 개의 list 형태로 return
        extract = reader.readtext(img, detail = 0, paragraph=True)
        print(type(extract)) # 타입 list
        run_label.config(text='60')
        
        res = ''.join(extract) # list를 str 형식으로 변환
        print(hanja.translate(res, 'combination-text')) # 출력
        res_txt.delete("1.0", tk.END) # 기존 텍스트 삭제
        res_txt.insert(tk.END, hanja.translate(res, 'combination-text')) # text창에 글자 추가
        # res_label.config(text=f"{hanja.translate(res, 'combination-text')}")
        run_label.config(text='100')
        info()
        button_normal()
        return True
    except:
        error()
        button_normal()
        return False

# 기본 tkinter 윈도우 생성
root = tk.Tk()
root.title("한자 번역 프로그램")
root.geometry("800x600")

# ttk 스타일 적용
style = ttk.Style(root)
style.theme_use("clam")

# 파일 선택 버튼
select_button = ttk.Button(root, text="파일 선택", command=select_file)
select_button.grid(row=0, column=0, columnspan=3, pady=20, padx=10, sticky="ew")

# 파일 경로 표시 라벨
file_info_lab = ttk.Label(root, text='파일 경로', font=(None, 10))
file_info_lab.grid(row=1, column=0, padx=10, pady=10, sticky="w")
file_label = ttk.Label(root, text="파일이 선택되지 않았습니다.", font=(None, 12))
file_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

# 라디오 버튼
gpu_choice = tk.IntVar()
gpu_choice.set(0)  # 초기값 설정

radio1 = Radiobutton(root, text="CPU", variable=gpu_choice, value=0)
radio1.grid(row=2, column=0, padx=10, pady=10, sticky="w")

radio2 = Radiobutton(root, text="GPU", variable=gpu_choice, value=1)
radio2.grid(row=2, column=1, padx=10, pady=10, sticky="w")

guide_label = ttk.Label(root, text="엔비디아 그래픽카드가 있는 경우 GPU, 없으면 CPU를 선택해주세요.", font=(None, 12))
guide_label.grid(row=2, column=2, pady=10, padx=10, sticky="ew")

# 번역 버튼
translate_button = ttk.Button(root, text="번역", command=lambda: ocr(file_path))
translate_button.grid(row=3, column=0, columnspan=3, pady=20, padx=10, sticky="ew")

# 진행률
run_info_lab = ttk.Label(root, text='진행률', font=(None, 10))
run_info_lab.grid(row=4, column=0, padx=10, pady=10, sticky="w")
run_label = ttk.Label(root, text="0", font=(None, 12))
run_label.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="w")

# 결과
res_info_lab = ttk.Label(root, text='결과', font=(None, 10))
res_info_lab.grid(row=5, column=0, padx=10, pady=10, sticky="w")
res_txt = Text(root, width=80, height=20, font=(None, 20))
res_txt.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# 행과 열에 비례하여 확장 가능하게 설정
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

# tkinter 메인 루프 시작
root.mainloop()