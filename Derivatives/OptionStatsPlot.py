import matplotlib.pyplot as plt

def plotOptionStats(stock_list, pv_list, delta_list, vega_list):
    plt.figure(figsize=(9, 7))
    sub1 = plt.subplot(311)
    plt.plot(stock_list, pv_list, 'ro', label='present value')
    plt.plot(stock_list, pv_list, 'b')
    plt.grid(True);
    plt.legend(loc=0)
    plt.setp(sub1.get_xticklabels(), visible=False)
    sub2 = plt.subplot(312)
    plt.plot(stock_list, delta_list, 'go', label='Delta')
    plt.plot(stock_list, delta_list, 'b')
    plt.grid(True);
    plt.legend(loc=0)
    plt.ylim(min(delta_list) - 0.1, max(delta_list) + 0.1)
    plt.setp(sub2.get_xticklabels(), visible=False)
    sub3 = plt.subplot(313)
    plt.plot(stock_list, vega_list, 'yo', label='Vega')
    plt.plot(stock_list, vega_list, 'b')
    plt.xlabel('initial value of underlying')
    plt.grid(True)
    plt.legend(loc=0)
    plt.show()