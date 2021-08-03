#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import os
import sqlite3
import time

class ButtonGen():

    def on_button_click(self, button):
        os.system(self.command + " &")

    def __init__(self, name, preferred_name, command):
        self.command = command
        
        if preferred_name:
            self.button = Gtk.Button(label = preferred_name)

        else:
            self.button = Gtk.Button(label = name)

        self.button.connect("clicked", self.on_button_click)

class SettingsButtonGen():

    def __init__(self, name):
        self.button_box = Gtk.ButtonBox()
        self.button_box.set_layout(Gtk.ButtonBoxStyle.START)
        self.button_box_label = Gtk.Label()
        self.button_box_label.set_text(name)
        self.button_box_label.set_alignment(0, 0.5)
        self.button_box_entry = Gtk.Entry()

        self.button_box.add(self.button_box_label)
        self.button_box.add(self.button_box_entry)

class MainWindow():

    def on_settings_button_click(self, button):
        self.settings_window = SettingsWindow()

    def on_settings_button_mouse_on(self, button):
        self.builder.get_object("settings_button").set_image(self.settings_image_dynamic)

    def on_settings_button_mouse_off(self, button):
        self.builder.get_object("settings_button").set_image(self.settings_image_still)
    
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.ui")
        self.window = self.builder.get_object("main_window")
        self.window.connect("destroy", Gtk.main_quit)

        self.settings_image_dynamic = Gtk.Image()
        self.settings_image_dynamic.set_from_file("cog_dynamic_32x32.gif")
        self.settings_image_still = Gtk.Image()
        self.settings_image_still.set_from_file("cog_still_32x32.png")

        # Gets the widgets.
        self.builder.get_object("settings_button").connect("clicked", self.on_settings_button_click)
        self.builder.get_object("settings_button").connect("enter", self.on_settings_button_mouse_on)
        self.builder.get_object("settings_button").connect("leave", self.on_settings_button_mouse_off)

        for program in sql_programs:
            self.button = ButtonGen(program[0], program[1], program[2])
            self.builder.get_object("hbox1").pack_start(self.button.button, False, False, 0)

        

        self.window.show_all()

class SettingsWindow(Gtk.Window):

    def on_apply_changes_button_click(self, button):
    
        if self.builder.get_object("entry_database").get_text() == "":
            self.alert = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Cannot apply changes without database name.")
            self.alert.run()
            self.alert.destroy()
    
        else:
            for self.setting in self.settings:

                for self.index, self.item in enumerate(self.settings_list):

                    if self.setting[0] in self.item:

                        if self.setting[2] == 1:
                            self.settings_list[self.index] = self.setting[0] + "=" + str(self.builder.get_object(self.setting[1]).get_value_as_int())

                        elif self.setting[2] == 2:
                            self.settings_list[self.index] = self.setting[0] + "=" + str(self.builder.get_object(self.setting[1]).get_text())

                    else:
                        continue

        with open("settings.cfg", "w") as settings_file:

            for self.item in self.settings_list:

                if self.item[-1] != "\n":
                    self.item = self.item + "\n"

                settings_file.write(self.item)
                
        for program in sql_programs:
        
            program[1] = program[-1].button_box_entry.get_text()
        
            if program[1]:

                c.execute("""
                            UPDATE Programs
                            SET PreferredProgramName='{0}'
                            WHERE ProgramName='{1}';
                        """.format(str(program[1]), str(program[0])))

                conn.commit()

    def on_close_button_click(self, button):
        self.confirm_dialog = ConfirmDialog(main_window.settings_window.set_window)
        self.close_response = self.confirm_dialog.run()
        self.confirm_dialog.destroy()
        
        if self.close_response == Gtk.ResponseType.OK:
            self.set_window.destroy()

    def on_select_button_click(self, doc):
        self.folder_path = self.dialog.get_current_folder()
        
        if doc == "folder":
            self.builder.get_object("entry_save_path").set_text(self.folder_path)
            self.builder.get_object("entry_database").set_text("")

        elif doc == "file":
            self.builder.get_object("entry_database").set_text(self.filename)

        for self.index, self.item in enumerate(self.settings_list):

            if "SAVE_PATH" in self.item:
                self.settings_list[self.index] = "SAVE_PATH=" + str(self.folder_path)

            elif "DATABASE" in self.item:
                self.settings_list[self.index] = "DATABASE=" + str(self.filename)

    def on_file_button_click(self, button, doc):

        if doc == "folder":
            self.dialog = Gtk.FileChooserDialog("Open...", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
            self.dialog.set_current_folder(self.folder_path)

        elif doc == "file":
            self.dialog = Gtk.FileChooserDialog("Open...", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
            self.dialog.set_filename(self.filename)

        self.dialog.set_resizable(False)
        self.dialog.set_transient_for(self.set_window)

        self.dialog.connect("destroy", self.dialog.destroy)
        
        self.response = self.dialog.run()

        if self.response == Gtk.ResponseType.OK:
            self.on_select_button_click(doc)

        self.dialog.destroy()

    def __init__(self):
        Gtk.Window.__init__(self)
        self.builder = Gtk.Builder()
        self.builder.add_from_file("settings2.ui")
        self.set_window = self.builder.get_object("settings_window")

        #self.dialog.set_transient_for(main_window.window)
        self.set_window.connect("destroy", self.set_window.destroy)

        # Reads the settings from the settings.cfg file.
        with open("settings.cfg", "r") as settings_file:
            self.settings_list = settings_file.readlines()

        self.settings = [["UPDATE_TIME", "spinbutton_update_time", 1], ["SAVE_PATH", "entry_save_path", 2], ["DATABASE", "entry_database", 2], ["TIME_PERIOD", "spinbutton_time_period", 1], ["UPDATE_INTERVAL", "spinbutton_update_interval", 1]]

        for self.setting in self.settings:

            for self.item in self.settings_list:

                if self.setting[0] in self.item:

                    if self.setting[2] == 1:
                        self.builder.get_object(self.setting[1]).set_value(int('='.join(self.item.rstrip().split('=')[1:])))

                    elif self.setting[2] == 2:
                        self.builder.get_object(self.setting[1]).set_text('='.join(self.item.rstrip().split('=')[1:]))
                else:
                    continue

        self.folder_path = self.builder.get_object("entry_save_path").get_text()
        self.filename = self.builder.get_object("entry_database").get_text()

        for self.index, self.program in enumerate(sql_programs):

            if self.program[1]:
                self.name = self.program[1]

            else:
                self.name = self.program[0]

            sql_programs[self.index].append(SettingsButtonGen(self.name))
            self.builder.get_object("box_programs").pack_start(self.program[-1].button_box, False, False, 0)

        self.builder.get_object("button_save_path").connect("clicked", self.on_file_button_click, "folder")
        self.builder.get_object("button_database").connect("clicked", self.on_file_button_click, "file")
        self.builder.get_object("apply_changes_button1").connect("clicked", self.on_apply_changes_button_click)
        self.builder.get_object("close_button1").connect("clicked", self.on_close_button_click)

        self.set_window.show_all()

class ConfirmDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Close...", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Close", Gtk.ResponseType.OK))
        self.parent = parent
        self.set_resizable(False)
        self.set_transient_for(main_window.settings_window.set_window)

        self.close_label = Gtk.Label()
        self.close_label.set_markup("<big><b>Are you sure you're done?</b></big>")
        self.box = self.get_content_area()
        self.box.add(self.close_label)
        self.show_all()

sql_programs = []

conn = sqlite3.connect('dbtrial1.db')
c = conn.cursor()

for record in c.execute("""
            SELECT Programs.ProgramName, Programs.PreferredProgramName, ProgramCommands.ProgramCMD
            FROM Programs, ProgramCommands
            WHERE Programs.ProgramNumber = ProgramCommands.ProgramNumber;
        """):
    sql_programs.append(list(record))

main_window = MainWindow()

Gtk.main()

