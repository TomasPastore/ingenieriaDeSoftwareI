require './transaction'

class CertificateOfDeposit < Transaction
  def self.register_for_on(capital,days,tna,account)
    certificateOfDeposit = self.new(capital,days,tna)
    account.register(certificateOfDeposit)
    certificateOfDeposit
  end

  def initialize(capital,days,tna)
    @capital = capital
    @days = days
    @tna = tna
  end

  def value
    @capital
  end

  def affect_balance(balance)
    balance-@capital
  end

  def accept(transaction_visitor)
    transaction_visitor.visit_certificate_of_deposit(self)
  end

  def earnings
    @capital*(@tna/360)*@days
  end

  def days
    @days
  end

  def tna
    @tna
  end
end