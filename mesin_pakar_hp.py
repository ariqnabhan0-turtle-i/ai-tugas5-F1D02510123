import json
import os


def baca_kb(nama_file="kb_kopi.json"):
    lokasi = os.path.join(os.path.dirname(os.path.abspath(__file__)), nama_file)
    with open(lokasi, "r", encoding="utf-8") as f:
        return json.load(f)


def kumpulkan_fakta_dasar(aturan):
    semua_maka = {r["maka"] for r in aturan}
    dasar = []
    for r in aturan:
        for kondisi in r["jika"]:
            if kondisi not in semua_maka and kondisi not in dasar:
                dasar.append(kondisi)
    return dasar


def tanya_fakta(fakta_dasar):
    memori = []
    print("Jawab y/t.")
    for i, fakta in enumerate(fakta_dasar, start=1):
        while True:
            jawab = input(f"{i}. Apakah {fakta}? (y/t) > ").strip().lower()
            if jawab in ("y", "t"):
                break
            print("   Masukan tidak valid, ketik 'y' atau 't'.")
        if jawab == "y":
            memori.append(fakta)
    return memori


def syarat_terpenuhi(aturan, memori):
    ada = [k in memori for k in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)


def forward_chaining(daftar_aturan, memori):
    jejak = []
    alasan = {}
    siklus = 0

    while True:
        siklus += 1
        cocok = [r for r in daftar_aturan
                 if syarat_terpenuhi(r, memori) and r["maka"] not in memori]

        if not cocok:
            jejak.append((siklus, None, None))
            break

        r = cocok[0]
        memori.append(r["maka"])
        terpenuhi = [k for k in r["jika"] if k in memori]
        alasan[r["maka"]] = (r, terpenuhi)
        jejak.append((siklus, r["id"], r["maka"]))

    return jejak, alasan


def cetak_alasan(fakta, alasan, tingkat=0):
    r, terpenuhi = alasan[fakta]
    spasi = " " * (4 * (tingkat + 1))
    print(f"{spasi}{fakta} <- {r['id']} ({', '.join(terpenuhi)})")
    for k in terpenuhi:
        if k in alasan:
            cetak_alasan(k, alasan, tingkat + 1)


def main():
    kb = baca_kb()
    aturan = kb["aturan"]

    print(kb["judul"])

    fakta_dasar = kumpulkan_fakta_dasar(aturan)
    memori = tanya_fakta(fakta_dasar)

    print()
    print("Fakta awal: " + (", ".join(memori) if memori else "(tidak ada)"))
    print()

    jejak, alasan = forward_chaining(aturan, memori)
    for nomor, id_aturan, hasil in jejak:
        if id_aturan is None:
            print(f"Siklus {nomor}: tidak ada aturan baru, berhenti")
        else:
            print(f"Siklus {nomor}: {id_aturan} -> {hasil}")
    print()

    semua_syarat = {k for r in aturan for k in r["jika"]}
    kesimpulan = [f for f in memori if f in alasan and f not in semua_syarat]

    if kesimpulan:
        print("Kesimpulan: " + ", ".join(kesimpulan))
        print("Alasan:")
        for k in kesimpulan:
            cetak_alasan(k, alasan)
    elif alasan:
        print("Kesimpulan: " + ", ".join(alasan.keys()))
        print("Alasan:")
        for k in alasan:
            cetak_alasan(k, alasan)
    else:
        print("Kesimpulan: tidak ada kesimpulan yang dapat ditarik dari fakta tersebut")

    print()
    print("Catatan: " + kb["batas"])


if __name__ == "__main__":
    main()