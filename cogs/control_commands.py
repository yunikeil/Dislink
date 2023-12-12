@bot.command()
async def cog_load(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.load_extension(f"cogs.{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} loaded!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command()
async def cog_unload(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.unload_extension(f"cogs.{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} unloaded!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command()
async def cog_reload(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.reload_extension(f"cogs.{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} reloaded!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command()
async def remove_cog(ctx: commands.Context, cog: str):
    if ctx.author.id not in bot.OWNERS:
        return
    try:
        await bot.remove_cog(name=f"{cog}")
    except BaseException as ex:
        message = await ctx.channel.send(f"Exception:\n```bash\n{ex}\n```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))
    else:
        message = await ctx.channel.send(f"```cogs.{cog} removed!```")
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))


@bot.command(name="eval")
async def eval_string(ctx: commands.Context, *, content: str):
    if ctx.author.id not in bot.EVAL_OWNER:
        return
    standart_args = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "asyncio": asyncio,
    }
    if "```" in content:
        content = "\n".join(content.split("\n")[1:-1])
    try:
        await aeval.aeval(content, standart_args, {})
    except Exception as ex:
        message = await ctx.channel.send(
            f"Exception:\n```bash\n{str(ex).replace('```', '`')}\n```"
        )
        await message.edit(view=DeleteMessage(ctx=ctx, message=message))