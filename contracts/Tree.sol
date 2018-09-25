pragma solidity ^0.4.0;

import "./SafeMath.sol";
import "./Merkle.sol";
import "./Leaf.sol";


/**
 * @title PercentTrees
 * @dev This contract secures merkelized p2sh construction for Ethereum.
 */
contract PercentTrees {
    using SafeMath for uint256;
    using Merkle for bytes32;


    /*
     * Events
     */

    event NewTree(
        uint256 indexed treeId,
        uint256 amount
    );

    event PTUpdated(
        uint256 indexed treeId,
        uint256 leaf,
        uint256 amount
    );

    event PTCached(
        uint256 indexed treeId,
        uint256 leaf,
        uint256 amount
    );


    struct Tree {
        bytes32 root;
        uint256 amount;
        /* bytes32 bits; */
    }

    /*
     * Storage
     */

    uint256 public counter = 0;
    mapping (uint256 => Tree) public trees;

    /*
     * Constructor
     */

    constructor() public {}

    /*
     * Public Functions
     */

    /**
     * @dev Allows anyone to create new tree. Body of the tree is propagated offchain among participants of the leaves. Logic of leaves is configurable per leaf.
     * @param _root The root of a new tree.
     */
    function addTree(bytes32 _root)
        public
        payable
    {
        uint256 newTreeId = counter;
        trees[newTreeId] = Tree({
            root: _root,
            amount: msg.value
            /* bits: bytes32(0) */
        });

        // Update counter, preventing tree reuse.
        counter = counter.add(1);

        emit NewTree(newTreeId, msg.value);
    }

    /**
     * @dev Cash out leaf by providing unlock data for leaf and inclusion proof.
     */
    function withdraw(uint256 _treeId, uint256 _index, uint256 _percent, address _unlockScript, bytes32 _anchor, bytes _unlockData, bytes _proof)
        public
    {
        require(is_unspent(_treeId, _index));
        require(_percent <= 1000000);
        bytes32 root = trees[_treeId].root;
        bytes32 merkleHash = keccak256(_index, _anchor, _percent, _unlockScript);
        require(merkleHash.checkMembership(_index, root, _proof));
        uint256 amount = _percent.mul(trees[_treeId].amount).div(1000000);
        // call unlock contract that will also spend money - instructions in in unlockData
        require(_unlockScript.delegatecall(bytes4(keccak256("unlock_and_spend")), _anchor, _unlockData, amount));
        mark_as_spent(_treeId, _index);
        // script is defined
        // agrs to script consist of two parts
        //   anchor, one defined by tree == keccak(signer, nonce)
        //   "keys", provided by caller
        //   leaf == h(unlockScript, anchor)
    }

    function is_unspent(uint256 _treeId, uint256 _index)
        public
        view
        returns (bool)
    {
        return true;
    }

    function mark_as_spent(uint256 _treeId, uint256 _index)
        public
    {
        return;
    }
}
