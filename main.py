#!/usr/bin/env python

import gi
gi.require_version('Gtk','3.0');
from gi.repository import Gtk
import os

convert_button = Gtk.Button(label="Convert")
convert_button.set_sensitive(False)

source_address_input = Gtk.Entry()
source_address_input.set_placeholder_text("Choose File ...")
source_address_input.set_sensitive(False)
source_address_input.set_hexpand(True)

target_address_input = Gtk.Entry()
target_address_input.set_placeholder_text("Output file will go here")
target_address_input.set_sensitive(False)

class MainWindow(Gtk.Window):
	command_prepare = ''
	def __init__(self):
		Gtk.Window.__init__(self, title="Video2Gif")
		self.set_default_size(400,200)

		box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
		box.set_margin_top(10)
		box.set_margin_start(10)
		box.set_margin_bottom(10)
		box.set_margin_end(10)

		self.add(box)

		self.source_file = ''
		self.target_file = ''
		self.rate = '15'

		label = Gtk.Label()
		label.set_markup("<b><big>Simple Video 2 Gif Converter</big></b>")
		box.add(label)

		source_file_label = Gtk.Label()
		source_file_label.set_text("Source File :")
		source_file_label.set_xalign(0)
		target_file_label = Gtk.Label()
		target_file_label.set_text("Target File :")
		target_file_label.set_xalign(0)

		box.add(source_file_label)
		source_box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)

		box.add(source_box)
		source_box.add(source_address_input)
		choose_btn = Gtk.Button(label="Choose...")
		choose_btn.connect("clicked",self.choose_button_clicked)
		source_box.add(choose_btn)

		box.add(target_file_label)
		box.add(target_address_input)

		convert_button.connect("clicked",self.convert_button_clicked)
		box.add(convert_button)


	def choose_button_clicked(self,widget):
		dialog = Gtk.FileChooserDialog(title="Select Video File",parent=self,action=Gtk.FileChooserAction.OPEN)
		dialog_filter = Gtk.FileFilter()
		dialog_filter.set_name("Videos")
		video_support = ['*.mp4','*.m4p','*.m4v','*.mpg','*.mpeg','*.mkv','*.flv','*.vob','*.ogg','*.ogv','*.gif','*.drc','*.gifv','*.mng','*.avi','*.wmv','*.mov']
		for i in video_support:
			dialog_filter.add_pattern(i)  # whats the pattern for a video file
		dialog.add_filter(dialog_filter)
		dialog.add_buttons("Cancel",Gtk.ResponseType.CANCEL,"Open",Gtk.ResponseType.OK)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			source_file = dialog.get_filename()
			target_file = source_file.split('.')
			target_file.pop()
			target_file.append('gif')
			target_file = '.'.join(target_file)
			self.source_file = source_file
			self.target_file = target_file
			print("Open>")
			print("Selected File: "+source_file)
			print("Output   File: "+target_file)
			source_address_input.set_text(source_file)
			target_address_input.set_text(target_file)
			convert_button.set_sensitive(True)

		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel Clicked")

		dialog.destroy()


	def convert_button_clicked(self, widget):
		convert_button.set_sensitive(False)
		command_prepare = self.source_file+"' -filter:v fps="+self.rate+" '"+self.target_file+"'"
		command = "ffmpeg -y -i '"+ command_prepare
		print("> "+command)
		os.system(command)
		print('Proccess FFMPEG Done !')


window = MainWindow()
window.connect("delete-event",Gtk.main_quit)
window.show_all()
Gtk.main()
