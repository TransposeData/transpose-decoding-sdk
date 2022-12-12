from transpose.decoder import TransposeContractDecoder


if __name__ == '__main__':

    # initialize decoder
    contract_decoder = TransposeContractDecoder(api_key='enP9LfNUmGt0WRg1LNG4nSYK2MC1waEH')

    # load contract
    contract_decoder.load_contract(
        contract_address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        abi_path='weth-abi.json',
        chain='ethereum'
    )
    
    # build stream
    stream = contract_decoder.stream_events(
        # event_name='Withdrawal',
        scroll_iterator=True
    )

    # iterate over stream
    for event in stream:
        print(event)