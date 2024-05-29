import os
import re
import argparse
from aliyundrive import Aliyundrive
from message_send import MessageSend


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token_string', type=str, required=True)
    args = parser.parse_args()

    token_string = args.token_string
    pushplus_token = os.environ.get('PUSHPLUS_TOKEN')
    serverChan_sendkey = os.environ.get('SERVERCHAN_SENDKEY')
    weCom_tokens = os.environ.get('WECOM_TOKENS')
    weCom_webhook = os.environ.get('WECOM_WEBHOOK')
    bark_deviceKey = os.environ.get('BARK_DEVICEKEY')
    feishu_deviceKey = os.environ.get('FEISHU_DEVICEKEY')
    bark_icon = os.environ.get('BARK_ICON')

    if not token_string:
        print('不执行签到1,token为null')
        return -1

    token_string = token_string.strip()
    if len(token_string) <= 3:
        print('不执行签到2,token的值无效')
        return -2

    message_tokens = {
        'pushplus_token': pushplus_token,
        'serverChan_token': serverChan_sendkey,
        'weCom_tokens': weCom_tokens,
        'weCom_webhook': weCom_webhook,
        'bark_deviceKey': bark_deviceKey,
        'feishu_deviceKey': feishu_deviceKey,
    }

    token_string = token_string.split(',')
    ali = Aliyundrive()
    message_all = []

    for idx, token in enumerate(token_string):
        result = ali.aliyundrive_check_in(token)
        message_all.append(str(result))

        if idx < len(token_string) - 1:
            message_all.append('--')

    title = '阿里云盘签到结果'
    message_all = '\n'.join(message_all)
    message_all = re.sub('\n+', '\n', message_all).rstrip('\n')

    message_send = MessageSend()
    message_send.send_all(message_tokens, title, message_all, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()
