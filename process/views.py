from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from process.models import *
import json
from datetime import date
import MySQLdb
import threading
import time
import math
import process.pir as pir_lib
# Create your views here.

def insert_data(request):
    import pandas_datareader as pdr
    if request.method == 'GET':
        ticker = request.GET['ticker']
        #print (ticker)
        end = date.today()
        start = date(end.year-1, end.month, end.day)
        ms = pdr.mstar.daily.MorningstarDailyReader('XBKK:'+ticker, start=start, end=end)
        price_close_data = ms.read().Close.tolist()
        price_close_str = list(map(lambda x: str(int(x)), price_close_data))
        #x = db.curser()
        #x.execute("""INSERT INTO Stock_Price (ticker, price) VALUES (%s,%s)""",(ticker, price_close_str))
        #if Stock_Price.objects.raw('SELECT * FROM Stock_Price WHERE ticker=%s' % (ticker, )) != None:
        check_in_db = Stock_Price.objects.filter(ticker=ticker)
        if check_in_db.exists():
            for i in check_in_db:
                print (i.id)
            i.price = price_close_str
            i.save()
            return HttpResponse("Data exists")
        else:
            p = Stock_Price(ticker=ticker, price=price_close_str)
            p.save()
        #print (price_close_data)
        return HttpResponse("Success")
        #return HttpResponse("Fail")

def calculate_z(price_arr, y_data, N, z_data, max_bin_digits, price_seq, price_per_thread):
    i = 0
    while i < price_per_thread:
        price_arr_num = price_seq*price_per_thread+i
        if price_arr_num >= len(price_arr): break
        #for s in price_data_list:
        for key,val in price_arr[price_arr_num].items():
            #if (price_arr_num >= len(s.price)): break
            base2_item = ("{0:0"+str(max_bin_digits)+"b}").format(int(val))
            count = 0
            for s1 in base2_item:
                arr_num = price_arr_num*max_bin_digits+count
                if s1 == '1': z_data[arr_num] = (z_data[arr_num] * y_data[key]) % N
                else: z_data[arr_num] = (z_data[arr_num] * y_data[key]**2) % N
                #z_data[arr_num] %= N
                count += 1
        i += 1
        #if (int(threading.current_thread().name) % 5 == 0): time.sleep(1)
    print ("Thread " + threading.current_thread().name + " completed.")

@csrf_exempt
def calculate_pir(request):
    data = Stock_Price.objects.all()
    max_bin_digits = 40
    price_list = list(data)
    request_body = json.loads(request.body.decode('utf-8'))
    N = int(request_body["number"])
    y = request_body["y"]
    data = {}
    for p in price_list:
        data[p.ticker] = {'y': y[p.ticker], 'data': json.dumps(p.price)}
    z_data_int = pir_lib.calculate_pir(data, N, 256)
    return HttpResponse(z_data_int, content_type="application/json")

def calculate_pir_1(request):
    from timeit import default_timer as timer
    start = timer()
    #data = {'A': [1,2,3,4,5],
    #    'B': [6,7,8,9,10],
    #    'C': [11,12,13,14,15],
    #    'D': [16,17,18,19,20],
    #    'E': [21,22,23,24,25]}
    #data = Stock_Price.objects.raw('SELECT * FROM Stock_Price')
    data = Stock_Price.objects.all()
    #for s in data:
    #    print (s.ticker)
    max_bin_digits = 40
    #data_per_row = 5
    #data_base2 = {}
    price_by_date = []
    data_computed = {}
    price_count_max = 0
    print (timer()-start)
    price_data_list = list(data)
    for s in data:
        #base2_item = ''
        price_count=0
        for i in s.price:
            #base2_item += ("{0:0"+str(max_bin_digits)+"b}").format(int(i))
            if len(price_by_date) <= price_count:
                price_at_date = {s.ticker: i}
                price_by_date.append(price_at_date)
            else:
                price_by_date[price_count][s.ticker] = i
            price_count += 1
        if len(s.price) > price_count_max: price_count_max = len(s.price)
    #data_base2[s.ticker] = base2_item
    z_data = [1] * (max_bin_digits * price_count_max)
    print (timer()-start)
    #z_data[0: data_count*max_bin_digits] = 1
    #request_body = request.POST.dict()
    #print (request.body)
    request_body = json.loads(request.body.decode('utf-8'))
    N = int(request_body["number"])
    y = request_body["y"]
    y_data = {}
    for key,val in y.items():
        y_data[key] = int(val, 16)
    count1 = 0
    thread_arr = []
    subcount = 0
    price_per_thread = 25
    count1_max = math.ceil(price_count_max/price_per_thread)
    while count1 < count1_max:
        a = threading.Thread(target=calculate_z, name=str(count1), kwargs={'price_arr': price_by_date, 'N': N, 'y_data': y_data, 'z_data': z_data, 'max_bin_digits': max_bin_digits, 'price_seq': count1, 'price_per_thread': price_per_thread})
        thread_arr.append(a)
        a.start()
        count1 += 1
    #print ("Start all threaded")
    #print (timer()-start)
    for t in thread_arr:
        t.join()
        #count1 += 1
    #count2 = 0
    #for key,val in data_base2.items():
    #    #print (key, val)
    #    count = 0
    #    for i in val:
    #        data_y = int(y[key],16)
    #        if i == '1': z_data[count] *= data_y
    #        else: z_data[count] *= data_y**2
    #        z_data[count] %= N
    #        count += 1
    #    #count2 += 1
    z_data_int = list(map(lambda x: '{:x}'.format(x), z_data))
    print (timer()-start)
    return HttpResponse(json.dumps(z_data_int), content_type="application/json")
