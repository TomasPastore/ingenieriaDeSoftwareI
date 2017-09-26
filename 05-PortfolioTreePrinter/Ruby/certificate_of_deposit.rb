require './transaction'

class CertificateOfDeposit < Transaction
  def self.register_for_on(capital,days,tna,account)
    self.should_implement
  end

end