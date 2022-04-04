"""APIC automated deployment testing"""
import json
import os
import urllib3
import requests
from apic_process_input_data import render_input

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# LAB IPs mapping
LAB_BASE = {
    "lab-apic": "https://{ip}/api"
}

# Name of the Fabric for an APIC, if needed for naming, etc
FABRIC_MAP = {
    "lab-apic": "FabricName"
}


def login(target):
    """Log into the APIC

    Args:
        target: The APIC (by name) to log into

    Returns:
        A requests Session object
    """
    uname, pword = os.getenv("CREDS").split(",")  # assuming creds are in ENV

    # Create the JSON content to send in Body
    body = json.dumps({
        "aaaUser": {
            "attributes": {
                "name": uname,
                "pwd": pword
            }
        }
    })

    session = requests.Session()
    resp = session.post(
        f"{LAB_BASE[target]}/aaaLogin.json",
        data=body,
        verify=False  # If we're hitting a self-signed APIC...
    )
    if not resp.ok:
        return None  # We can't return anything if we didn't log in successfully
    return session  # Return the session, not the resp for the session POST


def send_payload(session, base_url, mo_dn, payload, tenant=None):
    """Send a payload for a specified Managed Object DN

    Args:
        session: The requests session with valid auth
        base_url: The base IP URI string (from LAB_MAPPING)
        mo_dn: The Managed Object Distinguished Name for APIC
        payload: The payload to send, as a dict
        tenant: The name of the tenant we're touching

    Returns:
        A Requests response object
    """
    url = f"{base_url}/mo/{mo_dn}.json"
    # In this example, we're assuming that we're editing L3Outs in APIC
    # that were created via MSO
    if tenant == "lab-tenant":
        # This will set the URL to a specific l3o DN, even if it's
        # technically already done above
        url = f"{base_url}/mo/uni/tenant-{tenant}/out-{mo_dn}.json"
    return session.post(url, data=json.dumps(payload), verify=False)


def main():
    """Main

        This does the following steps:
         1. Log into APIC
         2. Run through source data file, yielding payload per row in source
         3. Send payload
    """
    for apic, base_uri in LAB_BASE.items():
        session = login(apic)
        if not session:
            print("Failed to log in")
            break
        for mo_dn, payload in render_input(FABRIC_MAP[apic]):
            if mo_dn:
                print(f"Sending payload for {mo_dn}\n{payload}")
                status = send_payload(session, base_uri,
                                      mo_dn, payload, "lab-tenant")
                if not status.ok:
                    print(f"Bad POST attempt for {mo_dn}")
                    print(status.text)
                    break


if __name__ == "__main__":
    main()
