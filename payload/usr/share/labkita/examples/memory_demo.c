/*
 * memory_demo.c - Contoh Pemrograman Sistem Operasi: Alokasi Memori Dinamis (Heap)
 *
 * Deskripsi:
 *   Program ini mendemonstrasikan cara mengalokasikan memori secara dinamis di heap
 *   menggunakan malloc(), menggunakannya, lalu membebaskannya dengan free().
 *   Setiap langkah disertai pengecekan error dan praktik aman (set pointer ke NULL
 *   setelah free untuk menghindari dangling pointer).
 *
 * Kompilasi (di LabKita Linux atau Linux lain dengan GCC):
 *   gcc -Wall -Wextra memory_demo.c -o memory_demo
 * Eksekusi:
 *   ./memory_demo
 *
 * Catatan: belum dikompilasi/diuji di mesin Windows (gcc tidak tersedia, WSL tidak terpasang).
 *          Kompilasi dan pengujian dilakukan di lingkungan LabKita Linux.
 */

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int jumlah_elemen = 5;
    int *larik_dinamis = NULL;  /* Inisialisasi ke NULL agar pointer jelas statusnya */

    printf("==================================================\n");
    printf(" Demonstrasi Alokasi Memori Dinamis C - LabKita\n");
    printf("==================================================\n");

    /* 1. Mengalokasikan blok memori di segmen Heap menggunakan malloc() */
    printf("[1] Mengalokasikan memori untuk %d integer di Heap...\n", jumlah_elemen);
    larik_dinamis = (int *)malloc(jumlah_elemen * sizeof(int));

    /* 2. Memeriksa keberhasilan alokasi — OS bisa menolak jika memori habis */
    if (larik_dinamis == NULL) {
        fprintf(stderr, "Error: Alokasi memori gagal! OS tidak menyediakan memori.\n");
        return 1;
    }

    printf("[2] Alokasi sukses. Alamat memori virtual: %p\n", (void *)larik_dinamis);

    /* 3. Mengisi dan membaca data pada blok memori yang telah dialokasikan */
    printf("[3] Mengisi data ke memori heap:\n");
    for (int i = 0; i < jumlah_elemen; i++) {
        larik_dinamis[i] = (i + 1) * 10;
        printf("    - Elemen [%d] di alamat %p = %d\n",
               i, (void *)&larik_dinamis[i], larik_dinamis[i]);
    }

    /* 4. Membebaskan memori ke OS — wajib dilakukan untuk mencegah memory leak */
    printf("[4] Membebaskan memori kembali ke OS (free)...\n");
    free(larik_dinamis);

    /* 5. Set pointer ke NULL setelah free — mencegah dangling pointer */
    larik_dinamis = NULL;
    printf("[5] Pointer di-set ke NULL setelah free — aman dari dangling pointer.\n");

    printf("==================================================\n");
    printf(" Memori berhasil dibebaskan dengan aman. Selesai.\n");
    printf("==================================================\n");

    return 0;
}
