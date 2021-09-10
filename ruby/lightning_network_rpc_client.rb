# frozen_string_literal: true
require 'lnrpc'

# Ligtning client for specific node
class LightningNetworkRpcClient
  def initialize(host, node_name = 'bob', macaroon_path = nil, cert_path = nil)
    if macaroon_path.nil?
      @macaroon_path = "/Users/mpc/.polar/networks/1/volumes/lnd/#{node_name}/data/chain/bitcoin/regtest/admin.macaroon"
    end

    @cert_path = "/Users/mpc/.polar/networks/1/volumes/lnd/#{node_name}/tls.cert" if cert_path.nil?
    @host = host
  end

  def subscribe_invoices(options = {})
    lnrpc_client.lightning.subscribe_invoices(**options)
  end

  def pay_invoice(options = {})
    lnrpc_client.router.send_payment_v2(**options)
  end

  def add_invoice(options = {})
    lnrpc_client.lightning.add_invoice(**options)
  end

  private

  def lnrpc_client
    @lnrpc_client ||= Lnrpc::Client.new(
      credentials_path: @cert_path,
      macaroon_path: @macaroon_path,
      address: @host
    )
  end
end
