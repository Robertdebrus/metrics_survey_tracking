class CreateComparisons < ActiveRecord::Migration[5.1]
  def change
    create_table :comparisons do |t|
      t.integer :similarity
      t.belongs_to :comment1, foreign_key: {to_table: :comments}
      t.belongs_to :comment2, foreign_key: {to_table: :comments}
      t.belongs_to :user

      t.timestamps
    end
  end
end
