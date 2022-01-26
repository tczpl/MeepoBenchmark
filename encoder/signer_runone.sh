port=$((30300+$1))
rpcport=$((8800+$1))
wsport=$((9800+$1))
echo $port
rm /tmp/parity$1
./openethereum_sign  --chain demo-spec.json --ipc-path /tmp/ipc$1.ipc -d /tmp/parity$1 --port $port --jsonrpc-port $rpcport --ws-port $wsport --jsonrpc-apis web3,eth,net,personal,parity,parity_set,traces,rpc,parity_accounts
