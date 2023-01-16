import json
import os
import sqlite3
import tkinter as tk
import webbrowser
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from PIL import Image
from PIL import ImageTk
from threading import Lock
from tkinter import ttk
from tkinter import messagebox as msg

import funcs
import classes

LAST_UPDATE = '2021-09-20'
SHORT_WAIT = 2000  # ms
LONG_WAIT = 10000  # ms
GLOBAL_LOCK = Lock()


# Tk.state() normal: 普通 zoomed: 最大化


class App:
    # 构造函数, 一些常量和主窗口在此定义.
    def __init__(self):
        self.orig_content = {}
        if os.path.exists('user_info.json'):
            with open('user_info.json', 'r', encoding='utf-8') as f:
                self.orig_content = json.load(f)
                try:
                    self.height, self.width = self.orig_content['height'], self.orig_content['width']
                    self.pic_size = self.orig_content['pic_size']
                except KeyError:
                    self.height, self.width = 20, 4
                    self.pic_size = 240
                    with open('user_info.json', 'w') as g:
                        self.orig_content['height'], self.orig_content['width'] = self.height, self.width
                        self.orig_content['pic_size'] = self.pic_size
                        json.dump(self.orig_content, g)
        else:
            self.height, self.width = 20, 4
            self.pic_size = 240
            with open('user_info.json', 'wb') as f:
                self.orig_content['height'], self.orig_content['width'] = self.height, self.width
                self.orig_content['pic_size'] = self.pic_size
                json.dump(self.orig_content, f)

        self.works_on_each_page = self.height * self.width

        self.win = tk.Tk()
        self.win.title('Pixiv Crawler')
        self.win.config(background='#787878')
        self.win.geometry(
            f'{21 + self.pic_size * self.width:d}x'
            f'{self.pic_size * self.height:d}'
        )
        self.win.state('zoomed')

        # 0: No R18; 1: Has R18; 2: Only R18
        self.show_R18 = 1
        self.cur = None
        self.db_num = 0
        self.db_num_new = 0
        self.auto_refresh = False
        self.download_thumb_thread = classes.StoppableThread()

        self.search_keyword = None
        self.current_page = 1
        self.total_page = 0

        self.create_widget()

    # 与<Configure>绑定，在绘制Canvas的时候自动调整Canvas的大小以容纳图片.
    def canvas_adjust(self, _):
        self.canvas.config(
            scrollregion=self.canvas.bbox('all'),
            width=self.pic_frame.winfo_width(),
            height=self.pic_frame.winfo_height()
        )
        self.search_input.config(
            width=self.pic_frame.winfo_width()
        )
        self.progress.config(length=self.pic_frame.winfo_width())

    # 拖动滑块时触发的事件, 尚未完成.
    # def scroll_bar_move(self, _):
    #     # print('Drag!')
    #     pass

    # 鼠标滚轮滚动时触发的事件, 暂定为上下滑动页面.
    def scroll_on_frame(self, event):
        # event.delta的符号可以用于判定上滚或下滚
        if event.delta < 0:
            self.canvas.yview_scroll(1, 'units')
        else:
            self.canvas.yview_scroll(-1, 'units')

    # 点击图片跳转到作品所在网址的函数.
    def click(self, x, y, _):
        # _是被传进来的event
        label = self.labels[x][y]
        # NULL是没有pixiv_id属性的
        id_to_get = getattr(label, 'pixiv_id', False)
        if id_to_get:
            webbrowser.open(
                f'https://www.pixiv.net/artworks/{id_to_get:d}'
            )

    def show_about(self):
        msg.showinfo(
            'About Pixiv Crawler',
            f'Written by Endericedragon\n'
            f'Powered by Python\n'
            f'Last update: {LAST_UPDATE:s}'
        )

    def refresh(self, _=0):
        self.__get_total_page()
        if 2 > self.current_page >= self.total_page:
            self.previous_button.config(state='disabled')
            self.next_button.config(state='disabled')
        elif self.current_page < 2:
            self.previous_button.config(state='disabled')
            self.next_button.config(state='enabled')
        elif self.current_page >= self.total_page:
            self.previous_button.config(state='enabled')
            self.next_button.config(state='disabled')
        else:
            self.previous_button.config(state='enabled')
            self.next_button.config(state='enabled')
        if self.current_page > self.total_page > 0:
            self.get_works_from_db(
                self.search_keyword,
                self.total_page,
                self.database_content,
                self.proxy
            )
        else:
            self.get_works_from_db(
                self.search_keyword,
                self.current_page if self.current_page>0 else 1,
                self.database_content,
                self.proxy
            )

    def clear_cache(self):
        try:
            os.remove('settings.pck')
        except FileNotFoundError:
            pass
        file_to_del = os.listdir('thumbs')
        for each in file_to_del:
            os.remove(f'thumbs\\{each:s}')
        msg.showinfo('Clear Cache', 'Clear successful!')

    def r18_off(self):
        self.show_R18 = 0
        funcs.config_settings('r18', 0)
        self.refresh()

    def r18_on(self):
        self.show_R18 = 1
        funcs.config_settings('r18', 1)
        self.refresh()

    def r18_only(self):
        self.show_R18 = 2
        funcs.config_settings('r18', 2)
        self.refresh()

    # 绝大多数控件都在此被定义并放置到主窗口上.
    def create_widget(self):
        # 事件
        self.win.bind('<MouseWheel>', self.scroll_on_frame, add=True)

        # 菜单栏
        self.menubar = tk.Menu(self.win)
        self.win.config(menu=self.menubar)

        self.option_menu = tk.Menu(self.menubar, tearoff=False)
        self.option_menu.add_command(
            label='Auto Refresh On',
            command=lambda _=0: self.use_auto_refresh(True)
        )
        self.option_menu.add_command(
            label='Auto Refresh Off',
            command=lambda _=0: self.use_auto_refresh(False)
        )
        self.option_menu.add_separator()
        self.option_menu.add_command(label='Show All', command=self.r18_on)
        self.option_menu.add_command(label='R18 Only', command=self.r18_only)
        self.option_menu.add_command(label='Hide R18', command=self.r18_off)
        self.option_menu.add_separator()
        self.option_menu.add_command(label='Clear Cache', command=self.clear_cache)

        self.menubar.add_cascade(label='Option', menu=self.option_menu)

        self.about_menu = tk.Menu(self.menubar, tearoff=False)

        self.about_menu.add_command(label='About', command=self.show_about)
        self.about_menu.add_command(
            label='Official Website', command=lambda _=0: webbrowser.open(
                'https://gitee.com/endericedragon'
            )
        )

        self.menubar.add_cascade(label='About', menu=self.about_menu)

        # 搜索框
        self.search_input = tk.Entry(
            self.win,
            font=('Jetbrains Mono', 16),
            relief=tk.SUNKEN, bd=4, justify=tk.CENTER
        )
        # self.search_input.focus_set()
        self.search_input.pack()

        self.refresh_button = tk.Button(
            self.win, state='disabled',
            text='Refresh Manually',
            font=('Jetbrains Mono', 12),
            command=self.refresh,
            width=160
        )
        self.refresh_button.pack()

        # 主框架
        self.main_frame = ttk.Frame(self.win)
        self.main_frame.pack(expand=True)
        # self.main_frame.pack(side=tk.TOP, anchor=tk.N)

        # 顶部框架
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(side=tk.TOP)

        # 搜索框

        self.progress = ttk.Progressbar(self.top_frame)
        self.progress.grid(row=1, column=0, columnspan=3, pady=10)

        self.previous_button = ttk.Button(self.top_frame, text=' <= ')
        self.previous_button.grid(row=2, column=0)

        self.page_indicator = ttk.Label(self.top_frame, text=f'0/0 [mode={self.show_R18:d}]')
        self.page_indicator.grid(row=2, column=1)

        self.next_button = ttk.Button(self.top_frame, text=' => ')
        self.next_button.grid(row=2, column=2)

        self.scroll_bar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(
            self.main_frame, yscrollcommand=self.scroll_bar.set,
        )
        self.scroll_bar.config(command=self.canvas.yview)

        self.pic_frame = tk.Frame(self.canvas)

        self.labels = [
            [tk.Label(self.pic_frame) for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for i in range(self.height):
            for j in range(self.width):
                self.labels[i][j].config(
                    bd=2, relief=tk.GROOVE
                )
                self.labels[i][j].grid(row=i, column=j)
                # 可以认为，partial的参数在传进去的时候就变成了const
                # 所以不会随着i，j的变化而变化
                self.labels[i][j].bind(
                    '<Button-1>', partial(self.click, i, j)
                )

        self.canvas.bind('<Configure>', self.canvas_adjust)
        # self.scroll_bar.bind('<Motion>', self.scroll_bar_move)
        self.scroll_bar.pack(side=tk.RIGHT, fill='y')
        self.canvas.create_window(0, 0, window=self.pic_frame, anchor=tk.NW)
        self.canvas.pack(side=tk.LEFT, fill='both')

    # 从迭代器中获得作品信息，并加载到显示界面上.
    def load_pics_to_gui(self, select_result: list = None):
        x, y = 0, 0
        if select_result:
            for each in select_result:
                setattr(self.labels[x][y], 'pixiv_id', each[0])
                # setattr(self.labels[x][y], 'title', each[1])
                try:
                    pic = Image.open(f'thumbs\\{each[0]:d}.jpg')
                except OSError:
                    # print('\n ', type(e), e)
                    pic = Image.open('empty.jpg')
                    # _thread.start_new_thread(
                    #     funcs.download_thumbnail,
                    #     (each[0], each[2], self.proxy)
                    # )
                pic = pic.resize((self.pic_size, self.pic_size), Image.ANTIALIAS)
                try:
                    if each[4]:
                        # is R18
                        self.labels[x][y].config(
                            text='R-18',
                            compound='top',
                            fg='white',
                            bg='#DB7093',
                            font=('Consolas', 10)
                        )
                    else:
                        self.labels[x][y].config(
                            text='Safe',
                            compound='top',
                            fg='white',
                            bg='#87CEEB'
                        )
                    tk_pic = ImageTk.PhotoImage(image=pic)
                    self.labels[x][y].config(image=tk_pic)
                    setattr(self.labels[x][y], 'image', tk_pic)
                    y += 1
                    if y >= self.width:
                        y = 0
                        x += 1
                    if x >= self.height:
                        return False
                except OSError:
                    print('\nError when loading thumbnail for', each[0])

        pic = Image.open('empty.jpg')
        pic = pic.resize((self.pic_size, self.pic_size), Image.ANTIALIAS)
        while x < self.height:
            # pic = Image.open('empty.jpg')
            tk_pic = ImageTk.PhotoImage(image=pic)
            self.labels[x][y].config(image=tk_pic)
            setattr(self.labels[x][y], 'image', tk_pic)
            setattr(self.labels[x][y], 'pixiv_id', None)
            self.labels[x][y].config(
                text=' ',
                compound='top',
                fg='black',
                bg='white'
            )
            y += 1
            if y >= self.width:
                y = 0
                x += 1

    def __get_total_page(self):
        cursor = self.database_content.cursor()
        search_keyword = self.search_keyword
        try:
            cursor.execute(f'CREATE TABLE [{search_keyword:s}] ('
                           f'    pixiv_id INT NOT NULL UNIQUE PRIMARY KEY,\n'
                           f'    title CHAR(1024) NOT NULL,\n'
                           f'    thumb_url CHAR(2048) NOT NULL,\n'
                           f'    like_num INT, \n'
                           f'    is_R18 INT\n'
                           f')')
            print(f'A new table {search_keyword:s} has been created...', end='')
        except sqlite3.OperationalError:
            pass
        if self.show_R18 == 0:
            temp = cursor.execute(
                f'SELECT COUNT(*)'
                f'  FROM [{search_keyword:s}]'
                f' WHERE is_R18=0'
            )
            self.total_page = [x for x in temp][0][0]
        elif self.show_R18 == 1:
            temp = cursor.execute(
                f'SELECT COUNT(*)'
                f'  FROM [{search_keyword:s}]'
            )
            self.total_page = [x for x in temp][0][0]
        else:
            temp = cursor.execute(
                f'SELECT COUNT(*)'
                f'  FROM [{search_keyword:s}]'
                f' WHERE is_R18=1'
            )
            self.total_page = [x for x in temp][0][0]
        if self.total_page % self.works_on_each_page:
            self.total_page = self.total_page // self.works_on_each_page + 1
        else:
            self.total_page //= self.works_on_each_page

    def refresh_by_db(self):
        if os.path.exists('storage.db'):
            if self.auto_refresh:
                search_keyword = self.search_keyword
                self.db_num_new = [x for x in self.cur.execute(
                    f'SELECT COUNT(*)'
                    f'  FROM [{search_keyword:s}]'
                )][0][0]
                if (self.db_num_new != self.db_num) and (not GLOBAL_LOCK.locked()):
                    self.refresh(False)
                    self.db_num = self.db_num_new
                    self.canvas.after(LONG_WAIT, self.refresh_by_db)
                else:
                    self.canvas.after(SHORT_WAIT, self.refresh_by_db)

    def use_auto_refresh(self, use: bool, show_msg: bool = True):
        if use and (not self.auto_refresh) and show_msg:
            msg.showinfo('Auto Refresh', 'Auto refresh is on.')
        elif (not use) and self.auto_refresh and show_msg:
            msg.showinfo('Auto Refresh', 'Auto refresh is off.')
        self.auto_refresh = use
        if use:
            self.canvas.after(100, self.refresh_by_db)

    def go_to_page(self, page):
        self.next_button.config(state='disabled')
        self.previous_button.config(state='disabled')
        self.__get_total_page()

        self.current_page = self.total_page if page > self.total_page else page
        if self.current_page < 1:
            self.current_page = 1

        self.__get_total_page()
        # f'0/0 [mode={self.show_R18:d}]'
        if self.current_page < 2 and self.current_page >= self.total_page:
            self.previous_button.config(state='disabled')
            self.next_button.config(state='disabled')
        elif self.current_page < 2:
            self.previous_button.config(state='disabled')
            self.next_button.config(state='enabled')
        elif self.current_page >= self.total_page:
            self.previous_button.config(state='enabled')
            self.next_button.config(state='disabled')
        else:
            self.previous_button.config(state='enabled')
            self.next_button.config(state='enabled')
        self.page_indicator.config(
            text=f'{self.current_page:d}/{self.total_page:d} [mode={self.show_R18:d}]'
        )

        search_keyword = self.search_keyword
        targets = []
        if self.show_R18 == 0:
            # The result of selection is as follow:
            # [(pixiv_id, title, thumb_url, like_num, is_R18)]
            targets = self.cur.execute(
                f'SELECT * '
                f'  FROM [{search_keyword:s}] '
                f' WHERE is_R18=0 '
                f' ORDER BY like_num DESC '
                f'LIMIT {(page-1) * self.works_on_each_page:d}, {self.works_on_each_page} '
            )
        elif self.show_R18 == 1:
            targets = self.cur.execute(
                f'SELECT * '
                f'  FROM [{search_keyword:s}] '
                f' ORDER BY like_num DESC '
                f'LIMIT {(page-1) * self.works_on_each_page:d}, {self.works_on_each_page} '
            )
        elif self.show_R18 == 2:
            targets = self.cur.execute(
                f'SELECT * '
                f'  FROM [{search_keyword:s}] '
                f' WHERE is_R18=1 '
                f' ORDER BY like_num DESC '
                f'LIMIT {(page-1) * self.works_on_each_page:d}, {self.works_on_each_page} '
            )
        pics = [x for x in targets]

        if not pics:
            return None

        # TODO
        self.previous_button.config(
            command=lambda x=0: self.go_to_page(page - 1)
        )
        self.next_button.config(
            command=lambda x=0: self.go_to_page(page + 1)
        )
        self.progress['maximum'] = self.works_on_each_page
        self.progress['value'] = 0

        def temp_func():
            flush_key = True
            page_before_start = self.current_page
            GLOBAL_LOCK.acquire()
            with ThreadPoolExecutor(max_workers=16) as p:
                tasks = [p.submit(
                    funcs.download_thumbnail,
                    each[0], each[2], self.proxy
                ) for each in pics]
                i = 0
                # 在这个for阻塞了
                for _ in as_completed(tasks):
                    i += 1
                    self.progress['value'] = i
                    self.progress.update()
                    if not i % 15:
                        if page_before_start == self.current_page:
                            self.load_pics_to_gui(pics)
                        else:
                            flush_key = False
                            if GLOBAL_LOCK.locked():
                                GLOBAL_LOCK.release()
            if flush_key:
                self.progress['value'] = self.works_on_each_page
                self.load_pics_to_gui(pics)
                if GLOBAL_LOCK.locked():
                    GLOBAL_LOCK.release()

        self.download_thumb_thread = classes.StoppableThread(temp_func)
        self.download_thumb_thread.start()

    def get_works_from_db(
            self, search_keyword: str = '',
            page: int = 1,
            database_content: sqlite3.Connection = None,
            proxy: str = ''):
        if not search_keyword:
            print('Empty search keyword!')
            return None
        elif not database_content:
            print('Empty database connection!')
            return None

        self.search_keyword = search_keyword
        self.current_page = page
        self.proxy = proxy
        self.database_content = database_content
        self.cur = database_content.cursor()

        self.__get_total_page()
        # f'0/0 [mode={self.show_R18:d}]'
        if page < 2 and page >= self.total_page:
            self.previous_button.config(state='disabled')
            self.next_button.config(state='disabled')
        elif page < 2:
            self.previous_button.config(state='disabled')
            self.next_button.config(state='enabled')
        elif page >= self.total_page:
            self.previous_button.config(state='enabled')
            self.next_button.config(state='disabled')
        else:
            self.previous_button.config(state='enabled')
            self.next_button.config(state='enabled')
        self.page_indicator.config(text=f'{page:d}/{self.total_page:d} [mode={self.show_R18:d}]')

        targets = []
        if self.show_R18 == 0:
            # The result of selection is as follow:
            # [(pixiv_id, title, thumb_url, like_num, is_R18)]
            targets = self.cur.execute(
                f'SELECT * '
                f'  FROM [{search_keyword:s}] '
                f' WHERE is_R18=0 '
                f' ORDER BY like_num DESC '
                f'LIMIT {(page-1) * self.works_on_each_page:d}, {self.works_on_each_page} '
            )
        elif self.show_R18 == 1:
            targets = self.cur.execute(
                f'SELECT * '
                f'  FROM [{search_keyword:s}] '
                f' ORDER BY like_num DESC '
                f'LIMIT {(page-1) * self.works_on_each_page:d}, {self.works_on_each_page} '
            )
        elif self.show_R18 == 2:
            targets = self.cur.execute(
                f'SELECT * '
                f'  FROM [{search_keyword:s}] '
                f' WHERE is_R18=1 '
                f' ORDER BY like_num DESC '
                f'LIMIT {(page-1) * self.works_on_each_page:d}, {self.works_on_each_page} '
            )
        pics = [x for x in targets]
        if not pics:
            return None

        # TODO
        self.previous_button.config(
            command=lambda x=0: self.go_to_page(page - 1)
        )
        self.next_button.config(
            command=lambda x=0: self.go_to_page(page + 1)
        )
        self.progress['maximum'] = self.works_on_each_page
        self.progress['value'] = 0

        def temp_func():
            GLOBAL_LOCK.acquire()
            with ThreadPoolExecutor(max_workers=16) as p:
                if proxy:
                    tasks = [p.submit(
                        funcs.download_thumbnail,
                        each[0], each[2], proxy
                    ) for each in pics]
                else:
                    tasks = [p.submit(
                        funcs.download_thumbnail,
                        each[0], each[2]
                    ) for each in pics]
                i = 0
                # 在这个for阻塞了
                for _ in as_completed(tasks):
                    i += 1
                    self.progress['value'] = i
                    self.progress.update()
                    if not i % 15:
                        self.load_pics_to_gui(pics)
            self.progress['value'] = self.works_on_each_page
            self.load_pics_to_gui(pics)
            if GLOBAL_LOCK.locked():
                GLOBAL_LOCK.release()

        self.download_thumb_thread = classes.StoppableThread(temp_func)
        self.download_thumb_thread.start()

    # 调用Tk()的mainloop
    def mainloop(self):
        self.win.mainloop()
