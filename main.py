from transpose.contract import TransposeDecodedContract
import time


if __name__ == '__main__':

    # initialize contract
    contract = TransposeDecodedContract(
        contract_address='0x00000000006c3852cbEf3e08E8dF289169EdE581',
        abi_path='abi/opensea-seaport-abi.json',
        chain='ethereum',
        api_key='4IfOT4rq7Vdi1mFpfVx3KLu3CN66p8Gm'
    )
    
    # # build event stream
    # stream = contract.stream_events(
    #     event_name='OrderFulfilled',
    #     start_block=0
    # )

    # build call stream
    stream = contract.stream_calls(
        live_stream=True,
        start_block=0
    )

    # iterate over stream
    t1 = time.time()
    counter = 0
    for event in stream:
        counter += 1
        print('\rEPS: {}\t'.format(round(counter / (time.time() - t1), 3)), end='')