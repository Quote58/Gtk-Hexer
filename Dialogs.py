import gi ; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

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
					bytes+="0"
			switch.newbytes = bytes
			hex_tweaks_local = open("hex_tweaks_local.txt", "r+")
			for i in range(0,self.max):
				hex_tweaks_local.seek(switch.seek-self.max+i)
				hex_tweaks_local.write(bytes[i])

			hex_tweaks_local.close()
			self.destroy()
























