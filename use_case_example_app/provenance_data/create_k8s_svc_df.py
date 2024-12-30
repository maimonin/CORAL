import json
import pandas as pd


# How to create kubectl_svc.json file --> see provenance_data_README.md

def create_kubectl_svc_df(kubectl_svc):
    """
    Create a dataframe consisting of services names and ports from kubectl_svc.json file

    :param: kubectl_svc: Path to kubectl_svc.json file

    :return: svc_df: Dataframe consisting of services names and ports from kubectl_svc.json file
    """
    # Load kubectl_svc.json file
    with open(kubectl_svc, 'r') as json_file:
        svc_data = json.load(json_file)

    # Create a dataframe consisting of services names and ports from kubectl_svc.json file
    svc_df = pd.DataFrame(columns=['service_name', 'port'])
    for item in svc_data['items']:
        svc_name = item['metadata']['name']
        for p in item['spec']['ports']:
            # port_name = item['spec']['ports'][0]['name']
            port_num = item['spec']['ports'][0]['port']
            # Add all of the above variables to the dataframe using pd.concat
            # svc_df = pd.concat([svc_df, pd.DataFrame([[svc_name, port_name, port_num]], columns=['service_name', 'port_name', 'port'])])
            svc_df = pd.concat([svc_df, pd.DataFrame([[svc_name, port_num]], columns=['service_name', 'port'])],
                               ignore_index=True)

    return svc_df


def create_svc_values_set(svc_df):
    """
    Extracts unique values from columns of a given DataFrame and modifies them for specific needs.

    :param: svc_df (pd.DataFrame): The DataFrame containing columns with values to extract and
        process.

    :return: set: A set of unique string values derived from the DataFrame's columns with
            "service" substring adjustments.
    """
    # Extract all values from 'svc_df' columns and convert them to a set for efficient lookup
    svc_values = set()
    for column in svc_df.columns:
        svc_values.update(svc_df[column].astype(str))

    # Remove the substring "service" from values in svc_values and add it as another item instead
    svc_values = set([value.replace('service', '') for value in svc_values])
    svc_values.add('service')

    return svc_values


if __name__ == "__main__":
    print(create_kubectl_svc_df('../provenance_data/services_data.json'))
    print(create_svc_values_set(create_kubectl_svc_df('../provenance_data/services_data.json')))
