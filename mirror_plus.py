import threading
import os
import json
import colorama
import time
import psutil
import shutil
import ruamel.yaml as yaml
from subprocess import Popen, PIPE
from signal import SIGTERM
from mcdreforged.api.all import *
from locale import getpreferredencoding
import sys


# process =
# for line in iter(pipe.stdout.readline, ''):
#     print(line.decode('gbk').rstrip())
ENCODING = sys.getdefaultencoding()
DECODING = getpreferredencoding()


def shorter_text(text, length=20):
    if len(text) > length:
        return text[:length] + '...'
    else:
        return text


class MirrorServer:
    def __init__(self, config_path, server: ServerInterface):
        self.config_path = config_path
        self.config = self.load_config()
        self.o_server_folder = self.get_server_folder()
        self.status = 0
        self.server = server
        colorama.init(autoreset=True)

    def load_config(self):
        default_config = {
            "work_folder": "mirror",
            "world_name": [
                "world"
            ],
            "start_command": "java -Xmx4G -jar server.jar",
            "start_after_main": True,
            "minimum_permission_level": {
                "start": 0,
                "stop": 0,
                "kill": 0,
                "restart": 0,
                "sync": 0,
                "reload": 0,
                "send": 0
            }
        }
        if not os.path.isfile(self.config_path):
            with open('config/mirror_plus.json', 'w', encoding='utf8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            return default_config
        else:
            with open('config/mirror_plus.json', 'r', encoding='utf8') as f:
                return json.load(f)

    def reload_config(self, source: CommandSource):
        self.config = self.load_config()
        source.reply('成功重载配置文件')

    def receive(self):
        while True:
            try:
                text = next(iter(self.process.stdout))
            except StopIteration:
                self.status = 2
                for i in range(600):
                    if not psutil.pid_exists(self.process.pid):
                        break
                    time.sleep(0.1)
                self.clean_pool()
                break
            else:
                try:
                    decoded_text = text.decode(DECODING)  # type: str
                except:
                    print('镜像服数据解码错误')
                    raise
                return decoded_text.rstrip('\n\r').lstrip('\n\r')

    def send(self, command):
        encoded_text = (command + '\n').encode()
        self.process.stdin.write(encoded_text)
        self.process.stdin.flush()
        self.server.say(f'成功向镜像服发送命令 §6{shorter_text(command)}')

    def start(self, source: CommandSource = None):
        if not self.status:
            self.process = Popen(
                self.config['start_command'], stdout=PIPE, stdin=PIPE, cwd=self.config['work_folder'])
            print(self.process)
            self.status = 1
            self.tick()
            self.server.say('正在启动镜像服...')
        elif source:
            source.reply('镜像服已开机或正在开启，请勿重复执行！')

    def kill(self, source: CommandSource = None):
        if self.status:
            os.kill(self.process.pid, SIGTERM)
            self.server.say('正在杀死镜像服...')
            self.clean_pool()
        elif source:
            source.reply('镜像服已关闭，请勿重复执行！')

    

    def stop(self, source: CommandSource = None, noout=False, blocking=False):
        def _stop():
            if self.status == 1:
                self.send('stop')
                if not noout: self.server.say('正在关闭镜像服...')
                while self.status: time.sleep(0.1)
                if not noout: self.server.say('镜像服关闭...')
                self.clean_pool()
            elif source and not noout:
                source.reply('镜像服已关闭或正在关闭，请勿重复执行！')
        if blocking:
            _stop()
        else:
            threading.Thread(target=_stop).start()

    def clean_pool(self):
        self.status = 0
        self.process.stdin.close()
        self.process.stdout.close()

    @new_thread('Mirror+')
    def restart(self, source: CommandSource):
        if self.status != 1:
            source.reply('镜像服未开机或正在关机，无法重启！')
        self.stop(blocking=True)
        self.start()

    def get_server_folder(self):
        with open('config.yml', 'r', encoding='utf8') as f:
            return yaml.safe_load(f)['working_directory']

    @new_thread('Mirror+')
    def sync(self):
        self.server.say('正在同步镜像服...')
        self.server.execute('save-all flush')
        time.sleep(self.config['save_all_wait'])
        self.stop(blocking=True)

        def filter_ignore(path, files):
            return [file for file in files if file == 'session.lock']
        for i in self.config['world_name']:
            shutil.rmtree(os.path.join(self.config['work_folder'], i))
            shutil.copytree(os.path.join(self.o_server_folder, i), os.path.join(
                self.config['work_folder'], i), ignore=filter_ignore)
        self.start()

    @new_thread('Mirror')
    def tick(self):
        while self.status:
            msg = self.receive()
            if msg != None:
                print(
                    f'{colorama.Fore.YELLOW}[Mirror]{colorama.Fore.CYAN} {msg}{colorama.Fore.RESET}')

    def change_server_interface(self, server: ServerInterface):
        self.server = server

    def get_status(self):
        return self.status

    def get_config(self):
        return self.config


PLUGIN_METADATA = {
    'id': 'mirror_plus',
    'version': '1.0.0',
    'name': 'Mirror+',  # RText component is allowed
    'description': '一个镜像服插件。',  # RText component is allowed
    'author': 'Alex3236',
    'link': 'https://github.com/eagle3236'
}


def show_status(source: CommandSource):
    global mirror
    status_list = {
        0: '已关机',
        1: '正常',
        2: '等待关机'
    }
    text = f'''
---------------------------
创造服状态：{status_list[mirror.get_status()]}
---------------------------
'''.strip()
    source.reply(text)


def on_load(server: ServerInterface, prev):
    global mirror
    if hasattr(prev, 'mirror'):
        mirror = prev.mirror
        mirror.change_server_interface(server)
    else:
        mirror = MirrorServer('config/mirror_plus.json', server)

    def get_literal_node(literal):
        lvl = mirror.get_config()['minimum_permission_level'].get(literal, 0)
        return Literal(literal).requires(lambda src: src.has_permission(lvl), lambda: '权限不足')

    cmd_tree = Literal('!!mirror'). \
        then(get_literal_node('start').runs(mirror.start)). \
        then(get_literal_node('stop').runs(mirror.stop)). \
        then(get_literal_node('kill').runs(mirror.kill)). \
        then(get_literal_node('restart').runs(mirror.restart)). \
        then(get_literal_node('sync').runs(lambda src: mirror.sync())). \
        then(get_literal_node('reload').runs(mirror.reload_config)). \
        then(get_literal_node('status').runs(show_status)). \
        then(get_literal_node('send').
             then(GreedyText('command').runs(lambda src, ctx: mirror.send(ctx['command']))))
    server.register_command(cmd_tree)


def on_mcdr_stop(server: ServerInterface):
    global mirror
    mirror.stop(blocking=True, noout=True)


def on_server_startup(server: ServerInterface):
    global mirror
    if mirror.get_config()['start_after_main']:
        mirror.start()
