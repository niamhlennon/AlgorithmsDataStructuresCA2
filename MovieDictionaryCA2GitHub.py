from functools import total_ordering
from math import log, ceil

#insert authorship, copyright, etc here

@total_ordering
class Movie:
    """ Represents a single Movie. """

    def __init__(self, movietuple):
        """ Initialise a Movie Object with a tuple of the 7 data elements. """
        if len(movietuple) != 7:
            print("ERROR - not a valid tuple: " + str(movietuple))
        else:
            self._title = movietuple[0]
            self._date = movietuple[1]
            self._time = movietuple[2]
            self._status = movietuple[3]
            self._pop = movietuple[4]
            self._vote = movietuple[5]
            self._count = movietuple[6]

    def __str__(self):
        """ Return a short string representation of this movie. """
        outstr = self._title
        return outstr

    def full_str(self):
        """ Return a full string representation of this movie. """
        outstr = self._title + ": "
        outstr = outstr + str(self._date) + "; "
        outstr = outstr + str(self._time) + "; "
        outstr = outstr + str(self._status) + "; "
        outstr = outstr + str(self._pop) + "; "
        outstr = outstr + str(self._vote) + "; "
        outstr = outstr + str(self._count)
        return outstr

    def get_title(self):
        """ Return the title of this movie. """
        return self._title

    def __eq__(self, other):
        """ Return True if this movie has exactly same title as other. """
        if (other._title == self._title): 
            return True
        return False

    def __ne__(self, other):
        """ Return False if this movie has exactly same title as other. """
        return not (self == other)

    def __lt__(self, other):
        """ Return True if this movie is ordered before other. 
            A movie is ordered before another if it's title is alphabetically
            before. 
        """
        if other._title > self._title:
            return True
        return False

class BSTNode:
    """ An internal node for a BST representing a MovieLibrary.
        Each node will store items with a movie title as a unique key.
    """
    
    def __init__(self, item):
        """ Initialise a BSTNode on creation, with value==item. """
        self._element = item
        self._leftchild = None
        self._rightchild = None
        self._parent = None

    def __str__(self):
        """ Return a string representation of the tree rooted at this node.
            The string will be created by an in-order traversal.
        """
        if self._element:
            if self._leftchild or self._rightchild:
                outstr = '(' + str(self._leftchild)
                outstr += ", " + str(self._element) + " , "
                outstr += str(self._rightchild) + ')'
                return outstr
            else:
                return str(self._element)
        else:
            return ''
               
    def _stats(self):
        """ Return the basic stats on the tree. """
        return ('size = ' + str(self.size())
               + '; height = ' + str(self.height()))
  
    def search(self, title):
        """ Return the first subtree rooted with that movie title, or None. """
        if title == self._element._title:
            return self
        elif title > self._element._title:
            if self._rightchild:
                return self._rightchild.search(title)
            else:
                return None 
        else: 
            if self._leftchild:
                return self._leftchild.search(title)
            else:
                return None 
            
    def add(self, movie):
        """ Add item to the tree, maintaining BST properties.
            Note: if a movie with same title is already in the tree,
            this does nothing.
        """
        movienode = BSTNode(movie)
        if self._element._title > movie._title:
            if self._leftchild is not None:
                self._leftchild.add(movie)
            else:
                self._leftchild = movienode
                movienode._parent = self
                
        elif self._element._title < movie._title:  
            if self._rightchild is not None:
                self._rightchild.add(movie)
            else:
                self._rightchild = movienode
                movienode._parent = self               
        
    def findmin(self): 
        """ Return the minimal element below this node. """
        minitem = self._findminnode()
        return minitem._element
    
    def _findminnode(self):  
        """ Return the BSTNode with the minimal element below this node. """
        minnode = self
        if self._leftchild != None:
            minnode = self._leftchild
            return minnode._findminnode()
        else:
            return minnode

    def findmax(self): 
        """ Return the maximal element below this node. """
        maxitem = self._findmaxnode()
        return maxitem._element

    def _findmaxnode(self): 
        """ Return the BSTNode with the maximal element below this node. """
        maxnode = self
        if self._rightchild != None:
            maxnode = self._rightchild
            return maxnode._findmaxnode()
        else:
            return maxnode
    
    def height(self):
        """ Return the height of this node.
            Note that with the recursive definition of the tree the height
            of the node is the same as the depth of the tree rooted at this
            node.
        """
        leftheight = -1
        rightheight = -1

        if self._leftchild != None:
            leftheight = self._leftchild.height()
        if self._rightchild != None:
            rightheight = self._rightchild.height()
        return (1 + max(leftheight, rightheight))
        

    def size(self):
        """ Return the size of this subtree.
            The size is the number of nodes (or elements) in the tree.
        """
        size = 0
        if self._leftchild:
            size += self._leftchild.size()
        if self._element:
            size += 1
        if self._rightchild:
            size += self._rightchild.size()
        return size
        

    def leaf(self):
        """ Return True if this node has no children. """
        if self._leftchild or self._rightchild:
            return False
        else:
            return True

    def semileaf(self):
        """ Return True if this node has exactly one child. """
        if self._leftchild and self._rightchild: 
            return False
        elif self._leftchild or self._rightchild: 
            return True
        else: 
            return False

    def full(self):
        """ Return true if this node has two children. """
        if self._leftchild and self._rightchild:
            return True
        else:
            return False

    def internal(self):
        """ Return True if this node has at least one child. """
        if self._leftchild or self._rightchild:
            return True
        else:
            return False

    def remove(self, title):
        """ Remove and return a movie.
            Remove the movie with the given title from the tree rooted at this node.
            Maintains the BST properties.
        """
        node = self.search(title)
        if node != None:
            return node._remove_node()
        else:
            return None
            
    def _remove_node(self):
        """ (Private) Remove this BSTBode from its tree.
            Maintains the BST properties.
        """

        #Internal/Full Node
           
        if self._leftchild and self._rightchild: 
            maxnode = self._leftchild
            while maxnode._rightchild != None: 
                maxnode = maxnode._rightchild
            self._pullup(maxnode) 
 

        #Leaf
        
        elif not self._leftchild and not self._rightchild:
            if self._parent:
                if self._element > self._parent._element:
                    self._parent._rightchild = None
                elif self._element < self._parent._element:
                    self._parent._leftchild = None
                else: 
                    if self._parent._leftchild == self:
                        self._parent._leftchild = None
                    else:
                        self._parent._rightchild = None
            self._parent = None
            temp = self._element
            self._element = None
            return temp
            

        #Semileaf
        
        elif not self._rightchild and self._leftchild:
            if self._parent:
                self._leftchild._parent = self._parent
                if self._leftchild._element > self._leftchild._parent._element:
                    self._leftchild._parent._rightchild = self._leftchild
                else:
                    self._leftchild._parent._leftchild = self._leftchild
                self._parent = None
                self._leftchild = None
                temp = self._element
                self._element = None
                return temp
            else: 
                self._pullup(self._leftchild._findmaxnode()) 
            

        elif not self._leftchild and self._rightchild:
            if self._parent:
                self._rightchild._parent = self._parent 
                if self._rightchild._element > self._rightchild._parent._element:
                    self._rightchild._parent._rightchild = self._rightchild 
                else:
                    self._rightchild._parent._leftchild = self._rightchild
                self._parent = None
                self._rightchild = None
                temp = self._element
                self._element = None
                return temp
            else: 
                self._pullup(self._rightchild._findminnode()) 


    def _pullup(self, node):  
        """ Pull up the data from a child (subtree) node into this BSTNode.
            Note: rather than updates the links so that the child node takes
            the place of the removed semileaf, instead, we will copy the
            child's element into the semileaf, and then read just the links, and
            then remove the now empty child node. This means that when we remove
            a root semileaf, the code that called the remove method still
            maintains a reference to the root of the tree, and so can continue
            processing the tree (otherwise, if we remvoed the actual BSTNode
            that was the root, the calling code would lose all reference to
            the tree). 
        """
        self._element = node._element 
        node.remove(node._element._title)
        
        
    def _print_structure(self):
        """ (Private) Print a structured representation of tree at this node. """

        outstr = str(self._element) + '(' + str(self.height()) + ')['
        if self._leftchild:
            outstr = outstr + str(self._leftchild._element) + ' '
        else:
            outstr = outstr + '* '
        if self._rightchild:
            outstr = outstr + str(self._rightchild._element) + ']'
        else:
            outstr = outstr + '*]'
        if self._parent:
            outstr = outstr + ' -- ' + str(self._parent._element)
        else:
            outstr = outstr + ' -- *'
        print(outstr)
        if self._leftchild:
            self._leftchild._print_structure()
        if self._rightchild:
            self._rightchild._print_structure()

    def _isthisapropertree(self):  
        """ Return True if this node is a properly implemented tree. """
        ok = True   
        
        if self._leftchild:                         
            if self._leftchild._parent != self:     
                print(self._leftchild._parent, self) 
                ok = False
            if self._leftchild._isthisapropertree() == False: 
                ok = False
                
        if self._rightchild:                        
            if self._rightchild._parent != self:    
                print(self._rightchild._parent, self) 
                ok = False
            if self._rightchild._isthisapropertree() == False: 
                ok = False
                
        if self._parent:                            
            if (self._parent._leftchild != self
                and self._parent._rightchild != self):  
                print(self._parent._leftchild, self._parent._rightchild, self)
                ok = False
        return ok

    def _testadd():
        node = BSTNode(Movie(("Memento", "11/10/2000", 113, "Released", 15.45, 8.1, 4168)))
        node._print_structure()
        print('> adding Melvin and Howard')
        node.add(Movie(("Melvin and Howard", "19/09/1980", 95, "Released", 6.737, 6.8, 18)))
        node._print_structure()
        print('> adding a second version of Melvin and Howard')
        node.add(Movie(("Melvin and Howard", "21/03/2007", 112, "Released", 4.321, 3.5, 7)))
        node._print_structure()
        print('> adding Mellow Mud')
        node.add(Movie(("Mellow Mud", "21/09/2016", 92, "Released", 9.321, 9.5, 7001)))
        node._print_structure()
        print('> adding Melody')
        node.add(Movie(("Melody", "21/03/2007", 113, "Released", 5.321, 3.5, 7)))
        node._print_structure()
        return node
       
    def _test():
        node = BSTNode(Movie(("B", "b", 1, "b", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "A")
        node.add(Movie(("A", "a", 1, "a", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "A")
        node.remove("A")
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(Movie(("C", "c", 1, "c", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "C")
        node.remove("C")
        print('Ordered:', node)
        node._print_structure()
        print('adding', "F")
        node.add(Movie(("F", "f", 1, "f", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "B")
        node.remove("B")
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(Movie(("C", "c", 1, "c", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "D")
        node.add(Movie(("D", "d", 1, "d", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "C")
        node.add(Movie(("C", "c", 1, "c", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "E")
        node.add(Movie(("E", "e", 1, "e", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "B")
        node.remove("B")
        print('Ordered:', node)
        node._print_structure()
        print('removing', "D")
        node.remove("D")
        print('Ordered:', node)
        node._print_structure()
        print('removing', "C")
        node.remove("C")
        print('Ordered:', node)
        node._print_structure()
        print('removing', "E")
        node.remove("E")
        print('Ordered:', node)
        node._print_structure()
        print('adding', "L")
        node.add(Movie(("L", "l", 1, "l", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "H")
        node.add(Movie(("H", "h", 1, "h", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "I")
        node.add(Movie(("I", "i", 1, "i", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('adding', "G")
        node.add(Movie(("G", "g", 1, "g", 1, 1, 1)))
        print('Ordered:', node)
        node._print_structure()
        print('removing', "L")
        node.remove("L")
        print('Ordered:', node)
        node._print_structure()
        print('removing', "H")
        node.remove("H")
        print('Ordered:', node)
        node._print_structure()
        print('removing', "I")
        node.remove("I")
        print('Ordered:', node)
        node._print_structure()
        print('removing', "G")
        node.remove("G")
        print('Ordered:', node)
        node._print_structure()
        print(node)

            
def read_movies(filename):
    """ Read and return a list of movies. """
    movies = []
    file = open(filename, 'r', encoding='utf-8')
    count = 0
    print(file)
    for line in file:
        line = line.replace('\n','')
        new_tuple = tuple(line.split('\t'))
        movies.append(Movie(new_tuple))
        #print(new_tuple[0])
        count += 1
    file.close()
    #for movie in movies:
        #print(movie)
    print("Read in " + str(count) + " movies ...")
    return movies

def build_tree(filename):
    movielist = read_movies(filename)
    bst = BSTNode(movielist[-1])
    movielist.pop()
    for movie in movielist:
        #print("Adding movie ", movie)
        bst.add(movie)
    print("Built a tree of height " + str(bst.height()))
    return bst

def min_tree_height(tree):
    """ Read and return a list of movies. """
    count = tree.size()
    return ceil(log(count+1, 2)-1) 
    
