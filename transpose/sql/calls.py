def calls_query(chain: str, contract_address: str, from_block: int, from_transaction_position: int, from_trace_index: int,
                function_selector: str=None,
                stop_block: int=None,
                order: str='asc',
                limit: int=None) -> str:

    """
    Defines a SQL query that returns transactions and traces for a given contract.

    :param chain: The chain name.
    :param contract_address: The contract address.
    :param from_block: The starting block number, inclusive.
    :param from_transaction_position: The starting transaction position, inclusive.
    :param from_trace_index: The starting trace index, inclusive.
    :param function_selector: The function selector.
    :param stop_block: The ending block number, exclusive.
    :param order: The order to return the transactions and traces in.
    :param limit: The maximum number of transactions and traces to return.
    :return: The SQL query.
    """

    if order == 'asc':
        return \
            f"""
            SELECT * FROM (

                (SELECT 
                    timestamp, block_number, transaction_hash, position AS transaction_position,
                    0 AS trace_index, array[]::integer[] AS trace_address, 'call' AS trace_type,
                    from_address, value, input, output, __confirmed
                FROM {chain}.transactions
                WHERE to_address = '{contract_address}'
                {f"AND LEFT(input, 10) = '{function_selector}'" if function_selector is not None else ""}
                AND (block_number, position) >= ({from_block}, {from_transaction_position})
                {f"AND block_number < {stop_block}" if stop_block is not None else ""}
                ORDER BY block_number ASC, transaction_position ASC
                {f"LIMIT {limit}" if limit is not None else ""})

                UNION ALL

                (SELECT 
                    timestamp, block_number, transaction_hash, transaction_position, 
                    trace_index + 1, trace_address, trace_type, 
                    from_address, value, input, output, __confirmed
                FROM {chain}.traces
                WHERE to_address = '{contract_address}'
                {f"AND LEFT(input, 10) = '{function_selector}'" if function_selector is not None else ""}
                AND (block_number, transaction_position, trace_index) >= ({from_block}, {from_transaction_position}, {from_trace_index})
                {f"AND block_number < {stop_block}" if stop_block is not None else ""}
                ORDER BY block_number ASC, transaction_position ASC, trace_index ASC
                {f"LIMIT {limit}" if limit is not None else ""})
            
            ) AS t

            ORDER BY block_number ASC, transaction_position ASC, trace_index ASC
            {f"LIMIT {limit}" if limit is not None else ""}
            """
    
    else:
        return \
            f"""
            SELECT * FROM (

                (SELECT 
                    timestamp, block_number, transaction_hash, position AS transaction_position,
                    0 AS trace_index, array[]::integer[] AS trace_address, 'call' AS trace_type,
                    from_address, value, input, output, __confirmed
                FROM {chain}.transactions
                WHERE to_address = '{contract_address}'
                {f"AND LEFT(input, 10) = '{function_selector}'" if function_selector is not None else ""}
                AND (block_number, position) <= ({from_block}, {from_transaction_position})
                {f"AND block_number > {stop_block}" if stop_block is not None else ""}
                ORDER BY block_number DESC, transaction_position DESC
                {f"LIMIT {limit}" if limit is not None else ""})

                UNION ALL

                (SELECT 
                    timestamp, block_number, transaction_hash, transaction_position, 
                    trace_index + 1, trace_address, trace_type, 
                    from_address, value, input, output, __confirmed
                FROM {chain}.traces
                WHERE to_address = '{contract_address}'
                {f"AND LEFT(input, 10) = '{function_selector}'" if function_selector is not None else ""}
                AND (block_number, transaction_position, trace_index) <= ({from_block}, {from_transaction_position}, {from_trace_index})
                {f"AND block_number > {stop_block}" if stop_block is not None else ""}
                ORDER BY block_number DESC, transaction_position DESC, trace_index DESC
                {f"LIMIT {limit}" if limit is not None else ""})
            
            ) AS t

            ORDER BY block_number DESC, transaction_position DESC, trace_index DESC
            {f"LIMIT {limit}" if limit is not None else ""}
            """