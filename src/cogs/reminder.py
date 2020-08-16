from discord.ext import commands, tasks
import discord
import uuid
from tinydb import TinyDB, Query
from datetime import datetime
import threading

days = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]
reminderChannel = "general"
reminderRole = "D&D"

def getDayRegex():
    return days[datetime.today().weekday()] + "|ALL"

def getTime():
    time = datetime.now()
    return time.strftime("%I:%M%p")

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('reminders.json')
        self.lock = threading.Lock()
        self.remind.start()
        self.untrigger.start()

    def addReminderToDb(self, title, repeating, day, time, id, guild):
        with self.lock:
            self.db.insert({'title': title, 'repeating': repeating, 'day': day, 'time': time, 'id': id, 'guild': guild, 'triggered': False})

    def removeReminder(self, id):
        with self.lock:
            Q = Query()
            self.db.remove(Q.id == id)

    def triggerReminder(self, id):
        with self.lock:
            Q = Query()
            self.db.update({'triggered': True}, Q.id == id)

    def getReminders(self):
        with self.lock:
            Q = Query()
            return self.db.search((Q.time == getTime()) & (Q.day.search(getDayRegex())) & (Q.triggered == False))

    def getRemindersToUntrigger(self):
        with self.lock:
            Q = Query()
            return self.db.search((Q.time != getTime()) & (Q.triggered == True))

    def untriggerReminder(self, id):
        with self.lock:
            Q = Query()
            self.db.update({'triggered': False}, Q.id == id)
    
    def getAllReminders(self):
        with self.lock:
            return self.db.all()

    @commands.command()
    async def listReminders(self, ctx):
        reminders = self.getAllReminders()
        response = "```"
        for reminder in reminders:
            response = response + f"{reminder['title']} - Repeating:{reminder['repeating']} - {reminder['day']} - {reminder['time']}\n{reminder['id']}\n\n"
        response = response + "```"
        await ctx.send(response)

    @commands.command()
    async def deleteReminder(self, ctx, id):
        self.removeReminder(id)

    @commands.command()
    async def addreminder(self, ctx, title, repeating, day, time):
        self.addReminderToDb(title, repeating.lower() == 'true', day, time, str(uuid.uuid4()), ctx.message.guild.id)

    @tasks.loop(seconds=10.0)
    async def remind(self):
        reminders = self.getReminders()
        for reminder in reminders:
            guild = self.bot.get_guild(reminder['guild'])
            role = discord.utils.get(guild.roles, name=reminderRole)
            channel = discord.utils.get(guild.channels, name=reminderChannel)
            if reminder['repeating']:
                self.triggerReminder(reminder['id'])
            else:
                self.removeReminder(reminder['id'])
            await channel.send(f"{role.mention} {reminder['title']}")

    @tasks.loop(seconds=125.0)
    async def untrigger(self):
        reminders = self.getRemindersToUntrigger()
        for reminder in reminders:
            self.untriggerReminder(reminder['id'])

