class CreateFunctions < ActiveRecord::Migration[5.1]
  def change
    create_table :functions do |t|
      t.string :fid
      t.string :name
      t.string :file
      t.string :text

      t.timestamps
    end
  end
end
