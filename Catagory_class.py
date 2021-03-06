import gi ; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import rom_functions
from code.Dialogs import *

class Switch(Gtk.Switch):
	def __init__(self, data, seek, parent):
		Gtk.Switch.__init__(self)
		self.data = data
		self.parent = parent
		self.offset = data[4].split(" ")
		self.originalbytes = data[5].split(" ")
		self.newbytes = data[6].split(" ")
		self.seek = seek
		

	def check_status(self):
		j = 0
		for i in self.offset:
			if (rom_functions.not_main(self.parent.parent_window.file_path, i, self.newbytes[j], 1) == 1):
				self.set_active(True)
			else:
				self.set_active(False)
				break

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
		n = 0 ; self.lineNum = 0
		for line in self.contents:
			self.line_str = line.rstrip("\n")
			data = line.split(" | ")
			if (len(data) < 7):
				dialog = ErrorDialog(self.parent_window, self, 1)
				dialog.run() ; dialog.destroy()
				self.parent_window.error = True
			self.lineNum+=1

		if (self.parent_window.error == True):
			return
		seek = 0

		for line in self.contents:
			for i in line:
				seek+=1
			data = line.split(" | ")
			if(self.catagory_name == data[1].strip()):

				name = data[0]
				label = Gtk.Label("\t%s" % name)
				label.set_line_wrap(True)
				label.props.halign = Gtk.Align.START
				if (len(data[4].split(" ")) != len(data[5].split(" ")) or len(data[4].split(" ")) != len(data[6].split(" "))):
					dialog = ErrorDialog(self.parent_window, self.parent_window, 6)
					dialog.run() ; dialog.destroy()
					continue

				switch = Switch(data, seek, self)

				#determine whether or not the tweak is there

				switch.check_status()
				seek+=1
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
		#TO DO: make a function that combines the apply and check functions
		if switch.get_active():
			bytes = switch.newbytes
			print("%s is ON" % name)
		else:
			bytes = switch.originalbytes
			print("%s is OFF" % name)
		j = 0
		for i in switch.offset:
			rom_functions.not_main(self.parent_window.file_path, i, bytes[j], 0)
			j+=1

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




















