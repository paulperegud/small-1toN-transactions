import pytest
from ethereum.tools.tester import TransactionFailed
from trees_core.fixed_merkle import FixedMerkle
from trees_core.leaf import Leaf

from ethereum.utils import encode_hex

def test_contract_deploy(ethtester, tree):
    assert tree.counter() == 0;

def test_leaf_deploy(ethtester, dummy):
    assert dummy.address

def test_p2pk_deploy(ethtester, p2pk):
    assert p2pk.address

def test_tree_create_basic(ethtester, tree):
    tree.addTree(b'0' * 32)
    assert tree.counter() == 1

def test_tree_create_with_leaves(ethtester, tree):
    a = Leaf(0, b'0' * 32, 100000)
    b = Leaf(1, b'0' * 32, 900000)
    merkle = FixedMerkle(1, leaves=[a, b])
    tree.addTree(merkle.root)
    assert tree.counter() == 1

def test_membership(ethtester, treetest):
    a = Leaf(0, b'0' * 31 + b'1', 100000)
    b = Leaf(1, b'0' * 32, 800000)
    c = Leaf(2, b'0' * 32, 50000)
    d = Leaf(3, b'0' * 32, 50000)
    merkle = FixedMerkle(2, leaves=[a, b, c, d])
    proof = merkle.create_membership_proof(a)
    assert a.hash() == treetest.hash(0, 100000, b'0' * 31 + b'1')
    assert len(merkle.root) == 32
    assert len(proof) == 64
    assert 64 == treetest.proofLength(proof)
    assert treetest.isMember(merkle.root, 0, 100000, b'0' * 31 + b'1', proof)

# # add token
# def test_token_adding(ethtester, token, root_chain):
#     assert not root_chain.hasToken(token.address)
#     root_chain.addToken(token.address)
#     assert root_chain.hasToken(token.address)
#     with pytest.raises(TransactionFailed):
#         root_chain.addToken(token.address)


# # deposit
# def test_deposit_should_succeed(testlang):
#     owner, amount = testlang.accounts[0], 100

#     deposit_blknum = testlang.deposit(owner, amount)

#     plasma_block = testlang.get_plasma_block(deposit_blknum)
#     assert plasma_block.root == get_deposit_hash(address_to_bytes(owner.address), NULL_ADDRESS, amount)
#     assert plasma_block.timestamp == testlang.timestamp
#     assert testlang.root_chain.currentDepositBlock() == 2


# # deposit ERC20 token
# def test_deposit_token(testlang, ethtester, root_chain, token):
#     owner, amount = testlang.accounts[0], 100

#     deposit_blknum = testlang.deposit_token(owner, token, amount)

#     plasma_block = testlang.get_plasma_block(deposit_blknum)
#     assert plasma_block.root == get_deposit_hash(address_to_bytes(owner.address), token.address, amount)
#     assert plasma_block.timestamp == testlang.timestamp
#     assert testlang.root_chain.currentDepositBlock() == 2


# # startDepositExit
# def test_start_deposit_exit_should_succeed(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)

#     testlang.start_deposit_exit(owner, deposit_blknum, amount)

#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     plasma_exit = testlang.get_plasma_exit(deposit_id)
#     assert plasma_exit.owner == owner.address
#     assert plasma_exit.token == NULL_ADDRESS_HEX
#     assert plasma_exit.amount == amount


# def test_start_deposit_exit_twice_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)

#     testlang.start_deposit_exit(owner, deposit_blknum, amount)

#     with pytest.raises(TransactionFailed):
#         testlang.start_deposit_exit(owner, deposit_blknum, amount)


# def test_start_deposit_exit_wrong_owner_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)

#     with pytest.raises(TransactionFailed):
#         testlang.start_deposit_exit(testlang.accounts[1], deposit_blknum, amount)


# def test_start_deposit_exit_wrong_amount_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)

#     with pytest.raises(TransactionFailed):
#         testlang.start_deposit_exit(owner, deposit_blknum, 999)


# def test_start_deposit_exit_wrong_blknum_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)

#     with pytest.raises(TransactionFailed):
#         testlang.start_deposit_exit(owner, deposit_blknum + 1, amount)


# def test_start_deposit_exit_child_blknum_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     testlang.deposit(owner, amount)

#     with pytest.raises(TransactionFailed):
#         testlang.start_deposit_exit(owner, 1000, amount)


# # startFeeExit
# def test_start_fee_exit_should_succeed(testlang):
#     operator, amount = testlang.accounts[0], 100

#     fee_exit_id = testlang.start_fee_exit(operator, amount)

#     plasma_exit = testlang.get_plasma_exit(fee_exit_id)
#     assert plasma_exit.owner == operator.address
#     assert plasma_exit.token == NULL_ADDRESS_HEX
#     assert plasma_exit.amount == amount


# def test_start_fee_exit_non_operator_should_fail(testlang):
#     amount = 100

#     with pytest.raises(TransactionFailed):
#         testlang.start_fee_exit(testlang.accounts[1], amount)


# # startExit
# def test_start_exit_should_succeed(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id, owner)

#     testlang.start_exit(owner, spend_id)

#     plasma_exit = testlang.get_plasma_exit(spend_id)
#     assert plasma_exit.owner == owner.address
#     assert plasma_exit.token == NULL_ADDRESS_HEX
#     assert plasma_exit.amount == amount


# def test_start_exit_twice_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id, owner)

#     testlang.start_exit(owner, spend_id)

#     with pytest.raises(TransactionFailed):
#         testlang.start_exit(owner, spend_id)


# def test_start_exit_wrong_owner_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id, owner)

#     with pytest.raises(TransactionFailed):
#         testlang.start_exit(testlang.accounts[1], spend_id)


# # challengeExit
# def test_challenge_exit_should_succeed(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id_1 = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id_1, owner)
#     testlang.start_exit(owner, spend_id_1)
#     spend_id_2 = testlang.spend_utxo(spend_id_1, owner, amount, owner)
#     testlang.confirm_spend(spend_id_2, owner)

#     testlang.challenge_exit(spend_id_1, spend_id_2)

#     plasma_exit = testlang.get_plasma_exit(spend_id_1)
#     assert plasma_exit.owner == NULL_ADDRESS_HEX


# def test_challenge_exit_invalid_challenge_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id, owner)
#     testlang.start_exit(owner, spend_id)

#     with pytest.raises(TransactionFailed):
#         testlang.challenge_exit(spend_id, spend_id)


# def test_challenge_exit_invalid_proof_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id_1 = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id_1, owner)
#     testlang.start_exit(owner, spend_id_1)
#     spend_id_2 = testlang.spend_utxo(spend_id_1, owner, amount, owner)
#     testlang.confirm_spend(spend_id_2, owner)

#     proof = b'deadbeef'
#     (input_index, encoded_spend, _, sigs, confirmation_sig) = testlang.get_challenge_proof(spend_id_1, spend_id_2)
#     with pytest.raises(TransactionFailed):
#         testlang.root_chain.challengeExit(spend_id_1, input_index, encoded_spend, proof, sigs, confirmation_sig)


# def test_challenge_exit_invalid_confirmation_should_fail(testlang):
#     owner, amount = testlang.accounts[0], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     spend_id_1 = testlang.spend_utxo(deposit_id, owner, amount, owner)
#     testlang.confirm_spend(spend_id_1, owner)
#     testlang.start_exit(owner, spend_id_1)
#     spend_id_2 = testlang.spend_utxo(spend_id_1, owner, amount, owner)
#     testlang.confirm_spend(spend_id_2, owner)

#     confirmation_sig = b'deadbeef'
#     (input_index, encoded_spend, proof, sigs, _) = testlang.get_challenge_proof(spend_id_1, spend_id_2)
#     with pytest.raises(TransactionFailed):
#         testlang.root_chain.challengeExit(spend_id_1, input_index, encoded_spend, proof, sigs, confirmation_sig)


# # finalizeExits for ETH
# def test_finalize_exits_should_succeed(testlang):
#     owner, amount = testlang.accounts[1], 100
#     deposit_blknum = testlang.deposit(owner, amount)
#     testlang.start_deposit_exit(owner, deposit_blknum, amount)
#     testlang.forward_timestamp(2 * WEEK + 1)

#     pre_balance = testlang.get_balance(owner)
#     testlang.finalize_exits()

#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     plasma_exit = testlang.get_plasma_exit(deposit_id)
#     assert plasma_exit.owner == NULL_ADDRESS_HEX
#     assert testlang.get_balance(owner) == pre_balance + amount


# # finalizeExists for tokens
# def test_finalize_exits_for_ERC20_should_succeed(testlang, ethtester, root_chain, token):
#     owner, amount = testlang.accounts[0], 100
#     root_chain.addToken(token.address)
#     deposit_blknum = testlang.deposit_token(owner, token, amount)

#     testlang.start_deposit_exit(owner, deposit_blknum, amount, token.address)
#     testlang.forward_timestamp(2 * WEEK + 1)

#     pre_balance = token.balanceOf(owner.address)
#     testlang.finalize_exits(token.address)

#     deposit_id = encode_utxo_id(deposit_blknum, 0, 0)
#     plasma_exit = testlang.get_plasma_exit(deposit_id)
#     assert plasma_exit.owner == NULL_ADDRESS_HEX
#     assert token.balanceOf(owner.address) == pre_balance + amount
