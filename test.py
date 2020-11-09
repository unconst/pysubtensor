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


# -----------------
# Get alice balance.
def get_balance(keypair):
    balance_info = substrate.get_runtime_state(
        module='System',
        storage_function='Account',
        params=[keypair.ss58_address],
        block_hash=current_block()
    ).get('result')
    return balance_info['data']['free'] / 10**12

alice_keypair = Keypair.create_from_uri('//Alice')
print ('Alice pubkey:', alice_keypair.public_key)
print ('Alice address:', alice_keypair.ss58_address)
print ('Alice balance:', get_balance(alice_keypair))

bob_keypair = Keypair.create_from_uri('//Bob')
print ('Bob pubkey:', bob_keypair.public_key)
print ('Bob address:', bob_keypair.ss58_address)
print ('Bob balance:', get_balance(bob_keypair))

# -----------------
# Print subtensor pallet info
print ('\n')
print ('Subtensor Pallet:', substrate.get_metadata_storage_function('SubtensorModule', 'Weights'))

# -----------------
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


value = 123123
print ('\n')
print ('Setting weight Alice --> Bob => {}'.format(value))
setWeights(alice_keypair, bob_keypair, value)
weight = substrate.get_runtime_state(
    module='SubtensorModule',
    storage_function='Weights',
    params=[alice_keypair.ss58_address, bob_keypair.ss58_address]
)
print ('weight Alice --> Bob =', weight['result'])
