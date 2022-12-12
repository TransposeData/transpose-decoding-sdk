def transactions_query(chain: str, contract_address: str, from_block: int, from_transaction_position: int,
                       function_selector: str=None,
                       stop_block: int=None,
                       limit: int=None) -> str:

    """
    Defines a SQL query that returns transactions for a given contract.

    :param chain: The chain name.
    :param contract_address: The contract address.
    :param from_block: The starting block number, inclusive.
    :param from_transaction_position: The starting transaction position, inclusive.
    :param function_selector: The function selector.
    :param stop_block: The ending block number, exclusive.
    :param limit: The maximum number of transactions to return.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT timestamp, block_number, transaction_hash, position, from_address, value, input, output, __confirmed
        FROM {chain}.transactions
        WHERE to_address = '{contract_address}'
        {f"AND LEFT(input, 10) = '{function_selector}'" if function_selector is not None else ""}
        AND (block_number, position) >= ({from_block}, {from_transaction_position})
        {f"AND block_number < {stop_block}" if stop_block is not None else ""}
        ORDER BY block_number ASC, position ASC
        {f"LIMIT {limit}" if limit is not None else ""}
        """


def traces_query(chain: str, contract_address: str, from_block: int, from_transaction_position: int, from_trace_index: int,
                 function_selector: str=None,
                 stop_block: int=None,
                 limit: int=None) -> str:

    """
    Defines a SQL query that returns traces for a given contract.

    :param chain: The chain name.
    :param contract_address: The contract address.
    :param from_block: The starting block number, inclusive.
    :param from_transaction_position: The starting transaction position, inclusive.
    :param from_trace_index: The starting trace index, inclusive.
    :param function_selector: The function selector.
    :param stop_block: The ending block number, exclusive.
    :param limit: The maximum number of traces to return.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT timestamp, block_number, transaction_hash, transaction_position, trace_index, trace_address, trace_type, from_address, value, input, output, __confirmed
        FROM {chain}.traces
        WHERE to_address = '{contract_address}'
        {f"AND LEFT(input, 10) = '{function_selector}'" if function_selector is not None else ""}
        AND (block_number, transaction_position, trace_index) >= ({from_block}, {from_transaction_position}, {from_trace_index})
        {f"AND block_number < {stop_block}" if stop_block is not None else ""}
        ORDER BY block_number ASC, transaction_position ASC, trace_index ASC
        {f"LIMIT {limit}" if limit is not None else ""}
        """