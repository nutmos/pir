# data is the dictionary with format
# key is the value of data
# value is the dictionary with format:
# key: y value: QR, QNR number in base 16 format string
# key: data value: the data string to encode
# N is the modulus value
# k is the bits of N (key)
# return data is array of z that contains array of base 16 number in string format
import threading
import math
import json

def calculate_z(data_arr, N, z_data, seq, char_per_thread, k):
    i = 0
    while i < char_per_thread:
        char_arr_num = seq*char_per_thread+i
        #for s in price_data_list:
        for key,val in data_arr.items():
            if char_arr_num >= len(val['data']): continue
            #print(val['data'])
            #if (price_arr_num >= len(s.price)): break
            #base2_item = ("{0:0"+str(max_bin_digits)+"b}").format(int(val))
            base2_item = format(ord(val['data'][char_arr_num]), '07b')
            count = 0
            for s1 in base2_item:
                z_arr_num = char_arr_num*7+count
                if s1 == '1': z_data[z_arr_num] = (z_data[z_arr_num] * int(val['y'], 16)) % N
                else: z_data[z_arr_num] = (z_data[z_arr_num] * int(val['y'],16)**2) % N
                #z_data[arr_num] %= N
                count += 1
        i += 1
        #if (int(threading.current_thread().name) % 5 == 0): time.sleep(1)
    #print ("Thread " + threading.current_thread().name + " completed. i = " + str(i))

def calculate_pir(data, N, k):
    from timeit import default_timer as timer
    start = timer()
    thread_arr = []
    #price_per_thread = 25
    max_length = 0
    for key,val in data.items():
        data_len = len(val['data'])
        if data_len > max_length: max_length = data_len
    number_of_thread = 9
    z_data = [1] * (max_length * k * 7)
    #print (max_length)
    if max_length % number_of_thread != 0: number_of_thread += 1
    char_per_thread = math.floor(max_length/number_of_thread)
    count1 = 0
    while count1 < number_of_thread:
        a = threading.Thread(target=calculate_z, name=str(count1), kwargs={'data_arr': data, 'N': N, 'z_data': z_data, 'seq': count1, 'char_per_thread': char_per_thread, 'k': k})
        thread_arr.append(a)
        a.start()
        count1 += 1
    for t in thread_arr:
        t.join()
    #print(' '.join(format(ord(x), 'b') for x in data['AOT']['data'][0:10]))
    z_data_int = list(map(lambda x: '{:x}'.format(x), z_data))
    z_data_len = len(z_data)
    i = 1
    #print (z_data[0])
    #while i < z_data_len:
    #    if z_data[i] == 1 and z_data[i-1] != 1: print (i)
    #    i += 1
    #print (z_data[512])
    return json.dumps(z_data_int)
