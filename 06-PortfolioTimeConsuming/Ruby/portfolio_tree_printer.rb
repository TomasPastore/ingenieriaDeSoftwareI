require './summarizing_account_visitor'

class PortfolioTreePrinter < SummarizingAccountVisitor

  def initialize(portfolio,accountNames)
    @root_portfolio = portfolio
    @accountNames = accountNames
  end

  def lines
    @lines = []
    @spaces = 0

    @root_portfolio.accept(self)

    return @lines
  end

  def visit_portfolio(portfolio)
    @lines << self.line_for(portfolio)
    @spaces += 1
    portfolio.visit_accounts_with(self)
    @spaces -= 1
  end

  def visit_receptive_account(receptive_account)
    @lines << self.line_for(receptive_account)
  end

  def line_for(account_to_name)
    line = ''
    @spaces.times { line = line + ' ' }
    line = line + @accountNames[account_to_name]
    return line
  end
end