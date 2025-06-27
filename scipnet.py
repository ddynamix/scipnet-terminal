from blessed import Terminal
import re
import scp_formatter
import db_connector


USING_LOCAL_DB = True  # Change this to true to use up-to-date online repo

db = db_connector.DBConnector(USING_LOCAL_DB)
term = Terminal()


def successful_response(scpnum, series):    
    print(term.yellow("Successfully retrieved SCP data"))
    
    scp = series.get(f"SCP-{scpnum}").get("raw_source")
    metadata = db.get_metadata().get(f"SCP-{scpnum}")

    print(term.home + term.clear)
    scp_formatter.formatted_print(metadata, scp)
    

def normalize_scp_id(user_input):
    match = re.match(r'(?i)(?:scp[\s\-]*)?(\d+)', user_input.strip())
    if match:
        scp_number = match.group(1).zfill(3)  # pad with zeros (e.g. 5 -> 005)
        return scp_number
    else:
        return None


if __name__ == "__main__":
    """
    Program entry point
    """
    print(term.home + term.clear)

    # Print scp logo
    f = open("scp_logo_small.txt", "r")
    logo = f.read()
    logo_lines = logo.split("\n")
    for line in logo_lines:
        line = line.strip()
        print(term.center(line))
    f.close()

    # Print welcome text
    f = open("welcome_text.txt", "r")
    logo = f.read()
    logo_lines = logo.split("\n")
    for line in logo_lines:
        print(term.center(term.white(line), fillchar=" "))
    f.close()

    print(term.green("> Welcome Researcher!"))
    command = input(f"> {term.blink}What scp would you like to access? {term.normal}")

    if re.match(r'(?i)(?:scp[\s\-]*)?(\d+)', command.strip()):
        scpnum = normalize_scp_id(command)
        scpnum_1 = scpnum[0]
        scpnum_2 = scpnum[1]

        match scpnum_1:
            case _ if scpnum_1 == "0" or len(scpnum) < 4:
                if scpnum == "001":
                    # TODO
                    print(term.red("Accessing SCP-001"))
                else:
                    print(term.green("Accessing series 1"))
                    series = db.get_content_series("1")
                    successful_response(scpnum, series)


            case "1" | "2" | "3" | "4" | "5":
                series_num = str(int(scpnum_1) + 1)
                print(term.green("Accessing series " + series_num))
                series = db.get_content_series(series_num)
                successful_response(scpnum, series)

            case "6" | "7" | "8" | "9":
                series_num = str(int(scpnum_1) + 1)
                print(term.green("Accessing series " + series_num))

                half_series_num = "0"
                if int(scpnum_2) > 5:
                    half_series_num = "5"

                series = db.get_content_series(series_num + "." + half_series_num)
                successful_response(scpnum, series)

    else:
        print(term.red("Invalid scp id"))
