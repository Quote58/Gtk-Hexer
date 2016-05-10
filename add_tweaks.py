import os

#this checks whether the file exists and if not creates it
if os.path.isfile("hex_tweaks.txt"):
	file = open("hex_tweaks.txt", "r+")
	size = len(file.read())
	file.seek(0)
else:
	file = open("hex_tweaks.txt", "w")
	size = 0

#because duplicate offsets would be annoying
def get_offsets(file):
	offset_list = []
	for i in file.readlines():
		line = i.split(" | ")
		if (len(line)>1):
			offset_list.append(line[4])
	file.seek(0)
	return offset_list

#just a function for input
def get_input(prompt, conditions):
	while True:
		user_in = input(prompt)
		if (user_in.upper() in conditions):
			return user_in
		else:
			print("Invalid input, please try again")

#useful shit
yes_means_true = {"Y" : "T", "N" : "F"}
E_means_enemy = {"H" : "HUD", "M" : "Misc", "E" : "Enemies", "P" : "Physics", "F" : "FX1"}
prompts = ["Okay, type in the offset in PC format (not SNES) > ", "Now the original byte/s > ", "And finally, the new byte/s > ", "What type of tweak is it? [H (HUD), M (Misc), E (Enemies), P (Physics), or F (FX1)] > ", "Does it need a description dialog? [Y/N] > ", "Is the value variable? [Y/N] > ", "Would you like to add this tweak? [Y/N] > "]
'''statinfo = os.stat("hex_tweaks.txt")
size = statinfo.st_size'''
if size>0:
	offset_list = get_offsets(file)
else:
	offset_list = []
print(offset_list)

#okay, the actual interaction starts here
print("Welcome! A hex tweak requires: Name, Catagory, Optional description, Ability to edit Yes/No, Offset, Original bytes, New bytes")

while True:
	hex_tweak = []
	user_in = input("\nWhat is the name of this hex tweak? [Type Q to quit] > ")
	if (user_in.upper() != 'Q'):
		hex_tweak.append(user_in)
		# Name | ... | ... | ... | ... | ... | ...

		user_in = get_input(prompts[3], ['H', 'M', 'E', 'P', 'F'])
		hex_tweak.append(E_means_enemy[user_in.upper()])
		# Name | Catagory | ... | ... | ... | ... | ...

		user_in = get_input(prompts[4], ['Y', 'N'])
		if (user_in.upper() == 'Y'):
				user_in = input("Okay, type the description here > ")
				hex_tweak.append(user_in)
		else:
				hex_tweak.append("")
		# Name | Catagory | Description | ... | ... | ... | ...

		user_in = get_input(prompts[5], ['Y', 'N'])
		hex_tweak.append(yes_means_true[user_in.upper()])
		# Name | Catagory | Description | Mutability | ... | ... | ...

		for i in range(3):		
			user_in = input(prompts[i])
			user_in = ''.join(user_in.upper().split())
			hex_tweak.append(user_in)
		# Name | Catagory | Description | Mutability | Offset | Original | New

		final_tweak = ""
		for i in hex_tweak:
			final_tweak = final_tweak + " | " + i

		final_tweak = final_tweak[3::]

		print("Tweak constructed:\n%s\n" % final_tweak)
		user_in = get_input(prompts[6], ['Y', 'N'])
		if (user_in.upper() == 'Y'):
			if (hex_tweak[4] in offset_list):
				print("There already seems to be a tweak that uses offset: %s, sorry about that" % hex_tweak[4])
			else:
				file.seek(size)
				file.write(final_tweak+'\n')
				size = file.tell()
				offset_list.append(hex_tweak[4])
				print("Hex tweak has been added!")
		else:
			print("Hex tweak was not added")

	else:
		print("Okay, goodbye!")
		break

file.close()





















