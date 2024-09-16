// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskChain {
    struct Block {
        uint index;
        bytes32 previousHash;
        uint timestamp;
        string task;
        bytes32 hash;
    }

    Block[] public blockchain;

    // Function to calculate the hash of a block
    function calculateHash(uint _index, bytes32 _previousHash, uint _timestamp, string memory _task) public pure returns (bytes32) {
        return sha256(abi.encodePacked(_index, _previousHash, _timestamp, _task));
    }

    // Function to create the genesis block
    function createGenesisBlock() public {
        require(blockchain.length == 0, "Genesis block already created");
        uint timestamp = block.timestamp;
        bytes32 hash = calculateHash(0, bytes32(0), timestamp, "Genesis Task");
        blockchain.push(Block(0, bytes32(0), timestamp, "Genesis Task", hash));
    }

    // Function to create a new block
    function createNewBlock(string memory _task) public {
        require(blockchain.length > 0, "Genesis block must be created first");
        Block memory previousBlock = blockchain[blockchain.length - 1];
        uint newIndex = previousBlock.index + 1;
        uint timestamp = block.timestamp;
        bytes32 newHash = calculateHash(newIndex, previousBlock.hash, timestamp, _task);
        blockchain.push(Block(newIndex, previousBlock.hash, timestamp, _task, newHash));
    }

    // Function to verify the blockchain integrity
    function isChainValid() public view returns (bool) {
        for (uint i = 1; i < blockchain.length; i++) {
            Block memory currentBlock = blockchain[i];
            Block memory previousBlock = blockchain[i - 1];

            // Verify current block's hash
            if (currentBlock.hash != calculateHash(currentBlock.index, currentBlock.previousHash, currentBlock.timestamp, currentBlock.task)) {
                return false;
            }

            // Verify the previous hash links
            if (currentBlock.previousHash != previousBlock.hash) {
                return false;
            }
        }
        return true;
    }

    // Function to view all tasks (can return task details for simplicity)
    function viewTasks() public view returns (Block[] memory) {
        return blockchain;
    }

    // Public function to add a task and create a new block
    function addTask(string memory _task) public {
        createNewBlock(_task);
    }
}
