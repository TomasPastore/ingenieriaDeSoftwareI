
class Stack

  @@STACK_EMPTY_ERROR_DESCRIPTION = "No element found"

  def initialize
    @stack = [EmptyNode.new(@@STACK_EMPTY_ERROR_DESCRIPTION)]
  end

  def push(an_object)
    @stack << (NodeWithValue.new an_object)
  end

  def pop   
    @stack.last.map_value_with lambda {
      |a_value|
      @stack.pop
      return a_value
    }

  end

  def top
    @stack.last.value
  end

  def empty?
    @stack.size == 1
  end

  def size
    @stack.size - 1
  end

  def self.stack_empty_error_description
    @@STACK_EMPTY_ERROR_DESCRIPTION
  end

  def should_implement
    raise 'Should be implemented'
  end

  module NodeInterface
  
    def value
      self.should_be_implemented_by_subclass
    end

    def map_value_with(a_block)
      self.should_be_implemented_by_subclass
    end 

    def should_be_implemented_by_subclass
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

    def map_value_with(a_block)
      a_block.call(@value)
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

    def map_value_with(*)
      value
    end
  end

end