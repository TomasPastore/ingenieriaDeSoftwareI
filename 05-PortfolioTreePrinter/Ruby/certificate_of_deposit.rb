require './transaction'

class CertificateOfDeposit < Transaction
  def self.register_for_on(capital,days,tna,account)
    transaction = self.new(capital,days.tna,account)
    account.register(transaction)
    transaction
  end

  def initialize(capital, days, tna, account)
    @capital = value
    @days = days
    @tna = tna
    @account = account
  end

  def value
    @capital
  end

  def days
    @days
  end

  def tna
    @tna
  end

  def account
    @account
  end

  def consult(query)
  	query.affect_query_with_certificate_of_deposit(self)
  end

end