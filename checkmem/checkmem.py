import requests
import psutil
import pandas as pd


def _color_red_or_green(val):
    color = 'red' if val < 0 else 'green'
    return 'color: %s' % color


class CheckMem:

    def __init__(self, address='localhost', port=8888, token=None):
        self.token = token
        self.port = port
        self.address = address
        self.kernels_info = None
        self.process_info = None
        self.combined_info = {}
        self.main()

    def get_kernels_info(self):

        url_sessions = "http://{}:{}/api/sessions".format(self.address, self.port)

        s = requests.Session()

        if self.token:
            headers = {
                'Authorization': 'token {}'.format(self.token)
            }
            s.headers = headers

        response = s.get(url_sessions)
        if response.status_code != 200:
            raise Exception('Impossibile connettersi a jupyter')

        self.kernels_info = {
            i['kernel']['id']: {
                'path': i['path'],
                'state': i['kernel']['execution_state']
            } for i in response.json()}

        if self.kernels_info == {}:
            raise Exception('No one kernel is running?')

    def get_processes_info(self):
        attrs = [
            'cpu_percent',
            'memory_percent',
            'pid',
            'name',
            'cmdline'
        ]
        self.process_info = [
            p.info for p in psutil.process_iter(attrs)
            if 'py' in p.info['name']
        ]

        for p in self.process_info:
            p['cmdline'] = ' '.join(p['cmdline'])

    def combine(self):
        for k in self.kernels_info:
            for p in self.process_info:
                if k in p['cmdline']:
                    self.combined_info[k] = self.kernels_info[k]
                    self.combined_info[k].update(p)

    def mem_occupancy(self):
        kernels_mem = pd.DataFrame(self.combined_info.values())
        kernels_mem.set_index('path', inplace=True)
        return (
            kernels_mem[['memory_percent']]
                .sort_values(by='memory_percent', ascending=False)
                .applymap(_color_red_or_green)

        )

    def cpu_usage(self):
        kernels_cpu = pd.DataFrame(self.combined_info.values())
        kernels_cpu.set_index('path', inplace=True)
        return (
            kernels_cpu[['cpu_percent']]
                .sort_values(by='cpu_percent', ascending=False)
                .applymap(_color_red_or_green)
        )

    def main(self):
        self.get_kernels_info()
        self.get_processes_info()
        self.combine()


if __name__ == '__main__':
    cm = CheckMem()
    cm.mem_occupancy()
