from typing import Optional
from web3 import Web3


def to_checksum_address(address: str) -> Optional[str]:
    """
    Convert an address to a checksum address. Will return None
    if the address is invalid.

    :param address: The address to convert.
    :return: The checksum address.
    """

    try: return Web3.toChecksumAddress(address)
    except: return None