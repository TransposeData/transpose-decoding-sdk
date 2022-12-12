from transpose.decoder import TransposeContractDecoder


if __name__ == '__main__':

    # initialize decoder
    contract_decoder = TransposeContractDecoder(api_key='enP9LfNUmGt0WRg1LNG4nSYK2MC1waEH')

    # load contract
    contract_decoder.load_contract(
        contract_address='0x00000000006c3852cbEf3e08E8dF289169EdE581',
        abi_path='abi/opensea-seaport-abi.json',
        chain='ethereum'
    )
    
    # build event stream
    stream = contract_decoder.stream_events(
        event_name='OrderFulfilled',
        start_block=0
    )

    # get next event
    print(stream.next(1))

    # # build call stream
    # stream = contract_decoder.stream_calls(
    #     function_name='deposit',
    #     start_block=15000000,
    #     end_block=15000010
    # )

    # # iterate over stream
    # for event in stream:
    #     print(event)