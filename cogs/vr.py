
import discord
import json
from discord.ext import commands
import datetime


class vr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def help_custom(self):
		      emoji = '<:ares_award:1072904477113327667>'
		      label = "Vanity"
		      description = "Use ?vanityroles setup <vanity> <channel> <role>"
		      return emoji, label, description 

    @commands.group(aliases=['vr'])
    @commands.has_permissions(administrator=True)
    async def vanityroles(self, ctx):
        prefix = ctx.prefix
        em = discord.Embed(
          description=f"`{prefix}vanityroles setup`\nSetups vanity in the server.\n\n`{prefix}vanityroles reset`\nDisabled vanity.\n\n`{prefix}vanityroles config`\nShows the configured vanity for the server.", color=0x030404)
        await ctx.reply(embed=em)
      
    @vanityroles.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx, vanity,
                     channel: discord.TextChannel,role: discord.Role):
        with open("penny.json", "r") as f:
            idk = json.load(f)
            if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
                if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members:
                    embed1 = discord.Embed(
                        description=
                        "Vanity roles won't be setup while role have administrator",
                        color=0x030404)
                    await ctx.send(embed=embed1)
                else:
                    pop = {
                        "vanity": vanity,
                        "role": role.id,
                        "channel": channel.id
                    }
                    idk[str(ctx.guild.id)] = pop
                    embed = discord.Embed(color=0x030404)
                    embed.set_author(name=f"Vanity Roles Config For {ctx.guild}", icon_url=ctx.author.display_avatar.url, url="https://discord.gg/PkADcr29VX")
                    embed.add_field(name="<a:Arrow:1072467877539618838> **__Vanity__**", value='Not Set' if vanity is None else vanity, inline=False)
                    embed.add_field(name="<a:Arrow:1072467877539618838> **__Role__**", value='Not Set' if role is None else role.mention, inline=False)
                    embed.add_field(name="<a:Arrow:1072467877539618838> **__Channel__**", value='Not Set' if channel is None else channel.mention, inline=False)

                    await ctx.send(embed=embed, mention_author=False)
                    with open("penny.json", "w") as f:
                        json.dump(idk, f, indent=4)
            else:
                embed5 = discord.Embed(
                    description=
                    """You have to be top of my role""",
                    color=0x030404)
                await ctx.reply(embed=embed5, mention_author=False)

  
    @vanityroles.command(aliases=[('delete','remove')])
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        with open("penny.json", "r") as f:
            xd = json.load(f)
            if ctx.author == ctx.guild.owner or ctx.guild.me.top_role <= ctx.author.top_role:
                if str(ctx.guild.id) not in xd:
                    embed1 = discord.Embed(
                        description=
                        "Please add vanity roles first",
                        color=0x030404)
                    await ctx.reply(embed=embed1, mention_author=False)
                else:
                    xd.pop(str(ctx.guild.id))
                    await ctx.reply(embed=discord.Embed(color=0x030404, description="Successfully Removed Vanity-Roles Setup"),
                        mention_author=False)
                    with open('penny.json', 'w') as f:
                        json.dump(xd, f, indent=4)
            else:
                embed5 = discord.Embed(
                    description=
                    """You have to be top of my role""",
                    color=0x030404)
                await ctx.reply(embed=embed5, mention_author=False)

    @vanityroles.command(aliases=[("show")])
    
    
    
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        with open("penny.json", "r") as f:
            xd = json.load(f)
        if str(ctx.guild.id) not in xd:
            embed1 = discord.Embed(
                        description=
                        "Please add vanity roles first",
                        color=0x030404)
            await ctx.reply(embed=embed1, mention_author=False)
        elif str(ctx.guild.id) in xd:
            vanity = xd[str(ctx.guild.id)]["vanity"]
            role = xd[str(ctx.guild.id)]["role"]
            channel = xd[str(ctx.guild.id)]["channel"]
            channel = self.bot.get_channel(channel)
            role = ctx.guild.get_role(role)
            embed = discord.Embed(color=0x030404)
            embed.set_author(name=f"Vanity Roles Config For {ctx.guild}", icon_url=ctx.author.display_avatar.url, url="https://discord.gg/PkADcr29VX")
            embed.add_field(name="<a:Arrow:1072467877539618838> **__Vanity__**", value='Not Set' if vanity is None else vanity, inline=False)
            embed.add_field(name="<a:Arrow:1072467877539618838> **__Role__**", value='Not Set' if role is None else role.mention, inline=False)
            embed.add_field(name="<a:Arrow:1072467877539618838> **__Channel__**", value='Not Set' if channel is None else channel.mention, inline=False)

            await ctx.send(embed=embed, mention_author=False)


    
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
      with open("penny.json", "r") as f:
        jnl = json.load(f)
      if str(before.guild.id) not in jnl:
        return
      elif str(before.guild.id) in jnl:
        vanity = jnl[str(before.guild.id)]["vanity"]
        role = jnl[str(before.guild.id)]["role"]
        channel = jnl[str(before.guild.id)]["channel"]
        if str(before.status) == "offline":
          return

          
        gchannel = self.bot.get_channel(channel)
        grole = after.guild.get_role(role)
        if before.bot:
            return
        if before.guild.id != after.guild.id:
            return

        if before.activity == after.activity:
            return

        if vanity in str(after.activity).lower() and grole not in after.roles:
            await after.add_roles(grole, reason=f"Added {vanity} In Status")
            embed=discord.Embed(color=0x030404, description=f"{after.mention} Thanks for Repping Vanity {vanity} in your status <3".title(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)
            embed.set_footer(text="Thanks For Choosing demom-vanity.")
            await gchannel.send(embed=embed)
          

        elif vanity not in str(after.activity).lower() and grole in after.roles:
            await after.remove_roles(grole, reason=f"Removed {vanity} From Status")
            embed=discord.Embed(color=0x030404, description=f"{after.mention} Removed [demon-vanity ](https://discord.gg/ded) Vanity {vanity} From His/Her Status <3".title(), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=after.name, icon_url=after.display_avatar.url)
            embed.set_footer(text="Thanks For Choosing demon-vanity")
            await gchannel.send(embed=embed)
async def setup(bot):
  await bot.add_cog(vr(bot))