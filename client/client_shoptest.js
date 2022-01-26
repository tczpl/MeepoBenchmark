const path = require('path');
const net = require('net');
const Web3 = require('web3');
const fs = require('fs');
const process = require('process');

var solc = require('solc');
const { resolve } = require('dns');
var solc = solc.setupMethods(require("./soljson-v0.4.26+commit.4563c3fc.js"))


ipc_path = "";
console.log(process.argv);
if (process.argv[2] == "0") {
    ipc_path = './jsonrpc.ipc';
}
if (process.argv[2] == "1") {
    ipc_path = './jsonrpc1.ipc';
}

var shard_cnt = process.argv[3];
var shard_id = process.argv[4];

const web3 = new Web3(path.resolve(ipc_path), net);

var encodedTxs = [];

var sending = "./media/sanxing/meepo_bench/buy8192x50in"
var batchCnt = 50;
var batchGap =1000;
var hbCnt = 100;

var template = fs.readFileSync("sharded_shop.sol.template").toString();
sol_str = template.replace("{{shard_cnt}}", shard_cnt);

var input = {
    language: 'Solidity',
    sources: {
      'contract.sol': {
        content: sol_str
      }
    },
    settings: {
      outputSelection: {
        '*': {
          '*': ['*']
        }
      }
    }
  };
  
var output = JSON.parse(solc.compile(JSON.stringify(input)));
// console.log(output)
var creationCode = output.contracts["contract.sol"].ShardedShop.evm.bytecode.object;
console.log(creationCode.length)


var batchIndex = 0;
var totalSend = 0;
var totalReceive = 0;


function eth_sendRawTransaction(rawtx , callback){
    web3._requestManager.send({
        method: 'eth_sendRawTransaction',
        params: [rawtx],
    },  callback);
}

var startTime = new Date().getTime();
const privateKey = "0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318";
var txObj = {
    to: null,
    value: '0',
    gas: '4700000',
    nonce: 0,
    data: creationCode
};
web3.eth.accounts.signTransaction(txObj , privateKey).then(data=>{
    console.log(data.transactionHash);
    web3.eth.sendSignedTransaction(data.rawTransaction).then(data=>{
        console.log(data.transactionHash);
        startTime = new Date().getTime();
        sendOneBatch();
    });
});



var nextBlock = 0;
var confirmedCount = 0;
function updateConfirmedCount() {
    let theNext = nextBlock
    console.log("updating ConfirmedCount", confirmedCount, theNext)
    web3.eth.getBlockTransactionCount(theNext, function(err, data) {
        console.log("getBlock", theNext, err)
        if(err==null && data!=null) {
            console.log("getBlock", theNext, data)
            if (theNext == nextBlock){
                confirmedCount += data;
                nextBlock++
            }
        }
    });
}
setInterval(updateConfirmedCount, 500);





function sleep(ms) {
    return new Promise(resolve=>setTimeout(resolve, ms))
}

async function sendOneBatch() {
    console.log("sendOneBatch", totalSend-totalReceive);

    if(batchIndex>=(batchCnt+hbCnt)) {
        return console.log("finish");
    }
        
    encodedTxs = [];
    temps = []
    for (let buyId=0; buyId<32; buyId++) {
        if (shard_id == buyId){ //%shard_cnt) {
            temp = fs.readFileSync(sending+buyId+"/"+batchIndex).toString().split("\n");
            temps.push(temp);
        }
    }
    console.log("read temps.length=",temps.length)
    for (let temp_index=0; temp_index<temps[0].length; temp_index++) {
        for (i in temps) {
            encodedTxs.push(temps[i][temp_index])
        }
    }

    //console.log(encodedTxs);
    batchIndex++;
    for (i in encodedTxs) {
        if(encodedTxs[i]!="") {
            totalSend++;

            while (totalSend-confirmedCount > 20000) {
                // 10k buy in on block (gaslimit = 0xbebc200)
                console.log("wating");
                await sleep(500);
            }

            eth_sendRawTransaction(encodedTxs[i], function(err,data){
                totalReceive++;
                //console.log(err, data)
                //console.log(totalReceive);
                if ( totalReceive%10000==0 ){
                    var endTime  = new Date().getTime();
                    var duration = endTime-startTime;
                    var tps = totalReceive/(duration/1000);
                    console.log(totalReceive, tps);
                }
                if(totalSend==totalReceive) {
                    if (batchIndex-1<batchCnt)
                        setTimeout(sendOneBatch, batchGap);
                    else
                        setTimeout(sendOneBatch, 500);
                }
            });
        }
    }
}



contractAddress= "0xc0AAe1EdD7A76C8cf99E5bA3cA69599eD29540ea"