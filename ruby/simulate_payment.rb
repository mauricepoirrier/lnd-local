require_relative 'lightning_network_rpc_client'

class SimulatePayment
  def run
    invoice = alice.add_invoice(value: 1000000000000, memo: 'Macdonald')
    puts "Invoice from alice: #{invoice.payment_request}"
    bob.pay_invoice(payment_request: invoice.payment_request, timeout_seconds: 120).each do |state|
      puts state.status
    end
  end

  def bob
    @bob ||= LightningNetworkRpcClient.new("127.0.0.1:10002", node_name = "bob")
  end

  def alice
    @alice ||= LightningNetworkRpcClient.new("127.0.0.1:10001", node_name = "alice")
  end
end


if $PROGRAM_NAME == __FILE__
  s = SimulatePayment.new
  s.run
end
