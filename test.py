from substrateinterface import SubstrateInterface, Keypair
import asyncio
import time

substrate = SubstrateInterface(
        url="http://127.0.0.1:9933",
        address_type=42,
        type_registry_preset='substrate-node-template'
    )

# Get current block.
def current_block():
    result = substrate.get_runtime_block()
    current_block = result['block']['header']['parentHash']
    return current_block
print ('Current block:', current_block())

# Get alice balance.
alice_keypair = Keypair.create_from_uri('//Alice')
print ('Alice pubkey:', alice_keypair.public_key)
print ('Alice address:', alice_keypair.ss58_address)


# Print subtensor pallet info
substrate.get_metadata_storage_function('SubtensorModule', 'Weights')


# Set a weight on the chain.
def setWeights(keypair_A, keypair_B, value):
    call = substrate.compose_call(
        call_module='SubtensorModule',
        call_function='set_weights',
        call_params={'dests': [keypair_B.public_key], 'values': [value]}
    )
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair_A)
    substrate.submit_extrinsic(extrinsic, wait_for_inclusion=False)
    print ('Wait for inclusion...')
    time.sleep(15)
    print ('Done. \n')


print ('set weights on chain.')
alice_keypair = Keypair.create_from_uri('//Alice')
bob_keypair = Keypair.create_from_uri('//Bob')
value = 123123
setWeights(alice_keypair, bob_keypair, value)

weights = substrate.get_runtime_state(
    module='SubtensorModule',
    storage_function='Weights',
    params=[alice_keypair.ss58_address, bob_keypair.ss58_address]
)

print (weights['result'])