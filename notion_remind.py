import os
import arrow

from notion.client import NotionClient
import requests

notion_token = os.environ['NOTION_TOKEN_V2']
notion_page = os.environ['NOTION_PAGE']
server_token = os.environ['SERVER_TOKEN']

client = NotionClient(token_v2=notion_token)
page = client.get_block(notion_page)

for remind in page.children:
    try:
        re_data = remind. _get_record_data()['properties']['title'][0][1][0][1]
        start_date = re_data['start_date']
        start_time = re_data['start_time']
        time_zone = re_data['time_zone']

        now = arrow.utcnow().to(time_zone)
        start = arrow.get(f'{start_date} {start_time}',
                          'YYYY-MM-DD HH:mm', tzinfo=time_zone)

        re_content = remind. _get_record_data()['properties']['title'][1][0]
        if now < start:
            duration = start - now
            if duration.total_seconds() <= 300:
                requests.get(f'https://sctapi.ftqq.com/{server_token}.send?title={start.humanize(now, locale="zh-cn")}&desp={re_content}')
    except:
        continue
