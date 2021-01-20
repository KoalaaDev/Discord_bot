from discord.ext import commands
import subprocess
import platform
import os

class Process():
    def __init__(self):
        if platform.system() == "Windows":
            subprocess.Popen(["wt","cmd","/k","java","-jar","C:\\Users\\Microsoft\\Desktop\\python\\Discord_bot\\Cogs\\Lavalink.jar"])
        else:
            subprocess.Popen([])
