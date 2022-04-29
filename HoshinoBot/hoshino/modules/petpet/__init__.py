import re
import shlex
from base64 import b64encode
from io import BytesIO
from typing import List, Tuple

from hoshino import HoshinoBot, Service
from hoshino.typing import CQEvent, MessageSegment

from .data_source import commands, make_image
from .download import DownloadError, ResourceError
from .models import UserInfo
from .utils import help_image

sv = Service("头像表情包")


def bytesio2b64(im: BytesIO) -> str:
    im = im.getvalue()
    return f"base64://{b64encode(im).decode()}"


@sv.on_fullmatch("头像表情包")
async def help(bot: HoshinoBot, ev: CQEvent):
    im = await help_image(commands)
    await bot.send(ev, MessageSegment.image(bytesio2b64(im)))


def is_qq(msg: str):
    return msg.isdigit() and 11 >= len(msg) >= 5


async def get_user_info(bot: HoshinoBot, user: UserInfo):
    if not user.qq:
        return

    if user.group:
        info = await bot.get_group_member_info(
            group_id=int(user.group), user_id=int(user.qq)
        )
        user.name = info.get("card", "") or info.get("nickname", "")
        user.gender = info.get("sex", "")
    else:
        info = await bot.get_stranger_info(user_id=int(user.qq))
        user.name = info.get("nickname", "")
        user.gender = info.get("sex", "")


async def handle(ev: CQEvent, prefix: str = "") -> Tuple[List[UserInfo], List[str]]:
    users: List[UserInfo] = []
    args: List[str] = []
    msg = ev.message
    is_reply = 0
    for msg_seg in msg:
        if is_reply:
            is_reply = 0
            continue
        if msg_seg.type == "at":
            users.append(UserInfo(qq=msg_seg.data["qq"], group=str(ev.group_id)))
        elif msg_seg.type == "image":
            users.append(UserInfo(img_url=msg_seg.data["url"]))
        elif msg_seg.type == "reply":
            msg_id = re.search(r"(?:id=)(.+)\]", str(msg_seg)).group(1)
            source_msg = await sv.bot.get_msg(message_id=int(msg_id))
            source_msg = source_msg["message"]
            url = re.search(r"(?:url=)(.+)(?:,)", str(source_msg))
            if not url:
                continue
            users.append(UserInfo(img_url=url.group(1)))
            is_reply = 1
        elif msg_seg.type == "text":
            raw_text = re.sub(prefix, "", str(msg_seg)).strip()
            try:
                texts = shlex.split(raw_text)
            except:
                texts = raw_text.split()
            for text in texts:
                if is_qq(text):
                    users.append(UserInfo(qq=text))
                elif text == "自己":
                    users.append(UserInfo(qq=str(ev.user_id), group=str(ev.group_id)))
                else:
                    text = text.strip()
                    if text:
                        args.append(text)
    if not users:
        users.append(UserInfo(qq=str(ev.self_id), group=str(ev.group_id)))
    return users, args


@sv.on_rex(r"^(?:pp)?/([\w@]+)(?:\s.+)?")
async def gen_image(bot: HoshinoBot, ev: CQEvent):
    match: re.Match = ev["match"]
    hit: str = match.group(1)
    for com in commands:
        for kw in com.keywords:
            if hit == kw:
                users, args = await handle(ev, f"/{hit}")
                sender = UserInfo(qq=str(ev.user_id))
                await get_user_info(bot, sender)
                for user in users:
                    await get_user_info(bot, user)
                try:
                    im = await make_image(com, sender, users, args=args)
                except DownloadError:
                    await bot.finish(ev, "图片下载出错，请稍后再试")
                except ResourceError:
                    await bot.finish(ev, "资源下载出错，请稍后再试")
                except Exception as e:
                    sv.logger.debug(f"{e}")
                    await bot.finish(ev, "出错了，请稍后再试")
                if isinstance(im, str):
                    im = MessageSegment.text(im)
                else:
                    im = MessageSegment.image(bytesio2b64(im))
                await bot.finish(ev, im)
