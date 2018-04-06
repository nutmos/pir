var private_ir = {
    jacobi: function(a, b) {
        if (b.leq(0) || b.mod(2).eq(0)) return 0;
        var j = 1;
        if (a.lt(0)) {
            a = bigInt(-a);
            if (b.mod(4).eq(3))
                j = -j;
        }
        while (!a.isZero()) {
            while (a.mod(2).isZero()) {
             /* Process factors of 2: Jacobi(2,b)=-1 if b=3,5 (mod 8) */
                a = a.divide(2);
                if (b.mod(8).eq(3) || b.mod(8).eq(5))
                    j = -j;
            }
            /* Quadratic reciprocity: Jacobi(a,b)=-Jacobi(b,a) if a=3,b=3 (mod 4) */
            var tmp = b;
            b = a;
            a = tmp;
            if (a.mod(4).eq(3) && b.mod(4).eq(3)) j = -j;
            a = a.mod(b);
        }
        if (b.eq(1)) return j;
        else return 0;
    },
    generatePrime: function(key_arr, key, kbits, url, method, retrieveDataFunction) {
        var n1, n2, numqnr = bigInt(0);
        forge.prime.generateProbablePrime(kbits/2, function(err, num) {
            n1 = bigInt(num.toString(16), 16);
            forge.prime.generateProbablePrime(kbits/2, function(err, num) {
                n2 = bigInt(num.toString(16),16);
                var N = n1.multiply(n2), count1 = 0, numqnr = bigInt(0), setplusqr = {}, get_data = key, tickers_arr = key_arr;
                if (!tickers_arr.includes(get_data)) {
                    window.alert("Stock not found! Please enter the new one.");
                    return;
                }
                for (var k in tickers_arr) {
                    if (tickers_arr[k] === get_data) continue;
                    while (true) {
                        var num = bigInt.randBetween(1, N-1);
                        if (private_ir.jacobi(num,N) === 1) {
                            if (private_ir.jacobi(num,n1) === 1 && private_ir.jacobi(num, n2) === 1) {
                                setplusqr[tickers_arr[k]] = num.toString(16);
                                break;
                            }
                            else {
                                if (numqnr.eq(0)) {
                                    numqnr = bigInt(num);
                                }
                            }
                        }
                    }
                }
                var y = setplusqr;
                if (numqnr.eq(0)) {
                    while (true) {
                        var num = bigInt.randBetween(1, N-1);
                        if (private_ir.jacobi(num,N) === 1) {
                            if (!(private_ir.jacobi(num,n1) === 1 && private_ir.jacobi(num,n2) === 1)) {
                                numqnr = bigInt(num);
                                break;
                            }
                        }
                    }
                }
                y[get_data] = numqnr.toString(16);
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.open(method, url, true);
                xmlHttp.onreadystatechange = function() {
                    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                        // Typical action to be performed when the document is ready:
                        var response_data = JSON.parse(this.responseText);
                        var data_tmp = "", count2 = 0, data_arr = new Array(), data_str = "";
                        for (i in response_data) {
                            var num_i = bigInt(response_data[i], 16);
                            if (private_ir.jacobi(num_i, n1) === 1 && private_ir.jacobi(num_i, n2) === 1) data_tmp += "0";
                            else data_tmp += "1";
                            count2 += 1;
                            if (count2 === 7) {
                                count2 = 0;
                                var char_tmp = String.fromCharCode(parseInt(data_tmp, 2));
                                if (char_tmp === '\0') break;
                                data_str += char_tmp;
                                data_tmp = "";
                            }
                        }
                        data_arr = JSON.parse(data_str)
                        retrieveDataFunction(data_str);
                    }
                }
                var sendStr = JSON.stringify({"number": N, "y": y});
                xmlHttp.send(sendStr);
            });
        });
    },
}
