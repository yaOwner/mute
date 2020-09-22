@client.command()
async def mute(ctx, member: discord.Member = None, time: int = None):
    if not member:
        emb = discord.Embed(description = 'Укажите пользователя!')
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = emb)

    elif not time:
        emb = discord.Embed(description = 'Укажите время!')
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = emb)

    elif member == ctx.guild.owner:
        emb = discord.Embed(description = 'Вы не можете замутить владельца гильдии!')
        emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))

        await ctx.send(embed = emb)

    elif ctx.author.top_role.position < member.top_role.position:
        emb = discord.Embed(description = 'Вы не можете замутить данного пользователя!')
        emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))

        await ctx.send(embed = emb)

    elif member == ctx.author:
        emb = discord.Embed(description = 'Вы не можете замутить самого себя!')
        emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))

        await ctx.send(embed = emb)

    else:
        mute_role = discord.utils.get(ctx.guild.roles, id = 757940746702684270)
        if mute_role in member.roles:   
            emb = discord.Embed(description = 'Данный **пользователь** уже замучен!')
            emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))
                
            await ctx.send(embed = emb)

        else:
            muted.insert_one({"_id": member.id, "time": time})
            await member.add_roles(mute_role)

            emb = discord.Embed(description = f'Вы замутили **{member}**!')
            emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))
                
            await ctx.send(embed = emb)
            
            while True:
                await asyncio.sleep(1)
                        
                for x in muted.find({"_id": member.id}):
                    mute_time = x['time'] - 1
                                
                    muted.update_one({"_id": member.id}, {"$set": {"time": mute_time}})

                    if x['time'] <= 0:
                        await member.remove_roles(mute_role)
                        muted.remove({"_id": member.id})
                        break

                await asyncio.sleep(1)

@client.command(aliases = ['chm'])
async def __check_mute(ctx, member: discord.Member = None):
    mute_role = discord.utils.get(ctx.guild.roles, id = 757940746702684270)

    if not member:
        emb = discord.Embed(description = 'Укажите пользователя!')
        emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))

        await ctx.send(embed = emb)

    elif mute_role in member.roles:
        emb = discord.Embed(description = 'Пользователь не в муте!')
        emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))

        await ctx.send(embed = emb)

    for x in muted.find({"_id": member.id}):
        time = x['time']

        h = int(time) // 3600
        m = (int(time) - h * 3600) // 60
        s = int(time) % 60
        if h < 10:
            h = f"0{h}"
        if m < 10:
            m = f"0{m}"
        if s < 10:
            s = f"0{s}"
        time_reward = f"{h} часа {m} минут {s} секунд"

        emb = discord.Embed(description = f'Мут **{member}** закончится через: `{time_reward}`')
        emb.set_author(name = '{}'.format(ctx.author), icon_url = '{}'.format(ctx.author.avatar_url))

        await ctx.send(embed = emb)