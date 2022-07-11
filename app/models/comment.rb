class Comment < ApplicationRecord
  belongs_to :function
  has_many :ratings
  has_many :comparisons
end
