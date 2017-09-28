require './object'

class SummarizingAccountVisitor

  def visit_portfolio(portfolio)
    self.should_implement
  end

  def visit_receptive_account(account)
    self.should_implement
  end

end