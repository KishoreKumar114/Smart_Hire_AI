class ListADT:
    def __init__(self):   
        self.items = []

    def insert(self, item):
        self.items.append(item)
        print(f"{item} inserted into the list.")

    def delete(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} deleted from the list.")
        else:
            print(f"{item} not found in the list.")

    def search(self, item):
        if item in self.items:
            index = self.items.index(item)
            print(f"{item} found at position {index}.")
        else:
            print(f"{item} not found in the list.")

    def display(self):
        print("List contents:", self.items)

    def size(self):
        print("Size of the list:", len(self.items))



my_list = ListADT()

my_list.insert(10)
my_list.insert(20)
my_list.insert(30)

my_list.display()
my_list.size()

my_list.search(20)
my_list.search(50)

my_list.delete(20)
my_list.display()
my_list.delete(50)
s="rohith"
rev=""
for ch in s:
    rev=ch+rev
print(rev)
s="xxxxyyyzzz"
result=(max(set(s)))
print(result)
s = "xyzwxyxzwyzzx"



