import json
import os
import time
from src.engines.turing_machine import TuringMachine
from src.engines.dfa_engine import DFA
from src.engines.pda_engine import PDA
from src.engines.lba_engine import LBA

def load_machine(filepath, machine_type):
    with open(filepath, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    if machine_type == "TM":
        return TuringMachine(states=config["states"], input_alphabet=config["input_alphabet"], tape_alphabet=config["tape_alphabet"], transitions=config["transitions"], initial_state=config["initial_state"], accept_states=config["accept_states"], reject_states=config["reject_states"], blank_symbol=config["blank_symbol"])
    elif machine_type == "LBA":
        return LBA(states=config["states"], input_alphabet=config["input_alphabet"], tape_alphabet=config["tape_alphabet"], transitions=config["transitions"], initial_state=config["initial_state"], accept_states=config["accept_states"], reject_states=config["reject_states"], blank_symbol=config["blank_symbol"])
    elif machine_type == "PDA":
        return PDA(states=config["states"], input_alphabet=config["input_alphabet"], stack_alphabet=config["stack_alphabet"], transitions=config["transitions"], initial_state=config["initial_state"], initial_stack_symbol=config["initial_stack_symbol"], accept_states=config["accept_states"])
    elif machine_type == "DFA":
        return DFA(states=config["states"], input_alphabet=config["input_alphabet"], transitions=config["transitions"], initial_state=config["initial_state"], accept_states=config["accept_states"])

def main():
    # Chomsky Hiyerarşisine göre makineleri yüklüyoruz
    dfa = load_machine(os.path.join("examples", "dfa_ends_with_ab.json"), "DFA")
    pda = load_machine(os.path.join("examples", "pda_an_bn.json"), "PDA")
    lba = load_machine(os.path.join("examples", "lba_an_bn_cn.json"), "LBA")
    tm = load_machine(os.path.join("examples", "copy_string_tm.json"), "TM")

    while True:
        print("\n" + "═"*55)
        print("🤖 CHOMSKY HİYERARŞİSİ - AUTOMATA LAB 🤖")
        print("═"*55)
        print("1. [Type 3] DFA: Düzenli Dil (Sonu 'ab' ile biten)")
        print("2. [Type 2] PDA: Bağlamdan Bağımsız (a^n b^n)")
        print("3. [Type 1] LBA: Bağlama Duyarlı (a^n b^n c^n)")
        print("4. [Type 0] TM : Özyineli Sayılabilir (w -> ww Kopyalama)")
        print("0. Çıkış")
        print("─" * 55)
        
        choice = input("Lütfen test etmek istediğiniz makineyi seçin (0-4): ")

        if choice == '0':
            print("Automata Lab kapatılıyor. GitHub'a yüklemeye hazırız!")
            break
            
        elif choice == '1':
            user_input = input("Type 3 (DFA) için katar girin (Örn: 'bbab'): ")
            dfa.run(user_input)
            time.sleep(1)
            
        elif choice == '2':
            user_input = input("Type 2 (PDA) için katar girin (Örn: 'aaabbb'): ")
            pda.run(user_input)
            time.sleep(1)

        elif choice == '3':
            user_input = input("Type 1 (LBA) için katar girin (Örn: 'aabbcc'): ")
            lba.run(user_input, delay=0.1)
            time.sleep(1)
            
        elif choice == '4':
            user_input = input("Type 0 (TM) için katar girin (Örn: 'ab'): ")
            tm.run(user_input, delay=0.1)
            time.sleep(1)
            
        else:
            print("Geçersiz seçim. Lütfen 0 ile 4 arasında bir değer girin.")

if __name__ == "__main__":
    main()