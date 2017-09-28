require './portfolio_tree_printer'

class ReversePortfolioTreePrinter

  def initialize(root_portfolio,account_names)
    @root_portfolio = root_portfolio
    @account_names = account_names
  end

  def lines
    return PortfolioTreePrinter.new(@root_portfolio,@account_names).lines.reverse
  end
end