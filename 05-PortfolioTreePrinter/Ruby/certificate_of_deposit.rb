require './transaction'

class CertificateOfDeposit < Transaction
  def self.register_for_on(capital,days,tna,account)
    transaction = self.new(capital,days,tna)
    account.register(transaction)
    transaction
  end

  def initialize(capital, days, tna)
    @capital = capital
    @days = days
    @tna = tna
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

  def consult(query)
  	query.affect_query_with_certificate_of_deposit(self)
  end

  def description
    "Plazo fijo por #{@capital} durante #{@days} días a una tna de #{@tna}"
  end

end