import discord

role_channel_id = 903678864717406268

teams = [
    {
        "roleId" : 905991024449585182,
        "team" : "Team 0",
        "description": "Un muy buen equipo",
        "emoji" : discord.PartialEmoji(name="0️⃣")
    },
    {
        "roleId" : 903679634858709052,
        "team" : "Team 1",
        "description": "Un muy buen equipo",
        "emoji" : discord.PartialEmoji(name="1️⃣")
    },
    {
        "roleId" : 907828811293425724,
        "team" : "Team 2",
        "description": "Un muy buen equipo",
        "emoji" : discord.PartialEmoji(name="2️⃣")
    },
    {
        "roleId" : 907828897637351435,
        "team" : "Team 3",
        "description": "Un muy buen equipo",
        "emoji" : discord.PartialEmoji(name="3️⃣")
    },
    {
        "roleId" : 907828939072868352,
        "team" : "Team 4",
        "description": "Un muy buen equipo",
        "emoji" : discord.PartialEmoji(name="4️⃣")
    }
#  0️⃣ keycap: 0 1️⃣ keycap: 1 2️⃣ keycap: 2 3️⃣ keycap: 3 4️⃣ keycap: 4 5️⃣ keycap: 5 6️⃣ keycap: 6 7️⃣ keycap: 7 8️⃣ keycap: 8 9️⃣ keycap: 9 🔟
]

teams_text = "\n".join(
    [
        f"{team['team']} : {team['emoji']}\n{team['description']}\n" for team in teams
    ]
)

role_message = f"""
Equipos:

{teams_text}
Reacciona con el emoji correspondiente para unirte a un equipo.
"""