from src.core.machine import Machine

class DFA(Machine):
    """
    Deterministik Sonlu Otomat (DFA) Simülatörü.
    Sadece ileri yönlü okuma yapar ve durumu günceller.
    """
    def __init__(self, states, input_alphabet, transitions, initial_state, accept_states):
        super().__init__(states, input_alphabet, transitions, initial_state, accept_states)
        self.tape = ""
        self.head_position = 0
        self.halted = False

    def load_string(self, input_string):
        self.tape = input_string
        self.head_position = 0
        self.reset()
        self.halted = False

    def step(self):
        """DFA'nın 1 karakter okuyup durum değiştirmesi."""
        if self.halted or self.head_position >= len(self.tape):
            self.halted = True
            return
        
        char = self.tape[self.head_position]
        
        # Alfabede olmayan bir karakter gelirse direkt reddet
        if char not in self.input_alphabet:
            self.current_state = f"REJECT (Geçersiz Karakter: {char})"
            self.halted = True
            return

        # Geçiş kuralı varsa uygula
        if self.current_state in self.transitions and char in self.transitions[self.current_state]:
            self.current_state = self.transitions[self.current_state][char]
            self.head_position += 1
        else:
            self.current_state = "REJECT (Tanımsız Geçiş veya Dead State)"
            self.halted = True

    def run(self, input_string):
        self.load_string(input_string)
        print(f"--- DFA Başlatılıyor | Girdi: '{input_string}' ---")
        
        # Kelime bitene veya makine çökene kadar çalış
        while not self.halted and self.head_position < len(self.tape):
            print(f"Anlık Durum: {self.current_state} | Okunan Harf: {self.tape[self.head_position]}")
            self.step()

        # Son durumu kontrol et
        if self.current_state in self.accept_states and self.head_position == len(self.tape):
            print(f"SONUÇ: KABUL (DFA '{input_string}' katarını {self.current_state} durumunda kabul etti.)\n")
        else:
            print(f"SONUÇ: RED (DFA '{input_string}' katarını {self.current_state} durumunda reddetti.)\n")