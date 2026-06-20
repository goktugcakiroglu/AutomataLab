[![AutomataLab Engine CI](https://github.com/goktugcakiroglu/AutomataLab/actions/workflows/python-ci.yml/badge.svg)](https://github.com/goktugcakiroglu/AutomataLab/actions/workflows/python-ci.yml)

AutomataLab, teorik bilgisayar biliminin temelini oluşturan **Chomsky Hiyerarşisi'ndeki** dört ana otomat tipini (DFA, PDA, LBA, Turing Machine) simüle eden bütünleşik bir yazılım mühendisliği aracıdır. Proje; formal matematiksel soyutlamalardan (Tuple tanımlamaları) başlayıp, Nesne Yönelimli Programlama (OOP) prensipleriyle kurulan motor katmanından (Backend Engine) geçerek modern ve asenkron bir Grafiksel Kullanıcı Arayüzüne (GUI) uzanan süreci modüler bir mimariyle birleştirir.

## Tasarım Mimarisi (Config-Driven MVC)

Proje, kuralların JSON'dan dinamik okunduğu ve GUI'nin asenkron çalıştığı sıkı bir mimariye sahiptir:

```mermaid
graph LR
    subgraph Configuration
        JSON[examples/*.json <br> State & Transition Rules]
    end

    subgraph Core Engine [Backend - Python OOP]
        Base[src/core/machine.py <br> Abstract Base]
        Engines[dfa_engine.py <br> pda_engine.py <br> turing_machine.py]
        Base <|-- Engines
    end

    subgraph UI [Frontend - CustomTkinter]
        GUI[gui.py <br> Asynchronous Event Loop]
    end

    JSON -->|1. Loads Config| Engines
    GUI -->|2. Injects Input String| Engines
    Engines -->|3. Yields Real-Time State| GUI
```

## Type-3 (DFA) Örnek Durum Geçiş Diyagramı
Aşağıdaki şema, sistemde yüklü olan "Sonu 'ab' ile biten katarları kabul eden" DFA'nın donanımsal mantığını (dfa_ends_with_ab.json) temsil eder:

```
stateDiagram-v2
    direction LR
    [*] --> q0 : Başlangıç
    q0 --> q1 : a
    q0 --> q0 : b
    q1 --> q1 : a
    q1 --> q2 : b
    q2 --> q1 : a
    q2 --> q0 : b
    q2 --> [*] : Kabul (Accept)
```

## Requirements

Projeyi derlemek ve çalıştırmak için aşağıdaki ortam gereksinimlerine ihtiyaç vardır:
* **Operating System:** Windows / Linux / macOS (Çapraz Platform Uyumlu)
* **Backend Environment:** Python 3.x
* **Frontend UI Library:** `customtkinter` (Modern, donanım ivmeli GUI motoru)
## Build & Run

1. Proje dizinine gidin:
```bash
git clone [https://github.com/goktugcakiroglu/AutomataLab.git](https://github.com/goktugcakiroglu/AutomataLab.git)
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
├── .github/workflows/python-ci.yml # Otomatik Motor Testleri (Pytest)
├── gui.py                 # Frontend: CustomTkinter tabanlı asenkron Dark Mode arayüz
├── examples/              # Configuration: JSON tabanlı kural setleri
│   ├── dfa_ends_with_ab.json
│   ├── pda_an_bn.json
│   ├── lba_an_bn_cn.json
│   └── copy_string_tm.json
├── tests/
|   └── test_automata.py   # Unit Testler (DFA, PDA, LBA, TM)
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
