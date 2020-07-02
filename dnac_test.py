import requests
import base64


def main():
    dnac_url = "https://sandboxdnac2.cisco.com"
    username = "dnacdev"
    password = "D3v93T@wK!"
    bytes_u_p = (username + ":" + password).encode("utf-8")
    print(base64.standard_b64encode(bytes_u_p))
    print(base64.urlsafe_b64encode(bytes_u_p).decode("utf-8"))
    token = requests.post(
        f'{dnac_url}/api/system/v1/auth/token',
        headers={'Authorization': f'Basic {base64.urlsafe_b64encode(bytes_u_p).decode("utf-8")}'}
    )
    print(token.json())
    print(base64.standard_b64decode('ZG5hY2RldjpEM3Y5M1RAd0sh'))
    return


if __name__ == '__main__':
    main()
