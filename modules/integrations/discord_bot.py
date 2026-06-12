import os
import threading

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
_bot_instance = None
_bot_thread = None


def start_bot() -> str:
    global _bot_instance, _bot_thread
    if not BOT_TOKEN:
        return "Discord bot token not set. Add DISCORD_BOT_TOKEN to .env"
    try:
        import discord
        from discord.ext import commands
    except ImportError:
        return "discord.py not installed. Run: pip install discord.py"
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"[DISCORD] Logged in as {bot.user}")

    @bot.command(name="friday")
    async def friday_cmd(ctx, *, message: str = ""):
        if not message:
            await ctx.send("FRIDAY Ultra online! Use !friday <your command>")
            return
        try:
            from modules.llm.llm_manager import query_llm, TaskType

            response = query_llm(
                f"Answer concisely: {message}", task_type=TaskType.FAST_CONVERSATION
            )
            await ctx.send(response[:1900] or "Sorry, I couldn't process that.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)[:100]}")

    @bot.command(name="status")
    async def status_cmd(ctx):
        import psutil

        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        await ctx.send(f"FRIDAY Status:\nCPU: {cpu}%\nRAM: {mem}%")

    @bot.command(name="help")
    async def help_cmd(ctx):
        await ctx.send("Commands: !friday <message>, !status, !help")

    _bot_instance = bot

    def _run():
        try:
            bot.run(BOT_TOKEN)
        except Exception as e:
            print(f"[DISCORD] Bot error: {e}")

    _bot_thread = threading.Thread(target=_run, daemon=True)
    _bot_thread.start()
    return "Discord bot started."


def stop_bot() -> str:
    global _bot_instance
    if _bot_instance:
        try:
            import asyncio

            asyncio.run_coroutine_threadsafe(_bot_instance.close(), _bot_instance.loop)
        except Exception:
            pass
        _bot_instance = None
    return "Discord bot stopped."


def status() -> str:
    return "Discord bot is running." if _bot_instance else "Discord bot is stopped."
