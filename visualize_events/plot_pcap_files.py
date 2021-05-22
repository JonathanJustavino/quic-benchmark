import matplotlib.pyplot as plt
from plot_timeplan import survey
from pcap_loader import get_avg_timestamp_duration


category_names = ['Pcap communication']
results = get_avg_timestamp_duration()
print(results)

survey(results, category_names, split_threshold=2000, pcap=True)
plt.show()