class Comparison < ApplicationRecord
  belongs_to :user
  belongs_to :comment1, :class_name => "Comment"
  belongs_to :comment2, :class_name => "Comment"
  has_one :function, through: :comment1
end
