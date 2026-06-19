from src.engines.turing_machine import TuringMachine

class LBA(TuringMachine):
    """
    Linear Bounded Automaton (LBA) Simülatörü.
    Turing makinesinden farkı: Şerit boyutu kullanıcının girdiği girdi kadardır.
    Makine şeridin dışına çıkmaya çalışırsa çöker (Sınır ihlali).
    """
    def load_tape(self, input_string):
        super().load_tape(input_string)
        # Sınırları belirliyoruz. Girdi boyutu + 1 (Sondaki boşluğu okuyabilmek için)
        self.left_bound = 0
        self.right_bound = len(input_string) if input_string else 0

    def move_head(self, direction):
        super().move_head(direction)
        # Sınır ihlali kontrolü
        if self.head_position < self.left_bound or self.head_position > self.right_bound:
            self.halted = True
            self.current_state = "CRASH (LBA Sınır İhlali: Bant dışına çıkılamaz!)"