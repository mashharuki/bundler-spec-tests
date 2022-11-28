import pytest
import requests
from dataclasses import asdict

from tests.types import RPCRequest
from tests.utils import is_valid_jsonrpc_response, requestId, assertRpcError
from .test_sendUserOperation import sendUserOperation


@pytest.mark.usefixtures('sendUserOperation')
def test_eth_getUserOperationReceipt(cmd_args, wallet_contract, userOp, w3):
    payload = RPCRequest(method="eth_getUserOperationReceipt", params=[requestId(wallet_contract, userOp)])
    response = requests.post(cmd_args.url, json=asdict(payload)).json()
    print(response)
    is_valid_jsonrpc_response(response)
    # TODO test receipt better
    assert response['result']['userOpHash'] == requestId(wallet_contract, userOp)
    receipt = w3.eth.getTransactionReceipt(response['result']['transactionHash'])
    assert response['result']['blockHash'] == receipt['blockHash'].hex()


def test_eth_getUserOperationReceipt_error(cmd_args):
    payload = RPCRequest(method="eth_getUserOperationReceipt", params=[''])
    bundler_response = requests.post(cmd_args.url, json=asdict(payload)).json()
    print(bundler_response)
    is_valid_jsonrpc_response(bundler_response)
    assertRpcError(bundler_response, 'Missing/invalid userOpHash')