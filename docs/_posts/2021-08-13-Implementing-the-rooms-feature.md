---
layout: post
title: Implementing the rooms feature
---

# Implementation of rooms
1. Create a room with a topic name.
2. The ability to make a room private, or public.
3. Deleting the room
4. Deleting a room after it's been inactive for 30 minutes.

The first part is already done.
```python
    async def create_new_room(self, ctx, name):
        guild = ctx.guild

        categories = guild.categories
        category_name = ""
        for category in categories:
            if category.name == "Rooms":
                category_name = category
                break

        topic = f"{ctx.author.name} would like to discuss about {name}."
        channel = await guild.create_text_channel(name, topic=topic, category=category_name)
        return channel
```
By passing in the context, and the name of the person who created to room. A new text channel under the room category will be created with a designated topic that always follows the format `"<author> would like to discuss about <topic>"`
