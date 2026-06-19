import customtkinter as ctk
import json
import os
from src.engines.turing_machine import TuringMachine
from src.engines.dfa_engine import DFA
from src.engines.pda_engine import PDA
from src.engines.lba_engine import LBA

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class AutomataGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Automata Lab - Chomsky Hiyerarşisi")
        self.geometry("900x600")
        
        self.current_machine = None
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Sol Menü (Kontrol Paneli)
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🤖 AUTOMATA LAB", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)
        
        self.machine_var = ctk.StringVar(value="Seçim Yapın")
        self.machine_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            variable=self.machine_var,
            values=["[Type 3] DFA: Sonu 'ab'", "[Type 2] PDA: a^n b^n", "[Type 1] LBA: a^n b^n c^n", "[Type 0] TM: Katar Kopyalama"]
        )
        self.machine_menu.pack(pady=10, padx=20, fill="x")
        
        self.input_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Test katarını girin...")
        self.input_entry.pack(pady=20, padx=20, fill="x")
        
        self.run_btn = ctk.CTkButton(self.sidebar_frame, text="▶ SİMÜLASYONU BAŞLAT", command=self.start_simulation)
        self.run_btn.pack(pady=10, padx=20, fill="x")
        
        # Sağ Panel (Konsol / Çıktı Ekranı)
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.console = ctk.CTkTextbox(self.output_frame, font=ctk.CTkFont(family="Consolas", size=14))
        self.console.pack(fill="both", expand=True, padx=10, pady=10)
        self.console.insert("0.0", "Sisteme hoş geldiniz. Sol menüden bir makine seçin ve test katarı girin.\n")

    def log(self, text):
        """Konsola metin yazdırır ve en alta kaydırır."""
        self.console.insert("end", text + "\n")
        self.console.see("end")

    def load_machine_config(self, machine_type):
        """Seçilen makineye göre JSON dosyasını okur ve motoru yükler."""
        if "DFA" in machine_type:
            with open(os.path.join("examples", "dfa_ends_with_ab.json"), 'r') as f: config = json.load(f)
            return DFA(config["states"], config["input_alphabet"], config["transitions"], config["initial_state"], config["accept_states"])
        elif "PDA" in machine_type:
            with open(os.path.join("examples", "pda_an_bn.json"), 'r') as f: config = json.load(f)
            return PDA(config["states"], config["input_alphabet"], config["stack_alphabet"], config["transitions"], config["initial_state"], config["initial_stack_symbol"], config["accept_states"])
        elif "LBA" in machine_type:
            with open(os.path.join("examples", "lba_an_bn_cn.json"), 'r') as f: config = json.load(f)
            return LBA(config["states"], config["input_alphabet"], config["tape_alphabet"], config["transitions"], config["initial_state"], config["accept_states"], config["reject_states"], config["blank_symbol"])
        elif "TM" in machine_type:
            with open(os.path.join("examples", "copy_string_tm.json"), 'r') as f: config = json.load(f)
            return TuringMachine(config["states"], config["input_alphabet"], config["tape_alphabet"], config["transitions"], config["initial_state"], config["accept_states"], config["reject_states"], config["blank_symbol"])
        return None

    def start_simulation(self):
        selection = self.machine_var.get()
        input_str = self.input_entry.get()
        
        if selection == "Seçim Yapın":
            self.log("LÜTFEN ÖNCE BİR MAKİNE SEÇİN!")
            return
            
        self.current_machine = self.load_machine_config(selection)
        
        if isinstance(self.current_machine, TuringMachine) or isinstance(self.current_machine, LBA):
            self.current_machine.load_tape(input_str)
        else:
            self.current_machine.load_string(input_str)
            
        self.console.delete("0.0", "end")
        self.log(f"--- {selection} BAŞLATILDI ---")
        self.log(f"Test Edilen Girdi: '{input_str}'\n")
        
        self.is_running = True
        self.run_btn.configure(state="disabled") # Çalışırken butonu kilitle
        self.simulation_step() # Döngüyü başlat
        
    def simulation_step(self):
        if not self.is_running or self.current_machine.halted:
            self.finish_simulation()
            return
            
        # 1. Önce anlık durumu ekrana bas (Motor tipine göre farklı format)
        if isinstance(self.current_machine, TuringMachine) or isinstance(self.current_machine, LBA):
            min_idx = min(min(self.current_machine.tape.keys()), self.current_machine.head_position) if self.current_machine.tape else 0
            max_idx = max(max(self.current_machine.tape.keys()), self.current_machine.head_position) if self.current_machine.tape else 0
            tape_str = "".join([f"[{self.current_machine.tape.get(i, '_')}]" for i in range(min_idx, max_idx + 1)])
            self.log(f"Durum: {self.current_machine.current_state} | Şerit: {tape_str} | Konum: {self.current_machine.head_position}")
            
        elif isinstance(self.current_machine, PDA):
            char = self.current_machine.tape[self.current_machine.head_position] if self.current_machine.head_position < len(self.current_machine.tape) else "epsilon"
            stack_str = "".join(self.current_machine.stack) if self.current_machine.stack else "[BOŞ]"
            self.log(f"Durum: {self.current_machine.current_state} | Okunan: {char} | Yığıt: {stack_str}")
            
        elif isinstance(self.current_machine, DFA):
            char = self.current_machine.tape[self.current_machine.head_position] if self.current_machine.head_position < len(self.current_machine.tape) else "BİTTİ"
            self.log(f"Durum: {self.current_machine.current_state} | Okunan: {char}")

        # 2. Makineye bir adım attır
        self.current_machine.step()
        
        # 3. GUI'yi dondurmadan 0.3 saniye sonra diğer adıma geç (Recursive UI loop)
        self.after(300, self.simulation_step)

    def finish_simulation(self):
        self.is_running = False
        self.run_btn.configure(state="normal")
        
        # Sonuç hesaplama
        if isinstance(self.current_machine, DFA) or isinstance(self.current_machine, PDA):
            accepted = self.current_machine.current_state in self.current_machine.accept_states and self.current_machine.head_position >= len(self.current_machine.tape)
        else:
            accepted = self.current_machine.current_state in self.current_machine.accept_states
            
        self.log("\n" + "="*30)
        if accepted:
            self.log(f"✅ SONUÇ: KABUL (Makine {self.current_machine.current_state} durumunda durdu.)")
        else:
            self.log(f"❌ SONUÇ: RED (Makine {self.current_machine.current_state} durumunda durdu.)")
        self.log("="*30 + "\n")

if __name__ == "__main__":
    app = AutomataGUI()
    app.mainloop()