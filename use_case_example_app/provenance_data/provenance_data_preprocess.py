import pandas as pd
import json
import use_case_example_app.provenance_data.create_k8s_svc_df

# Global Variables
# Path to Provenance Data
# prov_data_path = ''
# Path to raw provenance data JSON file
prov_JSON_path = 'prov_JSON/prov-worker-0912231.json'
# Path to Kubernetes Service Data
kubectl_svc_path = 'kubectl_svc.json'


def prepare_vertices_and_edges(prov_data_JSON):
    """
    Convert raw provenance data to dataframes for each provenance graph components.

    :param prov_data_JSON: dict: Raw provenance data in JSON format.

    :return: 3 DataFrames: Dataframe for each provenance graph components:
        1. edges_data: list of items to later create and edges dataframe
        2. vertices_process_df: Dataframe for vertices of type 'Process'
        3. vertices_artifacts_df: Dataframe for vertices of type 'Artifact'
    """
    # Separate edges and vertices data
    edges_data = []
    vertices_process = []
    vertices_artifacts = []

    for item in prov_data_JSON:
        if 'type' in item:
            # Separate vertices to dataframes according to their type - 'Process' or 'Artifact'
            if item['type'] == 'Process':
                vertices_process.append(item)
            elif item['type'] == 'Artifact':
                vertices_artifacts.append(item)
            else:
                edges_data.append(item)

    # Load process vertices data into a pandas dataframe
    process_df = pd.DataFrame(vertices_process)
    # Convert the dictionary in annotations column into columns in process_df
    annotations_process_df = pd.DataFrame(process_df['annotations'].tolist())
    # Combine annotations_process_df with process_df instead of the 'annotations' column in process_df
    process_df = pd.concat([process_df, annotations_process_df], axis=1).drop('annotations', axis=1)

    # Load artifact vertices data into a pandas dataframe
    artifact_df = pd.DataFrame(vertices_artifacts)
    # Convert the dictionary in annotations column into columns in artifact_df
    annotations_artifact_df = pd.DataFrame(artifact_df['annotations'].tolist())
    # Combine annotations_artifact_df with artifact_df instead of the 'annotations' column in artifact_df
    artifact_df = pd.concat([artifact_df, annotations_artifact_df], axis=1).drop('annotations', axis=1)

    return process_df, artifact_df, edges_data


def contains_substring(value, svc_values):
    """
    Helper function for boolean mask to filter rows according to svc_values

    :param value: str: Value to check if it contains any of the svc_values
    :param svc_values: set: Set of values to check if they are in the value

    :return: bool: True if value contains any of the svc_values, False otherwise
    """
    for svc_value in svc_values:
        if svc_value in value:
            return True
    return False


def get_k8s_svc_name(row, svc_values, svc_df):
    """
    Function to get the service_name for a given row

    :param row: pd.Series: Row of a DataFrame
    :param svc_values: set: Set of values to check if they are in the row
    :param svc_df: pd.DataFrame: DataFrame with Kubernetes Services data

    :return: str: Service name if a match is found, '.No app/k8s service found' otherwise
    """
    for value in row.astype(str):
        if any(svc_value in value for svc_value in svc_values):
            # Get the service_name from svc_df based on the matched value
            for index, row in svc_df.iterrows():
                if any(svc_value in value for svc_value in row.astype(str)):
                    return row['service_name']
    return ".No app/k8s service found"


def create_app_vertex_df(k8s_svc_values, filter_cols, vertex_df, k8s_svc_df):
    """
    Create a new DataFrame with rows from vertex_df that contain values in filter_cols that are also in k8s_svc_values

    :param k8s_svc_values: set: Set of values to check if they are in the filter_cols
    :param filter_cols: list: List of columns to filter the vertex_df
    :param vertex_df: pd.DataFrame: DataFrame with vertices data
    :param k8s_svc_df: pd.DataFrame: DataFrame with Kubernetes Services data

    :return: pd.DataFrame: DataFrame with rows from vertex_df that contain values in filter_cols that are also in k8s_svc_values
    """
    # Create a boolean mask to filter vertex_df rows  only by the filter_cols columns list
    svc_mask = vertex_df[filter_cols].apply(lambda row: any(contains_substring(value, k8s_svc_values) for value in
                                                            row.astype(str)), axis=1)
    # Use the mask to create a new DataFrame with matching rows
    app_vertex_df = vertex_df[svc_mask].copy()
    # Add a new 'svc' column to vertex_df with get_k8s_svc_name function
    app_vertex_df['svc'] = app_vertex_df[filter_cols].apply(
        lambda row: get_k8s_svc_name(row, k8s_svc_values, k8s_svc_df), axis=1)
    if filter_cols == ['exe', 'name', 'cwd', 'command line']:
        # Update dataframe without the rows with the value '.No app/k8s service found' in the 'svc' column
        app_vertex_df = app_vertex_df[app_vertex_df['svc'] != '.No app/k8s service found']
    return app_vertex_df


def complete_app_artifact_df(app_artifact_df, app_process_df):
    """
    Add to app_artifact_df rows from artifact_df that contain values in 'tgid' column that are also in app_process_df 'pid' column

    :param app_artifact_df: pd.DataFrame: DataFrame with Artifact vertices data
    :param app_process_df: pd.DataFrame: DataFrame with Process vertices data

    :return: pd.DataFrame: DataFrame with rows from artifact_df that contain values in 'tgid' column that are also in
                            app_process_df 'pid' column
    """
    tgid_app_artifact_df = pd.concat([app_artifact_df, artifact_df[artifact_df['tgid'].isin(app_process_df['pid'])]])
    # Create a dictionary to map 'pid' values to 'svc' values in app_process_df
    pid_to_svc_dict = app_process_df.set_index('pid')['svc'].to_dict()
    # Add to svc column of the new rows added the value from the svc column of the corresponding row in app_process_df
    tgid_app_artifact_df['svc'] = tgid_app_artifact_df['svc'].fillna(tgid_app_artifact_df['tgid'].map(pid_to_svc_dict))
    return tgid_app_artifact_df


def create_app_edges_df(edges_data, app_process_df, app_artifact_df):
    """
    Create a new DataFrame with rows from edges_data that contain values in 'from' or 'to' columns that are also in
    app_process_df 'id' column or app_artifact_df 'id' column

    :param edges_data: list: List of dictionaries with edges data
    :param app_process_df: pd.DataFrame: DataFrame with Process vertices data
    :param app_artifact_df: pd.DataFrame: DataFrame with Artifact vertices data

    :return: pd.DataFrame: DataFrame with rows from edges_data that contain values in 'from' or 'to' columns that are
                            also in app_process_df 'id' column or app_artifact_df 'id' column
    """
    # Create a DataFrame from edges_data
    edges_df = pd.DataFrame(edges_data)

    # Convert the dictionary in annotations column into columns in edges_df
    annotations_edges_df = pd.DataFrame(edges_df['annotations'].tolist())
    # Combine annotations_edges_df with edges_df instead of the 'annotations' column in edges_df
    edges_df = pd.concat([edges_df, annotations_edges_df], axis=1).drop('annotations', axis=1)

    # Create sets of unique IDs from app_process_df and app_artifact_df
    app_process_ids = set(app_process_df['id'])
    app_artifact_ids = set(app_artifact_df['id'])

    # Filter edges_df based on whether 'from' or 'to' vertices are in the sets of IDs
    app_edges_df = edges_df[
        edges_df['from'].isin(app_process_ids) | edges_df['to'].isin(app_process_df) | edges_df['from'].isin(
            app_artifact_ids) | edges_df['to'].isin(app_artifact_ids)]

    return app_edges_df


if __name__ == "__main__":
    # Load Provenance Data
    with open(prov_JSON_path, 'r') as json_file:
        prov_data_JSON = json.load(json_file)

    process_df, artifact_df, edges_data = prepare_vertices_and_edges(prov_data_JSON)

    # Add Kubernetes Service Data
    k8s_svc_df = use_case_example_app.provenance_data.create_k8s_svc_df.create_kubectl_svc_df(kubectl_svc_path)
    k8s_svc_values = use_case_example_app.provenance_data.create_k8s_svc_df.create_svc_values_set(k8s_svc_df)

    # Create app_process_df
    proc_filter_cols = ['exe', 'name', 'cwd', 'command line']
    app_process_df = create_app_vertex_df(k8s_svc_values, proc_filter_cols, process_df, k8s_svc_df)
    # Create app_artifact_df
    art_filter_cols = ['path', 'local address', 'remote port', 'protocol', 'remote address', 'local port']
    app_artifact_df = create_app_vertex_df(k8s_svc_values, art_filter_cols, artifact_df, k8s_svc_df)
    # Complete app_artifact_df
    app_artifact_df = complete_app_artifact_df(app_artifact_df, app_process_df)

    # Create app_edges_df
    app_edges_df = create_app_edges_df(edges_data, app_process_df, app_artifact_df)

    # Save DataFrames to CSV files
    app_process_df.to_csv(f'app_process_vertices.csv')
    app_artifact_df.to_csv(f'app_artifact_vertices.csv')
    app_edges_df.to_csv(f'app_edges.csv')
