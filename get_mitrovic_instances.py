import os
import sys
import requests

links = [
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_001.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_002.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_003.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_004.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_005.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_006.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_007.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_008.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_100_009.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_000.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_001.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_002.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_003.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_004.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_005.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_006.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_007.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_008.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_300_009.txt"
]

for link in links:
    result = requests.get(link)
    print(result.text)

    file_name = link.split("/")[-1]
    
    file_location = "./test_instances/input_files/Mitrovic-Minic/"
    if (len(sys.argv) > 1):
        file_location = sys.argv[1]

    with open(os.path.join(file_location, file_name), "w") as f:
        f.write(result.text)