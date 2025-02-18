import multiprocessing as mp
import queue
import time
import datetime

def main(
    args_list: list,
    devices: list[int],
):
    q = mp.Queue()
    for args in args_list:
        q.put(args)

    print("%s [main]: Creating processes..." % datetime.datetime.now())
    p_list = [
        mp.Process(target=run_jobs_gpu, args=(d, q))
        for d in devices
    ]

    print("%s [main]: Starting jobs..." % datetime.datetime.now())
    for p in p_list:
        p.start()

    for p in p_list:
        p.join()

    print("%s [main]: End of main function" % datetime.datetime.now())

def run_jobs_gpu(
    device: int,
    q: mp.Queue,
):
    while True:
        try:
            args = q.get(block=False)
            train(args, device)
        except queue.Empty:
            return

def train(
    args: int,
    device: int,
):
    timestamp = datetime.datetime.now()
    print("%s [train]: Device = %s, args = %s" % (timestamp, device, args))
    time.sleep(args)

if __name__ == "__main__":
    main(
        args_list=[3, 2, 2, 3, 2],
        devices=[3, 7],
    )
