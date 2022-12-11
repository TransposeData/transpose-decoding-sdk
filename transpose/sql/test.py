def test_query() -> str:
    """
    Defines a SQL query that returns the latest block number on Ethereum.

    :return: The SQL query.
    """

    return \
        f"""
        SELECT block_number 
        FROM ethereum.blocks 
        ORDER BY block_number DESC 
        LIMIT 1;
        """