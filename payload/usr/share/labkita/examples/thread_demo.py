#!/usr/bin/env python3
"""
thread_demo.py - Contoh Pemrograman Sistem Operasi: Konsep Threading (Multithreading)

Deskripsi:
  Program ini mendemonstrasikan pembuatan thread pekerja secara bersamaan (konkuren)
  dalam satu proses menggunakan modul bawaan 'threading' di Python.
  Thread berbagi ruang memori yang sama dalam satu proses (Process ID identik).

Cara jalankan:
  python3 thread_demo.py
"""

import os
import threading
import time


def pekerja(nomor_tugas, iterasi):
    """Fungsi yang dijalankan oleh setiap thread pekerja."""
    nama_thread = threading.current_thread().name
    print(f"[{nama_thread}] Mulai tugas {nomor_tugas} (PID proses: {os.getpid()})", flush=True)

    # Hitung jumlah 1 sampai N — simulasi beban kerja ringan
    total = sum(range(1, iterasi + 1))
    time.sleep(0.05)  # Simulasi jeda I/O singkat

    print(f"[{nama_thread}] Selesai tugas {nomor_tugas}. Hasil penjumlahan 1..{iterasi} = {total}", flush=True)


def main():
    print("=" * 50, flush=True)
    print(" Demonstrasi Threading Python - LabKita Linux", flush=True)
    print(f" PID Proses Utama: {os.getpid()}", flush=True)
    print("=" * 50, flush=True)

    # Menyiapkan 2 thread pekerja
    t1 = threading.Thread(target=pekerja, args=(1, 50_000), name="Thread-A")
    t2 = threading.Thread(target=pekerja, args=(2, 50_000), name="Thread-B")

    # Memulai eksekusi thread secara konkuren
    t1.start()
    t2.start()

    print("[Utama] Menunggu seluruh thread pekerja selesai...", flush=True)

    # Sinkronisasi: tunggu semua thread selesai sebelum keluar
    t1.join()
    t2.join()

    print("=" * 50, flush=True)
    print("[Utama] Semua thread telah selesai. Proses berakhir.", flush=True)
    print("=" * 50, flush=True)


if __name__ == "__main__":
    main()
