class Machine:
    """
    Tüm otomatların (DFA, NFA, PDA, Turing Machine) temelini oluşturan Soyut Sınıf (Base Class).
    Bir makinenin sahip olması gereken en temel özellikleri ve davranışları tanımlar.
    """
    def __init__(self, states, input_alphabet, transitions, initial_state, accept_states):
        self.states = states                  # Q: Tüm durumların kümesi
        self.input_alphabet = input_alphabet  # Σ: Girdi alfabesi
        self.transitions = transitions        # δ: Geçiş kuralları (Transition function)
        self.initial_state = initial_state    # q0: Başlangıç durumu
        self.accept_states = accept_states    # F: Kabul durumları
        
        self.current_state = initial_state    # Makinenin anlık durumu

    def reset(self):
        """Makineyi başlangıç durumuna sıfırlar."""
        self.current_state = self.initial_state

    def step(self):
        """
        Makinenin tek bir adım atmasını sağlar. 
        Her makinenin (Turing, DFA vb.) adım atma mantığı farklı olduğu için 
        burada sadece şablon (NotImplementedError) bırakıyoruz.
        """
        raise NotImplementedError("Bu metod alt sınıflar tarafından ezilmelidir (override).")

    def run(self):
        """
        Makineyi durana veya bitene kadar çalıştırır.
        """
        raise NotImplementedError("Bu metod alt sınıflar tarafından ezilmelidir (override).")