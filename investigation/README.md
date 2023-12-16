This is a scratch directory used to gather files during active investigations.

Examples:

I frequently make use of the "analyze" script to extract packets withtin a date range from my repository, piping the output through tcpdump with desired filters, output into the pcap directory.

I may run a for loop against a specific date to grab cowrie logs or other json logs, which are copied to respective subdirectories.

The zeek directory is for ad-hoc analysis of .pcap files and searches with zeek-cut

investigation/
├── cowrie
├── downloads
├── logs
├── pcap
└── zeek