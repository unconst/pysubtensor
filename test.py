from substrateinterface import SubstrateInterface
import asyncio
import time

substrate = SubstrateInterface(
        url="wss://127.0.0.1:9933",
        address_type=42,
        type_registry_preset='substrate-node-template'
    )
result = substrate.get_runtime_block()
#current_block = result['block']['header']['parentHash']
#print ('Current block:', current_block)
