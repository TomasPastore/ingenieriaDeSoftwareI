
class Stack

  @@stack_empty_error_description = "No element found"

  def initialize
    #@stack = [EmptyNode.new(@@stack_empty_error_description)]
    @stack = []

    class << @stack
      def pop_with_default
        self.last ? self.pop :  EmptyNode.new(@@stack_empty_error_description)
      end

      def top_with_default
        self.last ? self.last :  EmptyNode.new(@@stack_empty_error_description) 
      end
    end
    
  end


  def push(an_object)
    @stack << (NodeWithValue.new an_object)
  end

  def pop   
    @stack.pop_with_default.value
  end

  def top
    @stack.top_with_default.value
  end

  def empty?
    @stack.empty?
  end

  def size
    @stack.size
  end

  def self.stack_empty_error_description
    @@stack_empty_error_description
  end

  def should_implement
    raise 'Should be implemented'
  end

  module NodeInterface
    def value
      raise "Should be implemented by subclass"
    end
  end

  class NodeWithValue
    include NodeInterface
    def initialize(anObject)
      @value = anObject
    end

    def value
      @value
    end
  end

  class EmptyNode
    include NodeInterface
    def initialize(error_message_to_raise)
      @error_message = error_message_to_raise
    end

    def value
      raise @error_message
    end
  end

end