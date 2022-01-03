import discord
from discord.ext import commands

from Cogs.RandomCommands import embed_build, random_build, random_role_list, random_champion_list
from random import shuffle

class Teams(commands.Cog):
    """Team commands"""
    teams = {}

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        "Join a team"
        user = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.guild
        
        if server is None:
            reply = "You'll have to be in a server to join a team."
        else:
            self.add_to_team(user, team_name=channel.name, id=server.id)
            reply = "{} joined {}".format(user.mention, channel.name)
        await ctx.send(reply)

    @commands.command()
    async def leave(self, ctx):
        "Leave a team"
        user = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.guild
        
        if server is None:
            reply = "You'll have to be in a server to leave a team."
        else:
            self.remove_from_team(user, team_name=channel.name, id=server.id)
            reply = "{} left {}".format(user.mention, channel.name)
        await ctx.send(reply)

    @commands.command()
    async def reset(self, ctx):
        "Reset the current team"
        channel = ctx.message.channel
        server = ctx.message.guild
        
        if server is None:
            reply = "You'll have to be in a server to reset a team."
        else:
            self.create_team(channel.name, server.id)
            reply = "You reset the team"
        await ctx.send(reply)


    @commands.command(name="team")
    async def team(self, ctx):
        "Shows the current team"
        server = ctx.message.guild
        channel = ctx.message.channel
        team = None

        if server:
            team = self.get_team(channel.name, server.id)
        if team:
            users = team.get_users()
            if users:
                users = ['- {}'.format(user.name) for user in users]
                users = '\n'.join(users)
            else:
                users = 'This team is still empty'


            embed=discord.Embed(
            color=discord.Color.blurple(),
            )
            embed.set_author(
            name="{}".format(team.name), 
            )

            embed.add_field(name="**Users**", value=users, inline=False)
            await ctx.send(embed=embed)
        else:
            reply = "Team is not yet created"
            await ctx.send(reply)

    @commands.command(name='teambuild')
    async def team_build(self, ctx):
        "Generates a random build for the current team"
        server = ctx.message.guild
        channel = ctx.message.channel
        team = None
        users = None


        if server:
            team = self.get_team(channel.name, server.id)
        if team:
            users = team.get_users()
        if users:
            champions = random_champion_list()
            roles = random_role_list()
            for i in range(len(users)):
                build = random_build()
                #overwrite roles and champions
                build['Champion'] = champions[i]
                build['Role'] = roles[i]
                embed = embed_build(build)
                await ctx.send(users[i].mention, embed=embed)
        else:
            reply = "Please create a team first"
            await ctx.send(reply)



    @classmethod
    def add_to_team(cls, username, team_name, id):
        team = cls.get_team(team_name, id)
        if not team:
            cls.create_team(team_name, id)
            team = cls.get_team(team_name, id)
        return team.add_user(username)

    @classmethod
    def remove_from_team(cls, username, team_name, id):
        team = cls.get_team(team_name, id)
        if team:
            return team.remove_user(username)
        else:
            return False

    
    @classmethod
    def get_team(cls, team_name, id):
        team_list = cls.teams.get(id)
        if team_list:
            team = team_list.get(team_name)
        else:
            team = None
        return team

    @classmethod
    def create_team(cls, team_name, id):
        if cls.teams.get(id) is None:
            cls.teams[id] = {}
        cls.teams[id][team_name] = Team(team_name)



class Team():
    max_team_size = 5

    def __init__(self, name):
        self.reset()
        self.name = name

    def get_users(self):
        return self.users

    def get_team_size(self):
        return len(self.users)

    def remove_user(self, user_name):
        if user_name in self.users:
            self.users.remove(user_name)
        return True

    def add_user(self, user_name):
        if self.get_team_size() >= self.max_team_size:
            return False
        if user_name in self.users:
            return False
        
        self.users.append(user_name)
        return True

    def reset(self):
        self.users = []


if __name__ == '__main__':
    team = Team('Backstage')
    team.add_user('Stijn')
    team.add_user('Anne')
    team.add_user('Stijn')


    print(team.get_users())