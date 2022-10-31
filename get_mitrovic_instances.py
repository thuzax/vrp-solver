import os
import sys
import requests

links = [
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_000.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_001.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_002.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_003.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_004.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_005.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_006.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_007.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_008.txt",
    "http://www.sfu.ca/~snezanam/personal/PDPTW/TestInstances/Rnd6_1h-2h-4h-6h-7h-Req/Rnd6_10h_500_009.txt"
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