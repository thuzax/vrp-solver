
def removal_operator_pdptw():
    remov_data = {
    }

    return remov_data


def removal_operator_dpdptw():
    remov_data = {
    }

    return remov_data


def removal_operator_data(params, problem):
    if (problem == "PDPTW"):
        remov_data = {
            "RemovalOperatorPDPTW" : removal_operator_pdptw()
        }
    if (problem == "DPDPTW" or problem == "DPDPTWLF-R" or problem == "DPDPTWLHF-R"):
        remov_data = {
            "RemovalOperatorDPDPTW" : removal_operator_dpdptw()
        }

    return remov_data
