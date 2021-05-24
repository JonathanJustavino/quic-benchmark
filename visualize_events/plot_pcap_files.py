import matplotlib.pyplot as plt
from plot_timeplan import survey
from pcap_loader import get_avg_timestamp_duration


category_names = ['QUIC communication duration', 'TCP+TLS communication duration']
results = get_avg_timestamp_duration()
print(results)

survey(results, category_names, split_threshold=2000, multiple_graphs=True ,pcap=True)
plt.suptitle("Length of communication according to network packets captured")
plt.show()