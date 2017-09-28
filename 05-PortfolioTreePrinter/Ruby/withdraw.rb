require './transaction'

class Withdraw < Transaction
  def initialize(value)
    @value = value
  end

  def value
    @value
  end

  def consult(query)
    query.affect_query_with_withdraw(self)
  end 

  def description
    "Extracción por #{@value}"
  end

end
