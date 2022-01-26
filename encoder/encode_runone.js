const path = require('path');
const net = require('net');
const Web3 = require('web3');
const fs = require('fs');
const process = require('process');

oneIndex = parseInt(process.argv[2])
shardsLen = parseInt(process.argv[3])

ipcPath = '/tmp/ipc'+oneIndex+'.ipc'
const web3 = new Web3(path.resolve(ipcPath), net);


const privateKey = "0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318";

aa = web3.eth.accounts.privateKeyToAccount(privateKey);
console.log(aa.address, oneIndex);

var oneBatch = 8192;
var batchCnt = 500;

var accountCnt = 256*shardsLen*400;
var theDir = "/media/sanxing/meepo_bench/transfer"+oneBatch+"x"+batchCnt+"of"+accountCnt+"/";

var hbCnt = 100;

fs.mkdir(theDir, console.log);

console.log("encode!");

function int2addr(num) {
    int_str = num.toString(16)
    len = 40 - int_str.length
    res = "0x"
    for (let i=0;i<len;++i) {
        res += "0"
    }
    res += int_str
    return res
}

function int2hex64(num) {
    int_str = num.toString(16)
    len = 64 - int_str.length
    res = ""
    for (let i=0;i<len;++i) {
        res += "0"
    }
    res += int_str
    return res
}

function signHB(batchIndex) {
    if (batchIndex>= (batchCnt+hbCnt) ) {
        return
    }
    if (batchIndex%16!=oneIndex) {
        return signHB(batchIndex+1)
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
        data: '0x90dd2627'+int2hex64(0)+int2hex64(nonce%accountCnt)+int2hex64(1)
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
    if (batchIndex%16!=oneIndex) {
        return signBatch(batchIndex+1)
    }

    if (fs.existsSync(theDir+batchIndex)) {
        console.log("exist", batchIndex)
        return signBatch(batchIndex+1)
    }

    console.log("batch", batchIndex)
    let encodedTxs = [];
    let beginNonce = oneBatch * batchIndex +1
    let endNonce = beginNonce + oneBatch -1

    let signOne = function(nonce, batchIndex) {
        //console.log("signing", nonce, batchIndex)
        var txObj = {
            to: '0xc0AAe1EdD7A76C8cf99E5bA3cA69599eD29540ea',
            value: '0',
            gas: 100000,
            nonce: nonce,
            data: '0x90dd2627'+int2hex64(0)+int2hex64(nonce%accountCnt)+int2hex64(1)
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