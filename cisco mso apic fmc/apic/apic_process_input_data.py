"""Process input data that relates to APIC configurations"""
import json
from string import Template as StringTemplate


def get_known_facts(apic_name):
    """Get known facts from a JSON file if we have hardcoded attributes like
        Domain or virtual Port-Channels

    Args:
        apic_name: The name of the APIC to match against the JSON data file

    Returns:
        A dict containing static facts for the APIC
    """
    with open("apic_facts.json", "r") as factsfile:
        return json.load(factsfile)[apic_name]


def map_params(data):
    """Perform a key:value mapping for a given row of data in source file

    Args:
        data: a list representing columns of a given row in source file

    Returns:
        A dict with k:v mappings
    """
    # Concessions are made here due to the nature of the lab informing
    # this prototype python code
    # Key of "code" is used to represent identifying information for
    # the naming of the resource(s)
    # Assuming we have up to 2 leaf switches for a given L3Out
    # Assuming we may be configuring an SVI possibly, hence "sideAip", "sideBip"
    # Assuming we know what the int number is, in "#/#" without "eth" prefix
    # Not every key may have content, depending on the target String Template
    keys_map = {
        "fabric": "",
        "tenant": "",
        "code": "",
        "side": "",
        "encap_vlan": "",
        "node1id": "",
        "rtr1id": "",
        "node2id": "",
        "rtr2id": "",
        "sideAip": "",
        "sideBip": "",
        "primary_ip": "",
        "secondary_ip": "",
        "int_id": ""
    }
    for key in keys_map:
        keys_map[key] = data.next()  # data is a list derived from CSV/Excel
    return keys_map


def set_l3o_name(code=None, tenant=None, side=None, fabric=None, **kwargs):
    """In the Lab, this code is writing data to L3Outs, so we want to render
        the name here as defined via MSO script
        Args are defined as keyword args to receive in an expanded dict.
        **kwargs helps handle excess args

    Args:
        code: The identifying information for where an L3Out is dedicated for
        tenant: The name of the tenant in the APIC the L3Out is assigned to
        side: If we're doing something like Core/DMZ
            this would say "CORE" or "DMZ"
        fabric: The name of the APIC Fabric being touched. Assume multi-site,
            single-pod. Each site is a Fabric itself
            This is not network design advice, but only how it was done in the
            lab this code was written for

    Returns:
        A string that represents the L3Out name
    """
    return f"{code}_{tenant}_{f'{side}_' or ''}{fabric}_L3O"


def set_payload(side, params):
    """Populate a payload dict for a given L3Out

    Args:
        side: The side the L3Out is written for (CORE, DMZ, etc)
        params: The parameter mappings rendered by map_params()

    Returns:
        A dict for the payload
    """
    with open("apic_l3o_mo_template.json", "r") as l3o_templatef:
        # This loads in a specific template from a set of templates in a dict
        l3o_tmpl = StringTemplate(
            json.dumps(
                json.load(l3o_templatef)[f"{side}-l3o-template"]
            )
        )
    # This will work only if all the parameters in params exist in the template
    # Not written to safely handle dynamic templating right now
    l3o_tmpl = l3o_tmpl.substitute(**params)
    return json.loads(l3o_tmpl)


def render_input(apic_name):
    """Extract data from an input file that matches the expected configuration
        parameters needed for the lab

    Args:
        apic_name: The name of the APIC that the payload is being built for

    Yields:
        A tuple of the MO DN and the payload as a dict
    """
    apic_facts = get_known_facts(apic_name)
    with open("apic_lab_input_data.csv", "r") as inputf:
        _ = inputf.readline()  # skip the CSV headers row
        data = [_.replace("\n", "").split(",") for _ in inputf
                if apic_name in _]
    for row in data:
        params = map_params(row)
        l3o_name = set_l3o_name(**params)
        params.update(apic_facts)
        # Set DN for L3Out
        params["l3o_dn"] = f"uni/tn-{params['tenant']}/out-{l3o_name}"
        # Set EPG Name
        params["epg_name"] = f"{l3o_name[:-1]}EPG"

        # Perform a yield on the DN and payload back to caller
        yield params["l3o_dn"], set_payload(params["side"], params)
