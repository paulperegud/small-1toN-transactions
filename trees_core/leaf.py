from ethereum.utils import sha3
from trees_core.constants import NULL_HASH
from .exceptions import MemberNotExistException
from .node import Node

from ethereum.abi import encode_single

import rlp


class Leaf(object):
    def __init__(self, offset, anchor, permil):
        self.permil = permil
        self.anchor = anchor
        self.offset = offset

    def hash(self):
        enc_offset = encode_single(['uint', '256', False], self.offset)
        enc_anchor = encode_single(['bytes', '32', False], self.anchor)
        enc_permil = encode_single(["uint", '256', False], self.permil)
        assert len(enc_permil) == 32
        assert len(enc_anchor) == 32
        assert len(enc_offset) == 32
        hash = sha3(enc_offset + enc_anchor + enc_permil)
        return hash
