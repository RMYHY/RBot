import re
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
    for msg_seg in msg:
        if msg_seg.type == "at":
            users.append(UserInfo(qq=msg_seg.data["qq"], group=str(ev.group_id)))
        elif msg_seg.type == "image":
            users.append(UserInfo(img_url=msg_seg.data["url"]))
        elif msg_seg.type == "text":
            for text in str(msg_seg.data["text"]).split():
                if prefix != "":
                    text = re.sub(prefix, "", text)
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


@sv.on_prefix(("/", "pp/"))
async def gen_image(bot: HoshinoBot, ev: CQEvent):
    msg = ev.message.extract_plain_text().strip()
    assert isinstance(msg, str)
    for com in commands:
        for kw in com.keywords:
            if msg.startswith(kw):
                if kw == "玩" and msg.startswith("玩游戏"):
                    continue
                args = msg[len(kw) :]
                users, args = await handle(ev, kw)
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
