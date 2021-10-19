from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
#from kivy.core.window import Window
from kivy.factory import Factory
import math
from time import sleep
from threading import Thread
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
import os
from pytube import Playlist, YouTube
from jnius import autoclass

Environment = autoclass('android.os.Environment')
SD_CARD = Environment.getExternalStorageDirectory()

#Window.size = (432, 888)
performance_schema = []
to_configure = []
configured = []
id_number = 0
performance_start_TF = False
end = True
music_tf = False
sheldule_once = True
index_in_schema = 0
next_music = 0


class MainWindow(Screen):
    stopplay_icon = ObjectProperty(None)
    scheldule_screen = ObjectProperty(None)
    menu_button = ObjectProperty(None)
    display_time = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__()
        self.ml = Thread(target=self.music_length)
        self.ml.start()

    def scheldule_add(self):
        global id_number, to_configure, index_in_schema, sheldule_once, performance_schema
        if sheldule_once:
            for _ in range(20):
                i = performance_schema[index_in_schema]
                roundedlabel = Factory.RoundedLabel(cols=1, spacing=-30, size_hint=(0.9, self.parent.height), size_hint_max_y=self.parent.height/6, size_hint_min_y=self.parent.height/6)
                roundedlabel.ids.roundedlabel_row1.text = f'[b]{i}[/b]'
                self.scheldule_screen.ids[f'{id_number}'] = roundedlabel
                self.scheldule_screen.add_widget(roundedlabel)
                to_configure.append([id_number, i])
                index_in_schema += 1
                if index_in_schema > len(performance_schema)-1:
                    index_in_schema = 0
                id_number += 1
                sheldule_once = False

    def music_length(self):
        global sound
        while end:
            sleep(0.2)
            if 'sound' in globals():
                self.display_time.text = f'{math.floor(sound.get_pos())}/{math.floor(sound.length)}'

    def performance_start(self):
        global performance_start_TF
        if hasattr(self.scheldule_screen.ids, '0'):
            if self.scheldule_screen.ids['0'].ids.roundedlabel_row3.text != 'Brak Utworu' and self.scheldule_screen.ids['0'].ids.roundedlabel_row2.text != 'Brak Wykonawcy' and performance_start_TF == False:
                self.t = Thread(target=self.musicscheldule)
                self.t.start()
                performance_start_TF = True

    def add_music(self):
        self.add_music_pop = add_music_popup(self)
        self.add_music_pop.open()

    def add_user(self):
        self.add_user_pop = add_user_popup(self)
        self.add_user_pop.open()

    def open_next_music_pop(self):
        global next_music
        if self.scheldule_screen.children:
            if self.scheldule_screen.ids[f"{next_music+1}"].ids.roundedlabel_row3.text != 'Brak Utworu' and self.scheldule_screen.ids[f"{next_music+1}"].ids.roundedlabel_row2.text != 'Brak Wykonawcy':
                if 'sound' in globals():
                    self.next_music_pop = next_music_popup(self)
                    self.next_music_pop.open()

    def open_create_schema(self):
        self.create_schema_pop = create_schema_popup(self)
        self.create_schema_pop.open()

    def open_popup_to_sign_in(self):
        if self.scheldule_screen.children:
            self.popup = sign_to_list(self)
            self.popup.open()

        '''
        for i in range(len(to_configure)):
            if to_configure[i][1] == "Wachlarze" and to_configure[i] not in configured:
                self.scheldule_screen.ids[f'{to_configure[i][0]}'].ids.roundedlabel_row1.text = 'huj'
                configured.append(to_configure[i])
                break

    '''
    def menu_drop(self):
        if not hasattr(self, 'Menu_Dropdown'):
            self.Menu_Dropdown = Menu_Dropdown(self)
            self.menu_button.bind(on_press=self.Menu_Dropdown.open)
    def stop_start(self):
        if 'sound' in globals():
            if sound.state == 'stop':
                sound.play()
                self.stopplay_icon.source = 'stop.png'
                try:
                    sound.seek(when_stopped)
                except Exception:
                    pass
            else:
                when_stopped = sound.get_pos()
                self.stopplay_icon.source = 'play.png'
                sound.stop()

    def musicscheldule(self):
        global when_stopped,sound,end,index_in_schema,performance_schema,to_configure,id_number,next_music
        if hasattr(self.scheldule_screen.ids, '0'):
                if self.scheldule_screen.ids['0'].ids.roundedlabel_row3.text != 'Brak Utworu' and self.scheldule_screen.ids['0'].ids.roundedlabel_row2.text != 'Brak Wykonawcy':
                    sound = SoundLoader.load(f'{SD_CARD}\\Lake_of_fire\\Users\\{self.scheldule_screen.ids["0"].ids.roundedlabel_row2.text}\\{self.scheldule_screen.ids["0"].ids.roundedlabel_row3.text}')
                    sound.volume = 0
                    sound.play()
                    for _ in range(300):
                        sleep(0.01)
                        sound.volume += 0.0033
                    sound.volume = 1
                    while end:
                        sleep(0.4)
                        if math.floor(sound.length)<math.floor(sound.get_pos())+5 :
                            for _ in range(300):
                                sleep(0.01)
                                sound.volume -= 0.0033
                            sound.stop()
                            self.scheldule_screen.remove_widget(self.scheldule_screen.ids[f'{next_music}'])
                            roundedlabel = Factory.RoundedLabel(cols=1, spacing=-30, size_hint=(0.9, self.parent.height), size_hint_max_y=self.parent.height / 6, size_hint_min_y=self.parent.height / 6)
                            i = performance_schema[index_in_schema]
                            roundedlabel.ids.roundedlabel_row1.text = f'[b]{i}[/b]'
                            self.scheldule_screen.ids[f'{id_number}'] = roundedlabel
                            self.scheldule_screen.add_widget(roundedlabel)
                            to_configure.append([id_number, i])
                            index_in_schema += 1
                            if index_in_schema > len(performance_schema) - 1:
                                index_in_schema = 0
                            id_number += 1
                            next_music +=1
                            if self.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row3.text == 'Brak Utworu' and self.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row2.text == 'Brak Wykonawcy':
                                while self.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row3.text == 'Brak Utworu' and self.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row2.text == 'Brak Wykonawcy':
                                    if end == False:
                                        break
                                    sleep(0.1)
                            sound = SoundLoader.load(f'{SD_CARD}\\Lake_of_fire\\Users\\{self.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row2.text}\\{self.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row3.text}')
                            sound.play()
                            sound.volume = 0
                            for _ in range(300):
                                sleep(0.01)
                                sound.volume += 0.0033
                            sound.volume = 1

class create_schema_popup(Popup):
    def __init__(self, main_screen, **kwargs):
        super(create_schema_popup, self).__init__(**kwargs)
        self.main_screen = main_screen
        self.content = GridLayout(rows=2)
        self.title = 'Tworzenie Schematu Występu'
        self.title_align = 'center'

        self.contentup = GridLayout(rows=10, size_hint=(1, 0.8))
        self.input_eq_1 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5, font_size='20sp')
        self.input_eq_2 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_3 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_4 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_5 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_6 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_7 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_8 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_9 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')
        self.input_eq_10 = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5,
                                    font_size='20sp')

        self.contentup.add_widget(self.input_eq_1)
        self.contentup.add_widget(self.input_eq_2)
        self.contentup.add_widget(self.input_eq_3)
        self.contentup.add_widget(self.input_eq_4)
        self.contentup.add_widget(self.input_eq_5)
        self.contentup.add_widget(self.input_eq_6)
        self.contentup.add_widget(self.input_eq_7)
        self.contentup.add_widget(self.input_eq_8)
        self.contentup.add_widget(self.input_eq_9)
        self.contentup.add_widget(self.input_eq_10)

        self.contentdown = GridLayout(cols=2, size_hint=(1, 0.2))

        self.save_button = Button(text='Save', size_hint=(200, 100), size_hint_max_y=100)
        self.save_button.bind(on_press=self.save)

        self.cancel_button = Button(text='Cancel', size_hint=(200, 100), size_hint_max_y=100)
        self.cancel_button.bind(on_press=self.cancel)

        self.contentdown.add_widget(self.save_button)
        self.contentdown.add_widget(self.cancel_button)

        self.content.add_widget(self.contentup)
        self.content.add_widget(self.contentdown)

    def save(self, *args):
        global performance_schema
        for child in reversed(self.contentup.children):
            if child.text == '':
                break
            performance_schema.append(child.text)

        self.main_screen.scheldule_add()
        self.dismiss()

    def cancel(self, *args):
        self.dismiss()


class next_music_popup(Popup):
    def __init__(self, main_screen, **kwargs):
        super(next_music_popup, self).__init__(**kwargs)
        self.main_screen = main_screen
        self.content = GridLayout(rows=2)
        self.title = 'Przewijanie Utworu'
        self.title_align = 'center'

        self.contentup = GridLayout(rows=1, size_hint=(1, 0.8))
        self.for_sure_label = Label(text='Czy napewno chcesz przewinąć utwór?', font_size='20sp')
        self.contentup.add_widget(self.for_sure_label)

        self.contentdown = GridLayout(cols=2, size_hint=(1, 0.2))

        self.save_button = Button(text='Yes', size_hint=(200, 100), size_hint_max_y=100)
        self.save_button.bind(on_press=self.save)

        self.cancel_button = Button(text='No', size_hint=(200, 100), size_hint_max_y=100)
        self.cancel_button.bind(on_press=self.cancel)

        self.contentdown.add_widget(self.save_button)
        self.contentdown.add_widget(self.cancel_button)

        self.content.add_widget(self.contentup)
        self.content.add_widget(self.contentdown)

    def save(self, *args):
        self.sm = Thread(target=self.skip_music)
        self.sm.start()
        self.dismiss()

    def cancel(self, *args):
        self.dismiss()

    def skip_music(self):
        global when_stopped, sound, end, index_in_schema, performance_schema, to_configure, id_number, next_music
        if math.floor(sound.length) > math.floor(sound.get_pos()) + 10:
            for _ in range(300):
                sleep(0.01)
                sound.volume -= 0.0033
            sound.stop()
            self.main_screen.scheldule_screen.remove_widget(self.main_screen.scheldule_screen.ids[f'{next_music}'])
            roundedlabel = Factory.RoundedLabel(cols=1, spacing=-30, size_hint=(0.9, self.main_screen.parent.height),
                                                size_hint_max_y=self.main_screen.parent.height / 6,
                                                size_hint_min_y=self.main_screen.parent.height / 6)
            i = performance_schema[index_in_schema]
            roundedlabel.ids.roundedlabel_row1.text = f'[b]{i}[/b]'
            self.main_screen.scheldule_screen.ids[f'{id_number}'] = roundedlabel
            self.main_screen.scheldule_screen.add_widget(roundedlabel)
            to_configure.append([id_number, i])
            index_in_schema += 1
            if index_in_schema > len(performance_schema) - 1:
                index_in_schema = 0
            id_number += 1
            next_music += 1
            sound = SoundLoader.load(
                f'{SD_CARD}\\Lake_of_fire\\Users\\{self.main_screen.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row2.text}\\{self.main_screen.scheldule_screen.ids[f"{next_music}"].ids.roundedlabel_row3.text}')
            sound.play()
            sound.volume = 0
            for _ in range(300):
                sleep(0.01)
                sound.volume += 0.0033
            sound.volume = 1


class add_music_popup(Popup):
    def __init__(self, main_screen, **kwargs):
        super(add_music_popup, self).__init__(**kwargs)
        users_list = [d for d in os.listdir(f'{SD_CARD}\\Lake_of_fire\\Users')]
        self.main_screen = main_screen
        self.content = GridLayout(rows=2)
        self.title = 'Dodawnie Utworu'
        self.title_align = 'center'

        self.contentup = GridLayout(rows=5, size_hint=(1, 0.8))

        self.dropdown_who = DropDown()
        for i in users_list:
            who_button = Button(text=f'{i}', size_hint_y=None, height=44)
            who_button.bind(on_release=lambda who_btn: self.dropdown_who.select(who_btn.text))
            self.dropdown_who.add_widget(who_button)

        self.main_who_button = Button(text='Kogo utwór?', size_hint=(0.8, None))
        self.main_who_button.bind(on_release=self.dropdown_who.open)
        self.dropdown_who.bind(on_select=lambda instance, x: setattr(self.main_who_button, 'text', x))

        self.contentup.add_widget(self.main_who_button)

        self.label_song = Label(text='Daj link do utworu:', size_hint_y=0.25)
        self.input_song = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5, font_size='20sp')
        self.label_fill = Label()

        self.contentup.add_widget(self.label_song)
        self.contentup.add_widget(self.input_song)
        self.contentup.add_widget(self.label_fill)

        self.contentdown = GridLayout(cols=2, size_hint=(1, 0.2))

        self.save_button = Button(text='Save', size_hint=(200, 100), size_hint_max_y=100)
        self.save_button.bind(on_press=self.save)

        self.cancel_button = Button(text='Cancel', size_hint=(200, 100), size_hint_max_y=100)
        self.cancel_button.bind(on_press=self.cancel)

        self.contentdown.add_widget(self.save_button)
        self.contentdown.add_widget(self.cancel_button)

        self.content.add_widget(self.contentup)
        self.content.add_widget(self.contentdown)

    def add_song(self):
        yt = YouTube(f'{self.input_song.text}')
        yt.streams.filter(only_audio=True).first().download(f'{SD_CARD}\\Lake_of_fire\\Users\\{self.main_who_button.text}')
    def save(self, *args):
        if self.main_who_button.text != 'Kogo utwór?':
            if self.input_song.text[:6] == 'https:':
                self.ds = Thread(target=self.add_song)
                self.ds.start()
        self.dismiss()
    def cancel(self, *args):
        self.dismiss()

class add_user_popup(Popup):
    def __init__(self,main_screen,**kwargs):
        super(add_user_popup, self).__init__(**kwargs)
        self.main_screen = main_screen
        self.content = GridLayout(rows = 2)
        self.title = 'Dodawnie Artysty'
        self.title_align = 'center'

        self.contentup = GridLayout(rows=5, size_hint=(1, 0.8))
        self.label_who = Label(text = 'Wpisz kogo dodajesz:', size_hint_y = 0.25)
        self.input_who = TextInput(multiline = False , size_hint_y = None, height=self.contentup.height * 0.5,font_size = '20sp')
        self.label_playlist = Label(text='Jeśli masz playliste daj linka:', size_hint_y=0.25)
        self.input_playlist = TextInput(multiline=False, size_hint_y=None, height=self.contentup.height * 0.5, font_size='20sp')
        self.label_fill = Label()


        self.contentup.add_widget(self.label_who)
        self.contentup.add_widget(self.input_who)
        self.contentup.add_widget(self.label_playlist)
        self.contentup.add_widget(self.input_playlist)
        self.contentup.add_widget(self.label_fill)



        self.contentdown = GridLayout(cols=2, size_hint=(1, 0.2))

        self.save_button = Button(text='Save', size_hint=(200, 100), size_hint_max_y=100)
        self.save_button.bind(on_press=self.save)

        self.cancel_button = Button(text='Cancel', size_hint=(200, 100), size_hint_max_y=100)
        self.cancel_button.bind(on_press=self.cancel)

        self.contentdown.add_widget(self.save_button)
        self.contentdown.add_widget(self.cancel_button)

        self.content.add_widget(self.contentup)
        self.content.add_widget(self.contentdown)

    def save(self, *args):
        if self.input_who.text != '':
            os.mkdir(f'{SD_CARD}\\Lake_of_fire\\Users\\{self.input_who.text}')
            if self.input_playlist.text[:6] == 'https:':
                self.dm = Thread(target=self.download_music)
                self.dm.start()

        self.dismiss()

    def cancel(self, *args):
        self.dismiss()

    def download_music(self):
        p = Playlist(f'{self.input_playlist.text}')
        for video in p.videos:
            video.streams.filter(only_audio=True).first().download(f'{SD_CARD}\\Lake_of_fire\\Users\\{self.input_who.text}')
class Menu_Dropdown(DropDown):
    def __init__(self,main_screen,**kwargs):
        super(Menu_Dropdown,self).__init__(**kwargs)
        self.main_screen = main_screen
class sign_to_list(Popup):
    def __init__(self,my_widget,**kwargs):
        super(sign_to_list,self).__init__(**kwargs)
        users_list = [d for d in os.listdir(f'{SD_CARD}\\Lake_of_fire\\Users')]
        self.my_widget = my_widget
        self.content = GridLayout(rows = 2)
        self.title = 'Dopisz sie'
        self.title_align = 'center'

        #Inputy
        self.contentup = GridLayout(rows = 3,size_hint= (1,0.8))
        #Tool List Start
        self.dropdown_tool = DropDown()
        for i in performance_schema:
            tool_button = Button(text=f'{i}', size_hint_y=None, height=80)
            tool_button.bind(on_release=lambda tool_btn: self.dropdown_tool.select(tool_btn.text))
            self.dropdown_tool.add_widget(tool_button)

        self.main_tool_button = Button(text='Na co wychodzi?', size_hint=(0.8, None))
        self.main_tool_button.bind(on_release=self.dropdown_tool.open)
        self.dropdown_tool.bind(on_select=lambda instance, x: setattr(self.main_tool_button, 'text', x))
        #Tool list End

        #Who List Start
        self.dropdown_who = DropDown()
        for i in users_list:
            who_button = Button(text=f'{i}', size_hint_y=None, height=80)
            who_button.bind(on_press=lambda who_btn: self.dropdown_who.select(who_btn.text))
            who_button.bind(on_release=lambda who_btn_2: self.display_music(who_btn_2.text))
            self.dropdown_who.add_widget(who_button)

        self.main_who_button = Button(text='Kto wychodzi?', size_hint=(0.8, None))
        self.main_who_button.bind(on_release=self.dropdown_who.open)
        self.dropdown_who.bind(on_select=lambda instance, x: setattr(self.main_who_button, 'text', x))
        #Who list End

        self.dropdown_music = DropDown()
        self.main_music_button = Button(text='Do czego wychodzi?', size_hint=(0.8, None))
        self.main_music_button.bind(on_release=self.dropdown_music.open)
        self.dropdown_music.bind(on_select=lambda instance, x: setattr(self.main_music_button, 'text', x))


        self.contentup.add_widget(self.main_tool_button)
        self.contentup.add_widget(self.main_who_button)
        self.contentup.add_widget(self.main_music_button)


        #Guziki
        self.contentdown = GridLayout(cols = 2,size_hint= (1,0.2))

        self.save_button = Button(text='Save',size_hint = (200,100), size_hint_max_y = 100)
        self.save_button.bind(on_press=self.save)

        self.cancel_button = Button(text='Cancel',size_hint = (200,100), size_hint_max_y = 100)
        self.cancel_button.bind(on_press=self.cancel)

        self.contentdown.add_widget(self.save_button)
        self.contentdown.add_widget(self.cancel_button)

        #Koniec
        self.content.add_widget(self.contentup)
        self.content.add_widget(self.contentdown)
    def save(self,*args):
        global music_tf
        if self.main_tool_button.text != 'Na co wychodzi?' and self.main_who_button.text != 'Kto wychodzi?' and self.main_music_button.text != 'Do czego wychodzi?':
            for i in range(len(to_configure)):
                if to_configure[i][1] == self.main_tool_button.text and to_configure[i] not in configured:
                    self.my_widget.scheldule_screen.ids[f'{to_configure[i][0]}'].ids.roundedlabel_row2.text = self.main_who_button.text
                    self.my_widget.scheldule_screen.ids[f'{to_configure[i][0]}'].ids.roundedlabel_row3.text = self.main_music_button.text
                    configured.append(to_configure[i])
                    break
            music_tf = False
            self.dismiss()

    def cancel(self,*args):
        global music_tf
        music_tf = False
        self.dismiss()

    def display_music(self, whos):
        global music_tf
        user_music = [d for d in os.listdir(f'{SD_CARD}\\Lake_of_fire\\Users\\{whos}')]

        drop_down_child = self.dropdown_music.children[0]
        if user_music:
            drop_down_child.clear_widgets()
        # Tool List Start
        for i in user_music:
            music_button = Button(text=f'{i}', size_hint_y=None, height=80)
            music_button.bind(on_release=lambda music_btn: self.dropdown_music.select(music_btn.text))
            self.dropdown_music.add_widget(music_button)
        # Tool list End


class RoundedLabel(GridLayout):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")


class Lake_of_Fire(App):
    def build(self):
        return kv

    def on_start(self):
        if not os.path.isdir(f'{SD_CARD}\\Lake_of_fire\\Users'):
            os.mkdir(f'{SD_CARD}\\Lake_of_fire')
            os.mkdir(f'{SD_CARD}\\Lake_of_fire\\Users')
    def on_stop(self):
        global end
        end = False


if __name__ == "__main__":
    Lake_of_Fire().run()
