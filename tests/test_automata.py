import pytest
import json
import os
from src.engines.dfa_engine import DFA
from src.engines.pda_engine import PDA
from src.engines.lba_engine import LBA
from src.engines.turing_machine import TuringMachine

def load_cfg(filename):
    filepath = os.path.join("examples", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_dfa_ends_with_ab():
    cfg = load_cfg("dfa_ends_with_ab.json")
    dfa = DFA(cfg["states"], cfg["input_alphabet"], cfg["transitions"], cfg["initial_state"], cfg["accept_states"])
    
    # Kabul Durumu Testi
    dfa.run("bbab")
    assert dfa.current_state in dfa.accept_states
    
    # Ret Durumu Testi
    dfa.run("bba")
    assert dfa.current_state not in dfa.accept_states

def test_pda_an_bn():
    cfg = load_cfg("pda_an_bn.json")
    pda = PDA(cfg["states"], cfg["input_alphabet"], cfg["stack_alphabet"], cfg["transitions"], cfg["initial_state"], cfg["initial_stack_symbol"], cfg["accept_states"])
    
    pda.run("aaabbb")
    assert pda.current_state in pda.accept_states

    pda.run("aabbb") # Hatalı katar
    assert pda.current_state not in pda.accept_states

def test_lba_an_bn_cn():
    cfg = load_cfg("lba_an_bn_cn.json")
    lba = LBA(cfg["states"], cfg["input_alphabet"], cfg["tape_alphabet"], cfg["transitions"], cfg["initial_state"], cfg["accept_states"], cfg["reject_states"], cfg["blank_symbol"])
    
    lba.run("aabbcc", delay=0)
    assert lba.current_state in lba.accept_states

def test_turing_machine_copy():
    cfg = load_cfg("copy_string_tm.json")
    tm = TuringMachine(cfg["states"], cfg["input_alphabet"], cfg["tape_alphabet"], cfg["transitions"], cfg["initial_state"], cfg["accept_states"], cfg["reject_states"], cfg["blank_symbol"])
    
    tm.run("ab", delay=0)
    assert tm.current_state in tm.accept_states
