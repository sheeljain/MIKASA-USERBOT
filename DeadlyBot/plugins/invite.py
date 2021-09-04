from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from DeadlyBot.utils import deadly_cmd, edit_or_reply, sudo_cmd

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Group Link To Sahi Daal Yr Mere Bhai🤦‍♂️")
            return None
        except ChannelPrivateError:
            await event.reply(
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Group Link To Sahi Daal Yr Mere Bhai🤦‍♂️`")
            return None
    return chat_info


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


@bot.on(deadly_cmd(pattern="inviteall ?(.*)"))
@bot.on(sudo_cmd(pattern="inviteall ?(.*)", allow_sudo=True))
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        mafia = await edit_or_reply(event, "`PROCESSING...`")
    else:
        mafia = await edit_or_reply(event, "`PROCESSING...`")
    kraken = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await mafia.edit("`Sorry, Cant kidnape users here`")
    s = 0
    f = 0
    error = "None"

    await mafia.edit("**TERMINAL RUNNING ✅ **\n\n`MEMBERS UTHAYING.......`")
    async for user in event.client.iter_participants(kraken.full_chat.id):
        try:
            if error.startswith("Too"):
                return await mafia.edit(
                    f"**Terminal Finished With Error**\n(`May Got Limit Error from telethon Please try agin Later`)\n**Error** : \n`{error}`\n\n• kidnaped `{s}` people \n• Failed to kidnape `{f}` people"
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await mafia.edit(
                f"**TERMINAL RUNNING ✅...**\n\n• INVITES `{s}` PEOPLE \n• FAILED TO INVITE `{f}` PEOPLE\n\n**× LastError:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await mafia.edit(
        f"**TERMINAL FINISHED ✅** \n\n• SECCESSFULLY MEMBERS UTHAYING `{s}` \n• FAILED TO KIDNAP `{f}` PEOPLES"
    )


@bot.on(admin_cmd(pattern="add ?(.*)"))
@bot.on(sudo_cmd(pattern="add ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await edit_or_reply(event, "`.add` users to a chat, not to a Private Message")
    else:
        logger.info(to_add_users)
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await borg(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await edit_or_reply(event, "Invited Successfully")
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await borg(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await edit_or_reply(event, "Added user to the chat....")


