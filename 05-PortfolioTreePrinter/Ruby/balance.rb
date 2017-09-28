require './query.rb'

class Balance < Query
  
  def initialize(account)
  	@account = account
  end

  def consult
   	value = 0
    @account.transactions.each do |transaction| value + transaction.consult(self) end
  	value
  end

  def affect_query_with_deposit(deposit)
   deposit.value
  end 

  def affect_query_with_withdraw(withdraw)
   (-1) * withdraw.value
  end

  def affect_query_with_transference_withdraw(transference_withdraw)
   (-1) * transference_withdraw.value
  end

  def affect_query_with_transference_deposit(transference_deposit)
   transference_deposit.value
  end

  def affect_query_with_certificate_of_deposit(certificate_of_deposit)
   (-1) * certificate_of_deposit.value
  end

end