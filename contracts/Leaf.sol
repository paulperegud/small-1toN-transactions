pragma solidity ^0.4.18;

import "./ECRecovery.sol";

/**
 * @title Pay-to-script-hash interface for Ethereum
 */
contract P2SHE {
    constructor() public {}

    function unlock_and_spend(bytes32 anchor, bytes unlockData, uint256 amount)
        public
        returns (bool)
    {
        return false;
    }
}

contract Dummy is P2SHE {
    function unlock_and_spend(bytes32 anchor, bytes unlockData, uint256 amount)
        public
        returns (bool)
    {
        return false;
    }
}

contract P2PK is P2SHE {
    function unlock_and_spend(bytes32 anchor, bytes unlockData, uint256 amount)
        public
        returns (bool)
    {
        require(unlockData.length == 32 + 65 + 32);
        address signer;
        bytes32 nonce;
        address recovered_signer;
        address destination;
        bytes memory sig = new bytes(65);
        /* unlockData memory layout:
             0   - 32  (32) : structure size
             32  - 64  (32) : signer address
             64  - 96  (32) : nonce
             96  - 128 (32) : destination
             128 - 193 (65) : signature
         */
        assembly {
            /* let sig := mload(0x40) */
            calldatacopy(sig, add(unlockData, 128), 65)
            signer := mload(add(unlockData, 32))
            nonce := mload(add(unlockData, 64))
            destination := mload(add(unlockData, 96))
        }
        if (anchor != keccak256(signer, nonce)) return false;
        recovered_signer = ECRecovery.recover(keccak256(anchor, destination), sig);
        if (recovered_signer != signer) return false;
        destination.transfer(amount);
        return true;
    }
}
