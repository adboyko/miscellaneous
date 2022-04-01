"""A simple interface with Cisco MSO that logs in and makes API calls"""
import urllib3
import json
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from mso_process_input_data import render_input


# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Set mapping for the base URI of an MSO instance
# {ip} should represent the IP of an instance
INST_MAP = {"inst1": "https://{ip}/api/v1"}


def build_header(token):
    """Build a header that contains our Bearer token and other attribs

    Args:
        token: The Bearer token for our header

    Returns:
        A dict containing header info
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def login():
    """Log into MSO instance and get the bearer token

    Returns:
        A dict containing the Auth token and other header attribs
    """
    uname, pword = ("", "")  # Fill these in. Probably not here though
    body = {
        "domainId": "TACACS",  # Optional if using TACACS as auth provider
        "username": uname,
        "password": pword
    }
    resp = requests.post(
        f"{INST_MAP['inst1']}/auth/login",
        data=json.dumps(body),
        verify=False
    ).json()
    return build_header(resp["token"])


def make_payload(tmpl_name, component, op, val=None):
    """Compose a payload that is sent to MSO to perform an action 'op' on a
        template

    Args:
        tmpl_name: The name of the template in MSO being altered
        component: The name of the component in the template being altered
        op: The operation we're taking against that template/component
        val: The value being applied, if any (Delete doesn't require input)

    Returns:
        A dict containing the payload for the specified template/component/op
    """
    payload = {
        "op": op,
        "path": f"/templates/{tmpl_name}/{component}/-"
    }
    if val:
        payload["value"] = val
    return payload


def make_call(method, endpoint, headers=None, params=None, payload=None):
    """Send a requests call to MSO

    Args:
        method: The HTTP method
        endpoint: The endpoint in MSO's API to hit
        headers: Our headers, if any
        params: Any specific parameters for an endpoint
            (if an endpoint is deeper than one step.. needs refinement here)
        payload: The payload to send to the endpoint

    Returns:
        A requests Response object
    """
    if params:
        # Prefix params with a '/'
        params = f"/{params}"
    # Set URL to call
    url = f"{INST_MAP['inst1']}/{endpoint}{(params or '')}"
    # Set up kwargs for call
    # Do the specified method
    resp = requests.request(
        method.upper(),
        url,
        data=json.dumps(payload or {}),
        headers=(headers or {}),
        verify=False
    )
    return resp


def build_connection(schema, data):
    """Unpack a dataset and add it into the Schema obtained from MSO

    Args:
        schema: A dict that represents a schema from MSO
        data: Data that represents alterations to a schema template in MSO

    Returns:
        None -- pass-by-argument is used to alter 'schema' var
    """
    # This assumes only 1 template exists for the schema
    template = schema["templates"][0]["name"]
    # Set the reference base string needed to render resource references
    ref_base = f"/schemas/{schema['id']}/templates/{template}"

    # In this example code, we're creating a VRF with associated L3Out and eEPG
    # A single VRF may have multiple L3Outs and EPGs, so we loop to create them

    # Set the VRF reference
    vrf_ref = f"{ref_base}/vrfs/{data['vrf']['name']}"
    if not any(data["vrf"]["name"] == _["name"]
               for _ in schema["templates"][0]["vrfs"]):
        # If the VRF we're creating doesn't exist, put it into the template
        schema["templates"][0]["vrfs"].append(data["vrf"])
    # Remove the VRF record from input data so we can do a loop on remainder
    del data["vrf"]
    # Loop through the remainder of data
    for resource in data.values():
        # Update the resource dict with the refs we rendered above
        resource["l3o"]["vrfRef"] = vrf_ref
        resource["eepg"]["vrfRef"] = vrf_ref
        resource["eepg"]["l3outRef"] = f"{ref_base}/l3outs/" \
                                       f"{resource['l3o']['name']}"
        # If you have any contracts, patch them in here
        # resource["eepg"]["contractRelationships"][0]["contractRef"] = ref

        # Construct the payload for the template items
        if not any(resource["l3o"]["name"] == _["name"]
                   for _ in schema["templates"][0]["intersiteL3outs"]):
            # If the L3Out doesn't already exist, add it
            schema["templates"][0]["intersiteL3outs"].append(resource["l3o"])
        if not any(resource["eepg"]["name"] == _["name"]
                   for _ in schema["templates"][0]["externalEpgs"]):
            # If the L3Out doesn't already exist, add it
            schema["templates"][0]["externalEpgs"].append(resource["eepg"])


def main():
    """Main"""
    # This could be a SSoT file, etc.. representing schemas of interest
    schemas_of_interest = ["SomeSchemaName"]

    # Log in
    mso_auth = login()

    # Retrieve existing Schemas from MSO
    schemas = make_call(
        "get",
        "schemas",
        mso_auth,
        params="list-identity"
    ).json()

    # Extract any specific schemas being targetted
    target_schemas = {}
    for schema in schemas["schemas"]:
        if schema["displayName"] in schemas_of_interest:
            # If a schema we want is found, get the full schema and stash it
            # This may be unnecessary but Cisco APIs are unpredictable and may
            # return a cropped view of each schema instead of full views
            target_schemas[schema["displayName"]] = make_call(
                "get",
                "schemas",
                mso_auth,
                params=schema["id"]
            ).json()

    # Plug updates from input data into the Schema
    for config in render_input():
        mso_site, confdata = config
        if mso_site in target_schemas:
            build_connection(target_schemas[mso_site], confdata)

    # Finally, call the MSO API to patch in the schema with revisions
    for schema in target_schemas.values():
        resp = make_call(
            "put",
            "schemas",
            mso_auth,
            params=schema["id"],
            payload=schema
        )
        if resp.ok:
            # If the update was successful, tell MSO to deploy to APIC
            resp = make_call(
                "get",
                "execute",
                mso_auth,
                params=f"schema/{schema['id']}/"
                       f"template/{schema['templates'][0]['name']}"
            )
            if not resp.ok:
                print("Uh oh.. Deploy attempt failed!")
                sys.exit(1)


if __name__ == "__main__":
    main()
