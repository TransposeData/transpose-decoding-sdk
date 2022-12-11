def all_logs_query(contract_address: str, start_block: int, 
                   end_block: int=None,
                   limit: int=None) -> str:

    """
    Defines a SQL query that returns all logs for a given contract.

    :param contract_address: The contract address.
    :param start_block: The starting block number.
    :param end_block: The ending block number.
    :param limit: The maximum number of logs to return.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT *
        FROM ethereum.logs
        WHERE address = '{contract_address}'
        AND block_number >= {start_block}
        {'AND block_number <= ' + str(end_block) if end_block is not None else ''}
        {'LIMIT ' + str(limit) if limit is not None else ''};
        """


def logs_query(contract_address: str, topic_0: str, start_block: int, end_block: int,
               limit: int=None) -> str:

    """
    Defines a SQL query that returns logs for a given contract and event.

    :param contract_address: The contract address.
    :param topic_0: The event signature.
    :param start_block: The starting block number.
    :param end_block: The ending block number.
    :param limit: The maximum number of logs to return.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT *
        FROM ethereum.logs
        WHERE address = '{contract_address}'
        AND topic_0 = '{topic_0}'
        AND block_number >= {start_block}
        AND block_number <= {end_block}
        {'LIMIT ' + str(limit) if limit is not None else ''};
        """