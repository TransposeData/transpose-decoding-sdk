def events_query(chain: str, contract_address: str, from_block: int, from_log_index: int,
                 topic_0: str=None,
                 stop_block: int=None,
                 order: str='asc',
                 limit: int=None) -> str:

    """
    Defines a SQL query that returns logs for a given contract.

    :param chain: The chain name.
    :param contract_address: The contract address.
    :param from_block: The starting block number, inclusive.
    :param from_log_index: The starting log index, inclusive.
    :param topic_0: The event signature.
    :param stop_block: The ending block number, exclusive.
    :param order: The order to return the logs in.
    :param limit: The maximum number of logs to return.
    :return: The SQL query.
    """

    if order == 'asc':
        return \
            f"""
            SELECT timestamp, block_number, log_index, transaction_hash, transaction_position, address, data, topic_0, topic_1, topic_2, topic_3, __confirmed
            FROM {chain}.logs
            WHERE address = '{contract_address}'
            {f"AND topic_0 = '{topic_0}'" if topic_0 is not None else ""}
            AND (block_number, log_index) >= ({from_block}, {from_log_index})
            {f"AND block_number < {stop_block}" if stop_block is not None else ""}
            ORDER BY block_number ASC, log_index ASC
            {f"LIMIT {limit}" if limit is not None else ""}
            """
    
    else:
        return \
            f"""
            SELECT timestamp, block_number, log_index, transaction_hash, transaction_position, address, data, topic_0, topic_1, topic_2, topic_3, __confirmed
            FROM {chain}.logs
            WHERE address = '{contract_address}'
            {f"AND topic_0 = '{topic_0}'" if topic_0 is not None else ""}
            AND (block_number, log_index) <= ({from_block}, {from_log_index})
            {f"AND block_number > {stop_block}" if stop_block is not None else ""}
            ORDER BY block_number DESC, log_index DESC
            {f"LIMIT {limit}" if limit is not None else ""}
            """