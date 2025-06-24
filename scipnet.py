from blessed import Terminal
import requests
import re

base_url = "https://raw.githubusercontent.com/scp-data/scp-api/main/docs/data/scp/"
term = Terminal()

def successful_response(scpnum, response):
    print(term.yellow("Successfully retrieved SCP data"))
    response_json = response.json()
    scp = response_json.get(f"SCP-{scpnum}")
    print(term.white(scp.get("scp")))
    print(term.white(scp.get("raw_source")))


def normalize_scp_id(user_input):
    match = re.match(r'(?i)(?:scp[\s\-]*)?(\d+)', user_input.strip())
    if match:
        scp_number = match.group(1).zfill(3)  # Optional: pad with zeros (e.g. 5 -> 005)
        return scp_number
    else:
        return None  # or raise an error, depending on your use case


print(term.home + term.clear)
print(term.green("Welcome Researcher!"))
command = input("What scp would you like to access? ")

if re.match(r'(?i)(?:scp[\s\-]*)?(\d+)', command.strip()):
    scpnum = normalize_scp_id(command)
    scpnum_1 = scpnum[0]
    scpnum_2 = scpnum[1]

    match scpnum_1:
        case _ if scpnum_1 == "0" or len(scpnum) < 4:
            if scpnum == "001":
                print(term.red("Accessing SCP-001"))
            else:
                print(term.green("Accessing series 1"))
                response = requests.get(base_url + "items/content_series-1.json")
                if response.status_code == 200:
                    successful_response(scpnum, response)
                else:
                    print(term.red(f"Failed to fetch SCP"))

        case "1" | "2" | "3" | "4" | "5":
            series_num = str(int(scpnum_1) + 1)
            print(term.green("Accessing series " + series_num))
            response = requests.get(base_url + f"items/content_series-{series_num}.json")
            if response.status_code == 200:
                successful_response(scpnum, response)
            else:
                print(term.red(f"Failed to fetch SCP"))

        case "6" | "7" | "8" | "9":
            series_num = str(int(scpnum_1) + 1)
            print(term.green("Accessing series " + series_num))

            half_series_num = "0"
            if int(scpnum_2) > 5:
                half_series_num = "5"

            response = requests.get(base_url + f"items/content_series-{series_num}.{half_series_num}.json")
            if response.status_code == 200:
                successful_response(scpnum, response)
            else:
                print(term.red(f"Failed to fetch SCP"))

else:
    print(term.red("Invalid scp id"))



