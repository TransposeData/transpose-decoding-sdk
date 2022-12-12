from transpose.contract import TransposeDecodedContract


if __name__ == '__main__':

    # initialize contract
    contract = TransposeDecodedContract(
        contract_address='0x00000000006c3852cbEf3e08E8dF289169EdE581',
        abi_path='abi/opensea-seaport-abi.json',
        chain='ethereum',
        api_key='enP9LfNUmGt0WRg1LNG4nSYK2MC1waEH'
    )
    
    # # build event stream
    # stream = contract.stream_events(
    #     event_name='OrderFulfilled',
    #     start_block=0
    # )

    # build call stream
    stream = contract.stream_calls(
        function_name='fulfillBasicOrder',
        start_block=0
    )

    # get next event
    print(stream.next(1))

    # # iterate over stream
    # for event in stream:
    #     print(event)