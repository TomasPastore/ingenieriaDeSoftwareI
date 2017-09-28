require './transaction'

class Deposit < Transaction

  def initialize(value)
    @value = value
  end

  def value
    @value
  end

  def consult(query)
  	query.affect_query_with_deposit(self)
  end
  
  def description
  	"Depósito por #{@value}"
  end

end

