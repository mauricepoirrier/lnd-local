from logging import debug
from config import LNDConfiguration
import router_pb2 as routerrpc, lightning_pb2 as lnrpc

def main() -> None:
    alice = LNDConfiguration(node_name="alice", GRPC_host="127.0.0.1:10001")
    bob = LNDConfiguration(node_name="bob", GRPC_host="127.0.0.1:10002")

    lightning_stub = alice.lightning_stub()
    request_invoice = lnrpc.Invoice(memo="Mac donlad", value=1000)

    response = lightning_stub.AddInvoice(request_invoice, metadata=[('macaroon', alice.macaroon)])

    routing_stub = bob.router_stub()
    request = routerrpc.SendPaymentRequest(
        payment_request=response.payment_request,
        fee_limit_sat=10000,
        allow_self_payment = True,
        timeout_seconds=120
    )

    for response in routing_stub.SendPaymentV2(request, metadata=[('macaroon', bob.macaroon)]):
        print(response)

if __name__ == '__main__':
    main()