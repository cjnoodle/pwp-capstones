from TomeRater import *

Tome_Rater = TomeRater()

#Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
book2 = Tome_Rater.create_book("The Phone Book", 87654321)
book3 = Tome_Rater.create_book("Pi", 31412345)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
novel2 = Tome_Rater.create_novel("Journey to the Centre of the Earth", "Jules Verne", 31313)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

#Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")
Tome_Rater.add_user("Calum Adams", "calum@qwertyuiop.org")
Tome_Rater.add_user("Euan Adams", "ejpj@qwertyuiop.org")

#Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1, book3])

#Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 4)

Tome_Rater.add_book_to_user(novel1, "marvin@mit.edu", 4)
Tome_Rater.add_book_to_user(novel1, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 3)
Tome_Rater.add_book_to_user(novel3, "calum@qwertyuiop.org", 4)
Tome_Rater.add_book_to_user(novel2, "calum@qwertyuiop.org", 4)
Tome_Rater.add_book_to_user(book3, "ejpj@qwertyuiop.org", 4)

#Uncomment these to test your functions:
Tome_Rater.print_catalog()
Tome_Rater.print_users()
print("Printing Tome_Rater object: \n{tr}".format(tr=Tome_Rater))
print("Most positive user|(s):")
res=Tome_Rater.most_positive_user()
if type(res) == str:
    print(res)
else:
    print("{} Rating: {:3.1f}".format(res, res.get_average_rating()))
print("Highest rated book(s):")
res=Tome_Rater.highest_rated_book()
if type(res) == str:
    print(res)
else:
    print("{} Rating: {:3.1f}".format(res, res.get_average_rating()))
print("Most read book(s):")
res=Tome_Rater.get_most_read_book()
if type(res) == str:
    print(res)
else:
    print("{} Number of reads: {:3}".format(res, Tome_Rater.books[res]))
print("Top read books:")
print(Tome_Rater.get_n_most_read_books(3))
print("Most prolific readers:")
print(Tome_Rater.get_n_most_prolific_readers(3))

