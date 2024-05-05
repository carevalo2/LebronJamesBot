
import discord
from discord import  ui

import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class HistoryView(ui.View):
    def __init__(self, embeds, author):
        super().__init__()
        self.embeds = embeds
        self.author = author
        self.current_page = 0  # Page numbers start from 0 internally
        self.max_page = len(embeds) - 1

        # Define the navigation buttons
        self.previous_button = ui.Button(label='⬅️', style=discord.ButtonStyle.primary, custom_id='previous_button')
        self.next_button = ui.Button(label='➡️', style=discord.ButtonStyle.primary, custom_id='next_button')
        self.page_indicator = ui.Button(label=f'Page {self.current_page + 1}/{self.max_page + 1}', style=discord.ButtonStyle.secondary, disabled=True)
        self.stop_button = ui.Button(label='⏹️', style=discord.ButtonStyle.danger, custom_id='stop_button')

        self.previous_button.callback = self.previous_button_callback
        self.next_button.callback = self.next_button_callback
        self.stop_button.callback = self.stop_button_callback

        self.add_item(self.previous_button)
        self.add_item(self.page_indicator)
        self.add_item(self.next_button)
        self.add_item(self.stop_button)

        only_one_page: bool = self.current_page == 0 and self.current_page == self.max_page
        if only_one_page:
            self.previous_button.disabled = True
            self.next_button.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def update_embed(self, interaction: discord.Interaction):
        # Update the page indicator label
        page_indicator_label = f'Page {self.current_page + 1}/{self.max_page + 1}'
        self.page_indicator.label = page_indicator_label

        # Edit the message with the new embed and updated view
        await interaction.edit_original_response(embed=self.embeds[self.current_page], view=self)

    async def previous_button_callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            if self.current_page == 0:
                self.current_page = self.max_page
            else:
                self.current_page -= 1
            await self.update_embed(interaction)
        except Exception as e:
            logging.error("Error in previous_button_callback: %s", traceback.format_exc())

    async def next_button_callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            if self.current_page == self.max_page:
                self.current_page = 0
            else:
                self.current_page += 1
            await self.update_embed(interaction)
        except Exception as e:
            logging.error("Error in next_button_callback: %s", traceback.format_exc())

    async def stop_button_callback(self, interaction: discord.Interaction):
        try:
            stopped_embed = discord.Embed(title="Command History", description="The command history view has been stopped.", color=0x00ff00)
            for item in self.children:
                item.disabled = True
            await interaction.response.defer()
            await interaction.edit_original_response(embed=stopped_embed, view=self)
            self.stop()
        except Exception as e:
            logging.error("Error in stop_button_callback: %s", traceback.format_exc())