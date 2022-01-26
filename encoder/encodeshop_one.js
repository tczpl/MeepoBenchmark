const path = require('path');
const net = require('net');
const Web3 = require('web3');
const fs = require('fs');
const process = require('process');

oneIndex = parseInt(process.argv[2])
shardsLen = parseInt(process.argv[3])

ipcPath = '/tmp/ipc'+oneIndex%16+'.ipc'
const web3 = new Web3(path.resolve(ipcPath), net);

prikeyIndex = 1000+oneIndex

const privateKey = "0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f36"+prikeyIndex; // + 1000

aa = web3.eth.accounts.privateKeyToAccount(privateKey);
console.log(aa.address, oneIndex);

var oneBatch = 8192;
var batchCnt = 50;

var theDir = "/media/sanxing/meepo_bench/buy"+oneBatch+"x"+batchCnt+"in"+oneIndex+"/";

// extract the "buy" behavior from https://tianchi.aliyun.com/dataset/dataDetail?dataId=649
theRead = fs.readFileSync("/media/xijie/taobao/buy/"+oneIndex+".csv").toString();

lines = theRead.split("\n")
console.log(lines.length)
txs = []
lastTime = -1
lastUser = -1
lines.pop()
for (i in lines) {
    oneArray = lines[i].split(",");
    user = parseInt(oneArray[0])
    item = parseInt(oneArray[1])
    var timeStamp = parseInt(oneArray[4])
    if (timeStamp==lastTime && user==lastUser) {
        txs[txs.length-1][1].push(item)
        console.log(txs[txs.length-1])
    }
    else {
        lastTime = timeStamp
        lastUser = user
        txs.push([user, [item]])
    }
}
console.log(txs.length)

var encodedDataOf = []
var meeposhopdddContract = new web3.eth.Contract([{"constant":true,"inputs":[],"name":"settleFunc","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"billOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getPriceFunc","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"user","type":"uint256"},{"name":"item","type":"uint256"},{"name":"index","type":"uint256"},{"name":"length","type":"uint256"}],"name":"getPrice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"user","type":"uint256"},{"name":"prices","type":"uint256[50]"},{"name":"length","type":"uint256"}],"name":"settle","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"user","type":"uint256"},{"name":"items","type":"uint256[]"}],"name":"buy","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"calltype","type":"string"},{"indexed":false,"name":"shard","type":"uint256"},{"indexed":false,"name":"addr","type":"address"},{"indexed":false,"name":"func","type":"bytes32"},{"indexed":false,"name":"user","type":"uint256"},{"indexed":false,"name":"price","type":"uint256[50]"},{"indexed":false,"name":"length","type":"uint256"}],"name":"SEND","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"calltype","type":"string"},{"indexed":false,"name":"shard","type":"uint256"},{"indexed":false,"name":"addr","type":"address"},{"indexed":false,"name":"func","type":"bytes32"},{"indexed":false,"name":"user","type":"uint256"},{"indexed":false,"name":"item","type":"uint256"},{"indexed":false,"name":"index","type":"uint256"},{"indexed":false,"name":"length","type":"uint256"}],"name":"SEND","type":"event"}]);//, "0xc0AAe1EdD7A76C8cf99E5bA3cA69599eD29540ea");

for (i in txs) {
    tx = txs[i]
    var encodedData = meeposhopdddContract.methods.buy(tx[0], tx[1]).encodeABI();
    encodedDataOf.push(encodedData)
}

console.log("encodedDataOf", encodedDataOf.length)

var hbCnt = 100;

fs.mkdir(theDir, console.log);

console.log("encode!");

function signHB(batchIndex) {
    if (batchIndex>= (batchCnt+hbCnt) ) {
        process.exit()
    }

    if (fs.existsSync(theDir+batchIndex)) {
        signHB(batchIndex+1)
    }

    console.log("HB", batchIndex)
    let encodedTxs = [];
    let nonce = oneBatch * batchCnt + (batchIndex-batchCnt)

    var txObj = {
        to: '0xc0AAe1EdD7A76C8cf99E5bA3cA69599eD29540ea',
        value: '0',
        gas: 100000,
        nonce: nonce,
        data: '0x'
    };
    web3.eth.accounts.signTransaction(txObj , privateKey).then(data=>{
        var rawTx = data.rawTransaction;
        encodedTxs.push(rawTx);

        console.log("write!", batchIndex, encodedTxs.length);
        var toWrite = "";
        for (let i in encodedTxs){
            toWrite += encodedTxs[i]+"\n";
        }
        fs.writeFileSync(theDir+batchIndex, toWrite);
        signHB(batchIndex+1)
    });
}

function signBatch(batchIndex) {
    if (batchIndex>=batchCnt) {
        return signHB(batchIndex)
    }

    if (fs.existsSync(theDir+batchIndex)) {
        console.log("exist", batchIndex)
        return signBatch(batchIndex+1)
    }

    console.log("batch", batchIndex)
    let encodedTxs = [];
    let beginNonce = oneBatch * batchIndex
    let endNonce = beginNonce + oneBatch -1

    let signOne = function(nonce, batchIndex) {
        //console.log("signing", nonce, batchIndex)
        var txObj = {
            to: "0xc0AAe1EdD7A76C8cf99E5bA3cA69599eD29540ea",
            value: '0',
            gas: '4700000',
            nonce: nonce,
            data: encodedDataOf[(nonce-1)%encodedDataOf.length],
        };
        web3.eth.accounts.signTransaction(txObj , privateKey).then(data=>{
            var rawTx = data.rawTransaction;
            encodedTxs.push(rawTx);

            if (nonce == endNonce) {
                console.log("write!", batchIndex, encodedTxs.length);
                var toWrite = "";
                for (let i in encodedTxs){
                    toWrite += encodedTxs[i]+"\n";
                }
                //fs.writeFileSync("/media/sanxing/meepo_bench/transfer"+oneBatch+"x"+batchCnt+"of"+accountCnt+"/"+batchIndex, toWrite);
                fs.writeFileSync(theDir+batchIndex, toWrite);
                signBatch(batchIndex+1)
            }
            else {
                signOne(nonce+1, batchIndex)
            }
        });
    }

    signOne(beginNonce, batchIndex)
}

signBatch(0)