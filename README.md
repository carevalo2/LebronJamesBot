An all purpose Discord bot written in discord.py. I started this Discord bot when I was in middle school, and will update occasionally 
throughout my time at University.

Two things to note:

This bot uses asyncpg, an async wrapper for PostgreSQL. 

1. You need to create a .env file in the directory under LebronJamesBot.

You need to set four secrets:
discord_token (your bot's discord token)
database_password (your database password, postgresql)
DATABASE_URL (the url to your database, use pgadmin if you don't know it)
guild_id (your server's id)

I recommend using PgAdmin for ease of access when using PostgreSQL.

This bot has a built in command tracker, cryptocurrency price tracker and converter (BTC, ETH, LTC), among other things.


