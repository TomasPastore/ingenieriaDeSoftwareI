require './transaction'

class CertificateOfDeposit < Transaction
  def self.register_for_on(capital,days,tna,account)
    self.should_implement
  end

  def initialize(value)
    @value = value
  end

  def value
    @value
  end

  
  def consult()

end