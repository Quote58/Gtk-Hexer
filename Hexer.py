#---import gtk and whatnot---
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
from Window import *

class Hexer(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self)
	def do_activate(self):
		main_window = Window(self)
		main_window.show_all()
	def do_startup(self):
		Gtk.Application.do_startup(self)

class InfoStack(Gtk.Stack):
	def __init__(self):
		Gtk.Stack.__init__(self)
		self.add(Gtk.Label("Hexer Version 0.0.2\noh hai there"))

if __name__ == "__main__":
	app = Hexer()
	exit_status = app.run(sys.argv)
	sys.exit(exit_status)





















