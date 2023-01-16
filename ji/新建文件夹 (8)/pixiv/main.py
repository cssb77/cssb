import json
import os
import pickle
import sqlite3
import time
import urllib.request
import funcs
import classes
import GUI


class Main:
    def __init__(self):
        self.t = None
        self.network_module = classes.PixivMobilePage()
        try:
            with open('user_info.json', 'rb') as f:
                content = json.load(f)
                self.user_name = content['username']
                self.user_pass = content['password']
                self.user_proxy = content.get(
                    'proxy',
                    urllib.request.getproxies().get('http', None)
                )
        except (EOFError, KeyError, FileNotFoundError, json.decoder.JSONDecodeError) as e:
            funcs.user_info_generate()
            with open('user_info.json', 'rb') as f:
                content = json.load(f)
                self.user_name = content['username']
                self.user_pass = content['password']
                self.user_proxy = content.get(
                    'proxy',
                    urllib.request.getproxies().get('http', None)
                )
        self.app = GUI.App()

    def start_to_run(self):
        login_info = classes.PixivLoginPage(self.user_proxy)
        login_info.login(self.user_name, self.user_pass)

        self.network_module.set_proxy(self.user_proxy)
        self.network_module.set_cookies(login_info.custom_cookie_dict)

        try:
            with open('settings.pck', 'rb') as f:
                temp_dict = pickle.load(f)
                r18_option = temp_dict.get('r18', -1)
                if r18_option != -1:
                    self.app.show_R18 = r18_option
        except FileNotFoundError:
            with open('settings.pck', 'wb'):
                pass
        except EOFError:
            pass

        def t_start(_):
            self.app.load_pics_to_gui()
            self.network_module.set_year()
            if self.t:
                self.network_module.go_ahead = False
                self.t.stop()
            if self.network_module.search_thread:
                self.network_module.search_thread.stop()
            if self.t:
                self.t.join()
            if self.network_module.search_thread:
                self.network_module.search_thread.join()
            self.app.search_keyword = self.app.search_input.get().strip()
            if not self.app.search_keyword:
                return None
            print(f'Starting searching for [{self.app.search_keyword}]...')
            self.network_module.go_ahead = True
            self.network_module.set_search_keyword(self.app.search_keyword)

            with sqlite3.connect('storage.db') as g:
                self.app.get_works_from_db(self.app.search_keyword, 1, g, self.user_proxy)

            self.app.refresh_button.config(state='normal')
            temp_dict_2 = {}
            try:
                with open('settings.pck', 'rb') as g:
                    temp_dict_2 = pickle.load(g)
            except (FileNotFoundError, EOFError):
                pass
            self.network_module.set_year(
                temp_dict_2.get(
                    self.app.search_keyword,
                    (0, time.localtime(time.time()).tm_year)
                )[1])
            self.network_module.is_first_half_year = temp_dict_2.get(
                self.app.search_keyword, (0, 0, False)
            )[2]
            # print(self.network_module.is_first_half_year)
            self.t = classes.StoppableThread(
                self.network_module.get_artworks_from_all_pages,
                (temp_dict_2.get(self.app.search_keyword, (1,))[0],)
            )
            self.t.start()
            self.app.use_auto_refresh(use=True, show_msg=False)

        self.app.search_input.bind(
            '<Return>', t_start
        )

        self.app.load_pics_to_gui()
        self.app.mainloop()

        self.network_module.go_ahead = False
        if getattr(self.t, 'stop', False):
            self.t.stop()


if __name__ == '__main__':
    program = Main()
    program.start_to_run()
