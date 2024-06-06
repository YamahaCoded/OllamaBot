import discord, ollama

messages = []

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):

        if message.author.id == self.user.id:
            return

        if self.user.mention in message.content:
            await message.channel.typing()
            
            user_input = message.content
            messages.append({'role': 'user', 'content': user_input.replace(self.user.mention, '')})
            response = ollama.chat(model='model', messages=messages)
            assistant_reply = response['message']['content']
            
            await message.reply(f"{assistant_reply}")
            messages.append({'role': 'assistant', 'content': assistant_reply})

            history_limit = 3
            if(len(messages) > history_limit):
                messages.pop(0)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('token')
