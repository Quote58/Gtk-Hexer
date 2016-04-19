import gi ; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class PreferencesDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "Preferences", parent, 0)
		self.props.resizable = False
		self.size = "NORMAL"

		box = Gtk.Box(spacing=10)
		box.props.halign = Gtk.Align.START
		content = self.get_content_area()

		apply_button = Gtk.Button()
		apply_button.set_image(Gtk.Image(stock="gtk-apply"))
		apply_button.connect("clicked", self.on_apply_clicked)

		size_normal = Gtk.RadioButton.new_with_label_from_widget(None, "Normal")
		size_small = Gtk.RadioButton.new_with_label_from_widget(size_normal, "Small")
		size_large = Gtk.RadioButton.new_with_label_from_widget(size_normal, "Large")
		
		size_small.connect("toggled", self.on_button_toggled, "SMALL")
		size_normal.connect("toggled", self.on_button_toggled, "NORMAL")
		size_large.connect("toggled", self.on_button_toggled, "BIG")

		Preferences = open("/files/Preferences.txt", "r")
		choice = Preferences.readline()
		choice = choice.lstrip("size=").rstrip()
		Preferences.close()
		if (choice == "SMALL"):
			size_small.set_active(True)
		elif (choice == "BIG"):
			size_large.set_active(True)

		box.pack_start(Gtk.Label("Default Size\t"), True, True, 0)
		box.add(size_small)
		box.add(size_normal)
		box.add(size_large)
		content.add(box)
		content.pack_end(apply_button, True, True, 0)
		self.show_all()

	def on_apply_clicked(self, button):
		Preferences = open("files/Preferences.txt", "w")
		Preferences.write("size=%s" % self.size)
		Preferences.close()
		self.destroy()

	def on_button_toggled(self, button, size):
		if button.get_active():
			self.size = size

class ErrorDialog(Gtk.MessageDialog):
	def __init__(self, parent_window, widget, errorNum):
		if (errorNum == 1):
			lineNum = widget.lineNum ; line_str = widget.line_str
		else:
			lineNum = 0 ; line_str = "Inproper string given"
		error_1 = "Too few arguments given for entry in <span foreground=\"dark blue\"><b>hex_tweaks.txt</b></span> :(\n<span foreground=\"green\"><b>Line:</b></span> %s <span foreground=\"green\"><b>-</b></span> \"%s\"" %  (lineNum, line_str)
		self.errorMessages = [0,error_1] + ["Incorrect input - Must be digits from 0 to F", "Enter a value before clicking Apply", "Preferences.txt is fucked up"]

		Gtk.MessageDialog.__init__(self, parent_window, 0,
						Gtk.MessageType.ERROR,
						Gtk.ButtonsType.CANCEL,
						("ERROR %i" % errorNum))
		self.format_secondary_markup(self.errorMessages[errorNum])

class EditDialog(Gtk.Dialog):
	def __init__(self, parent, data, switch):
		#self.props.resizable = False	<--causes segmentation fault???
		apply_button = Gtk.Button()
		apply_button.set_image(Gtk.Image(stock="gtk-apply"))
		apply_button.connect("clicked", self.on_apply_clicked, switch, parent)
		
		Gtk.Dialog.__init__(self, data[0], parent, 0)
		
		content = self.get_content_area()
		old_bytes = Gtk.Label("Original Bytes ==> [%s]" % switch.originalbytes)
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

	def on_apply_clicked(self, button, switch, parent):
		bytes = self.byte_entry.get_text()
		if (len([i for i in bytes.lower() if
			(not(i in "0123456789abcdef"))]) > 0):
			dialog = ErrorDialog(parent, button, 2)
			dialog.run() ; dialog.destroy()
		elif (len(bytes) < 1):
			dialog = ErrorDialog(parent, button, 3)
			dialog.run() ; dialog.destroy()
		else:
			if (len(bytes)<self.max):
				for i in range(0,self.max-len(bytes)):
					bytes = "0"+bytes
			switch.newbytes = bytes
			hex_tweaks_local = open("files/hex_tweaks_local.txt", "r+")
			i = self.max
			while i > 0:
				hex_tweaks_local.seek(switch.seek-(i-1))
				hex_tweaks_local.write(bytes[self.max-i])
				i -= 1

			hex_tweaks_local.close()
			self.destroy()
























