import os
import json
import datetime

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from data.teams import teams, role_channel_id, role_message
from data.schedules import scheduled_messages

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client()


# This example requires the 'members' privileged intents

import discord

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        # Team Role code
        with open("data/reaction_message.json") as f:
            self.team_role_message = json.load(f)["id"]
            # ID of the message that can be reacted to to add/remove a role.
        self.team_roles = {team.pop("emoji"): team for team in teams}
        self.scheduled_messages_sender.start()

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=GUILD)

        # Init team selection
        channel = self.get_channel(role_channel_id)
        messages = await channel.history(limit=200).flatten()
        if len([m for m in messages if m.author.id == self.user.id]) == 0:
            message = await channel.send(role_message)
            for emoji in self.team_roles.keys():
                await message.add_reaction(emoji)
            with open("data/reaction_message.json", "w") as f:
                json.dump({"id": message.id}, f)
            self.team_role_message = message.id

    # async def on_member_join(self, member):
    #     await member.add_roles(900563813173170207)

    @tasks.loop(seconds=60)
    async def scheduled_messages_sender(self):
        for message in scheduled_messages:
            if datetime.datetime.now() - datetime.timedelta(seconds=60) < message["datetime"] < datetime.datetime.now():
                await self.get_channel(message["channelID"]).send(message["message"])

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.team_role_message:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.team_roles[payload.emoji]["roleId"]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
            # Remove other roles
            for other_role in [role.id for role in payload.member.roles]:
                if other_role in [i["roleId"] for i in self.team_roles.values()]:
                    await payload.member.remove_roles(guild.get_role(other_role))
                    other_emoji = [e for e, r in zip(self.team_roles.keys(), self.team_roles.values()) if r["roleId"]==other_role][0]
                    await message.remove_reaction(other_emoji, payload.member)

            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.team_role_message:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.team_roles[payload.emoji]["roleId"]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(TOKEN)

