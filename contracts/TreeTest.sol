pragma solidity ^0.4.0;

import "./Merkle.sol";

contract TreeTest {
    using Merkle for bytes32;

    constructor() public {}

    function isMember(bytes32 _root, uint256 _index, uint256 _percent, bytes32 _anchor, bytes _proof)
        public
        view
        returns (bool)
    {
        bytes32 merkleHash = keccak256(_index, _anchor, _percent);
        return merkleHash.checkMembership(_index, _root, _proof);
    }

    function hash(uint256 _index, uint256 _percent, bytes32 _anchor)
        public
        view
        returns (bytes32)
    {
        return keccak256(_index, _anchor, _percent);
    }

    function proofLength(bytes _proof)
        public
        returns (uint256)
    {
        return _proof.length;
    }
}
