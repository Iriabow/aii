from main.models import User, Book, Rating
from datetime import datetime

path = "csv"

def deleteTables():  
    Rating.objects.all().delete()
    Book.objects.all().delete()
    User.objects.all().delete()    

def populateFilms():
    print("Loading movies...")
       
    fileobj=open(path+"\\books.csv", "r")
    line=fileobj.readline()
    while line:
        data = line.split(',')
        try:
            if len(data)>1:
                isbn = int(data[0].strip())
                tit = data[1].strip() #.encode('utf-8', 'replace')
                author = data[2].strip()#.encode('utf-8', 'replace')
                if(data[3].strip() == 'Unknown'):
                    year = None
                else:
                    year = datetime.strptime(data[3].strip())
                publisher = data[4].strip()#.encode('utf-8', 'replace')
                Book.objects.create(ide=isbn, title=tit, author=author, year=year, publisher=publisher)  
            line=fileobj.readline()
        except:
            print("Error line: "+line)
    fileobj.close()
    
    print("Books inserted: " + str(Book.objects.count()))
    print("---------------------------------------------------------")

       
def populateRatings():
    print("Loading ratings...")
    
    fileobj=open(path+"\\ratings.csv", "r")
    line=fileobj.readline()
    while line:
        data = line.split(', ')
        try:
            if len(data)>1:
                User = User.objects.get(id = int(data[0].strip()))
                isbn = User.objects.get(id = int(data[1].strip()))
                Book_Rating = int(data[2].strip())
                Rating.objects.create(ide=User, book=isbn, Book_Rating=Book_Rating)
                User.objects.create(id=User)   
            line=fileobj.readline()
        except:
            print("Error line: "+line)
    fileobj.close()
       
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    deleteTables()
    populateFilms()
    populateRatings()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()