import discord


class GeneralResponseButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Tell me more.", style=discord.ButtonStyle.blurple)
    async def blurple_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.style = discord.ButtonStyle.red
        await interaction.response.edit_message(content=f"This is merely a test of button functionality!", view=self)

    @discord.ui.button(label="OK", style=discord.ButtonStyle.grey)
    async def ok_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.style = discord.ButtonStyle.green
        await interaction.response.edit_message(content=f"You clicked OK!", view=self)

    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.red)
    async def cancel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.style = discord.ButtonStyle.grey
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="Cancelled!", view=self)


class ButtonLinks:
    github = discord.ui.Button(label="IODES LYKOS", style=discord.ButtonStyle.link,
                               url="https://github.com/iodeslykos", emoji="<:iodes:750029680907780146>")


class AdminActionPrompt(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="SHUTDOWN", style=discord.ButtonStyle.red)
    async def shutdown_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.style = discord.ButtonStyle.grey
        await interaction.response.edit_message(content=f"Shutting down!", view=self)

    @discord.ui.button(label="CANCEL", style=discord.ButtonStyle.green)
    async def cancel_button(self, button: discord.ui.Button, interaction: discord.InteractionMessage):
        button.style = discord.ButtonStyle.grey
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="Shutdown cancelled!", view=self)
