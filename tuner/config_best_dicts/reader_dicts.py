def reader_json_PDPTW():
    data = {
        "input_path" : "",
        "input_name" : "",
        "input_type" : "json"
    }
    return data

def reader_json_DPDPTW():
    data = {
        "input_path" : "",
        "input_name" : "",
        "input_type" : "json"
    }
    return data

def reader_json_DPDPTWLF():
    data = {
        "input_path" : "",
        "input_name" : "",
        "input_type" : "json"
    }
    return data

def reader_json_DPDPTWLHF():
    data = {
        "input_path" : "",
        "input_name" : "",
        "input_type" : "json"
    }
    return data

def reader_data(params, problem):
    if (problem == "PDPTW"):
        reader_classes_data = {
            "ReaderJsonPDPTW" : reader_json_PDPTW(),
        }
    if (problem == "DPDPTW"):
        reader_classes_data = {
            "ReaderJsonDPDPTW" : reader_json_DPDPTW(),
        }
    if (problem == "DPDPTWLF-R" or problem == "DPDPTWNoC-D"):
        reader_classes_data = {
            "ReaderJsonDPDPTWLimitedFleet" : (
                reader_json_DPDPTWLF()
            ),
        }
    if (problem == "DPDPTWLHF-R"):
        reader_classes_data = {
            "ReaderJsonDPDPTWLimitedHeterogeneousFleet" : (
                reader_json_DPDPTWLHF()
            )
        }
    
    return reader_classes_data