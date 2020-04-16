import discord, sys, re, yagmail, random


yag = yagmail.SMTP("username", "password")

random.seed(1)

token = "token"

client = discord.Client()
id = None
unverified = {}

@client.event
async def on_member_join(member):
	
	global unverified

	unverified.update({member.id: None})
	await member.send("Welcome. Please type the email address you registered with to confirm your identity.")

@client.event
async def on_message(message):

	global unverified

	if message.author.id in unverified:
		if re.match("^\S*@\S*\.\S*$", message.content) is not None:

			pin = random.randint(100000, 999999)
			unverified.update({message.author.id: pin})

			email = [
				"Please type the pin below into the ID-Check bot channel to verify email.\n"
				"PIN: {}".format(pin)
			]

			yag.send(message.content, 'subject', email)

			await message.author.send("Verification email has been sent.")
		
		elif re.match("\d{6}", message.content) is not None:

			if int(message.content) == unverified[message.author.id]:

				print("{} has been verified".format(message.author))
				del unverified[message.author.id]


try:
	client.run(token)
except KeyboardInterrupt:
	sys.exit()