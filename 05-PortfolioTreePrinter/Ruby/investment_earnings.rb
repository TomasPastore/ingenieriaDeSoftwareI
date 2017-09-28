require './query.rb'

class InvestmentEarnings < Query

    def initialize(account)
        @account = account
    end

    def consult
        value = 0
        @account.transactions.each do |transaction| value += transaction.consult(self) end
        value
    end

    def affect_query_with_certificate_of_deposit(certificate_of_deposit)
       certificate_of_deposit.value*(certificate_of_deposit.tna / 360.0) * certificate_of_deposit.days  
    end
end
