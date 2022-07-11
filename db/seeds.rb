require 'csv'

table = CSV.parse(File.read("db/seeds.csv"), headers: true)

function_list = []

comment_list = []

table.each do |row|
  fid = row["fid"]
  fname = row["name"]
  ref = row["ref"]
  attendgru = row["attendgru"]
  ftext = row["function"]

  function = Function.create(fid: fid, name: fname, text: ftext)
  Comment.create( text: ref, source: "reference", function: function)
  Comment.create( text: attendgru, source: "alex1", function: function)
end


