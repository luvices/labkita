/*
 * memory_demo.c - Contoh Pemrograman Sistem Operasi: Alokasi Memori Dinamis (Heap)
 * Distro: LabKita Linux 0.3
 *
 * Kompilasi di LabKita Linux (GCC):
 *   gcc -Wall -Wextra memory_demo.c -o memory_demo
 * Eksekusi:
 *   ./memory_demo
 */

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int jumlah_elemen = 5;
    int *larik_dinamis = NULL;

    printf("==================================================\n");
    printf(" LabKita Linux 0.3 - Demonstrasi Alokasi Memori C \n");
    printf("==================================================\n");

    /* 1. Mengalokasikan blok memori pada segmen Heap menggunakan malloc() */
    printf("[1] Mengalokasikan memori untuk %d integer di Heap...\n", jumlah_elemen);
    larik_dinamis = (int *)malloc(jumlah_elemen * sizeof(int));

    /* 2. Memeriksa keberhasilan alokasi sistem */
    if (larik_dinamis == NULL) {
        fprintf(stderr, "Error: Alokasi memori gagal oleh sistem operasi!\n");
        return 1;
    }

    printf("[2] Alokasi sukses. Alamat memori virtual: %p\n", (void *)larik_dinamis);

    /* 3. Mengisi dan membaca data pada blok memori yang dialokasikan */
    printf("[3] Mengisi data ke memori heap:\n");
    for (int i = 0; i < jumlah_elemen; i++) {
        larik_dinamis[i] = (i + 1) * 10;
        printf("    - Elemen [%d] pada alamat %p = %d\n",
               i, (void *)&larik_dinamis[i], larik_dinamis[i]);
    }

    /* 4. Membebaskan kembali memori ke sistem operasi untuk mencegah memory leak */
    printf("[4] Membebaskan memori kembali ke OS (free)...\n");
    free(larik_dinamis);
    larik_dinamis = NULL; /* Mencegah dangling pointer */

    printf("==================================================\n");
    printf(" Memori berhasil dibebaskan dengan aman. Selesai. \n");
    printf("==================================================\n");

    return 0;
}
