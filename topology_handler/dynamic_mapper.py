import pandas as pd
import subprocess
import os
import threading

# Define the output file name for Hubble data
FILE_NAME = "hubble_out.txt"

# Define IP addresses for various services
ip_dict = {'adservice': '10.0.1.205', 'cartservice': '10.0.1.247', 'checkoutservice': '10.0.0.51',
           'currencyservice': '10.0.1.22', 'emailservice': '10.0.0.55', 'frontend': '10.0.0.208',
           'paymentservice': '10.0.1.253', 'productcatalogservice': '10.0.0.155', 'recommendationservice': '10.0.1.99',
           'redis-cart': '10.0.0.31', 'shippingservice': '10.0.1.36'}


def run_shell_commands():
    """
    Execute shell commands to download stable.txt.
    """
    try:
        subprocess.run(["/usr/bin/curl", "-LO", "-o", "stable.txt",
                        "https://raw.githubusercontent.com/cilium/hubble/master/stable.txt"], check=True)

        print("Shell commands executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing shell commands:", e)


def run_kubectl_port_forward():
    """
    Run kubectl port-forward command to expose Hubble relay service.
    Executes the kubectl port-forward command to forward a specific service port.
    This function handles possible subprocess-related exceptions and ensures appropriate error handling during command execution.

    Raises:
        subprocess.TimeoutExpired: If the subprocess execution exceeds the allowed time.
        subprocess.CalledProcessError: If the command results in a non-zero exit status.

    """
    process = None  # Initialize process outside the try block
    try:
        command = ['sudo', '/usr/bin/kubectl', 'port-forward', '-n', 'kube-system', 'svc/hubble-relay', '4245:80']
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if process.returncode == 0:
            print("kubectl port-forward command executed successfully.")
        else:
            print(f"Command execution failed with return code {process.returncode}.")
    except subprocess.TimeoutExpired:
        print("Process timed out. Terminating...")
        if process:
            process.terminate()  # Make sure 'process' is not None before terminating
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with return code {e.returncode}: {e.output}")
        if "An existing connection was forcibly closed by the remote host" in e.output:
            print("An existing connection was forcibly closed by the remote host. Please check your network.")


def run_hubble_observe(out_hubble):
    """
    Run the `hubble observe` command to capture network data and save the output to a specified file.

    Arguments:
        out_hubble (str): Path to the file where the output of `hubble observe` should be saved.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    try:
        subprocess.run([f'hubble observe > {out_hubble}'], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with return code {e.returncode}: {e.output}")


def remove_substring(string, start_char, end_char):
    """
    Removes a substring from the input string that starts and ends with specified characters.
    If both the start and end characters are found, and the starting character precedes the ending character,
    the substring is replaced with a single space.

    Parameters:
        string (str): The input string from which the substring will be removed.
        start_char (str): The character that marks the beginning of the substring.
        end_char (str): The character that marks the end of the substring.

    Returns:
        str: The modified string with the specified substring replaced by a space.
    """
    start_index = string.find(start_char)
    end_index = string.find(end_char, start_index + 1)  # Find the next occurrence after start_index
    if start_index != -1 and end_index != -1 and start_index < end_index:
        substring = string[start_index:end_index + 1]
        string = string.replace(substring, ' ')

    return string


def protocol_adding(my_list):
    """
    Add protocol type (TCP/UDP) to each element of the list.

    Args:
        my_list (list of str): List of strings to be modified.

    Returns:
        list of str: Modified list with appropriate prefixes added to strings containing 'TCP' or 'UDP'.
    """
    for i, my_string in enumerate(my_list):
        if 'TCP' in my_string:
            my_list[i] = 'TCP ' + my_string
        elif 'UDP' in my_string:
            my_list[i] = 'UDP ' + my_string

    return my_list


def add_frontend_row(grouped_lists):
    """
    Add a new row for 'frontend' with specified values.

    Arguments:
        grouped_lists (DataFrame): The existing DataFrame to which the frontend
                                   pod row will be added.

    Returns:
        DataFrame: The updated DataFrame containing the new frontend pod row.

    """
    frontend_row = pd.DataFrame({'Pod-ID': ['frontend'],
                                 'IP': [ip_dict['frontend']],
                                 'Pod-Inbound-List': [['Internet']],
                                 'Protocol': ['TCP'],
                                 'Port': [8080]})
    grouped_lists = pd.concat([grouped_lists, frontend_row], ignore_index=True)

    return grouped_lists


def process_list(listed_data, namespace="default"):
    """
    Process a list of data to extract relevant information.

    Args:
        listed_data (list of str): A list of strings to be processed.
        namespace (str): A namespace string to filter the input list. Defaults to "default".

    Returns:
        list of list of str: A final filtered and processed list where each element is a sublist of exactly five strings.

    """
    new_list = [x for x in listed_data if namespace in x]
    a = [item.split('/', 1)[1] for item in new_list]
    b = [remove_substring(item, '-', ':') for item in a]
    c = [remove_substring(item, ' (', '/') for item in b]
    d = [remove_substring(item, '-', ':') for item in c]
    protocol_adding(d)
    e = [item.split(' (', 1)[0] for item in d]
    filtered_list = [item for item in e if sum(key in item for key in ip_dict) == 2]  # assuming ip_dict is defined
    f = [*set(filtered_list)]
    final_list = [item.split() for item in f if len(item.split()) == 5]

    return final_list


def process_data(csv_file_path, out_hubble):
    """
    Process the data extracted from Hubble and create a CSV file.

    Args:
        csv_file_path (str): The path to save the generated CSV file.
        out_hubble (str): The path to the input text file containing the data to be processed.

    Returns:
        pandas.DataFrame: A DataFrame containing columns ['Pod-ID', 'IP', 'Pod-Inbound-List', 'Protocol', 'Port'].

    """
    # turn the text file into a list
    with open(out_hubble, 'r') as f:
        lines = f.readlines()

    # remove the irrelevant list's items
    final_list = process_list(lines)
    if not final_list:
        # If final_list is empty, create an empty DataFrame
        grouped_lists = pd.DataFrame(columns=['Pod-ID', 'IP', 'Pod-Inbound-List', 'Protocol', 'Port'])

    else:
        # creating a dataframe from the list
        process_file_df = pd.DataFrame(final_list,
                                       columns=['Protocol', 'Source Name', 'Source Port', 'Target Name', 'Target Port'])

        # creating the right output format
        grouped_lists = process_file_df.groupby(['Target Name', 'Target Port', 'Protocol']).apply(
            lambda group: [(row[0], int(row[1]), row[2]) for row in
                           group[['Source Name', 'Source Port', 'Protocol']].values]
        ).reset_index()
        grouped_lists = grouped_lists.rename(columns={0: 'Pod-Inbound-List'}).reset_index(drop=True)
        grouped_lists['IP'] = grouped_lists['Target Name'].map(ip_dict)
        grouped_lists = grouped_lists.rename(columns={'Target Name': 'Pod-ID', 'Target Port': 'Port'})
        grouped_lists = grouped_lists[['Pod-ID', 'IP', 'Pod-Inbound-List', 'Protocol', 'Port']]

        # Convert the 'Pod-Inbound-List' column to a string representation of a list of tuples
        grouped_lists['Pod-Inbound-List'] = grouped_lists['Pod-Inbound-List'].apply(str)

    grouped_lists.to_csv(csv_file_path, index=False)

    return grouped_lists


def run_full_script(dir_path, out_hubble):
    """
    Run the full script including shell commands, port forwarding, Hubble observe, and data processing.

    Args:
        dir_path (str): The directory path where intermediate and final output files will be saved.
        out_hubble (str): File path or identifier for the output data to be processed.

    Raises:
        subprocess.CalledProcessError: If the external process executed within run_hubble_observe fails,
                                        this exception will be raised with the corresponding return code and output.
    """
    run_shell_commands()
    kubectl_port_forward_thread = threading.Thread(target=run_kubectl_port_forward)
    kubectl_port_forward_thread.start()

    os.makedirs(dir_path, exist_ok=True)
    hubble_out_path = os.path.join(dir_path, FILE_NAME)
    if not os.path.exists(hubble_out_path):
        with open(hubble_out_path, 'x'):
            pass
    try:
        run_hubble_observe(out_hubble)
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with return code {e.returncode}: {e.output}")

    csv_file_name = 'sub_graph_topology.csv'
    csv_file_path = os.path.join(dir_path, csv_file_name)
    processed_data = process_data(csv_file_path, out_hubble)
    processed_data = add_frontend_row(processed_data)
    processed_data.to_csv(csv_file_path, index=False)


if __name__ == "__main__":
    OUT_HUBBLE = os.path.join("/home/ubuntu/attack-graphs-/topology_handler", 'hubble_out.txt')
    run_full_script("/home/ubuntu/attack-graphs-/topology_handler", OUT_HUBBLE)
