const path = require('path');
const net = require('net');
const Web3 = require('web3');
const fs = require('fs');
const process = require('process');

var solc = require('solc');
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
var error_percent = 100// *100;

const web3 = new Web3(path.resolve(ipc_path), net);
//const web3 = new Web3("http://localhost:8545");
//aa = web3.eth.accounts.privateKeyToAccount(privateKey);
//console.log(aa);

var encodedTxs = [];

var sending = "/media/sanxing/meepo_bench/transfer8192x500of3276800/"
//var sending = "./media/sanxing/meepo_bench/transfer8192x400of3276800/"
//var sending = "./transfer3x100of10/"
//var sending = "./transfer100x100/";
var batchGap = 1000;
var batchCnt = 100;
var hbCnt = 0;
if (process.argv.length>4) {
    sending = "./media/sanxing/meepo_bench/"+process.argv[4]
    batchCnt = parseInt(process.argv[4].split("x")[1])
    batchGap = 0
    hbCnt = 100
}


if (process.argv.length>5) {
    error_percent = parseInt(process.argv[5])// *100;
}



var template = fs.readFileSync("sharded_error20.sol.template").toString();
sol_str = template.replace("{{shard_cnt}}", shard_cnt).replace("{{error_percent}}", error_percent);


console.log(shard_cnt, error_percent);

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
var creationCode = output.contracts["contract.sol"].ShardedERC20.evm.bytecode.object;
console.log(creationCode)



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
    console.log(data);
    web3.eth.sendSignedTransaction(data.rawTransaction).then(data=>{
        console.log(data);
        startTime = new Date().getTime();
        sendOneBatch();
    }).catch(data=>{
        console.log(data);
        startTime = new Date().getTime();
        sendOneBatch();
    });
});




function sendOneBatch() {
    console.log("sendOneBatch", totalSend-totalReceive);

    if(batchIndex>=(batchCnt+hbCnt)) {
        return console.log("finish");
    }
        
    encodedTxs = fs.readFileSync(sending+batchIndex).toString().split("\n");
    //console.log(encodedTxs);
    batchIndex++;
    for (i in encodedTxs) {
        if(encodedTxs[i]!="") {
            totalSend++;
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