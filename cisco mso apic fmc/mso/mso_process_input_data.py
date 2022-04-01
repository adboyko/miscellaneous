"""This contains supporting work to process input data from a CSV file"""


def make_l3o_params(prefix, description=''):
    """Create L3Out parameters for the payload

    Args:
        prefix: The prefix name of an L3Out to follow naming convention
        description: The description to apply to the L3Out

    Returns:
        A dict of parameters
    """
    name = f"{prefix}_L3O"
    return {
        "displayName": name,
        "name": name,
        "description": description
    }


def make_eepg_params(prefix):
    """Create the External EPG parameters for the payload

    Args:
        prefix: The prefix name of an External EPG to follow naming convention

    Returns:
        A dict of parameters
    """
    name = f"{prefix}_L3EXTEPG"
    return {
        "displayName": name,
        "name": name,
        "subnets": [
            {
                "ip": "0.0.0.0/0",  # Define EPG IP for subnets here
                "scope": [  # Define Route Control Import/Export flags here
                    "export-rtctrl",
                    "import-rtctrl"
                ],
                "aggregate": []  # Define Aggregate Route Control flags here
            },
        ],
        "contractRelationships": [
            {
                "relationshipType": "consumer",  # Define the contract rel here
                "contractRef": ""  # Fill in later if defined in input data
            }
        ]
    }


def render_input():
    """A generator that produces a payload extracted from input data

    Returns:
        A dict containing all data needed to establish a Schema update
    """
    # Open CSV and load into memory
    with open("input-data-file.csv", "r") as indata:
        # Skips the first row (assumes headers), and makes a list of lists
        indata = [_.replace("\n", "").split(',') for _ in indata[1:]]
    for row in indata:
        # Prefix for resource name assuming data in input needs to be leveraged
        prefix = f"MSO_{row[0]}_{row[1]}_{row[2]}"
        # Set the data. Do some code to handle X number of conngroups per VRF
        data = {
            "vrf": {
                "displayName": f"{row[3]}_VRF",
                "name": f"{row[3]}_VRF"
            },
            "conngroup1": {
                "l3o": make_l3o_params(prefix, description="Some Description"),
                "eepg": make_eepg_params(prefix)
            },
            "conngroupX": {
                "l3o": make_l3o_params(prefix, description="Some Description"),
                "eepg": make_eepg_params(prefix)
            }
        }
        yield row[0], data  # Assume row[0] in CSV == the target MSO APIC site
