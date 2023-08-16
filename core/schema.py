import graphene
from graphene_django import DjangoObjectType
#importar el modelo de libros
from books.models import Book

"""
Clase BookType dedicada a libros , es para saber ocmo van aa lucir los libros
cuando se consulten 
"""
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        #especificar los campos que requiero, los cuales estan definidos en books->models.py
        fields = ("id", "title", "description", "created_at", "updated_at")


#Clases para crear, borrar y actualizar libros, que se ejecutara cuando llame a a la class Mutation de abajo
class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()

    #lo que va a retornar , el libro y sus campos
    book = graphene.Field(BookType)

    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()
        #Retornar la instancia
        return CreateBookMutation(book=book)

class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    #devuelve un mensaje de que se ha borrado el libro
    message = graphene.String()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBookMutation(message = "Book deleted")
    
class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
    
    #lo que va a retornar , el libro y sus campos
    book = graphene.Field(BookType)

    def mutate(self, info, id,  title, description):
        book = Book.objects.get(pk=id)
        book.title = title
        book.description = description
        book.save()
        #Retornar la instancia
        return UpdateBookMutation(book=book)

    
########################

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello")
    #colocar el nombre de la consulta, es decir cuando consulten books
    #en este caso no quiero devolver 1 solo libro, sino una lista de libros
    books = graphene.List(BookType)
    #consulta para un solo libro, por ello se usa Field
    book = graphene.Field(BookType, id=graphene.ID())

    #funcion para consultar datos de todos los libros al modelo
    def resolve_books(self, info):
        return Book.objects.all()
    
    #funcion para consultar datos de un unico libro
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)


#Clase para realizar muutaciones ( cambios en la bd)
class Mutation(graphene.ObjectType):
    #crea un libro
    create_book = CreateBookMutation.Field()
    #borra un libro
    delete_book = DeleteBookMutation.Field()
    #actualiza libro
    update_book = UpdateBookMutation.Field()



#Agregar tambien la mutacion al schema
schema = graphene.Schema(query=Query, mutation=Mutation)


    # def resolve_hello(self, info):
    #     return "World"