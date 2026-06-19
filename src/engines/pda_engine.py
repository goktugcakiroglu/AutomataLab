from src.core.machine import Machine

class PDA(Machine):
    """
    Pushdown Automaton (Yığıtlı Otomat) Simülatörü.
    Karakter okumanın yanında LIFO (Son Giren İlk Çıkar) mantığıyla yığıt (stack) hafızasını kullanır.
    """
    def __init__(self, states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol, accept_states):
        super().__init__(states, input_alphabet, transitions, initial_state, accept_states)
        self.stack_alphabet = stack_alphabet
        self.initial_stack_symbol = initial_stack_symbol
        self.stack = []
        self.tape = ""
        self.head_position = 0
        self.halted = False

    def load_string(self, input_string):
        self.tape = input_string
        self.head_position = 0
        self.reset()
        self.stack = [self.initial_stack_symbol] # Yığıt başlangıç sembolü ile başlar (Genelde Z)
        self.halted = False

    def step(self):
        if self.halted: return

        # 1. Önce epsilon (okumadan geçiş) var mı kontrol et
        if self.current_state in self.transitions and "epsilon" in self.transitions[self.current_state]:
            stack_top = self.stack[-1] if self.stack else None
            if stack_top in self.transitions[self.current_state]["epsilon"]:
                next_state, push_symbols = self.transitions[self.current_state]["epsilon"][stack_top]
                self.stack.pop() # Üsttekini çıkar
                
                # Yeni sembolleri yığıta ekle (epsilon değilse)
                for symbol in reversed(push_symbols):
                    if symbol != "epsilon":
                        self.stack.append(symbol)
                
                self.current_state = next_state
                return # Epsilon geçişi karakter tüketmez, turu bitir

        # Katar bittiyse durdur
        if self.head_position >= len(self.tape):
            self.halted = True
            return

        # 2. Normal Karakter Okuma İşlemi
        char = self.tape[self.head_position]
        stack_top = self.stack[-1] if self.stack else None

        if self.current_state in self.transitions and char in self.transitions[self.current_state]:
            if stack_top in self.transitions[self.current_state][char]:
                next_state, push_symbols = self.transitions[self.current_state][char][stack_top]
                
                self.stack.pop() # Zirveyi uçur
                
                for symbol in reversed(push_symbols):
                    if symbol != "epsilon":
                        self.stack.append(symbol)
                        
                self.current_state = next_state
                self.head_position += 1
            else:
                self.halted = True # Yığıt uyuşmazlığı
        else:
            self.halted = True # Tanımsız kural

    def run(self, input_string):
        self.load_string(input_string)
        print(f"--- PDA Başlatılıyor | Girdi: '{input_string}' ---")
        
        while not self.halted:
            char = self.tape[self.head_position] if self.head_position < len(self.tape) else "epsilon"
            stack_str = "".join(self.stack) if self.stack else "[BOŞ]"
            print(f"Durum: {self.current_state} | Okunan: {char} | Yığıt: {stack_str}")
            self.step()

        # Katar bittikten sonra son bir epsilon geçişiyle accept state'e gidilebiliyorsa diye kontrol
        if not self.halted and self.head_position >= len(self.tape):
             self.step()

        stack_str = "".join(self.stack) if self.stack else "[BOŞ]"
        if self.current_state in self.accept_states and self.head_position >= len(self.tape):
            print(f"SON DURUM: {self.current_state} | Yığıt: {stack_str}")
            print(f"SONUÇ: KABUL (PDA '{input_string}' katarını kabul etti.)\n")
        else:
            print(f"SON DURUM: {self.current_state} | Yığıt: {stack_str}")
            print(f"SONUÇ: RED (PDA '{input_string}' katarını reddetti.)\n")