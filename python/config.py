import codecs, grpc, os
import router_pb2_grpc as routerstub, lightning_pb2_grpc as lightningstub

class LNDConfiguration:
    def __init__(self, node_name = "bob", macaroon_path = None, cert_path = None, GRPC_host = "127.0.0.1:10002") -> None:
        if macaroon_path == None:
            macaroon_path = f"/Users/mpc/.polar/networks/1/volumes/lnd/{node_name}/data/chain/bitcoin/regtest/admin.macaroon"
        if cert_path == None:
            cert_path = f"/Users/mpc/.polar/networks/1/volumes/lnd/{node_name}/tls.cert"
        self.macaroon = codecs.encode(open(macaroon_path, "rb").read(), "hex")
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        self.cert = open(cert_path, "rb").read()
        self.ssl_creds = grpc.ssl_channel_credentials(self.cert)

        self.channel = grpc.secure_channel(GRPC_host, self.ssl_creds)

    def router_stub(self) -> routerstub.RouterStub:
        return routerstub.RouterStub(self.channel)
    
    def lightning_stub(self) -> lightningstub.LightningStub:
        return lightningstub.LightningStub(self.channel)