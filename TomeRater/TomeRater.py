class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        result = "{:50}{:12}{:12}\n".format("User Name/ Book Title", "Num Reads", "Avg Rating")
        for user in self.users.values():
            result = result + "{user:50}{nread:^10}{avg_rating:^10.1f}\n".format(user=user.__repr__()[:48], nread=len(user.books), avg_rating=user.get_average_rating())
        for book in self.books.keys():
            result = result + "{book:50}{nread:^10}{avg_rating:^10.1f}\n".format(book=book.__repr__()[:48], nread=self.books[book], avg_rating=book.get_average_rating())
        return result

    def __eq__(self, other):
        return self.users == other.users and self.books == other.books

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        # If user exists, add book to book list, rating it if raitng provided.
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                #Book does not exist in list. However dict is using title & ISBN to hash the key so
                #need to look for non-unique ISBN which might indicate incorrect data entry
                unique_isbn = True
                for check_book in self.books.keys():
                    if book.isbn == check_book.isbn:    #Different title but same isbn => problem. Do not add or rate book.
                        print("*WARNING* Unable to add book {title} as ISBN {isbn} already exists for a different title".format(title=book.title, isbn=book.isbn))
                        unique_isbn = False
                        continue
                if unique_isbn:     #Only gets here if not an existing book but has a new, unique isbn.
                    self.books[book] = 1
        else:
            print("*WARNING* No user with email {email}!".format(email=email))

    def add_user(self, name, email, user_books=None):
        # Check for syntactically valid email address using regular expression
        import re
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        result = pattern.match(email)
        if result:      #ie not None - the pattern match was found.
            #Check if email for user already exists. 
            if email in self.users.keys():
                print("*WARNING* Unable to add user {name} with email {email}. A user with that email already exists.".format(name=name, email=email))
            else:
                new_user = User(name, email)
                self.users[email] = new_user
            #If adding user with list of books read then add these to TomeRater.books
            if user_books:  #ie. if not None
                for book in user_books:
                    self.add_book_to_user(book, email)  #No rating provided - defaults to None
        else:           #regex pattern for valid email address was not found
            print("*WARNING* Unable to add user {name} with email {email} as not a valid email address".format(name=name, email=email))

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        result_list = [book for book, times_read in self.books.items() if times_read == max(self.books.values())]
        #There could be more than 1 book top equal. If not, return book object for compatibility with
        #specification and importing modules. If > 1 top equal then return a string representation of what should be displayed
        if len(result_list) > 1:
            res_str = ''
            for book in result_list:
                res_str = res_str + "{} Number of reads: {:3}\n".format(book.__repr__(), len(book.ratings))
            return res_str
        else:
            return result_list[0]

    def get_n_most_read_books(self, n):
        return sorted(self.books, key=self.books.get, reverse=True)[:n]

    def get_n_most_prolific_readers(self, n):
        user_list = list(self.users.values())
        return sorted(user_list, key=lambda user: len(user.books), reverse=True)[:n]
       
    def highest_rated_book(self):
        avg_ratings_list = [book.get_average_rating() for book in self.books.keys()]
        result_list = [book for book, avg_rating in zip(self.books.keys(), avg_ratings_list) if avg_rating == max(avg_ratings_list)]
        #Again, there could be more than 1 book top equal. If not, return book object for compatibility with
        #specification and importing modules. If > 1 top equal then return a string representation of what should be displayed
        if len(result_list) > 1:
            res_str = ''
            for book in result_list:
                res_str = res_str + "{} Average book rating: {:3.1f}\n".format(book.__repr__(), book.get_average_rating())
            return res_str
        else:
            return result_list[0]

    def  most_positive_user(self):
        #TomeRater.users is {email:user} Use .values() to get user object
        avg_ratings_list = [user.get_average_rating() for user in self.users.values()]
        result_list = [user for user, avg_rating in zip(self.users.values(), avg_ratings_list) if avg_rating == max(avg_ratings_list)]
        #Again, there could be more than 1 user top equal. If not, return user object for compatibility with
        #specification and importing modules. If > 1 top equal then return a string representation of what should be displayed
        if len(result_list) > 1:
            res_str = ''
            for user in result_list:
                res_str = res_str + "{} Average user rating: {:3.1f}\n".format(user.__repr__(), user.get_average_rating())
            return res_str
        else:
            return result_list[0]
           
        
class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address

    def __repr__(self):
        return "User: {user} email: {email}".format(user=self.name, email=self.email)

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating
        #what if self.books[book] already exists? Perhaps doesn't matter as could mean user has reread
        #and is re-rating the book. Not same as another user reading it and no need to prevent it.

    def get_average_rating(self):
        sum_ratings = 0
        num_ratings = 0
        for val in self.books.values():
            if val:    #ie rating is not None - a rating was provided
                sum_ratings += val
                num_ratings += 1
        try:                                        #Need to catch divbyzero error - user may not have rated any books
            return sum_ratings/num_ratings          #average of those who expressed a preference
        except ZeroDivisionError:
            if sum_ratings == 0:
                return 0
            else:
                print("*WARNING* Sum of ratings non-zero but number of ratings zero - problem somewhere!")
                return 9999
        
            
class Book():
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __repr__(self):
        return "Title: {title} ISBN: {isbn}".format(title=self.title, isbn=self.isbn)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Title: {title} ISBN updated to: {isbn}".format(title=self.title, isbn=self.isbn))

    def add_rating(self, rating):
        if type(rating) == int:
            if 0 <= rating <= 4:
                self.ratings.append(rating)
            else:
                print("*Warning* Invalid Rating")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def get_average_rating(self):
        try:                                                    #Need to catch divbyzero error - book may not have been rated
            return sum(self.ratings)/len(self.ratings)
        except ZeroDivisionError:
            if sum(self.ratings) == 0:
                return 0
            else:
                print("*WARNING* Sum of ratings non-zero but number of ratings zero - problem somewhere!")
                return 9999

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return(self.author)

    def __repr__(self):
        return "Title: {title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "Title: {title} A {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)
    
