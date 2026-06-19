# AutomataLab: Chomsky Hierarchy Simulator

AutomataLab, teorik bilgisayar biliminin temelini oluşturan **Chomsky Hiyerarşisi'ndeki** dört ana otomat tipini (DFA, PDA, LBA, Turing Machine) simüle eden bütünleşik bir yazılım mühendisliği aracıdır. Proje; formal matematiksel soyutlamalardan (Tuple tanımlamaları) başlayıp, Nesne Yönelimli Programlama (OOP) prensipleriyle kurulan motor katmanından (Backend Engine) geçerek modern ve asenkron bir Grafiksel Kullanıcı Arayüzüne (GUI) uzanan süreci modüler bir mimariyle birleştirir.

**Tasarım Mimarisi:** Proje, **MVC (Model-View-Controller)** mimari deseni ve **Config-Driven (Yapılandırma Odaklı)** bir yaklaşım esas alınarak geliştirilmiştir. Otomat kurallarının JSON dosyalarından dinamik olarak okunduğu ve kullanıcı arayüzü bileşenlerinin çekirdek motor mantığından tamamen izole edildiği, genişletilebilir bir simülasyon platformudur.

## Requirements

Projeyi derlemek ve çalıştırmak için aşağıdaki ortam gereksinimlerine ihtiyaç vardır:
* **Operating System:** Windows / Linux / macOS (Çapraz Platform Uyumlu)
* **Backend Environment:** Python 3.x
* **Frontend UI Library:** `customtkinter` (Modern, donanım ivmeli GUI motoru)
## Build & Run

1. Proje dizinine gidin:
```bash
cd AutomataLab
```
2. Gerekli arayüz kütüphanesini sisteme kurun:
```bash
python -m pip install customtkinter
```
3. Grafiksel Kullanıcı Arayüzünü (GUI) başlatın:
```bash
python gui.py
```

## How It Works (The Pipeline)

Simülasyon süreci, verinin statik dosyalardan alınıp dinamik olarak ekranda canlandırıldığı 3 farklı katmandan oluşur:

1. **Pass 1 — Config Loading (JSON Katmanı):** Kullanıcı GUI üzerinden bir makine seçtiğinde, `examples/` klasöründeki ilgili JSON dosyası okunur. Bu dosya; makinenin alfabesini, durumlarını (states) ve geçiş fonksiyonlarını barındırır.
2. **Pass 2 — OOP Engine Execution (Python Backend):** JSON'dan alınan kurallar, `src/core/machine.py` içindeki soyut (abstract) temel sınıfa beslenir. Makinenin tipine göre (örneğin PDA ise `stack`, Turing ise `tape` yönetimi) ilgili motor ayağa kalkar ve kullanıcının girdiği katarı adım adım (step-by-step) işletmeye başlar.
3. **Pass 3 — Asynchronous UI Rendering (CustomTkinter Frontend):** Motorun ürettiği her anlık durum (state, kafa pozisyonu, yığıt durumu), GUI'yi dondurmamak (kitlememek) için `after()` metodu kullanılarak recursive (özyineli) bir UI döngüsüyle ekrana gerçek zamanlı olarak yansıtılır.

## Supported Automata Features (Chomsky Hierarchy)

AutomataLab motorları, Chomsky hiyerarşisindeki dillere ait karakteristik yapıları şu şekilde donanımsal mantığa çevirir:

| Hiyerarşi (Tip) | Otomat Karşılığı | Çözdüğü Problem / Simülasyon Mantığı | Bellek Mimarisi |
| :--- | :--- | :--- | :--- |
| **Type-3 (Düzenli Dil)** | **DFA** (Deterministik Sonlu Otomat) | `ab` ile biten katarların tespiti (Regex Engine tabanı). | Hafıza yoktur (Sadece durum takibi). |
| **Type-2 (Bağlamdan Bağımsız)** | **PDA** (Yığıtlı Otomat) | `a^n b^n` eşitlik kontrolü (Derleyici parantez eşleştirme mantığı). | **LIFO Stack** (Son giren ilk çıkar). |
| **Type-1 (Bağlama Duyarlı)** | **LBA** (Doğrusal Sınırlı Otomat) | `a^n b^n c^n` kontrolü. Üçlü senkronizasyon gerektiren dil yapıları. | **Bounded Tape** (Girdi boyutu ile sınırlı şerit). |
| **Type-0 (Özyineli Sayılabilir)** | **TM** (Turing Makinesi) | Katar Kopyalama (`w -> ww`). RAM ve CPU'nun teorik eşleniği. | **Infinite Tape** (Çift yönlü sonsuz şerit). |

## Error Handling Strategy

Sistem, çalışma anında makinenin çökmesini engelleyen ve otomata teorisine sadık kalan bir hata (Reject/Crash) yönetim mekanizmasına sahiptir.

| Error Type | Trigger Condition | Output Example |
| :--- | :--- | :--- |
| **Invalid Alphabet** | Kullanıcının, makinenin girdi alfabesinde olmayan bir karakter girmesi. | `REJECT (Geçersiz Karakter: c)` |
| **Undefined Transition** | Bulunulan durum ve okunan karakter için kuralın tanımlanmamış olması. | `REJECT (Tanımsız Geçiş veya Dead State)` |
| **Stack Mismatch (PDA)** | Yığıttan silinmesi beklenen sembol ile yığıtın zirvesindeki (top) sembolün uyuşmaması. | `SONUÇ: RED (Yığıt Uyuşmazlığı)` |
| **Boundary Violation (LBA)** | Okuma/Yazma kafasının, girdi katarı için ayrılan hafıza bloğunun (şeridin) dışına çıkmaya çalışması. | `CRASH (LBA Sınır İhlali: Bant dışına çıkılamaz!)` |

## Project Structure

```text
AutomataLab/
├── gui.py                 # Frontend: CustomTkinter tabanlı asenkron Dark Mode arayüz
├── examples/              # Configuration: JSON tabanlı kural setleri
│   ├── dfa_ends_with_ab.json
│   ├── pda_an_bn.json
│   ├── lba_an_bn_cn.json
│   └── copy_string_tm.json
├── src/               
│   ├── core/
│   │   └── machine.py     # Base Model: Tüm otomatların miras aldığı soyut ana sınıf
│   └── engines/           # Backend: Otomatlara özel bellek ve okuma/yazma motorları
│       ├── dfa_engine.py
│       ├── pda_engine.py
│       ├── lba_engine.py
│       └── turing_machine.py
```

## Future Work

* **Dinamik Otomat İnşası:** Kullanıcıların JSON dosyalarına kod üzerinden dokunmadan, GUI üzerinden "Durum, Alfabe ve Kural" ekleyerek kendi otomatlarını tasarlayabilecekleri interaktif bir "Automata Builder" modülü.
