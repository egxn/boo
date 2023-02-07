import time
import random
import string
import jiwer

def get_timestamp():
    return str(int(time.time()))

def create_id():
    return get_timestamp() + "-" + ''.join(random.choices(string.ascii_letters, k=5))

def calculate_wer(reference, hypothesis):
    return jiwer.wer(reference, hypothesis)