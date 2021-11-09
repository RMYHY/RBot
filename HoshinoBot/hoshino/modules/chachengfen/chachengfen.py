import json
import os

import httpx
from nonebot import CommandSession, on_startup

import hoshino
from hoshino import Service

sv = Service('查成分')

vtb_dict = {}


@sv.on_command('查成分')
async def _vtb_search(session: CommandSession):
	bid = session.current_arg.strip()
	if not bid.isdigit():
		session.finish("格式有误，应为数字uid")
	async with httpx.AsyncClient() as client:
		try:
			resp = await client.get(
				f"https://account.bilibili.com/api/member/getCardByMid?mid={bid}", timeout=10)
			if resp.status_code != 200:
				session.finish(f"获取关注列表失败：HTTP {resp.status_code}\n请检查账号的隐私设置")
		except Exception as e:
			hoshino.logger.exception(e)
			session.finish(f"获取关注列表失败：{e}\n请联系维护组")
	try:
		data = resp.json()
		subscriptions = set([str(x) for x in data["card"]["attentions"]])
		vtbs = set(vtb_dict.keys())
		subscribe_vtbs = subscriptions & vtbs
		subscribe_vtbs_name = [vtb_dict[x] for x in subscribe_vtbs]
		message = f"{data['card']['name']} 关注的vtb有{len(subscribe_vtbs)}位，TA们是：\n{'，'.join(subscribe_vtbs_name)}"
	except Exception as e:
		hoshino.logger.exception(e)
		message = f"检索关注列表时失败:{e}\n请检查账号的隐私设置"

	session.finish(message)


@on_startup
async def _update_vtb_list():  # 只在启动时更新
	global vtb_dict
	hoshino.logger.info("更新vtb名单...")
	async with httpx.AsyncClient() as client:
		try:
			resp = await client.get(
				f"https://vdb.vtbs.moe/json/list.json", timeout=10)
			if resp.status_code != 200:
				hoshino.logger.error(f"更新vtb列表时发生错误:HTTP {resp.status_code}")
				return
		except Exception as e:
			hoshino.logger.exception(e)
			hoshino.logger.error(f"更新vtb列表时发生错误:{repr(e)}")
			return
		data = resp.json()["vtbs"]
		bilibili_vtbs = filter(lambda x: len(x["accounts"]) != 0 and [lambda a: a["platform"]=='bilibili',x["accounts"][0].get("platform") == 'bilibili',
		                       data)
		bilibili_vtbs_dict = {x["accounts"][0].get(
			"id"): x["name"][x["name"]["default"]] for x in bilibili_vtbs}
		with open(os.path.join(os.path.dirname(__file__), 'bilibili_vtbs.json'), 'w', encoding='utf8') as f:
			json.dump(bilibili_vtbs_dict, f, ensure_ascii=False, indent=2)
		vtb_dict = bilibili_vtbs_dict
