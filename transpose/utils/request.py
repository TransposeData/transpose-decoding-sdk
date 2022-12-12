from typing import List
import requests

from transpose.utils.exceptions import TransposeAPIError


def send_transpose_sql_request(api_key: str, query: str,
                               debug: bool=False) -> List[dict]:

    """
    Send a SQL query to the Transpose API and return the response results. Will
    raise a TransposeAPIError if the API returns an error.

    :param api_key: A valid API key for Transpose.
    :param query: A valid SQL query.
    :param debug: Whether to print the query.
    :return: The response from the Transpose API.
    """
        
    # send POST request to Transpose API
    response = requests.post(
        url='https://api.transpose.io/sql',
        json={'sql': query},
        headers={'X-Api-Key': api_key}
    )

    # check for errors
    api_response = response.json()
    if api_response['status'] == 'error':
        raise TransposeAPIError(
            status_code=response.status_code,
            message=api_response['message']
        )

    # print query
    if debug: print(query)
    
    # return results
    return api_response['results']