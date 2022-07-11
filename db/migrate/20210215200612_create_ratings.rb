class CreateRatings < ActiveRecord::Migration[5.1]
  def change
    create_table :ratings do |t|
      t.integer :accurate
      t.integer :adequate
      t.integer :concise
      t.belongs_to :user
      t.belongs_to :comment

      t.timestamps
    end
  end
end
