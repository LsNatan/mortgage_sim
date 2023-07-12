import json

import matplotlib.pyplot as plt


with open(r"C:\Users\dp26422\Desktop\inflation_finwiz.json", 'r') as json_reader:
    inflation_pred = json.load(json_reader)
    inflation_pred_values = [(point['x'],point['y']) for point in inflation_pred['data']]
with open(r"C:\Users\dp26422\Desktop\intereset_Prime_finwiz.json", 'r') as json_reader:
    prime_interest_pred = json.load(json_reader)
    prime_interest_pred_values = [(point['x'],point['y']) for point in prime_interest_pred['data']]


fig, ax = plt.subplots(1,2)


ax[0].plot(*zip(*inflation_pred_values))
ax[1].plot(*zip(*prime_interest_pred_values))
plt.show()


