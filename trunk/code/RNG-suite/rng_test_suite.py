#Import necessary modules
import glob, subprocess, tempfile, shutil, os, binascii, threading, sys
import numpy as np
import time
#Tkinter to produce a GUI
import tkinter as tk
import tkinter.ttk as tkk

#Global variables for tests
PASSED_FIPS = False
PASSED_SMALLCRUSH = False

#Application constants to describe the program
TITLE="RNG Test Suite"
DESC="A user friendly way of testing a TRNG using a combined set of existing statistical testing suites."

#Application class for tkinter windows
class Application(object):
	def __init__(self, root, size):
		self.root = root
		root.title(TITLE)
		root.geometry(size)
		root.resizable(False, False)

	#spawn a label inside the window
	def spawn_label(self, textinput, width, padding):
		self.label = tk.Label(self.root, text=textinput, wraplength=width)
		self.label.pack(pady=padding)
		return self.label

	#spawn an unpacked label inside the window
	def spawn_unpacked_label(self, textinput, width):
		self.label = tk.Label(self.root, text=textinput, wraplength=width)
		return self.label

	#spawn a button inside the window
	def spawn_button(self, text, command):
		self.button = tk.Button(self.root, text=text, command=command)
		self.button.pack()
		return self.button

	#spawn a listbox inside the window
	def spawn_listbox(self, width, height):
		self.listbox = tk.Listbox(self.root, width=width, height=height)
		self.listbox.pack()
		return self.listbox

	#spawn a progressbar inside the window
	def spawn_progressbar(self, length):
		self.progressbar = tkk.Progressbar(self.root, orient='horizontal', length=length, mode='indeterminate')
		return self.progressbar

#List the usb devices in a listbox
def list_usb_devices(listbox):
	#Delete previous listed devices from the listbox to prevent duplicates
	listbox.delete(0, tk.END)
	#Store device list in array
	list_of_connected_devices = glob.glob('/dev/*')
	#Append each device as a new list item
	for idx, device in enumerate(list_of_connected_devices):
		listbox.insert(idx, device)

	#Open new window on double clicking a list item
	listbox.bind("<Double-Button>", lambda event: open_usb_item(event, listbox))

#Let the user interact with the connected device
#Pass 'event' containing information about the listbox item highlighted
def open_usb_item(event, listbox):
	#The selection number from the listbox array
	cs = listbox.curselection()
	#The content of the item selected
	cs_content = listbox.get(cs)

	#Initialize a new Tkinter window
	root = tk.Tk()

	#Create a reference to the Application class in root window for new window
	usb_item_app = Application(root, "500x300")

	#Spawn a label showing the USB path and intention of the window
	usb_item_app.spawn_label("Here you can run TRNG tests on " + cs_content, 300, 20)

	#Instantiate a progressbar variable used in both upcoming threads.
	#progressbar = None;

	#Spawn the progressbar in the window
	progressbar = usb_item_app.spawn_progressbar(300)

	update_progress_text = usb_item_app.spawn_unpacked_label("", 300)

	#Spawn a button to run tests
	#Use threading to allow the progressbar and test suites to run async!
	run_tests_btn = usb_item_app.spawn_button("Perform analysis", lambda: [threading.Thread(target=progress_update, args=(usb_item_app, progressbar, run_tests_btn)).start(), threading.Thread(target=run_tests_on_usb_device, args=(usb_item_app, cs_content, progressbar, update_progress_text)).start()])

	#Halt python input on completion
	root.mainloop()

#Define a method to show the progressbar
def progress_update(usb_item_app, progressbar, run_tests_btn):
	#Destroy the perform analysis button in order to prevent calling the methods multiple times
	run_tests_btn.destroy()
	#Pack the progressbar to display it in the window
	progressbar.pack(pady=50)
	#use update_idleatasks to allow the progressbar to update its value during runtime
	usb_item_app.root.update_idletasks()
	#Start the progressbar with a step of 10ms
	progressbar.start(10)

#When called by a button, run several tests and display it back to the user
def run_tests_on_usb_device(usb_item_app, cs_content, progressbar, update_progress_text):
	global PASSED_FIPS
	global PASSED_SMALLCRUSH
	#Begin rendering text to let the user know what the current process is.
	#This will be done through multiple calls to update_progress_text.config()
	update_progress_text.pack(pady=20)
	update_progress_text.config(text="Rendering output from " + cs_content + "...")
	#Run a subprocess to call the necessary amount of bits from the RNG with `head`
	start_timer = time.time()
	process = subprocess.run(['dd', 'if='+cs_content, 'iflag=fullblock', 'bs=32MB', 'count=8'], stdout=subprocess.PIPE)
	update_progress_text.config(text="Writing output to temporary file...")
	#Open a temporary file to store the bit information from the RNG
	with tempfile.NamedTemporaryFile(mode='wb') as output_file:
		#Write output to temp file
		output_file.write( process.stdout )
		update_progress_text.config(text="Running FIPS 140-2 tests on RNG output...")
		#Use the FipsTesting C program to test the RNG output against FIPS 140-2
		testFips = subprocess.run(['./FipsTesting', output_file.name], stdout=subprocess.PIPE)
		#Print the result fo the FIPS test to the terminal.
		print(testFips.stdout.decode('latin1'))
		#Check if all tests in FIPS 140-2 were passed
		if (testFips.stdout.decode('latin1').splitlines()[-4] == " All values are within the required intervals of FIPS-140-2"):
			PASSED_FIPS = True
		update_progress_text.config(text="Converting output to SmallCrush testing format...")
		#Convert the output file to floating point using a filter program written in python (To run SmallCrush)
		convert_output_file = subprocess.run(['python3', 'ffb.py', output_file.name], stdout=subprocess.PIPE)
		update_progress_text.config(text="Writing converted output to temporary file...")
		#Open a new temporary file to store the converted & filtered output
		with tempfile.NamedTemporaryFile(mode='wb') as converted_file:
			#Write the output to the temporary file
			converted_file.write(convert_output_file.stdout)
			update_progress_text.config(text="Running SmallCrush tests on output...")
			#Open a new subprocess to perform the testing from the temp file on the RNG_testing C program.
			testSC = subprocess.run(['./SmallCrushTesting', converted_file.name], stdout=subprocess.PIPE)
			update_progress_text.config(text="Finished SmallCrush and FIPS 140-2 testing")
			#Store the output in a variable
			testSC_result = testSC.stdout
			#Print the result from SmallCrush to terminal.
			print(testSC_result.decode('latin1'))
			#Check if all tests in SmallCrush were passed
			if (testSC_result.decode('latin1').splitlines()[-4] == " All tests were passed"):
				PASSED_SMALLCRUSH = True
	end_timer = time.time()
	#Stop the progressbar from running
	progressbar.stop()
	progressbar.destroy()
	processed_time = usb_item_app.spawn_label("Elapsed time: {:.1f}s".format((end_timer-start_timer)), 300, 10)
	#Display yhe binary pass/fail results of the tests
	if (PASSED_FIPS and PASSED_SMALLCRUSH):
		test_results = usb_item_app.spawn_label("Passed both tests (SmallCrush and FIPS-140-2).", 350, 5)
		test_results.config(fg='green')
	else:
		test_results = usb_item_app.spawn_label("Did not pass both tests. Not recommended for use. Further testing suggested.", 300, 5)
		test_results.config(bg='red')
		test_results.config(fg='white')

#The main method
def main():
	#Initialize a Tkinter window
	root = tk.Tk()

    #Create a reference to the Application class in root window
	app = Application(root, "500x350")
	#Spawn a label describing the application
	app.spawn_label(DESC, 300, 10)

	#Spawn a list of the devices listed in /dev on the target system
	app.spawn_label("list of available devices connected to your system:", 350, 5)
	device_list = app.spawn_listbox(50, 10)
	refresh_device_list = app.spawn_button("Refresh", lambda: list_usb_devices(device_list))

	#Halt python input on completion
	root.mainloop()

#Call the main method
main()

