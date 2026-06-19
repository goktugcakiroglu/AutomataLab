from src.core.machine import Machine
import time

class TuringMachine(Machine):
    """
    Klasik bir Turing Makinesi simülatörü.
    Sonsuz şerit (tape) mantığını simüle etmek için Python sözlükleri (dictionary) kullanır.
    """
    def __init__(self, states, input_alphabet, tape_alphabet, transitions, initial_state, accept_states, reject_states, blank_symbol='_'):
        # Üst sınıfın (Machine) başlatıcısını çağırıyoruz
        super().__init__(states, input_alphabet, transitions, initial_state, accept_states)
        
        self.tape_alphabet = tape_alphabet    # Γ: Şerit alfabesi (Girdi alfabesi + Boşluk sembolü vb.)
        self.reject_states = reject_states    # q_reject: Ret durumları
        self.blank_symbol = blank_symbol      # Boşluk sembolü (Genelde _, B veya boşluk karakteri)
        
        self.tape = {}                        # Şeridi dictionary olarak tanımlıyoruz (Negatif indeksler için ideal)
        self.head_position = 0                # Okuma/Yazma kafasının konumu

    def load_tape(self, input_string):
        """Kullanıcının verdiği katarı (string) şeride yükler ve makineyi sıfırlar."""
        self.tape = {i: char for i, char in enumerate(input_string)}
        self.head_position = 0
        self.reset()
        self.halted = False

    def read_tape(self):
        """Okuma kafasının bulunduğu konumdaki karakteri döndürür. Boşsa blank_symbol döner."""
        return self.tape.get(self.head_position, self.blank_symbol)

    def write_tape(self, symbol):
        """Okuma kafasının bulunduğu konuma yeni sembolü yazar."""
        self.tape[self.head_position] = symbol

    def move_head(self, direction):
        """Kafayı sağa (R), sola (L) hareket ettirir veya sabit tutar (S)."""
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'S' (Stay) durumu için pozisyon değişmez

    def print_tape_state(self):
        """Terminalde şeridin ve kafanın anlık durumunu görselleştirir."""
        if not self.tape:
            return

        min_idx = min(min(self.tape.keys()), self.head_position)
        max_idx = max(max(self.tape.keys()), self.head_position)
        
        tape_str = ""
        head_str = ""
        
        for i in range(min_idx, max_idx + 1):
            char = self.tape.get(i, self.blank_symbol)
            tape_str += f"[{char}]"
            if i == self.head_position:
                head_str += " ^ "
            else:
                head_str += "   "
                
        print(f"Durum: {self.current_state}")
        print(tape_str)
        print(head_str)
        print("-" * 30)

    def step(self):
        """Makinenin 1 birimlik kural işlemesini (sağ/sol/yazma) yapar."""
        if self.halted:
            return

        current_symbol = self.read_tape()
        
        # Geçerli durum için kural var mı kontrolü
        if self.current_state in self.transitions and current_symbol in self.transitions[self.current_state]:
            # Kuralı al: (yeni_durum, yazılacak_sembol, hareket_yönü)
            next_state, write_symbol, move_dir = self.transitions[self.current_state][current_symbol]
            
            # 1. Yazma işlemi
            self.write_tape(write_symbol)
            
            # 2. Durum geçişi
            self.current_state = next_state
            
            # 3. Kafa hareketi
            self.move_head(move_dir)
            
            # Makine kabul veya ret durumuna ulaştıysa durdur
            if self.current_state in self.accept_states or self.current_state in self.reject_states:
                self.halted = True
        else:
            # Gidilecek bir yol/kural yoksa makine çöker (crash/reject)
            self.halted = True
            self.current_state = "CRASH (Tanımsız Geçiş)"

    def run(self, input_string, delay=0.5):
        """Makineyi baştan sona çalıştırır ve adımları ekrana basar."""
        self.load_tape(input_string)
        print("--- Turing Makinesi Başlatılıyor ---")
        self.print_tape_state()
        
        while not self.halted:
            time.sleep(delay)  # Görselleştirme için ufak bir bekleme süresi
            self.step()
            self.print_tape_state()
            
        if self.current_state in self.accept_states:
            print(f"\nSONUÇ: KABUL (Makine {self.current_state} durumunda durdu.)")
        else:
            print(f"\nSONUÇ: RED (Makine {self.current_state} durumunda durdu.)")