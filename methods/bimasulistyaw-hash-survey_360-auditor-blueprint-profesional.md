---
name: auditor-blueprint-profesional
description: Melakukan audit menyeluruh terhadap dokumen Blueprint.md untuk memastikan kepatuhan terhadap standar pengembangan perangkat lunak (SSOT), kesinambungan logis terpadu (BRD vs PRD vs SRS vs ERD vs MOD), kepatuhan format PRD (Persona, JTBD, MoSCoW, Gherkin), kesesuaian seluruh modul terhadap kebutuhan bisnis BRD, dan kelengkapan arsitektur.
---

# Auditor Blueprint Profesional

## Tujuan
Menganalisis dan mengaudit dokumen `Blueprint.md` secara mendalam untuk memverifikasi kepatuhan terhadap aturan Single Source of Truth (SSOT) Antigravity 2.0 (standar Pemkot Yogyakarta). Audit mencakup kesinambungan logis terpadu (BRD vs PRD vs SRS vs ERD vs MOD-xx), kepatuhan format spesifikasi produk (PRD), kesesuaian seluruh modul terhadap kebutuhan proyek pada BRD, kelengkapan traceability matrix, spesifikasi teknis (Go Clean Architecture, PostgreSQL, Keycloak JSS, MinIO), kepatuhan UI/UX Apple HIG, keamanan (OWASP), dan standar pengujian (QA).

## Prosedur Audit
1. **Analisis Dokumen**: Baca dan telusuri seluruh isi file `Blueprint.md` dari hulu ke hilir (Bagian A s.d F).
2. **Audit Kesesuaian Modul vs BRD (Forward & Backward Traceability)**:
   - **Forward Traceability**: Periksa setiap Kebutuhan Bisnis (`BR-xx`) dan Alur Proses Bisnis (`[Aktor]` vs `[Sistem]`) di BRD apakah telah diwadahi secara penuh oleh fitur di PRD, dirinci dalam SRS-F, dan memiliki modul implementasi konkret (`MOD-xx`).
   - **Backward Traceability**: Periksa setiap modul implementasi (`MOD-xx`) dan skema database apakah memiliki dasar kebutuhan bisnis yang sah pada BRD (mencegah *scope creep* / fitur liar).
3. **Audit Kepatuhan Format PRD**: Periksa kelengkapan persona (`P-xx`), JTBD, diagram User Journey Map (`flowchart LR`), Feature Decomposition Tree (`flowchart TD`), prioritas MoSCoW, serta 6 komponen wajib pendalaman modul bisnis (anti-halusinasi AI) termasuk form input dan acceptance criteria Gherkin.
4. **Evaluasi Checklist Terperinci**: Lakukan validasi poin demi poin terhadap checklist audit di bawah.
5. **Penyusunan Laporan Audit**: Buat laporan audit terstruktur yang berisi:
   - **Status Kelulusan**: Lulus (PASSED) / Perlu Perbaikan (REVISION REQUIRED)
   - **Tabel Matriks Evaluasi Kesinambungan Modul vs BRD**: Daftar seluruh modul dan status kesesuaiannya terhadap kebutuhan bisnis BRD.
   - **Temuan (Findings)**: Poin-poin spesifik yang hilang, tidak sinkron, atau menyimpang dari standar format BRD, PRD, SRS, ERD, maupun MOD.
   - **Rekomendasi Tindak Lanjut (Action Items)**: Instruksi perbaikan konkret pada `Blueprint.md`.

---

## Checklist Audit Terperinci

Saat mengevaluasi `Blueprint.md`, berikan tanda `[v]` atau `[x]` pada laporan audit untuk setiap poin di bawah ini:

### 1. Struktur, Traceability SSOT, dan Kepatuhan Format
- [ ] **Ketersediaan Dokumen Utama**: Apakah dokumen memuat seluruh konteks dari hulu ke hilir sebagai acuan tunggal (Bagian A s.d F)?
- [ ] **Hierarki Kebutuhan & Traceability Menyeluruh**: Apakah pemetaan dari Kebutuhan Bisnis (BR) → Fitur Produk (PRD) → Kebutuhan Fungsional (SRS) → Struktur Basis Data (ERD) → Modul Implementasi (MOD) → Spesifikasi Layar (UI) terstruktur tanpa putus (*0 Broken Links*)?
- [ ] **Penomoran Traceability Standar**: Apakah penomoran *traceability* konsisten dan tercantum eksplisit di setiap tabel/bagian?
  - `BR-xx` (Business Requirements)
  - `PRD-xx` (Product Requirements)
  - `SRS-F-xx` (Functional Requirements)
  - `SRS-NF-xx` (Non-Functional Requirements)
  - Pemetaan Entitas Data (ERD)
  - `MOD-xx` (Modular Implementation Units)
  - `UI-xx` (Apple HIG Screen Specifications)
- [ ] **Kesinambungan Logis Terpadu (BRD vs PRD vs SRS vs ERD vs MOD-xx)**: 
  - **Cakupan Kebutuhan BRD ke PRD**: Apakah seluruh fitur produk di **PRD** merangkum, menjawab, dan memetakan 100% kebutuhan bisnis di **BRD**?
  - **Kesesuaian Seluruh Modul (`MOD-xx`) terhadap BRD**: Apakah **SETIAP** modul implementasi (`MOD-00` s.d `MOD-xx`) dan sub-modulnya benar-benar selaras, presisi, dan menjawab kebutuhan operasional serta fungsional proyek yang dituntut di BRD?
  - **Zero Orphan BRD (Tanpa Kebutuhan Yatim Piatu)**: Apakah dipastikan tidak ada satupun kebutuhan bisnis (`BR-xx`) atau alur proses bisnis di BRD yang terlewat tanpa modul pengampu di `MOD-xx` dan `SRS-F-xx`?
  - **Zero Scope Creep (Anti-Rogue Modules)**: Apakah seluruh modul dan sub-modul yang dirancang berada dalam batasan *In-Scope* proyek dan tidak ada modul "liar" tanpa dasar pemikiran bisnis pada BRD?
  - **Presisi Alur `[Aktor]` vs `[Sistem]` ke Modul Teknis**: Apakah alur proses bisnis interaktif `[Aktor]` vs `[Sistem]` pada BRD diterjemahkan secara presisi ke dalam sequence diagram, aturan validasi usecase, kontrak REST API, dan tata letak UI masing-masing modul?
  - **Dukungan Skema ERD Terkunci**: Apakah skema **ERD** mendukung penuh dan berkesinambungan dengan kebutuhan penyimpanan data seluruh modul bisnis yang didefinisikan di **PRD**, **SRS**, dan **MOD-xx**?
- [ ] **Kepatuhan Format BRD (Proses Bisnis)**: Apakah **SETIAP** penjabaran proses bisnis di BRD secara eksplisit telah memuat alur interaksi terstruktur antara `[Aktor]` dan `[Sistem]`? (Pastikan tidak ada proses bisnis yang terlewat).
- [ ] **Kepatuhan Format PRD (Standar Spesifikasi Produk & Anti-Halusinasi AI)**:
  - **Persona Pengguna Mendalam (`P-xx`)**: Apakah setiap persona memuat peran, tujuan utama, *Jobs-to-be-Done* (JTBD: *"Ketika [situasi], saya ingin [motivasi], sehingga [hasil]"*), *pain points* konkret, *success metrics*, dan konteks pakai (device, frekuensi)?
  - **Pemetaan Role Terpusat (Keycloak JSS)**: Apakah seluruh persona pengguna dipetakan secara tegas ke 4 Role Baku Pemkot Yogyakarta (`Superadmin`, `Pengawas`, `Admin`, `Operator`)?
  - **Visualisasi User Journey Map**: Apakah alur interaksi pengguna kritis dimodelkan dengan diagram `flowchart LR` (Discovery → Onboarding SSO Keycloak → Core Usage → Completion)?
  - **Visualisasi Feature Decomposition Tree**: Apakah dekomposisi struktur fitur divisualisasikan dengan diagram hierarkis `flowchart TD` (Root Sistem → Modul Bisnis Utama/Pendukung → Sub-modul & Aksi Operasional + 5 Modul Pengaturan Sistem)?
  - **Matriks Fitur & Prioritas MoSCoW**: Apakah setiap fitur memiliki ID `PRD-xx`, nama modul/fitur, deskripsi fungsionalitas, prioritas MoSCoW (Must, Should, Could, Won't), dan tautan traceability ke `BR-xx` yang valid?
  - **6 Komponen Wajib Pendalaman Modul Bisnis (Anti-Halusinasi AI)**: Apakah **SETIAP** modul bisnis pada PRD dirinci tuntas dan memuat 6 komponen baku tanpa pengecualian:
    1. *Tujuan & Fungsi Modul* (problem pengguna yang dipecahkan & entitas yang dikelola)
    2. *Dekomposisi Sub-Fitur & Aksi Operasional* (Tabel & Filter Data, Form Tambah/Ubah, Detail & Audit Trail, Ekspor/Cetak)
    3. *Alur Bisnis Modul (Flowchart TD / Sequence Diagram)*
    4. *Spesifikasi Data Input (Tabel Field, Tipe Data, Constraint Validasi, & Komponen Input UI)*
    5. *Spesifikasi Tampilan & Feedback Visual Apple HIG (Layout Container, Semantik Status Badge, Modal Dialog Konfirmasi)*
    6. *Acceptance Criteria Baku (Format Gherkin: Scenario, Given, When, Then)*
    *(Auditor WAJIB menolak Blueprint jika ada modul bisnis PRD yang hanya berupa narasi umum fiktif AI tanpa rincian spesifikasi input form dan skenario Gherkin)*
- [ ] **Kepatuhan Format SRS (6 Bagian Wajib)**: Apakah **SETIAP** *Functional Requirement* (`SRS-F-xx`) telah merinci alur fiturnya dengan sempurna menggunakan struktur baku 6 bagian:
  1. *Input Data*
  2. *Validasi*
  3. *Penyimpanan Data*
  4. *Status*
  5. *Error Handling*
  6. *QA Testing Acceptance*
  *(Auditor WAJIB menolak Blueprint jika ada SRS-F yang kehilangan satupun dari 6 poin ini)*

### 2. Kepatuhan Arsitektur dan Infrastruktur
- [ ] **Stack Backend**: Apakah secara eksplisit mendeskripsikan penggunaan **Go (Golang)** dengan **Clean Architecture** (domain, usecase, delivery, repository)?
- [ ] **Database Utama**: Apakah menyebutkan spesifikasi **PostgreSQL 16+** (termasuk connection pooling `pgxpool`) dengan penguncian skema ERD global 100%?
- [ ] **Manajemen File & Storage**: Apakah diwajibkan menggunakan **MinIO Object Storage** (bukan penyimpanan lokal) dengan validasi *Magic Bytes* (header biner) dan mekanisme *Presigned URL* (masa aktif 5–15 menit)?
- [ ] **Caching & Rate Limiting**: Apakah penggunaan **Redis 7+** sudah didefinisikan secara rasional (opsional/hanya jika butuh performa tinggi, session, atau job queue)?
- [ ] **Deployment/Environment**: Apakah mencantumkan dukungan containerization via **Docker Compose** (`docker-compose.yml` di root proyek) serta endpoint diagnostic `/api/v1/health`?

### 3. Keamanan, SSO, dan Akses (RBAC)
- [ ] **Otentikasi OIDC Terpusat**: Apakah mekanisme login wajib diarahkan ke **SSO Keycloak JSS (`sso.jogjakota.go.id`)**?
- [ ] **Halaman Login Terpisah & Sandbox Dummy**: Apakah dirancang **Halaman Login Terpisah (`/login`)** yang memuat panel sandbox 4 Dummy User testing (Superadmin, Pengawas, Admin, Operator) dengan fitur *1-Click Quick Login*?
- [ ] **Standard Role**: Apakah skema hak akses mencakup 4 Role minimum Pemkot Yogyakarta?
  1. `Superadmin` (Full Access seluruh modul & konfigurasi)
  2. `Pengawas` (Read-Only / Get Only / Dashboard Analitik & Akses Log Aktivitas Pengguna)
  3. `Admin` (Manajemen User & Pengaturan Aplikasi)
  4. `Operator` (Transaksi Modul Bisnis Harian)
- [ ] **Log Aktivitas Pengguna / Audit Trail (RBAC Eksklusif)**: Apakah audit trail aktivitas pengguna dirancang wajib ada dan **HANYA BISA DIAKSES oleh role `Superadmin` dan `Pengawas`**, sedangkan `Admin` dan `Operator` diblokir (HTTP 403 Forbidden)?

### 4. Kepatuhan UI/UX Apple HIG dan Modul Pengaturan Wajib
- [ ] **Kepatuhan Apple HIG**: Apakah desain UI mengadopsi prinsip Apple Human Interface Guidelines:
  - Sudut membulat continuous squircle (`rounded-2xl` 16–20px)
  - Efek frosted glass blur (`backdrop-filter: blur(20px) saturate(180%)`)
  - Tipografi San Francisco / Inter
  - Ruang kosong lega (8pt grid system)
- [ ] **Pola Navigasi Utama**:
  - Aplikasi Backoffice/Operasional: Wajib menggunakan **Left Panel Menu (Sidebar)** collapsible.
  - Aplikasi Publik/Landing Page: Wajib menggunakan **Top Navigation (Header Navbar)**.
- [ ] **Identitas & Branding Pemkot Yogyakarta**: Wajib menampilkan **Logo Resmi Vektor Pemkot Jogja (`logo-jogja.svg`) + Nama Aplikasi** di pojok kiri atas dan footer resmi `© [Tahun] Pemerintah Kota Yogyakarta`.
- [ ] **Tema & Aksesibilitas Anti-Color Clash**: Apakah mendefinisikan 8 Tema Terstandarisasi (4 Light + 4 Dark Themes) dengan rasio kontras tinggi (**WCAG AA/AAA Ratio ≥ 4.5:1**)?
- [ ] **5 Modul Pengaturan Sistem Wajib**: Apakah kelima modul pengaturan berikut sudah terdefinisi secara fungsional:
  1. **Manajemen Pengguna**: Sinkronisasi SSO JSS (ID JSS + Nama Lengkap otomatis + Role dropdown)
  2. **Manajemen Role**: Proteksi role aktif (role yang masih digunakan dilarang dihapus)
  3. **Manajemen Hak Akses**: Matriks izin per-role terhadap menu/sub-menu dengan switch toggle 4 aksi (Lihat, Tambah, Ubah, Hapus)
  4. **Manajemen Menu Sidebar**: Pengaturan hierarki menu/sub-menu, icon, badge, route, dan **PENGURUTAN POSISI MENU WAJIB INTERAKTIF MENGGESER / DRAG-AND-DROP (DRAG-TO-REORDER)**
  5. **Manajemen Tema dan Tampilan**: Pilihan 8 tema terstandarisasi anti-color clash
- [ ] **Modul Manajemen Master Data Terpadu**: Apakah entitas master data pendukung bisnis telah terdefinisi secara fungsional?

### 5. Rencana Implementasi Modular (`MOD-xx`) & Kontrak Teknis
- [ ] **Peta Modul & Dependensi Build**: Apakah seluruh implementasi dipecah ke dalam unit modular bertahap (`MOD-00`, `MOD-01`, dst.) dengan urutan build yang logis dan bebas dari siklik dependensi?
- [ ] **Spesifikasi Teknis per Modul**: Apakah setiap modul memuat:
  - Struktur file/folder Go Clean Architecture & React/Vue Vite
  - Skema tabel PostgreSQL 16+ persis
  - Kontrak REST API lengkap (Method, Path, Body, Response Success, Response Error, Traceability)
  - Kriteria Definition of Ready (DoR) dan Definition of Done (DoD) teknis
- [ ] **Matriks 4 State Wajib per Layar**: Apakah setiap layar modul (`UI-xx`) mendefinisikan 4 status wajib: *Loading Skeleton*, *Empty State*, *Error State*, dan *Success State*?

### 6. Standar Pengujian (QA), Keamanan & Dokumentasi API
- [ ] **QA & Negative Testing Suite**: Apakah spesifikasi pengujian (QA) mewajibkan *Positive Testing* (Happy Path) sekaligus *Automated Negative Testing Suite* (Type Mismatch, Boundary Violations, Form Injection, File Spoofing, 403 Forbidden Gate)?
- [ ] **Code Coverage**: Apakah terdapat target *code coverage* minimal **85%**?
- [ ] **Security Audit / Pentest**: Apakah terdapat klausul pelaksanaan SAST (`gosec`, `semgrep`), SCA (`govulncheck`, `npm audit`), dan DAST Pentest (OWASP Top 10) lengkap dengan bukti screenshot PoC?
- [ ] **Dokumentasi OpenAPI & Swagger**: Apakah semua endpoint RESTful API diwajibkan memiliki anotasi Swagger (`swaggo/swag`) dan auto-generate TypeScript client (`api.ts`) untuk frontend?
- [ ] **Standar Deliverables Format**: Apakah `Blueprint.md` mengamanatkan kompilasi seluruh laporan resmi (QA, KAK, Spesifikasi API, User Manual, Laporan Pentest) dalam format `.docx` formal di folder `docs/`?
