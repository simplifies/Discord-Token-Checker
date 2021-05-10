# github.com/LocalsGithub
# Enjoy!




# The 'name' module is needed in order to check whether or 
# not the script is running on a linux or windows machine.

# The 'system' module is needed (for some commands) to execute 
# CMD/Terminal commands.

from os import name, system, sys

# Clears Screen ('cls' on windows)
def clear():
    if name == 'nt':
        system('cls')
    elif name == "posix":
        system('clear')

# Pauses ('pause' on windows)
def pause():
	print("Press the <enter> key to continue!")
	input()

# Sets window title
def title(text):
	if name == 'nt':
		ctypes.windll.kernel32.SetConsoleTitleW(text)
	elif name == "posix":
		sys.stdout.write(f"\x1b]2;{text}\x07")
