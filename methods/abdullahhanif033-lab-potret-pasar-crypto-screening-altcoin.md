---
name: screening-altcoin
description: Memindai 750 altcoin teratas dengan urutan narasi → attention → demand → harga — narasi yang menghangat di Reddit/berita, perhatian yang datang sebelum harga, pola multi-waktu, anomali terhadap Bitcoin, lonjakan volume terhadap kebiasaannya sendiri, rotasi sektor, struktur suplai, dan TVL — lalu menyerahkan daftar pendek berisi 3-6 nama beserta narasi, pemicu, jejak dompet, kerangka risiko, dan syarat batal. Gunakan saat user minta dicarikan peluang crypto, bertanya "ada altcoin menarik nggak", "koin apa yang mau naik", "cari yang mau pump", "screening altcoin", "ada yang lagi diakumulasi nggak", menyodorkan hasil CryptoBubbles, atau minta daftar kandidat sebelum analisis mendalam.
---

# Screening Altcoin

Skill ini menjawab pertanyaan **"yang mana yang layak dibedah?"** — bukan
"aset ini bagus atau tidak" (itu tugas `analis-aset`), dan bukan "beli apa"
(itu bukan tugas siapa pun di sini).

Keluarannya: **daftar pendek 3-6 nama**, tiap nama membawa sinyalnya, angkanya,
pekerjaan riset yang belum bisa dikerjakan mesin, dan **syarat yang membatalkan
tesisnya**. Setelah itu skill ini berhenti dan menyerahkan nama terpilih ke
`analis-aset`.

---

## Aturan pembuka yang tidak bisa ditawar

**Tidak ada yang bisa meramal koin mana yang akan pump.** Siapa pun yang mengaku
bisa sedang menjual sesuatu. Yang bisa dinilai adalah **asimetri**: seberapa
besar ruang naik dibanding ruang turun, dan seberapa banyak hal yang harus
berjalan benar agar tesisnya jadi.

Konsekuensinya untuk cara menulis:

1. Jangan pernah menulis "koin ini akan naik". Tulis **"kalau X terjadi maka Y,
   dan probabilitas X bisa dinilai dari Z"**.
2. **Momentum adalah alasan untuk menoleh, bukan alasan untuk membeli.** Ia
   menandai ada sesuatu yang sedang terjadi, bukan bahwa yang terjadi itu baik.
3. **Skor tinggi bukan rekomendasi.** Skor adalah urutan antrean riset.
4. Setiap kandidat wajib punya **syarat batal**. Kandidat tanpa syarat batal
   berarti pemindaiannya belum selesai, bukan berarti tesisnya kuat.
5. **Jangan pernah mengarang angka.** Yang tidak ditemukan ditulis
   `tidak tersedia`. Data pendanaan, jadwal unlock, dan porsi insider memang
   tidak tersedia gratis lewat API — itu kenyataan yang dilaporkan, bukan celah
   yang ditambal tebakan.
6. **Bukan penasihat investasi.** Hanif Investment Service menjual riset dan
   analisis. Tutup tiap keluaran dengan penegasan itu.

---

## Kerangka yang mengatur urutan kerja

> Sebuah koin dibeli karena ada demand. Demand tercipta karena ada attention.
> Attention tercipta karena ada narasi.

Koin datang paling belakang. Karena itu pencarian **tidak pernah dimulai dari
koin yang naik**, melainkan dari narasi yang menghangat, lalu perhatian yang
datang sebelum harga, lalu siapa yang memegang, lalu berapa ukurannya. Empat
pilar ini — narasi, attention, wallet tracking, risk management — dipetakan ke
lapis-lapis mesin dan pekerjaan manual di `references/kerangka-narasi.md`.

## Urutan kerja

```
1. NARASI       → tabel "Narasi hari ini" di laporan: mana yang menghangat
                  (≥2× kebiasaannya), mana yang mendingin. Cari di yang menghangat.
2. ATTENTION    → kandidat yang ramai SEBELUM harga bergerak, di narasi itu;
                  daftar pendek mesin di laporan/crypto/_screening/terbaru.md
                  (terbit sendiri tiap pagi; jalankan skor-altcoin.py hanya
                  untuk menyempitkan)
3. STRUKTUR     → FDV/MC, unlock, insider — mesin + riset manual b-c
4. DOMPET       → riset manual e: pemegang terbesar, aliran ke bursa, likuiditas nyata
5. DUA ALASAN   → mikro (riset manual a, mulai dari "Yang dibicarakan hari ini") dan makro
6. RISIKO       → ukuran, cara masuk bertahap, syarat batal, jurnal (references/manajemen-risiko.md)
7. SERAHKAN     → 2-3 nama ke skill analis-aset
```

Langkah 1-2 sebagian besar mesin. **Langkah 3-6 adalah pekerjaan yang membuat
skill ini bernilai** — tanpa itu, keluarannya cuma tabel momentum yang bisa
dibuat siapa saja dari CryptoBubbles.

### Langkah 1-2 secara praktis

**Biasanya tidak perlu perintah apa pun.** Dua pekerja bergiliran tiap pagi:
GitHub Actions (05:07 WIB) mengambil potret dan menyusun laporan mesin, lalu
routine Claude di cloud (06:05 WIB, prompt di `routine.md` repo
`potret-pasar-crypto`) membaca skill ini, meriset web, dan menulis **daftar
pendek final** yang tersemat di paling atas halaman:

- Halaman HP: <https://hanif-dossier.github.io/potret-pasar-crypto/>
  (tampilannya sama dengan briefing harian, ada di tab "Screening Altcoin")
- Salinan lokal setelah laptop menyala: `laporan/crypto/_screening/terbaru.md`

Baca dulu yang sudah terbit. Jalankan ulang penilaian hanya kalau ingin
menyempitkan (kapitalisasi tertentu, `--utamakan-ramai`) atau laporannya
belum ada — misalnya cloud gagal pagi ini:

```bash
git -C "D:/Ai Agent/riset/pasar-crypto" pull --ff-only && cd "D:/Ai Agent/skill/screening-altcoin/scripts" && python skor-altcoin.py
```

`skor-altcoin.py` akan menyebut tanggal potret yang dipakainya. Kalau tanggalnya
bukan hari ini — berarti cloud belum jalan atau gagal — barulah ambil sendiri:

```bash
cd "D:/Ai Agent/skill/screening-altcoin/scripts" && python ambil-data.py && python skor-altcoin.py
```

`ambil-data.py` butuh 2-4 menit (ada jeda sengaja supaya tidak diblokir
CoinGecko) dan hasilnya masuk ke `snapshot-lokal/`, bukan ke folder cloud.
Jangan mengambil ulang data yang sudah ada.

Pilihan yang sering berguna:

| Perintah | Gunanya |
|---|---|
| `python skor-altcoin.py --jumlah 10` | daftar pendek lebih panjang |
| `python skor-altcoin.py --min-cap 100000000` | buang koin di bawah $100 juta |
| `python skor-altcoin.py --maks-cap 500000000` | khusus berburu kapitalisasi kecil |
| `python skor-altcoin.py --tanggal 2026-09-01` | menilai ulang potret hari lalu |
| `python skor-altcoin.py --utamakan-ramai` | daftar pendek hanya dari koin yang hari ini dibicarakan di Reddit/berita atau trending |

Pakai `--utamakan-ramai` saat user secara eksplisit minta "yang ramai" atau
"yang lagi dibicarakan". Tanpa itu, keramaian tetap ikut dihitung sebagai poin —
tapi koin yang diam-diam diakumulasi tanpa satu pun berita **justru kandidat
yang paling berharga**, dan penyaring ini akan membuangnya. Jadi jangan
dijadikan bawaan.

---

## Langkah 4 — empat lapis yang wajib dikerjakan manual

Mesin berhenti di angka. Empat lapis ini butuh pencarian web, dan **semuanya
wajib untuk tiap nama yang masuk daftar pendek final.** Rinciannya di
`references/riset-manual.md`.

**a. Pemicu mikro.** Apa yang terjadi pada asetnya sendiri dalam 7-14 hari
terakhir: rilis produk, mainnet, kemitraan, listing bursa besar, perubahan
tokenomics, lonjakan pengguna, unlock yang baru lewat. **Mulai dari blok "Yang
dibicarakan hari ini" di laporan** — judul Reddit dan berita yang menyebut koin
itu sering langsung menunjuk pemicunya, atau menunjukkan bahwa keramaiannya cuma
promosi. **Kandidat tanpa pemicu
mikro yang bisa ditunjuk adalah kandidat lemah** — kenaikannya berarti belum
ada penjelasannya, dan yang tidak punya penjelasan tidak punya daya tahan.

**b. Jadwal unlock 90 hari ke depan.** Batas peringatan: >5% suplai beredar.
Sumber gratis: CryptoRank, TokenUnlocks, halaman tokenomics proyeknya.

**c. Pendana dan valuasi ronde terakhir.** Kalau FDV sekarang jauh di atas
valuasi ronde terakhir, ritel sedang membeli dari orang yang sudah untung besar.

**d. Pendiri dan tim.** Anonim tidak otomatis merah, tapi menaikkan beban
pembuktian pada audit dan repositori kode. Pernah meninggalkan proyek sebelum
tuntas adalah pola yang wajib disebut.

Untuk tiap nama, sebutkan juga **satu alasan makro** — arah likuiditas, dominasi
BTC, fase siklus, regulasi. Aturan pemadu: **makro menentukan apakah ini
waktunya, mikro menentukan apakah ini asetnya.**

---

## Cara membaca skor

Skor adalah jumlah poin sinyal, kira-kira −40 sampai +90. Yang penting **bukan
angkanya, melainkan sinyal apa yang menyusunnya.**

| Sinyal penyusun | Bacaan |
|---|---|
| **Akumulasi diam-diam** (+18) | Paling jarang, paling layak diteliti. Harga hampir tak bergerak sementara volume berlipat = ada yang mengumpulkan tanpa mengejar harga |
| **Anomali kuat vs BTC** (+15) | Bergerak menjauhi indeksnya. Di sinilah satu-satunya sumber untung di luar BTC |
| **Kemungkinan pembalikan** (+14) | Jatuh dalam sebulan lalu berbalik sepekan. **Wajib ada pemicunya** — kalau tidak ketemu, ini cuma pantulan teknis |
| **Volume meledak** (+12) | Perhatian datang tiba-tiba. Cari sebabnya sebelum ikut |
| **Tarikan napas** (+12) | Koreksi sehat di dalam tren naik — asalkan volume ikut mengering |
| **Fundamental mendahului harga** (+10) | TVL naik lebih cepat daripada harga. Sinyal paling "fundamental" yang bisa diambil gratis |
| **Ramai sebelum harga bergerak** (+10) | Dibicarakan ≥3× kebiasaannya di Reddit/berita sementara harga masih diam. Perhatian mendahului harga |
| **Ramai setelah naik** (−5) | Keramaian datang setelah harga naik >12% — yang ramai sekarang membeli dari yang masuk lebih dulu |
| **Sudah terlalu jauh** (−10) | Naik >150% sebulan. Bukan peluang lagi |
| **Lonjakan sesaat** (−12) | Melompat sejam, rentang lain datar. Pola yang paling sering menjebak |
| **Dilusi berat** (−15) | FDV >5× kapitalisasi. Pembeli hari ini menanggung dilusi besok |

Daftar lengkap beserta asal tiap ambang: `references/kriteria-skor.md`.

**Dua bacaan yang paling sering salah:**

- Skor tinggi yang seluruhnya berasal dari momentum (anomali BTC + tren) hanya
  berarti koin itu sudah naik. Itu informasi yang sudah dimiliki semua orang.
- Skor sedang yang berisi **akumulasi diam-diam + fundamental mendahului harga**
  jauh lebih berharga daripada skor tinggi berisi momentum saja.

---

## Format daftar pendek final

Untuk tiap nama, tulis persis blok ini:

```
**SIMBOL (Nama)** — peringkat #N · kapitalisasi $X · skor Y

Narasi:   [narasi/sektor yang menaunginya, dan apakah narasi itu menghangat atau mendingin hari ini]
Sinyal:   [pola dari mesin, dengan angkanya — sebutkan apakah perhatian datang sebelum atau sesudah harga]
Mikro:    [pemicu 7-14 hari terakhir; kalau tidak ketemu, tulis begitu — itu temuan, bukan kekosongan]
Makro:    [kondisi yang mendukung atau melawan]
Struktur: [FDV/kapitalisasi, unlock terdekat, porsi insider — atau `tidak tersedia`]
Dompet:   [konsentrasi pemegang terbesar, aliran ke bursa, likuiditas DEX — atau `belum diperiksa`]
Risiko:   [tier kapitalisasi → ukuran relatif (jangkar / sedang / spekulatif kecil), cara masuk bertahap]
Batal kalau: [syarat yang menggugurkan tesis ini]
```

Baris **Risiko** tidak pernah berisi persentase untuk orang tertentu — hanya
tier dan cara masuk. Ukuran adalah keputusan pemilik uangnya.

Tutup daftar dengan kalimat yang menegaskan statusnya: ini hasil pemindaian,
belum analisis, dan belum layak jadi dasar keputusan sebelum dibedah mendalam.
Lalu disclaimer Hanif Investment Service.

---

## Dari mana riwayatnya datang

Dua sinyal terkuat — akumulasi diam-diam dan lonjakan volume — mengukur hari ini
terhadap **kebiasaan koin itu sendiri**, dan itu hanya bisa dihitung kalau
riwayatnya ada. Riwayat 0 hari mematikan dua sinyal itu; 7 hari menghidupkan
keduanya; 14 hari membuatnya stabil.

Riwayat itu **diambil GitHub Actions tiap 05:07 WIB**, bukan oleh laptop, supaya
tidak bolong saat laptop mati. Hasilnya ditarik ke laptop lewat `git pull` tiap
kali menyala.

| Folder | Diisi oleh |
|---|---|
| `riset/pasar-crypto/snapshot/` | GitHub Actions — repo `potret-pasar-crypto` |
| `riset/pasar-crypto/snapshot-lokal/` | Laptop, hanya kalau cloud melewatkan satu hari |

Artinya **`ambil-data.py` tidak perlu dijalankan tiap hari secara manual.**
Jalankan hanya kalau potret hari ini benar-benar belum ada — misalnya cloud
gagal dan Anda sedang butuh screening sekarang juga.

Berkas potret lama tidak boleh dihapus: itu satu-satunya riwayat volume yang
dimiliki sistem ini, dan hari yang terlewat tidak bisa diambil ulang dengan cara
apa pun. Rinciannya di `references/sumber-data.md`.

---

## Hubungan dengan skill dan laporan lain

| Sumber | Perannya |
|---|---|
| `laporan/harian/terbaru.md` | Briefing pagi otomatis sudah menjalankan versi dangkal Lapis 1-2. Baca dulu; jangan mengulang pemindaian yang hasilnya sudah ada di sana |
| `skill/analis-aset/references/berburu-kandidat.md` | Kerangka lima lapis yang jadi asal-usul skill ini |
| `skill/analis-aset/` | Penerima daftar pendek — dossier penuh dikerjakan di sana |
| `laporan/crypto/<SIMBOL>/` | Dossier yang sudah pernah dibuat. Skrip menandai otomatis kalau kandidat hari ini pernah dibedah — bandingkan tesis lama dengan sinyal hari ini |

---

## Berkas dalam skill ini

```
scripts/sumber.py         alamat folder, pengambil data yang sopan, perapi angka
scripts/ambil-data.py     mengambil potret pasar dan menyimpannya jadi riwayat
scripts/keramaian.py      menghitung sebutan tiap koin di Reddit dan berita
scripts/kata-umum.txt     10.000 kata Inggris umum, penyaring nama koin yang ambigu
scripts/skor-altcoin.py   menilai, memeringkat, menulis laporan markdown
references/kerangka-narasi.md narasi → attention → dompet → risiko; peta pilar ke lapis mesin
references/kriteria-skor.md   tiap sinyal: ambangnya berapa, asalnya dari mana, kapan salah
references/riset-manual.md    lima lapis manual (pemicu, unlock, pendana, pendiri, dompet)
references/manajemen-risiko.md sizing tiga sumbu, cut loss sebagai tesis, take profit bertahap, jurnal
references/sumber-data.md     API yang dipakai, yang diblokir, dan batas kecepatannya
references/belajar-koding.md  pembacaan kode baris demi baris untuk pemilik sistem ini
```
