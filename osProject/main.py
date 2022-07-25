import time
from queue import PriorityQueue
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class Process:
    def __init__(self, process_id, arrival_time, cpu_time1, io_time, cpu_time2):
        self.end_time = None
        self.turnaround_time = 0
        self.waitting_time = 0
        self.response_time = None
        self.cpu_time2 = cpu_time2
        self.io_time = io_time
        self.cpu_time1 = cpu_time1
        self.arrival_time = arrival_time
        self.cpu_time = cpu_time1
        self.p_id = process_id
        self.start = False
        self.first_operation = None

    def set_response_time(self):
        self.response_time += self.first_operation  # - self.arrival_time

    def set_turnaround_time(self):
        self.turnaround_time += self.end_time  # - self.arrival_time


class CpuAlgos:

    def show(self, title, ):
        fig, gnt = plt.subplots()
        gnt.set_ylim(0, 10)
        gnt.set_xlabel('time')
        #        gnt.set_ylabel('')
        gnt.set_title(title)
        gnt.set_yticks([])
        for p in self.chart:
            color = self.colorDict[p[1]]
            start = p[0]
            y = p[2]
        #    print(start, p,y)
            gnt.broken_barh([(start, 1)], y, facecolors=color)
        plt.show()

    def processes_length(self):
        if self.processes_len == 0:
            self.processes_len = len(self.processes)
        return self.processes_len

    def set_throughput(self):
        self.throughput = 1000 * self.processes_length() / self._time

    def set_CPU_Utilization(self):
        self.CPU_Utilization = 100 * (self._time - self.wait) / self._time

    def cpu_results(self):
        processesLen = self.processes_length()

        print('\n\t\t\t\t\t\t\t\t\t\t\t\tCPU\n')
        myTable = PrettyTable(["Avg Turnaround Time", "Response Time", "Avg Waiting Time", "Throughput", "Utilization", "Total Time","Idle Time"])
        myTable.add_row([str(self.turnaround_times / processesLen),str( self.response_times / processesLen),
                         str(self.waitting_times / processesLen),str(self.throughput),str(self.CPU_Utilization),str(self._time),str(self.wait)
                         ])
        print(myTable)

    def process_results(self, ):
        print('\n\t\t\t\t\t\t\t\tPROCESSES\n')
#        print('\nProcess', f'  Response   Waiting   Turnaround   Start   End\n')
        myTable = PrettyTable(["Process", "Response Time", "Waiting Time", "Turnaround Time", "Start Time", "End Time"])
        for p in self.processes.values():
            myTable.add_row([str(p.p_id) ,p.response_time ,p.waitting_time,
                             p.turnaround_time  , p.first_operation , p.end_time])
        print(myTable)
    def read(self):
        with open("/home/ayda/Desktop/proces_inputs.csv", 'r') as file:
            processesData = [[i for i in line.strip().split(',')][:5] for line in file.readlines()[1:]]
        for x in processesData:
            for i in range(len(x)):
                x[i] = int(x[i])
            Id, arr, t1, io, t2 = x
            self.processes[Id] = Process(Id, arr, t1, io, t2)
            self.arrivalTimes.append(self.processes[Id])

    def __init__(self):
        self.jobs = []
        self.response_times = 0
        self.processes_len = 0
        self.turnaround_times = 0
        self.waitting_times = 0
        self.wait = 0
        self.CPU_Utilization = 0
        self.ioQ = []
        self.processes = {}
        self.arrivalTimes = []
        self.readyQueue = []
        self.waittingQueue = []
        self._time = 0
        self.start_time = None
        self.last_arrived = None
        self.colorDict = {}
        self.chart = []
        self.intColor = 0
        self.throughput = None
        self.colors = [
            '#00e6e6',  # cyan
            '#ff99ff',  # pink
            '#421100',  # brown pod
            '#fce300',  # yellow
            '#ff7300',  # orange
            '#990099',  # purple
            '#320042',  # blackcurrant
            '#87b100',  # citrus
            '#423200',  # mikado
            '#00b187',  # persian green
            '#004232',  # british racing green
            '#dd0000',  # red
            '#009900',  # green
            '#002db3',  # blue

        ]
        self.read()
        self.start_time = 0

    def clear(self):
        self.jobs = []
        self.start_time = 0
        self.wait = 0
        self.processes_len = 0
        self.ioQ = []
        self.CPU_Utilization = 0
        self.processes = {}
        self.arrivalTimes = []
        self.readyQueue = []
        self.waittingQueue = []
        self._time = 0
        self.start_time = None
        self.last_arrived = None
        self.colorDict = {}
        self.chart = []
        self.intColor = 0
        self.throughput = None
        self.read()
        self.response_times = 0
        self.turnaround_times = 0
        self.waitting_times = 0

    def uppdateReady(self):
        for p in self.arrivalTimes:
            if p.arrival_time == self._time:
                if p not in self.readyQueue:
                    self.readyQueue.append(p)

    def updateIo(self):
        p = self.readyQueue[0]
        p.cpu_time = p.cpu_time2
        p.response_time = 0 - p.arrival_time
        p.turnaround_time = 0 - p.arrival_time
        p.arrival_time = p.io_time + self._time
        self.last_arrived = max(self.last_arrived, p.arrival_time)
        p.io_time = 0

    def nextQ(self, q):
        temp = self.readyQueue.pop(0)
        q.append(temp)

    def updateReady_MLFQ(self, q):
        for p in self.arrivalTimes:
            if p.arrival_time == self._time and p not in q:
                if p not in self.readyQueue:
                    self.readyQueue.append(p)

    def RR_MLFQ(self, tq, q2, y):
        self.last_arrived = self.arrivalTimes[-1].arrival_time
        i = 0
        while self._time <= self.last_arrived or any(self.readyQueue):
            self.updateReady_MLFQ(q2)
            if self.readyQueue:
                p = self.readyQueue[0]
                if not p.start:
                    p.start = True
                    p.waitting_time += self._time - p.arrival_time
                if p.end_time is None:
                    self.colorDict[p.p_id] = self.colors[self.intColor]
                    self.intColor += 1
                    p.end_time = 0
                    p.first_operation = self._time

                if p.cpu_time > 0:
                    if i < tq:
                        i += 1
                        #if(p.p_id==4):
                         #   print(p.cpu_time,i,self._time)
                        p.cpu_time -= 1
                        self.chart.append((self._time, p.p_id, y))
                        self._time += 1
                        self.uppdateReady()
                    else:
                        i = 0
                        self.nextQ(q2)
                        # temp=self.readyQueue.pop(0)
                        # self.readyQueue.append(temp)
                else:
                    if p.cpu_time == 0 or (p.io_time == 0 and p not in self.ioQ):
                        if p.io_time:
                            # io time
                            p.start = False
                            p.cpu_time -= 1
                            self.ioQ.append(p)
                            self.updateIo()
                            self.readyQueue.remove(p)
                            i = 0

                        elif p.io_time == 0:  # and p in q1:
                            p.start = False
                            p.end_time = self._time
                            p.set_turnaround_time()
                            p.set_response_time()
                            self.response_times += p.response_time
                            self.turnaround_times += p.turnaround_time
                            self.waitting_times += p.waitting_time
                            self.readyQueue.remove(p)
                            i=0
            else:
                self.wait += 1
                self._time += 1

        #  self._time = time.time() - start_time

    # self.clear()
    # self._time=0

    def FCFS_MLFQ(self, y):
        #   self.arrivalTimes=sorted(self.arrivalTimes, key=lambda p: p.arrival_time)
        self.last_arrived = self.arrivalTimes[-1].arrival_time
        while self._time <= self.last_arrived or any(self.readyQueue):
            self.uppdateReady()
            if self.readyQueue:
                p = self.readyQueue[0]
                if not p.start:
                    p.start = True
                    p.waitting_time += self._time - p.arrival_time
                if p.end_time is None:
                    self.colorDict[p.p_id] = self.colors[self.intColor]
                    self.intColor += 1
                    p.end_time = 0
                    p.first_operation = self._time

                if p.cpu_time > 0:
                    p.cpu_time -= 1
                    self.chart.append((self._time, p.p_id, y))
                    self._time += 1
                    self.uppdateReady()

                else:
                    if p.cpu_time == 0 or (p.io_time == 0 and p not in self.ioQ):
                        if p.io_time:
                            # io time
                            p.start = False
                            p.cpu_time -= 1
                            self.updateIo()
                            self.readyQueue.remove(p)

                        elif p.io_time == 0:  # and p in q:
                            p.start = False
                            p.end_time = self._time
                            p.set_turnaround_time()
                            p.set_response_time()
                            self.response_times += p.response_time
                            self.turnaround_times += p.turnaround_time
                            self.waitting_times += p.waitting_time
                            self.readyQueue.remove(p)

            else:
                self.wait += 1
                self._time += 1

    def MLFQ(self):
        queue1 = []
        self.start_time = time.time()
        y1 = (0, 2)
        self.RR_MLFQ(8, queue1, y1)
        y2 = (2, 4)
        self.readyQueue = queue1

        queue2 = []
        self.RR_MLFQ(16, queue2, y2)
        y3 = (4, 6)
        self.readyQueue = queue2
        self.FCFS_MLFQ(y3)
        self.set_throughput()
        self.process_results()
        self.set_CPU_Utilization()
        self.cpu_results()
        self.show("MLFQ")
        self.clear()

    def RR(self, tq):
        self.start_time = time.time()
        self.last_arrived = self.arrivalTimes[-1].arrival_time
        i = 0
        while self._time <= self.last_arrived or any(self.readyQueue):
            self.uppdateReady()
            if self.readyQueue:
                p = self.readyQueue[0]
                if not p.start:
                    p.start = True
                    p.waitting_time += self._time - p.arrival_time
                if p.end_time is None:
                    self.colorDict[p.p_id] = self.colors[self.intColor]
                    self.intColor += 1
                    p.end_time = 0
                    p.first_operation = self._time

                if p.cpu_time > 0:
                    if i < tq:
                        i += 1
                        p.cpu_time -= 1
                        self.chart.append((self._time, p.p_id, (0, 2)))
                        self._time += 1
                        self.uppdateReady()
                    else:
                        i = 0
                        temp = self.readyQueue.pop(0)
                        self.readyQueue.append(temp)
                else:
                    if p.cpu_time == 0 or (p.io_time == 0 and p not in self.ioQ):
                        if p.io_time:
                            # io time
                            p.start = False
                            p.cpu_time -= 1
                            self.updateIo()
                            self.readyQueue.remove(p)

                        elif p.io_time == 0:
                            p.start = False
                            p.end_time = self._time
                            p.set_turnaround_time()
                            p.set_response_time()
                            self.response_times += p.response_time
                            self.turnaround_times += p.turnaround_time
                            self.waitting_times += p.waitting_time
                            self.readyQueue.remove(p)
            else:
                self.wait += 1
                self._time += 1

        #  self._time = time.time() - start_time
        self.set_throughput()
        self.process_results()
        self.set_CPU_Utilization()
        self.cpu_results()
        self.show("RR")
        self.clear()

    def SJF(self):
        self.start_time = time.time()
        self.arrivalTimes = sorted(self.arrivalTimes, key=lambda p: p.arrival_time)
        self.last_arrived = self.arrivalTimes[-1].arrival_time
        while self._time <= self.last_arrived or any(self.readyQueue):
            self.uppdateReady()
            if self.readyQueue:
                p = self.readyQueue[0]
                self.uppdateReady()
                if not p.start:
                    p.start = True
                    p.waitting_time += self._time - p.arrival_time
                if p.end_time is None:
                    self.colorDict[p.p_id] = self.colors[self.intColor]
                    self.intColor += 1
                    p.end_time = 0
                    p.first_operation = self._time

                if p.cpu_time > 0:
                    p.cpu_time -= 1
                    self.chart.append((self._time, p.p_id, (0, 2)))
                    self._time += 1
                    self.uppdateReady()

                else:
                    if p.cpu_time == 0:
                        if p.io_time or (p.io_time == 0 and p not in self.ioQ):
                            # io time
                            p.start = False
                            self.readyQueue = sorted(self.readyQueue, key=lambda p: p.cpu_time)
                            p.cpu_time -= 1
                            self.ioQ.append(p)
                            self.updateIo()
                            self.readyQueue.remove(p)

                        elif p.io_time == 0:
                            p.start = False
                            p.end_time = self._time
                            p.set_turnaround_time()
                            p.set_response_time()
                            self.response_times += p.response_time
                            self.turnaround_times += p.turnaround_time
                            self.waitting_times += p.waitting_time
                            self.readyQueue.remove(p)
                            self.readyQueue = sorted(self.readyQueue, key=lambda p: p.cpu_time)

            else:
                self.wait += 1
                self._time += 1

        #  self._time = time.time() - start_time
        self.set_throughput()
        self.set_CPU_Utilization()
        self.process_results()
        self.cpu_results()
        self.show("SJF")
        self.clear()

    def FCFS(self):
        self.start_time = time.time()
        #   self.arrivalTimes=sorted(self.arrivalTimes, key=lambda p: p.arrival_time)
        self.last_arrived = self.arrivalTimes[-1].arrival_time
        while self._time <= self.last_arrived or any(self.readyQueue):
            self.uppdateReady()
            if self.readyQueue:
                p = self.readyQueue[0]
                if not p.start:
                    p.start = True
                    p.waitting_time += self._time - p.arrival_time
                if p.end_time is None:
                    self.colorDict[p.p_id] = self.colors[self.intColor]
                    self.intColor += 1
                    p.end_time = 0
                    p.first_operation = self._time

                if p.cpu_time > 0:
                    p.cpu_time -= 1
                    self.chart.append((self._time, p.p_id, (0, 2)))
                    self._time += 1
                    self.uppdateReady()

                else:
                    if p.cpu_time == 0 or (p.io_time == 0 and p not in self.ioQ):
                        if p.io_time:
                            # io time
                            p.start = False
                            p.cpu_time -= 1
                            self.updateIo()
                            self.readyQueue.remove(p)

                        elif p.io_time == 0:
                            p.start = False
                            p.end_time = self._time
                            p.set_turnaround_time()
                            p.set_response_time()
                            self.response_times += p.response_time
                            self.turnaround_times += p.turnaround_time
                            self.waitting_times += p.waitting_time
                            self.readyQueue.remove(p)

            else:
                self.wait += 1
                self._time += 1

        #  self._time = time.time() - start_time
        self.set_throughput()
        self.process_results()
        self.set_CPU_Utilization()
        self.cpu_results()
        self.show("FCFS")
        self.clear()


x = CpuAlgos()

x.FCFS()
x.SJF()
x.RR(5)
x.MLFQ()
