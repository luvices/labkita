#!/usr/bin/env python3
"""
thread_demo.py - Contoh Pemrograman Sistem Operasi: Konsep Threading (Multithreading)
Distro: LabKita Linux 0.3

Deskripsi:
Program ini mendemonstrasikan pembuatan thread pekerja secara bersamaan (konkuren)
dalam satu proses menggunakan modul bawaan 'threading' pada pustaka standar Python.
Thread berbagi ruang memori yang sama dalam satu proses (Process ID identik).
"""

import os
import threading
import time


def pekerja(nomor_tugas, iterasi):
    """Fungsi yang dijalankan oleh setiap thread pekerja."""
    nama_thread = threading.current_thread().name
    print(f"[{nama_thread}] Mulai tugas {nomor_tugas} (PID proses: {os.getpid()})")

    total = 0
    for i in range(1, iterasi + 1):
        total += i
        time.sleep(0.01)  # Simulasi jeda komputasi ringan

    print(f"[{nama_thread}] Selesai tugas {nomor_tugas}. Hasil penjumlahan 1..{iterasi} = {total}")


def main():
    print("==================================================")
    print(" LabKita Linux 0.3 - Demonstrasi Threading Python ")
    print(f" PID Proses Utama: {os.getpid()}")
    print("==================================================")

    # Menyiapkan 2 thread pekerja
    t1 = threading.Thread(target=pekerja, args=(1, 5), name="Thread-A")
    t2 = threading.Thread(target=pekerja, args=(2, 5), name="Thread-B")

    # Memulai eksekusi thread secara independen/konkuren
    t1.start()
    t2.start()

    print("[Utama] Menunggu seluruh thread pekerja selesai...")

    # Sinkronisasi: menunggu thread selesai sebelum proses utama keluar
    t1.join()
    t2.join()

    print("==================================================")
    print("[Utama] Semua thread telah selesai. Proses berakhir.")
    print("==================================================")


if __name__ == "__main__":
    main()
