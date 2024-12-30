import sys
import pandas as pd
import json


def load_json_data(file_path):
    """
    Reads and converts a JSON file into a Python data structure.

    :param file_path: str: The path to the JSON file to be read and parsed.

    :return: Any: The Python data structure resulting from parsing the input JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def process_annotations(df, annotations_col='annotations'):
    """
    Processes annotations in a provenance DataFrame by converting dictionaries in the specified
    annotations column into separate columns, then drops the original annotations' column.

    :param df: pandas DataFrame containing the annotations column
    :param annotations_col: string name of the column with dictionary data to expand

    :return: DataFrame with expanded annotation data
    """
    # Check if the annotations column exists to prevent errors
    if annotations_col in df.columns:
        annotations_df = pd.DataFrame(df[annotations_col].tolist())
        df = pd.concat([df, annotations_df], axis=1).drop(annotations_col, axis=1)
    return df


def create_provenance_dataframes(provenance_data_loaded):
    """
    Create dataframes for each provenance graph components from raw provenance data in JSON format.

    :param provenance_data_loaded: dict: Raw provenance data in JSON format

    :return: 3 DataFrames: Dataframe for each provenance graph components:
        1. vertices_process_df: Dataframe for vertices of type 'Process'
        2. vertices_artifacts_df: Dataframe for vertices of type 'Artifact'
        3. edges_data_df: Dataframe for all edges
    """
    # Separate edges and vertices data
    edges_data_list = []
    vertices_process = []
    vertices_artifacts = []

    for item in provenance_data_loaded:
        if 'type' in item:
            # Separate vertices to dataframes according to their type - 'Process' or 'Artifact'
            if item['type'] == 'Process':
                vertices_process.append(item)
            elif item['type'] == 'Artifact':
                vertices_artifacts.append(item)
            else:
                edges_data_list.append(item)

    # Load provenance data into DataFrames
    process_df = pd.DataFrame(vertices_process)
    artifact_df = pd.DataFrame(vertices_artifacts)
    edges_df = pd.DataFrame(edges_data_list)

    # Apply the function to process annotations in each DataFrame
    process_df = process_annotations(process_df)
    artifact_df = process_annotations(artifact_df)
    edges_df = process_annotations(edges_df)

    return process_df, artifact_df, edges_df


def create_service_map(svc_data='services_data.json'):
    """
    Constructs a mapping of services to their respective ports from a JSON input.

    :param svc_data: str: The path to the JSON file containing service data. Defaults to 'services_data.json'.

    :return: dict: A dictionary mapping each service name (adjusted to exclude the string 'service') to a list of its ports.
    """
    with open(svc_data, 'r') as json_file:
        svc_data = json.load(json_file)

    service_map = {}
    for item in svc_data['items']:
        svc_name_value = item['metadata']['name'].replace('service', '')
        service_map[svc_name_value] = [p['port'] for p in item['spec']['ports']]

    # with open('service_map.json', 'w') as f:
    #     json.dump(service_map, f)
    return service_map


def create_reverse_lookup_service_map(service_map):
    """
    Creates a reverse lookup service map from the given service map, where each port and service name points directly to the service name.

    :param service_map: dict: Dictionary where keys are service name values (str) and values are lists of ports (list[int]).

    :return: dict: A dictionary where keys are service name values (str) and ports  (str) from the input service map,
                    and values are the corresponding  fully qualified service names (str).
    """
    reverse_lookup = {}
    for service_name_value, ports in service_map.items():
        service_name = service_name_value + "service"
        reverse_lookup[service_name_value] = service_name  # Map service name value to the service name
        for port in ports:
            reverse_lookup[str(port)] = service_name  # Map each port to the service name
    return reverse_lookup


def add_matching_services_to_vertices_df(vertices_df, filter_cols, service_map):
    """
    Create a new DataFrame with rows from vertices_df that contain any service_map value in filter_cols.
    
    :param vertices_df: pd.DataFrame: DataFrame with vertices data
    :param filter_cols: list: List of columns to filter the vertex_df
    :param service_map: dict: Dictionary with service names as keys and port numbers as values

    :return: pd.DataFrame: DataFrame with rows from vertices_df that contain any service_map value in filter_cols
    """
    # Creating a set from both keys and values in the dictionary
    all_service_values = set(service_map.keys())
    all_service_values.update(port for ports in service_map.values() for port in ports)

    # Create a boolean mask to filter vertex_df rows only by the filter_cols columns list
    def is_service_value_present(row):  # Helper function to check if any value in the row matches a service value
        return any(str(cell_value) in all_service_values for cell_value in row if pd.notna(cell_value))

    # Apply the function across the specified filter columns
    svc_mask = vertices_df[filter_cols].apply(is_service_value_present, axis=1)
    # Use the mask to create a new DataFrame with matching rows
    vertices_df_matching_services = vertices_df[svc_mask].copy()

    # Create a reverse lookup map for fast service name retrieval
    reverse_lookup_map = create_reverse_lookup_service_map(service_map)

    def get_service_name_from_map(vertex_row):  # Helper function to retrieve service name based on reverse lookup map
        for value in vertex_row:
            value_str = str(value)
            # Check for substring matches within the reverse lookup map keys
            for key, service_name in reverse_lookup_map.items():
                if key in value_str:
                    return service_name
        return ".No app/k8s service found"

    # Apply the function to each row in specified filter columns and create a new 'svc' column
    vertices_df['svc'] = vertices_df[filter_cols].apply(get_service_name_from_map, axis=1)

    if filter_cols == ['exe', 'name', 'cwd', 'command line']:  # Process vertices
        # Update dataframe without the rows with the value '.No app/k8s service found' in the 'svc' column
        vertices_df_matching_services = vertices_df_matching_services[
            vertices_df_matching_services['svc'] != '.No app/k8s service found']

    return vertices_df_matching_services


def complete_artifact_df(artifact_df, process_df):
    """
    Add to artifact_df rows from artifact_df that contain values in 'tgid' column that are also in process_df 'pid' column.

    :param artifact_df: pd.DataFrame: DataFrame with Artifact vertices data
    :param process_df: pd.DataFrame: DataFrame with Process vertices data

    :return: pd.DataFrame: DataFrame with new rows added
    """
    tgid_artifact_df = pd.concat([artifact_df, artifact_df[artifact_df['tgid'].isin(process_df['pid'])]])
    # Create a dictionary to map 'pid' values to 'svc' values in app_process_df
    pid_to_svc_dict = process_df.set_index('pid')['svc'].to_dict()
    # Add to svc column of the new rows added the value from the svc column of the corresponding row in app_process_df
    tgid_artifact_df['svc'] = tgid_artifact_df['svc'].fillna(tgid_artifact_df['tgid'].map(pid_to_svc_dict))
    return tgid_artifact_df


def create_edges_df(edges_df, process_df, artifact_df):
    """
    Create a new DataFrame with rows from edges_df that contain values in 'from' or 'to' columns that are also in
    process_df 'id' column or artifact_df 'id' column.

    :param edges_df: Dataframe of all edges
    :param process_df: pd.DataFrame: DataFrame with Process vertices data
    :param artifact_df: pd.DataFrame: DataFrame with Artifact vertices data

    :return: pd.DataFrame: new filtered edges DataFrame
    """
    # Create sets of unique IDs from app_process_df and app_artifact_df
    process_ids = set(process_df['id'])
    artifact_ids = set(artifact_df['id'])

    # Filter edges_df based on whether 'from' or 'to' vertices are in the sets of IDs
    edges_df = edges_df[edges_df['from'].isin(process_ids) | edges_df['to'].isin(process_df) |
                        edges_df['from'].isin(artifact_ids) | edges_df['to'].isin(artifact_ids)]

    return edges_df


def main(path_to_provenance_data, path_to_services_data):
    """
    Main function to process provenance and services data, filter and integrate them, and then save the processed data to CSV files.

    Parameters:
        path_to_provenance_data: str
            The path to a JSON file containing provenance data.
        path_to_services_data: str
            The path to a file containing services data.

    Returns:
        None
    """
    provenance_data = load_json_data(path_to_provenance_data)

    process_df, artifact_df, edges_df = create_provenance_dataframes(provenance_data)

    service_map = create_service_map(path_to_services_data)

    process_filter_cols = ['exe', 'name', 'cwd', 'command line']
    process_with_services_df = add_matching_services_to_vertices_df(process_df, process_filter_cols, service_map)

    artifact_filter_cols = ['path', 'local address', 'remote port', 'protocol', 'remote address', 'local port']
    artifact_with_services_df = add_matching_services_to_vertices_df(artifact_df, artifact_filter_cols, service_map)
    artifact_with_services_df = complete_artifact_df(artifact_with_services_df, process_with_services_df)

    filtered_edges_df = create_edges_df(edges_df, process_with_services_df, artifact_with_services_df)

    process_with_services_df.to_csv(f'provenance_data_processes_with_services.csv')
    artifact_with_services_df.to_csv(f'provenance_data_artifacts_with_services.csv')
    filtered_edges_df.to_csv(f'provenance_data_edges_filtered_by_services.csv')


if __name__ == "__main__":
    # Command-line execution support
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_provenance_data> <path_to_services_data>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
