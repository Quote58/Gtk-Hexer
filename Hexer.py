#---import gtk---
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import sys

class EditDialog(Gtk.Dialog):
	def __init__(self, parent, data, switch):
		apply_button = Gtk.Button()
		apply_button.set_image(Gtk.Image(stock="gtk-apply"))
		apply_button.connect("clicked", self.on_apply_clicked, switch)
		Gtk.Dialog.__init__(self, data[0], parent, 0)
		content = self.get_content_area()
		old_bytes = Gtk.Label("Current Bytes ==> [%s]" % switch.originalbytes)
		old_bytes.props.halign = Gtk.Align.START
		content.add(old_bytes)
		self.max = len(data[6])
		self.byte_entry = Gtk.Entry()
		self.byte_entry.set_max_length(self.max)
		box = Gtk.Box()
		box.pack_start(Gtk.Label("New Bytes ==> "),False, False, 0)
		box.add(self.byte_entry)
		content.add(box)
		content.add(apply_button)
		self.show_all()

	def on_apply_clicked(self, button, switch):
		bytes = self.byte_entry.get_text()
		if (len(bytes)<self.max):
			for i in range(0,self.max-len(bytes)):
				bytes+="0"
		switch.newbytes = bytes
		switch.originalbytes = switch.newbytes
		self.destroy()


class Switch(Gtk.Switch):
	def __init__(self, data):
		Gtk.Switch.__init__(self)
		
		self.offset = data[4]
		self.originalbytes = data[5]
		self.newbytes = data[6]
		
		print(data)


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

class Catagory(Gtk.Stack):
	#takes in the catagory name, so it knows what to fill the
	#grid with
	def __init__(self, catagory_name, parent_window):
		Gtk.Stack.__init__(self)

		self.parent_window = parent_window
		self.catagory_name = catagory_name
		self.contents = self.parent_window.hex_tweaks

		#put the window together in the stack
		self.swindow = Gtk.ScrolledWindow()
		self.viewport = Gtk.Viewport()
		self.switches = Gtk.Grid()

		self.viewport.add(self.switches)
		self.swindow.add(self.viewport)
		self.add_titled(self.swindow, "test", "Hex")

		if self.parent_window.error == False:
			self.add_switches()

	def add_switches(self):
		#parse this shit
		n = 0 ; i = 0
		for line in self.contents:
			data = line.split(" | ")
			if (len(data) < 7):
				dialog = Gtk.MessageDialog(self.parent_window,
						0, Gtk.MessageType.ERROR,
						Gtk.ButtonsType.CANCEL,
						"ERROR 0")
				dialog.format_secondary_markup(
"Too few arguments given for entry in <span foreground=\"dark blue\"><b>hex_tweaks.txt</b></span> :(\n<span foreground=\"green\"><b>Line:</b></span> %s <span foreground=\"green\"><b>-</b></span> \"%s\""
								% (i,line.rstrip("\n")))
				dialog.run() ; dialog.destroy()
				self.parent_window.error = True
			i+=1

		if (self.parent_window.error == True):
			return

		for line in self.contents:
			data = line.split(" | ")
			if(self.catagory_name == data[1].strip()):
				name = data[0]
				label = Gtk.Label("\t%s" % name)
				label.set_line_wrap(True)
				label.props.halign = Gtk.Align.START
				switch = Switch(data)
				switch.connect("notify::active",
						self.on_switch_activated,
						name)
				self.switches.attach(switch, 0,n,1,1)
				self.switches.attach(label, 1,n,1,1)

				m = 2

				if (len(data[2]) > 1):	#if it needs a description
					about = Gtk.Button()
					about.set_image(Gtk.Image(stock="gtk-about"))
					about.connect("clicked", self.on_info_clicked, data)
					self.switches.attach(Gtk.Image(stock="gtk-discard"), m,n,1,1)
					self.switches.attach(about, m+1,n,1,1)
					m+=2

				if (data[3] == "T"):
					edit = Gtk.Button()
					edit.set_image(Gtk.Image(stock="gtk-edit"))
					edit.connect("clicked", self.on_edit_clicked, data, switch)
					self.switches.attach(Gtk.Image(stock="gtk-discard"), m,n,1,1)
					self.switches.attach(edit, m+1,n,1,1)

				n+=1


	def on_switch_activated(self, switch, gparsam, name):
		if switch.get_active():
			print("%s is ON" % name)
			print(switch.offset)
			print(switch.originalbytes)
			print(switch.newbytes)
		else:
			print("%s is OFF" % name)

	def on_info_clicked(self, button, data):
		dialog = Gtk.MessageDialog(self.parent_window, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK,
						data[0])
		dialog.format_secondary_markup(data[2])
		dialog.run() ; dialog.destroy()

	def on_edit_clicked(self, button, data, switch):
		dialog = EditDialog(self.parent_window, data, switch)
		dialog.run()
		dialog.destroy()


class Window(Gtk.ApplicationWindow):

	def __init__(self):
		Gtk.Window.__init__(self, title="Hexer", application=app)
		self.set_border_width(10)
		self.set_default_size(700,550)
		self.error = False
		self.hex_tweaks,self.hex_tweaks_not_custom = self.get_hex_tweaks()

		load_rom, refresh, add_switch, preferences = (Gtk.FileChooserButton(),
								Gtk.Button(), Gtk.Button(),
								Gtk.Button())

		refresh.set_image(Gtk.Image(stock="gtk-refresh"))
		refresh.connect("clicked", self.on_refresh_clicked)

		preferences.set_image(Gtk.Image(stock="gtk-preferences"))
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
		hex_tweaks = hex_tweaks.read()
		hex_tweaks = str(hex_tweaks)
		hex_tweaks = hex_tweaks.replace("\\\\", "")
		hex_tweaks = hex_tweaks.replace("\\\'", "\'")
		hex_tweaks = hex_tweaks.rstrip("\\n'")
		hex_tweaks = hex_tweaks.split("\\n")
		hex_tweaks[0] = hex_tweaks[0].lstrip("b'")
		return hex_tweaks

if __name__ == "__main__":
	app = Hexer()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)





















