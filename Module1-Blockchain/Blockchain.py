#Create a Blockchain
#
#install - 
#Flask==0.12.2: pip install Flask==0.12.2
#postman HTTP CLient: https://www.getpostman.com/

#import the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

#part 1 - building a blockchain


class Blockchain:
   def _init_(self):
          #initialize the chain of the blocks
          self.chain = []
          #create the genesis block
          self.create_block(proof = 1, previous_hash = '0')
          
   def create_block(self, proof, previous_hash):
        #define new block that is mined {essential keys}
        block = {'index': len(self.chain)+ 1, 
                 'timestamp': str(datetime.datetime.now()), 
                 'proof' : proof ,
                 'previous_hash': previous_hash}#data added as it is mined
        self.chain.append(block)
        return block

   def get_previous_block(self):
        return self.chain[-1]#chain -1 gives last index pos of chain
    
   def proof_of_work(self, previous_proof):
       new_proof = 1
       check_proof = False
       while check_proof is False:
           hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
           if hash_operation[:4] == '0000' :
               check_proof = True
           else:
               new_proof += 1
       return new_proof


   def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
   def is_chain_valid(self, chain):
       previous_block = chain[0]
       block_index = 1
       while block_index < len(chain):
           block = chain[block_index]
           if block['previous_hash'] != self.hash(previous_block):
               return False
           previous_proof = previous_block['proof']
           proof = block['proof']
           hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
           if hash_operation[:4] != '0000' :
               return False
           previous_block = block
           block_index += 1
           return True



#part 2 - mining blockchain

#creating a webapp
app = Flask(__name__)



#creating a blockchain
blockchain = Blockchain()

#mine a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats you just mined a block!!!!:D!!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block[previous_hash]}
    return jsonify(response), 200


#getting the full blockchain 
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#check if the blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid: 
        response = {'message': 'All good block chain is valid! :D'}
    else:
        response = {'message': 'Houston, we have a problem, blockchain not valid'}
    return jsonify(response), 200

#running the app
app.run(host = '0.0.0.0', port = 5000)



