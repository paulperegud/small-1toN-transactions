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

