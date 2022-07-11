class Rating < ApplicationRecord
  belongs_to :user
  belongs_to :comment
  has_one :function, through: :comment
end
