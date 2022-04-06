import argparse
import os


def parse_command_line_arguments():
    """Manage the command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--ip",
        dest="host_ip",
        help="Server IP",
        action="store",
        default="127.0.0.1",
        type=str,
        required=False
    )

    parser.add_argument(
        "--port",
        dest="host_port",
        help="Server Port",
        action="store",
        default=6969,
        type=int,
        required=False
    )

    parser.add_argument(
        "--time-slice",
        dest="time_slice_size",
        help="Size of each time slice (in minutes).",
        action="store",
        default=600,
        type=int,
        required=False
    )

    parser.add_argument(
        "--horizon",
        dest="horizon",
        help="Planning horizon time (in minutes).",
        action="store",
        default=3000,
        type=int,
        required=False
    )

    parser.add_argument(
        "--is-test",
        dest="is_test",
        help="Will the server be used for tests? Needs the argument --test-instance-path if it is a test.",
        action="store_true",
        default=False,
        required=False
    )
    
    parser.add_argument(
        "--test-instance",
        dest="test_instance_path",
        help="path to test instance file. Only used when flag --is-test is active",
        action="store",
        type=str,
        default=None,
        required=False
    )
    
    args = parser.parse_args()

    arguments = vars(args)

    if (arguments["is_test"] and arguments["test_instance_path"] is None):
        raise Exception("A test needs a test instance")
    
    if (arguments["is_test"]):
        if (not os.path.exists(arguments["test_instance_path"])):
            raise Exception("Test instance does not exists")

    arguments["time_slice_size"] *= 60
    arguments["horizon"] *= 60

    return arguments