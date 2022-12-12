def latest_block_query(chain: str) -> str:
    """
    Defines a SQL query that returns the latest block number.

    :param chain: The chain name.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT block_number 
        FROM {chain}.blocks 
        ORDER BY block_number DESC 
        LIMIT 1;
        """