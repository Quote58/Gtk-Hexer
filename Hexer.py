#---import gtk---
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

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

		#put the window together in the stack
		self.swindow = Gtk.ScrolledWindow()
		self.viewport = Gtk.Viewport()
		self.switches = Gtk.Grid()
		self.viewport.add(self.switches)
		self.swindow.add(self.viewport)
		self.add_titled(self.swindow, "test", "Hex")

		#get the tweaks from the repository, and add the
		#local ones from opening the file
		self.contents = self.parse_data()
		if self.parent_window.error == False:
			self.add_switches()

	def on_switch_activated(self, switch, gparsam, name):
		if switch.get_active():
			print("%s is ON" % name)
		else:
			print("%s is OFF" % name)

	def on_info_clicked(self, button, data):
		dialog = Gtk.MessageDialog(self.parent_window, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK, 
						data[0])
		dialog.format_secondary_markup(data[3])
		dialog.run() ; dialog.destroy()

	def parse_data(self):
		hex_tweaks = urllib2.urlopen(
		"https://raw.githubusercontent.com/Quote58/Gtk-Hexer/master/hex_tweaks.txt")
		hex_tweaks = hex_tweaks.read()
		hex_tweaks = str(hex_tweaks)
		hex_tweaks = hex_tweaks.replace("\\\\", "")
		hex_tweaks = hex_tweaks.replace("\\\'", "\'")
		hex_tweaks = hex_tweaks.rstrip("\\n'")
		hex_tweaks = hex_tweaks.split("\\n")
		hex_tweaks[0] = hex_tweaks[0].lstrip("b'")
		hex_tweaks_local = open("hex_tweaks.txt", "r")
		for i in hex_tweaks_local.readlines():
			hex_tweaks.append(i)

		#close the file after it's finished
		hex_tweaks_local.close()
		return hex_tweaks

	def add_switches(self):
		#parse this shit
		n = 0
		#temp = True
		i = 0
		for line in self.contents:
			data = line.split("|")
			if (len(data) < 4):
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
			data = line.split("|")
			if(self.catagory_name == data[1].strip()):
				name = data[0]
				label = Gtk.Label("\t%s" % name)
				label.set_line_wrap(True)
				label.set_justify(Gtk.Justification.LEFT)
				switch = Gtk.Switch()
				switch.connect("notify::active",
						self.on_switch_activated,
						name)
				self.switches.attach(switch, 0,n,1,1)
				self.switches.attach(label, 1,n,1,1)
				if (data[2] == "T"):	#if it needs a description
					about = Gtk.Button()
					about.set_image(Gtk.Image(stock="gtk-about"))
					about.connect("clicked", self.on_info_clicked, data)
					self.switches.attach(Gtk.Image(stock="gtk-discard"), 2,n,1,1)
					self.switches.attach(about, 3,n,1,1)
				n+=1

			


class Window(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Hexer")
		self.set_border_width(10)
		self.set_default_size(600,500)
		self.error = False

		load_rom, save_rom, add_switch = (Gtk.FileChooserButton(), 
						 Gtk.Button(), Gtk.Button())

		save_rom.set_image(Gtk.Image(stock="gtk-apply"))
		add_switch.set_image(Gtk.Image(stock="gtk-add"))

		headerbar = Gtk.HeaderBar()
		headerbar.set_show_close_button(True)
		headerbar.props.spacing = 20
		self.set_titlebar(headerbar)

		headerbar.pack_start(load_rom)
		headerbar.pack_end(save_rom)

		stack_main = Gtk.Stack()
		stack_hex = Gtk.Stack()

		stack_main.set_transition_type(
			Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		stack_main.set_transition_duration(300)

		stack_switcher_main = Gtk.StackSwitcher()
		stack_switcher_main.set_stack(stack_main)

		stack_switcher_hex = Gtk.StackSwitcher()
		stack_switcher_hex.props.halign = Gtk.Align.CENTER
		stack_switcher_hex.set_stack(stack_hex)
		
		headerbar.set_custom_title(stack_switcher_main)

		vertical_box = Gtk.Box(orientation=
					Gtk.Orientation.VERTICAL, spacing=20)
		
		vertical_box.pack_start(stack_switcher_hex,
					False, False, 0)	#halign/valign
		vertical_box.add(stack_hex)
		stack_hex.props.expand = True
		vertical_box.add(add_switch)

		stack_main.add_titled(vertical_box, "test", "Hex")
		stack_main.add_titled(InfoStack(), "info", "Info")

		for i in ["HUD","Physics","Enemies","Misc"]:
			stack_hex.add_titled(Catagory(i, self), "%s Stack" % i, i)

		self.add(stack_main)


Hexer_window = Window()
Hexer_window.connect("delete-event", Gtk.main_quit)
Hexer_window.show_all()
Gtk.main()





























