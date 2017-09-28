require './query.rb'

class TransferNet < Query

    def initialize(account)
        @account = account
    end

    def consult(account)
        raise 'Implementar'
        value = 0
        @account.transactions.each do |transaction| value + transaction.consult(self) end
           value
    end

end