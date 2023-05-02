# This is a sample Python script.
import numpy as np
import random
import argparse

signals = 0
u = 0
sig_len = 0


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def rand_bin_array(K, N):
    # N: cantidad de bits totales
    # K: cantidad de 1s ubicados aleatoreamente.
    arr = np.zeros(N)
    arr[:K] = 1
    np.random.shuffle(arr)
    return arr


def generate_signals(nsignals):
    mylist = []
    for n in range(0, nsignals):
        mylist.append(rand_bin_array(random.randrange(1, u), random.randrange(1, sig_len)))
    return mylist


def get_hexa(signal):
    result = 0
    temp = 0
    elements = len(signal)
    for x in range(0, elements):
        temp = signal.item(elements - 1 - x)
        result += int((temp * 2 ** x))
    return result


def generate_payload(sig_list, bits):
    bit_count = 0
    sig_count = int(len(sig_list))
    byte_value = 0
    pload = []

    if (bits % 8) == 0:
        print(f'bytes calculados: {int(bits / 8)}')
    else:
        print(f'bytes calculados: {int((bits / 8) + 1)}')

    print(f'cantidad de señales: {sig_count}')

    for s in range(sig_count):
        item_len = int(len(sig_list[s]))
        for item in range(0, item_len):
            byte_value += int(sig_list[s].item(item_len - 1 - item) * 2 ** bit_count)
            bit_count += 1
            if bit_count == 8:
                pload.append(byte_value)
                bit_count = 0
                byte_value = 0

        if s == (sig_count - 1) and 8 > bit_count > 0:
            pload.append(byte_value)

    print(f'pload length: {int(len(pload))}')

    return pload


def calculate_total_bits(signals_array):
    total_bit_length = 0
    for i in range(int(len(signals_array))):
        total_bit_length += int(len(signals_array[i]))
    return total_bit_length


def show_signal_order(signals_array):
    top_signals = int(len(signals_array))

    for i in range(0, top_signals):
        print(
            f'signals: {i} -> {signals_array[i]} bit length: {int(len(signals_array[i]))} signal value: {get_hexa(signals_array[i])}')

    bits = calculate_total_bits(signals_array)
    print(f'bits totales: {bits}')

    print('')
    for i in range(0, top_signals):
        print(f'{signals_array[top_signals - 1 - i]}', end='')
    print('')
    print('')


def show_payload(pload):
    print("payload = ", end='')
    print(pload)
    print(f'uint8_t payload[{int(len(pload))}] = ', end='')

    print('{', end='')
    for k in range(0, int(len(pload))):
        print(f"0x{pload[k]:02x}", end='')
	
        if k == int(len(pload)) - 1:
            print(f'', end='')
        else:
            print(f', ', end='')

    print('}', end='')
    print("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("gen", type=str,
                        help='se usa para correr el script de forma generica '
                             '(cantidad max de unos y largo max de la señal: random.)')
    parser.add_argument("-s", type=str, dest='quantity_of_signals', nargs='+',
                        help='con "-s" indica la cantidad de señales a generar')
    parser.add_argument("-u", type=str, dest='quantity_of_ones', nargs='+',
                        help='con "-u" indica la cantidad max random de unos que la señal va a tener')
    parser.add_argument("-l", type=str, dest='sig_length', nargs='+',
                        help='con "-l" indica el largo max random de cada señal')

    args = parser.parse_args()

    print(args)

    if args.quantity_of_signals is None:
        signals = 6  # default
    else:
        signals = int(args.quantity_of_signals[0])

    if args.quantity_of_ones is None:
        u = 8  # default
    else:
        u = int(args.quantity_of_ones[0])

    if args.sig_length is None:
        sig_len = 32
    else:
        sig_len = int(args.sig_length[0])

    print_hi('PyCharm')

    array_list = generate_signals(signals)
    show_signal_order(array_list)
    bits = calculate_total_bits(array_list)
    payload = generate_payload(array_list, bits)
    show_payload(payload)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''
"python3 generator.py gen" 
cantidad max de unos y largo max de la señal: random.

"python3 generator.py gen -u 8 -l 64" 
con "-u" indica que hay que setar la cantidad max random de unos y el largo max random de cada señal.
'''
