require './transaction'

class TransferenceDeposit < Transaction

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

  def consult(query)
  	query.affect_query_with_transference_deposit(self)
  end	

  def transfer
    @transference
  end

  def description
  	"Transferencia por #{@value}"
  end

end
