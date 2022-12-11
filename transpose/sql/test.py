TEST_QUERY =\
    """
    SELECT block_number 
    FROM ethereum.blocks 
    ORDER BY block_number DESC 
    LIMIT 1;
    """