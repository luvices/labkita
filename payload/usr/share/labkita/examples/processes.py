#!/usr/bin/env python3
"""Dua proses anak dengan beban terbatas, tanpa akses jaringan."""
import multiprocessing
import os


def worker(number):
    print(f"Pekerja {number}: PID={os.getpid()}, induk={os.getppid()}", flush=True)
    print(f"Pekerja {number}: jumlah={sum(range(100_000))}", flush=True)


if __name__ == "__main__":
    print(f"Proses induk: PID={os.getpid()}", flush=True)
    # Fork dipilih eksplisit agar PPID pekerja menunjuk langsung ke proses induk.
    context = multiprocessing.get_context("fork")
    workers = [context.Process(target=worker, args=(number,)) for number in (1, 2)]
    for process in workers:
        process.start()
    for process in workers:
        process.join()
        if process.exitcode != 0:
            raise SystemExit(process.exitcode)
    print("Semua proses anak selesai.")
