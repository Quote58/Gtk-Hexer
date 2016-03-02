#---import gtk---
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
import gi ; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import sys
from Dialogs import *
from Catagory_class import *

class Hexer(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self)
	def do_activate(self):
		main_window = Window()
		main_window.show_all()
	def do_startup(self):
		Gtk.Application.do_startup(self)

class InfoStack(Gtk.Stack):
	def __init__(self):
		Gtk.Stack.__init__(self)
		self.add(Gtk.Label("Hexer Version 0.0.1\noh hai there"))

class Window(Gtk.ApplicationWindow):
	def __init__(self):
		Gtk.Window.__init__(self, title="Hexer", application=app)
		self.set_border_width(10)
		Preferences = open("Preferences.txt", "r")
		choice = Preferences.readline()
		choice = choice.lstrip("size=").rstrip()
		sizes = {"NORMAL" : (700, 550), "SMALL" : (600, 375), "BIG" : (850, 650)}

		if choice in sizes:
			self.set_default_size(sizes[choice][0], sizes[choice][1])
		else:
			dialog = ErrorDialog(self, self, 4)
			dialog.run() ; dialog.destroy()
			self.set_default_size(700,550)

		Preferences.close()
		self.error = False
		self.hex_tweaks,self.hex_tweaks_not_custom = self.get_hex_tweaks()

		load_rom, refresh, add_switch, preferences = (Gtk.FileChooserButton(),
								Gtk.Button(), Gtk.Button(),
								Gtk.Button())

		refresh.set_image(Gtk.Image(stock="gtk-refresh"))
		refresh.connect("clicked", self.on_refresh_clicked)

		preferences.set_image(Gtk.Image(stock="gtk-preferences"))
		preferences.connect("clicked", self.on_preferences_clicked)

		add_switch.set_image(Gtk.Image(stock="gtk-add"))

		headerbar = Gtk.HeaderBar()
		headerbar.set_show_close_button(True)
		headerbar.props.spacing = 20
		self.set_titlebar(headerbar)

		headerbar.pack_start(load_rom)
		headerbar.add(preferences)
		headerbar.pack_end(refresh)

		stack_main = Gtk.Stack()
		stack_hex = Gtk.Stack()

		stack_main.set_transition_type(
			Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack_main.set_transition_duration(300)

		stack_hex.set_transition_type(
			Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack_hex.set_transition_duration(300)

		stack_switcher_main = Gtk.StackSwitcher()
		stack_switcher_main.set_stack(stack_main)

		stack_switcher_hex = Gtk.StackSwitcher()
		stack_switcher_hex.props.halign = Gtk.Align.CENTER
		stack_switcher_hex.set_stack(stack_hex)

		headerbar.set_custom_title(stack_switcher_main)

		vertical_box = Gtk.Box(orientation=
					Gtk.Orientation.VERTICAL, spacing=25)

		vertical_box.pack_start(stack_switcher_hex,
					False, False, 0)	#halign/valign
		vertical_box.add(stack_hex)
		stack_hex.props.expand = True
		vertical_box.add(add_switch)

		stack_main.add_titled(vertical_box, "test", "Hex")
		stack_main.add_titled(InfoStack(), "info", "Info")

		for i in ["HUD","Physics","Enemies","FX1","Misc"]:
			stack_hex.add_titled(Catagory(i, self), "%s Stack" % i, i)

		self.add(stack_main)

	def get_hex_tweaks(self):
		hex_tweaks_local_file = open("hex_tweaks_local.txt", "r")
		hex_tweaks_custom = open("hex_tweaks_custom.txt", "r")

		temp = hex_tweaks_local_file.readlines()
		hex_tweaks_local = []
		for i in temp:
			hex_tweaks_local.append(i.rstrip())
		hex_tweaks_not_custom = list(hex_tweaks_local)
		for i in hex_tweaks_custom.readlines():
			hex_tweaks_local.append(i.rstrip())
		#close the file after it's finished
		hex_tweaks_local_file.close()
		return hex_tweaks_local,hex_tweaks_not_custom

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
			file_to_change = open("hex_tweaks_local.txt", "w")
			file_to_change.truncate()
			for i in web_contents:
				file_to_change.write(i+"\n")
			file_to_change.close()



			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK,
						"Stuff has been changed! Take a look :3")
			dialog.format_secondary_text("Please restart Hexer for the changes to take effect")
			dialog.run() ; dialog.destroy()

	def parse_web_data(self):
		hex_tweaks = urllib2.urlopen(
		"https://raw.githubusercontent.com/Quote58/Gtk-Hexer/master/hex_tweaks.txt")
		hex_tweaks = str(hex_tweaks.read())
		hex_tweaks = hex_tweaks.replace("\\\\", "")
		hex_tweaks = hex_tweaks.replace("\\\'", "\'")
		hex_tweaks = hex_tweaks.rstrip("\\n'\"")
		hex_tweaks = hex_tweaks.split("\\n")
		hex_tweaks[0] = hex_tweaks[0].lstrip("\"b'")
		return hex_tweaks

if __name__ == "__main__":
	app = Hexer()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)





















