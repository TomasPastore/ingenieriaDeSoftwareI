require './receptive_account'

class ReceptiveAccountPrinter

  def initialize(account)
    @account = account
  end

  def print_account_summary_lines
    
    account_sumary_lines = []
    @account.transactions.each do | transaction | 
      account_sumary_lines << transaction.description
    end

    account_sumary_lines
  end  

end