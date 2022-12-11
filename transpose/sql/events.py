def all_logs_query(contract_address: str, block_start: int, block_end: int,
                   limit: int=None) -> str:

    """
    Defines a SQL query that returns all logs for a given contract.

    :param contract_address: The contract address.
    :param block_start: The starting block number.
    :param block_end: The ending block number.
    :param limit: The maximum number of logs to return.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT *
        FROM ethereum.logs
        WHERE address = '{contract_address}'
        AND block_number >= {block_start}
        AND block_number <= {block_end}
        {'LIMIT ' + str(limit) if limit is not None else ''};
        """


def logs_query(contract_address: str, topic_0: str, block_start: int, block_end: int,
               limit: int=None) -> str:

    """
    Defines a SQL query that returns logs for a given contract and event.

    :param contract_address: The contract address.
    :param topic_0: The event signature.
    :param block_start: The starting block number.
    :param block_end: The ending block number.
    :param limit: The maximum number of logs to return.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT *
        FROM ethereum.logs
        WHERE address = '{contract_address}'
        AND topic_0 = '{topic_0}'
        AND block_number >= {block_start}
        AND block_number <= {block_end}
        {'LIMIT ' + str(limit) if limit is not None else ''};
        """