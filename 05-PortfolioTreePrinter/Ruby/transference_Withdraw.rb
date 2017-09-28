require './transaction'

class TransferenceWithdraw < Transaction
  
  def self.register_for_on(amount, account, my_transference)
    transaction = self.new(amount, my_transference)
    account.register(transaction)
    transaction
  end

  def initialize(value, my_transference)
    @value = value
    @transference = my_transference
  end

  def value
    @value
  end

  def affect_balance(balance)
  	balance - @value
  end

  def affect_transferNet(trasnfer_net)
  	trasnfer_net - @value
  end	

  def transfer
    @transference
  end

  def description
  	"Transferencia por -#{@value}"
  end


end