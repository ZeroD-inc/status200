from time import sleep
from queue import Queue
from argparse import ArgumentParser
from requests.packages.urllib3 import disable_warnings
from lib.checker import Check
from lib.writer import Writer
from lib.utils import get_count_lines
from lib.progress import Progress


def arg_parse():
    parser = ArgumentParser(description='Многопоточный чекер сайтов на доступность')
    parser.add_argument('-u', '--urls', type=str, help='Файл с целями')
    parser.add_argument('-t', '--threads', type=int, help='Кол-во потоков', default=5)
    parser.add_argument('-o', '--output', type=str, help='Имя файла для сохранения результатов', default='good.txt')
    parser.add_argument('--timeout', type=int, help='Задать таймаут', default=3)

    args = parser.parse_args()

    return args


def main():
    disable_warnings()
    u_queue = Queue(maxsize=1000)
    w_queue = Queue()
    progress = Queue()
    arg = arg_parse()

    count_lines = get_count_lines(arg.urls)
    print(f'Загружено строк: {count_lines}')

    writer = Writer(w_queue, arg.output)
    writer.setDaemon(True)
    writer.start()

    progress_bar = Progress(count_lines, progress)
    progress_bar.setDaemon(True)
    progress_bar.start()

    for _ in range(arg.threads):
        t = Check(u_queue, w_queue, progress, arg.timeout)
        t.setDaemon(True)
        t.start()

    with open(arg.urls, 'r', encoding='utf8') as urls:
        for url in urls:
            url = url.rstrip()
            protocol = url.split('//')
            if 'http' in protocol[0]:
                u_queue.put(url)
            else:
                url = f'http://{url}'
                u_queue.put(url)
        u_queue.join()

    sleep(30)


if __name__ == '__main__':
    main()
