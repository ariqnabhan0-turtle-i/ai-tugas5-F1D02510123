import json
import os

FILE_KB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kb_hp.json")


def muat_kb(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def kumpulkan_fakta_dasar(aturan):
    semua_maka = {r["maka"] for r in aturan}
    fakta, terlihat = [], set()
    for r in aturan:
        for k in r["jika"]:
            if k not in semua_maka and k not in terlihat:
                fakta.append(k)
                terlihat.add(k)
    return fakta


def tanya_user(fakta_dasar):
    memori = set()
    print("Jawab pertanyaan berikut dengan y (ya) atau t (tidak).\n")
    for f in fakta_dasar:
        while True:
            jawab = input(f"Apakah {f}? (y/t): ").strip().lower()
            if jawab in ("y", "t"):
                break
            print("  Masukkan hanya 'y' atau 't'.")
        if jawab == "y":
            memori.add(f)
    print()
    return memori


def syarat_terpenuhi(aturan, memori):
    ada = [k for k in aturan["jika"] if k in memori]
    if aturan["mode"] == "dan":
        return ada if len(ada) == len(aturan["jika"]) else None
    if aturan["mode"] == "atau":
        return ada if ada else None
    return None


def forward_chaining(aturan, memori):
    jejak = {} 
    siklus = 0
    while True:
        siklus += 1
        cocok = []
        for r in aturan:
            if r["maka"] in memori:
                continue
            dipakai = syarat_terpenuhi(r, memori)
            if dipakai is not None:
                cocok.append((r, dipakai))

        if not cocok:
            print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break

        r, dipakai = cocok[0] 
        memori.add(r["maka"])
        jejak[r["maka"]] = (r["id"], dipakai)
        print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    return memori, jejak


def cetak_alasan(fakta, jejak, level):
    id_aturan, dipakai = jejak[fakta]
    print(" " * (4 * level) + f"{fakta} <- {id_aturan} ({', '.join(dipakai)})")
    for k in dipakai:
        if k in jejak:  
            cetak_alasan(k, jejak, level + 1)


def main():
    kb = muat_kb(FILE_KB)
    aturan = kb["aturan"]
    solusi = {r["maka"]: r.get("solusi", "") for r in aturan}

    print("=" * 60)
    print(kb["judul"])
    print("=" * 60)

    fakta_dasar = kumpulkan_fakta_dasar(aturan)
    memori = tanya_user(fakta_dasar)

    memori, jejak = forward_chaining(aturan, memori)

    diagnosis = [m for m in jejak if m.startswith("diagnosis:")]
    print()
    if not diagnosis:
        print("Kesimpulan: tidak ada diagnosis yang dapat disimpulkan dari jawaban Anda")
    else:
        if len(diagnosis) == 1:
            print(f"Kesimpulan: {diagnosis[0]}")
        else:
            print(f"Kesimpulan ({len(diagnosis)} diagnosis):")
            for d in diagnosis:
                print(f"  - {d}")
        print("Alasan:")
        for d in diagnosis:
            cetak_alasan(d, jejak, 1)
        print("\nSolusi:")
        for d in diagnosis:
            print(f"  - {d.replace('diagnosis: ', '')}: {solusi[d]}")

    print(f"\nCatatan: {kb['batas']}.")


if __name__ == "__main__":
    main()