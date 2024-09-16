import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, task, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.task = task
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, task):
    value = str(index) + str(previous_hash) + str(timestamp) + str(task)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Task", calculate_hash(0, "0", int(time.time()), "Genesis Task"))

def create_new_block(previous_block, task):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, task)
    return Block(index, previous_block.hash, timestamp, task, hash)

def is_chain_valid(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.task):
            return False

        if current_block.previous_hash != previous_block.hash:
            return False

    return True

def add_task(task, blockchain):
    previous_block = blockchain[-1]
    new_block = create_new_block(previous_block, task)
    blockchain.append(new_block)
    print(f"Task '{task}' added as Block #{new_block.index} with Hash: {new_block.hash}")

def view_tasks(blockchain):
    for block in blockchain:
        print(f"Block #{block.index} - Task: {block.task}, Hash: {block.hash}")

# Main code to interact with TaskChain
if __name__ == "__main__":
    # Initialize the blockchain with the genesis block
    blockchain = [create_genesis_block()]

    while True:
        print("\n1. Add Task")
        print("\n2. View Tasks")
        print("\n3. Check Blockchain Integrity")
        print("\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter the task: ")
            add_task(task, blockchain)

        elif choice == "2":
            view_tasks(blockchain)

        elif choice == "3":
            is_valid = is_chain_valid(blockchain)
            print("\nBlockchain is valid!" if is_valid else "\nBlockchain is not valid!")

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please choose again.")
