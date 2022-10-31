
def insertion_operator_pdptw():
    insert_data = {
    }

    return insert_data

def insertion_operator_dpdptw():
    insert_data = {
    }

    return insert_data

def insertion_operator_dpdptw_no_cap():
    insert_data = {
    }

    return insert_data


def insertion_operator_data(params, problem):
    if (problem == "PDPTW"):
        insert_data = {
            "InsertionOperatorPDPTW" : insertion_operator_pdptw()
        }
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R" 
        or problem == "DPDPTWLHF-R"
    ):
        insert_data = {
            "InsertionOperatorDPDPTW" : insertion_operator_dpdptw()
        }

    if (problem == "DPDPTWNoC-D"):
        insert_data = {
            "InsertionOperatorDPDPTWNoCap" : insertion_operator_dpdptw_no_cap()
        }


    return insert_data
