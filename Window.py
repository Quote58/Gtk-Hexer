try:
	import urllib.request as urllib2
except ImportError:
	import urllib2

import gi ; gi.require_version('Gtk', '3.0')
import rom_functions
from gi.repository import Gtk, Gio
import sys
from Dialogs import *
from Catagory_class import *
from Hexer import *

class Window(Gtk.ApplicationWindow):
	def __init__(self, app):
		Gtk.Window.__init__(self, title="Hexer", application=app)
		self.set_border_width(10)
		Preferences = open("files/Preferences.txt", "r")
		choice = Preferences.readline()
		choice = choice.lstrip("size=").rstrip()
		sizes = {"NORMAL" : (700, 550), "SMALL" : (600, 375), "BIG" : (850, 650)}

		rom_name = Preferences.readline()
		rom_name = rom_name[4::].rstrip()

		if choice in sizes:
			self.set_default_size(sizes[choice][0], sizes[choice][1])
		else:
			dialog = ErrorDialog(self, self, 4)
			dialog.run() ; dialog.destroy()
			self.set_default_size(700,550)

		Preferences.close()

		temp_path = rom_name

		if (rom_name == "NONE"):
			file_choose = Gtk.FileChooserDialog("Select a rom file (file name must end with .smc)", self, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
			response = file_choose.run()

			if response == Gtk.ResponseType.OK:
				temp_path = file_choose.get_filename()

			file_choose.destroy()

		self.set_up_window()

		if (temp_path[len(temp_path)-3:len(temp_path)] == "smc"):
			self.file_path = temp_path
				#is it a rom?
			if rom_name == "NONE":
				self.change_path(temp_path)

			for i in ["HUD","Physics","Enemies","FX1","Misc"]:
				self.stack_hex.add_titled(Catagory(i, self), "%s Stack" % i, i)
		else:
			print(temp_path)
			print("must be a rom, n00b")

		self.add(self.stack_main)
			
	def on_load_clicked(self, button):
		file_choose = Gtk.FileChooserDialog("Select a rom file (file name must end with .smc)", self, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))
		response = file_choose.run()
		if response == Gtk.ResponseType.CANCEL:
			print("Oh noes :(")
			file_choose.destroy()

		elif response == Gtk.ResponseType.OK:
			temp_path = file_choose.get_filename()
			file_choose.destroy()

			if (temp_path[len(temp_path)-3:len(temp_path)] == "smc"):
				self.file_path = temp_path
				self.change_path(temp_path)

				if len(self.stack_hex) == 0:
					for i in ["HUD","Physics","Enemies","FX1","Misc"]:
						self.stack_hex.add_titled(Catagory(i, self), "%s Stack" % i, i)
					self.show_all()

				else:
					for i in self.stack_hex:
						for j in i.switches:
							if isinstance(j, Gtk.Switch):
								j.check_status()
			else:
				print("that's not a rom file n00b")

	def change_path(self, temp_path):
		Preferences = open("files/Preferences.txt", "r+")
		current_line = ""
		i = 0
		while current_line != "rom=":
			current_line = Preferences.read(4)
			Preferences.seek(i)
			i+=1
		Preferences.seek(i-2)
		Preferences.write("rom=%s" % temp_path)
		Preferences.seek(0)
		Preferences.truncate(i+3+len(temp_path)-1)
		Preferences.close()

	def set_up_window(self):
		self.error = False
		self.hex_tweaks = ""
		self.hex_tweaks_not_custom = ""

		self.get_hex_tweaks()

		load_rom, refresh, add_switch, preferences = (Gtk.Button(),
								Gtk.Button(), Gtk.Button(),
								Gtk.Button())

		refresh.set_image(Gtk.Image(stock="gtk-refresh"))
		refresh.connect("clicked", self.on_refresh_clicked)
	
		preferences.set_image(Gtk.Image(stock="gtk-preferences"))
		preferences.connect("clicked", self.on_preferences_clicked)

		load_rom.set_image(Gtk.Image(stock="gtk-open"))
		load_rom.connect("clicked", self.on_load_clicked)

		add_switch.set_image(Gtk.Image(stock="gtk-add"))

		headerbar = Gtk.HeaderBar()
		headerbar.set_show_close_button(True)
		headerbar.props.spacing = 20
		self.set_titlebar(headerbar)

		headerbar.pack_start(load_rom)
		headerbar.add(preferences)
		headerbar.pack_end(refresh)

		self.stack_main = Gtk.Stack()
		self.stack_hex = Gtk.Stack()

		self.stack_main.set_transition_type(
			Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		self.stack_main.set_transition_duration(300)
	
		self.stack_hex.set_transition_type(
			Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		self.stack_hex.set_transition_duration(300)

		stack_switcher_main = Gtk.StackSwitcher()
		stack_switcher_main.set_stack(self.stack_main)

		self.stack_switcher_hex = Gtk.StackSwitcher()
		self.stack_switcher_hex.props.halign = Gtk.Align.CENTER
		self.stack_switcher_hex.set_stack(self.stack_hex)

		headerbar.set_custom_title(stack_switcher_main)

		self.vertical_box = Gtk.Box(orientation=
					Gtk.Orientation.VERTICAL, spacing=25)

		self.vertical_box.pack_start(self.stack_switcher_hex,
					False, False, 0)	#halign/valign
		self.vertical_box.add(self.stack_hex)
		self.stack_hex.props.expand = True
		self.vertical_box.add(add_switch)

		self.stack_main.add_titled(self.vertical_box, "test", "Hex")
		self.stack_main.add_titled(InfoStack(), "info", "Info")

	def get_hex_tweaks(self):
		hex_tweaks_local_file = open("files/hex_tweaks_local.txt", "r")
		#hex_tweaks_custom = open("files/hex_tweaks_custom.txt", "r")

		temp = hex_tweaks_local_file.readlines()
		hex_tweaks_local = []
		for i in temp:
			hex_tweaks_local.append(i.rstrip())
		hex_tweaks_not_custom = list(hex_tweaks_local)
		#for i in hex_tweaks_custom.readlines():
			#hex_tweaks_local.append(i.rstrip())
		#close the file after it's finished
		hex_tweaks_local_file.close()

		self.hex_tweaks = hex_tweaks_local
		self.hex_tweaks_not_custom = hex_tweaks_not_custom		

	def on_preferences_clicked(self, button):
		dialog = PreferencesDialog(self)
		dialog.run() ; dialog.destroy()


	def on_refresh_clicked(self, button):
		web_contents = self.parse_web_data()
		if (web_contents == self.hex_tweaks_not_custom):
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK,
						"You're up to date :D")
			dialog.run() ; dialog.destroy()
		else:
			file_to_change = open("files/hex_tweaks_local.txt", "w")
			file_to_change.truncate()
			for i in web_contents:
				file_to_change.write(i+"\n")
			file_to_change.close()

			self.get_hex_tweaks()

			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK,
						"Stuff has been changed! Take a look :3")
			dialog.format_secondary_text("Please restart Hexer for the changes to take effect")
			dialog.run() ; dialog.destroy()

			for i in self.stack_hex:
				i.destroy()
			for i in ["HUD","Physics","Enemies","FX1","Misc"]:
					self.stack_hex.add_titled(Catagory(i, self), "%s Stack" % i, i)
			for i in self.stack_hex:
				print(i)
			print()
			self.show_all()

	def parse_web_data(self):
		hex_tweaks = urllib2.urlopen(
		"https://raw.githubusercontent.com/Quote58/Gtk-Hexer/master/files/hex_tweaks_local.txt")
		hex_tweaks = str(hex_tweaks.read())
		hex_tweaks = hex_tweaks.replace("\\\\", "")
		hex_tweaks = hex_tweaks.replace("\\\'", "\'")
		hex_tweaks = hex_tweaks.rstrip("\\n'\"")
		hex_tweaks = hex_tweaks.split("\\n")
		hex_tweaks[0] = hex_tweaks[0].lstrip("\"b'")
		return hex_tweaks






