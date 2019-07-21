#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#Misc imports
import asyncio
import random

def setup( client ):
    client.add_cog( quiz(client) )

class quiz( commands.Cog ):

    def __init__(self, client):
        self.client = client

    @commands.command
    async def qqq( self, ctx ):

        client = self.client
        message = ctx.message

        personalities = [  ["BOLD", 0], ["QUIRKY", 0], ["TIMID", 0], ["NAIVE", 0], ["HASTY", 0] ]
        questions = [0,1,2,3,4,5,6,7,8,9,10,11,12]

        def check(author):
            def check2( answer ):
                if answer.author != message.author:
                    return False
                try:
                    int(answer.content)
                    return True
                except ValueError :
                    return False
            return check2
            
        count = 0
        while count < 6 :

            current = random.choice( questions )
            if current == 0 :
                await message.channel.send("Have you ever thought that if you dug in your backyard you could find buried treasure? \n\n1) Yes.\n2) No.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[3][1] += 2
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 1 :
                await message.channel.send("You're in class when you realize that you really have to go to the restroom. What do you do? \n\n1) Ask for permission to leave.\n2) Sneak out.\n3) Hold on until class ends.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[4][1] += 1
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 2 :
                await message.channel.send("You discover a beat-up-looking treasure chest in some ruins. What do you do? \n\n1) Open It!\n2) Get help opening it.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        personalities[4][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        personalities[4][1] -= 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 3 :
                await message.channel.send("If you saw someone doing something bad, could you scold them? \n\n1) Of Course.\n2) Not Really.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 4 :
                await message.channel.send("Are you truly sincere when you apologize? \n\n1) Of Course.\n2) That's not easy to admit.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        personalities[3][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 5 :
                await message.channel.send("You're hiking up a mountain when you reach diverging paths. Which kind do you take? \n\n1) Narrow.\n2) Wide.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[3][1] += 2
                        personalities[4][1] += 1
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        personalities[0][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")
            
            elif current == 6 :
                await message.channel.send("Everyone around you is laughing hard at something you think is pretty boring. What do you do? \n\n1) Nothing.\n2) Laugh Along.\n3) It depends on the situation.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 2
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[1][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 7 :
                await message.channel.send("Good news and bad news... Which one do you want to hear first? \n\n1) The good news.\n2) The bad news.\n3) I don't want either.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[4][1] += 2
                        personalities[3][1] += 1
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 8 :
                await message.channel.send("There's a rumor around about a ghost haunting the school bathrooms! What do you do?	 \n\n1) Avoid them.\n2) Go in there anyway.\n3) Bring your friends with you.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[1][1] += 1
                        personalities[0][1] -= 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[0][1] += 1
                        personalities[4][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")
            
            elif current == 9 :
                await message.channel.send("You see a cake that is past its expiration date, but only by one day. What do you do? \n\n1) Not a problem, eat it anyway.\n2) Think about it briefly, then decide.\n3) Get someone to try it first. \n4) Refuse to eat it.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[4][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[2][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("4") != -1 :
                        personalities[0][1] += 1
                        personalities[1][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 10 :
                await message.channel.send("You're eating at a very fancy restaurant known for its food. Which course do you select? \n\n1) Whatever is cheapest.\n2) Healthy fish.\n3) Prime Steak, enjoy the experience. \n4) Anything, it's all good.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[1][1] += 1
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[0][1] -= 1
                        personalities[1][1] += 2
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("4") != -1 :
                        personalities[2][1] += 1
                        personalities[3][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 11 :
                await message.channel.send("You find something at a great bargain price. What do you do? \n\n1) Buy it right away.\n2) Think about whether you need it.\n3) Demand an even bigger discount.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[1][1] += 1
                        personalities[4][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[4][1] -= 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        personalities[3][1] += 2
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            elif current == 12 :
                await message.channel.send("You've been handed a large bag as a souvenir. What do you do? \n\n1) Shake it.\n2) Open it.\n3) Wait until I get home to open it.")          
                done = False
                while done == False :

                    temp = await client.wait_for('message', check=check(message.author) )
                    if temp.content.find("1") != -1 :
                        personalities[3][1] += 1
                        personalities[1][1] += 2
                        done = True
                    elif temp.content.find("2") != -1 :
                        personalities[4][1] += 2
                        personalities[0][1] += 1
                        done = True
                    elif temp.content.find("3") != -1 :
                        personalities[2][1] += 1
                        done = True
                    else :
                        await temp.channel.send("Invalid Response, Try Again.")

            #Remove current question from list of questions    
            i = 0
            for x in questions:
                if current == x :
                    questions.pop(i)
                else :
                    i += 1

            count += 1
            
        #Determine Nature
        rand = random.randint(0,4)
        nature = personalities[rand]
        for x in personalities :
            if x[1] > nature[1] :
                nature = x

        #Send Nature to Discord Chat
        await message.channel.send(f"You are the {nature[0]} type.")
