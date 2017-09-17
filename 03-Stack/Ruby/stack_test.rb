require "./stack"
require 'minitest/autorun'
require 'minitest/reporters'

MiniTest::Reporters.use!

class NumberTest < Minitest::Test

  def test_01_stack_should_be_empty_when_created

    stack = Stack.new

    assert stack.empty?
  end

  def test_02_push_add_elements_to_the_stack

    stack = Stack.new
    stack.push 'Something'

    assert !stack.empty?
  end

  def test_03_pop_removes_elements_from_the_stack

    stack = Stack.new
    stack.push 'Something'
    stack.pop

    assert stack.empty?
  end

  def test_04_pop_returns_last_pushed_object

    stack = Stack.new
    pushedObject = 'Something'
    stack.push pushedObject

    assert_equal pushedObject,stack.pop
  end

  def test_05_stack_behaves_LIFO

    stack = Stack.new
    firstPushedObject = 'first'
    secondPushedObject = 'second'
    stack.push firstPushedObject
    stack.push secondPushedObject

    assert_equal secondPushedObject,stack.pop
    assert_equal firstPushedObject,stack.pop
    assert stack.empty?
  end

  def test_06_top_returns_last_pushed_object

    stack = Stack.new
    firstPushedObject = 'first'
    stack.push firstPushedObject

    assert_equal firstPushedObject,stack.top
  end

  def test_07_top_does_not_remove_object_from_stack

    stack = Stack.new
    firstPushedObject = 'first'
    stack.push firstPushedObject

    assert_equal 1,stack.size
    stack.top
    assert_equal 1,stack.size
  end

  def test_08_can_not_pop_when_there_are_no_objects_in_the_stack

    stack = Stack.new

    begin
      stack.pop
      self.fail
    rescue Exception => anException
      assert_equal Stack.stack_empty_error_description, anException.message
    end
  end

  def test_09_can_not_top_when_there_are_no_objects_in_the_stack

    stack = Stack.new

    begin
      stack.top
      self.fail
    rescue Exception => anException
      assert_equal Stack.stack_empty_error_description, anException.message
    end
  end

end