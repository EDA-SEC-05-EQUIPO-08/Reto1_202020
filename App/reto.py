"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt

from Sorting import insertionsort as insort
from Sorting import selectionsort as sort
from Sorting import shellsort

from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")


def loadCSVFile_2_at_once (file,file_1, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file
            Archivo csv del cual se importaran los datos
        sep = ";"
            Separador utilizado para determinar cada objeto dentro del archivo
        Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None  
    """
    lst = lt.newList("ARRAY_LIST") #Usando implementacion arraylist
    #lst = lt.newList() #Usando implementacion linkedlist
   
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            with open(file_1, encoding="utf-8") as csvfile2:
                countrdr = csv.DictReader(csvfile, dialect=dialect)
                totalrows = 0
                for row in countrdr:
                    totalrows += 1
                csvfile.seek(0)
                spamreader1 = csv.DictReader(csvfile2, dialect=dialect)
                for i in range(0,totalrows): 
                    lt.addLast(lst,{**next(spamreader),**next(spamreader1)})
    except:
        print("Hubo un error con la carga del archivo")
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return lst

def crear_ranking_de_peliculas(function, column, lst, elements):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        #Organiza la lista 
        #usa insertion sort
        #insort.insertionSort(lst, function,column)
        #usa selection sort
        #sort.selectionSort(lst,function,column)
        #usa shell sort
        shellsort.shellSort(lst,function,column)
        iterator = it.newIterator(lst)
        
        res=lt.newList()
        for i in range (0,elements):
            element = it.next(iterator)
            res1=lt.newList()
            lt.addLast(res1,element[column])
            lt.addLast(res1,element['title'])
            lt.addLast(res,res1)
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return res

def less(element1, element2,criterio='id'):
    if float(element1[criterio]) < float(element2[criterio]):
        return True
    return False
    
def greater(element1, element2,criterio='id'):
    if float(element1[criterio]) > float(element2[criterio]):
        return True
    return False

def conocer_a_un_director(criteria, column, lst):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    
    Retorna el numero de películas buenas o con votación positiva y el promedio de la votación  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    
    if lt.isEmpty(lst):
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        prom=0 #Promedio de votos por director
        iterator = it.newIterator(lst)
        size=lt.size(lst)
        res=lt.newList("ARRAY_LIST")
        res1=lt.newList("ARRAY_LIST")
        for i in range (0,size):
            element = it.next(iterator)
            if criteria.lower() in element[column].lower(): #filtrar por director  
                    counter+=1
                    lt.addLast(res1,{'title':element['title'],'average':element['vote_average']})
                    prom+=float(element["vote_average"])
        prom*=1/counter
        shellsort.shellSort(res1,greater,'average')
        lt.addLast(res,prom)
        lt.addLast(res,counter)
        lt.addLast(res,res1)
        
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return res

def conocer_a_un_actor(criteria, lst):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    
    Retorna el numero de películas buenas o con votación positiva y el promedio de la votación  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    
    if lt.isEmpty(lst):
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        prom=0 #Promedio de votos por director
        iterator = it.newIterator(lst)
        size=lt.size(lst)
        res=lt.newList("ARRAY_LIST")
        res1=lt.newList("ARRAY_LIST")
        directors=lt.newList("ARRAY_LIST")
        size_directors=0
        for j in range (1,6):
            busqueda="actor{}_name".format(j)
            for i in range (0,size):
                element = it.next(iterator)
                if criteria.lower() in element[busqueda].lower(): #filtrar por director  
                    counter+=1
                    lt.addLast(res1,{'title':element['title'],'average':element['vote_average'],'director':element['director_name'],'director_number':element['director_number']})
                    prom+=float(element["vote_average"])
                    lt.addLast(directors,{'director_name':element['director_name']})
            iterator = it.newIterator(lst)
        if counter>0:
            prom*=1/counter
        else: 
            prom=-1
        counter_dir=0

        shellsort.shellSort(res1,greater,'average')
        director_name=""
        count_new=0
        count=0
        for i in range (1,lt.size(res1)+1):
            name=lt.getElement(res1,i)['director']
            count_new=0
            for j in range (1,lt.size(res1)+1):
                if name in lt.getElement(res1,j)['director']:
                    count_new+=1
                else:
                    a=1
            
            if count<count_new:
                director_name=name
                count=count_new


        lt.addLast(res,director_name)
        lt.addLast(res,prom)
        lt.addLast(res,counter)
        lt.addLast(res,res1)
    
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return res

def entender_un_genero_cine(criteria,lst):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    
    Retorna el numero de películas buenas o con votación positiva y el promedio de la votación  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    
    if lt.isEmpty(lst):
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        prom=0 #Promedio de votos por director
        iterator = it.newIterator(lst)
        size=lt.size(lst)
        res=lt.newList("ARRAY_LIST")
        res1=lt.newList("ARRAY_LIST")
        directors=lt.newList("ARRAY_LIST")
        size_directors=0
        busqueda='genres'
        
        for i in range (0,size-1):
            element = it.next(iterator)
            if criteria.lower() in element[busqueda].lower(): #filtrar por director  
                counter+=1
                lt.addLast(res1,{'title':element['title'],'vote_average':element['vote_average'],'vote_count':element['vote_count'],'director_name':element['director_name'],'genres':element['genres']})
                prom+=float(element["vote_average"])
                lt.addLast(directors,{'director_name':element['director_name']})
           
            
        if counter>0:
            prom*=1/counter
        else: 
            prom=-1
        counter_dir=0

        shellsort.shellSort(res1,greater,'vote_average')
        director_name=""
        count_new=0
        count=0
        for i in range (1,lt.size(res1)+1):
            name=lt.getElement(res1,i)['director_name']
            count_new=0
            for j in range (1,lt.size(res1)+1):
                if name in lt.getElement(res1,j)['director_name']:
                    count_new+=1
                else:
                    a=1
            
            if count<count_new:
                director_name=name
                count=count_new


        lt.addLast(res,director_name)
        lt.addLast(res,prom)
        lt.addLast(res,counter)
        lt.addLast(res,res1)
    
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return res   

def crear_ranking_del_genero (function,column,lst,elements):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        #Organiza la lista 
        #usa insertion sort
        #insort.insertionSort(lst, function,column)
        #usa selection sort
        #sort.selectionSort(lst,function,column)
        #usa shell sort
        shellsort.shellSort(lst,function,column)
        iterator = it.newIterator(lst)
        
        res=lt.newList()
        for i in range (0,elements):
            element = it.next(iterator)
            res1=lt.newList()
            lt.addLast(res1,element[column])
            lt.addLast(res1,element['title'])
            lt.addLast(res1,element['genres'])
            lt.addLast(res,res1)
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return res


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lista=lt.newList("ARRAY_LIST")
                lista=loadCSVFile_2_at_once("Data/Kaggle/AllMoviesDetailsCleaned.csv","Data/Kaggle/AllMoviesCastingRaw.csv")
                #lista=loadCSVFile_2_at_once("Data/Kaggle/SmallMoviesDetailsCleaned.csv","Data/Kaggle/MoviesCastingRaw-small.csv")
                print("Datos cargados, "+str(lt.size(lista))+" elementos cargados")
            
            elif int(inputs[0])==2: #opcion 2
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    res=lt.newList()
                    print("Criterio de busqueda:  \n 1-Votos \n 2-Promedio")
                    criteria =input('Ingrese el criterio de búsqueda\n:')
                    if criteria=='1':
                        column='vote_count' 
                        criteria='conteo'
                        print("Criterio de busqueda:  \n 1-Peores peliculas segun %s \n 2-Mejores peliculas segun %s" %(criteria,criteria))
                        criteria =input('Ingrese el criterio de búsqueda\n:')
                        if criteria=='1':
                            function='less'
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                res=crear_ranking_de_peliculas(less, column, lista, numero_de_peliculas)
                                print("-{0:<50}{1:>8}".format("Titulo",column))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    
                                    print("-{0:<50}{1:>8}".format(title,count))
                            else:
                                print('Debe ser un numero mayor a 10')
                        elif criteria=='2':
                            function='greater'
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                res=crear_ranking_de_peliculas(greater, column, lista, numero_de_peliculas)
                                print("-{0:<50}{1:>8}".format("Titulo",column))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    
                                    print("-{0:<50}{1:>8}".format(title,count))
                            else:
                                print('Debe ser un numero mayor a 10')
                        else:
                            print ('Opción invalida') 
                                      
                    elif criteria=='2':
                        column='vote_average'
                        print("Criterio de busqueda:  \n 1-Peores peliculas segun %s \n 2-Mejores peliculas segun %s"%(column,column))
                        criteria =input('Ingrese el criterio de búsqueda\n:')
                        if criteria=='1':
                            function='less'   
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                res=crear_ranking_de_peliculas(less, column, lista, numero_de_peliculas)
                                print("-{0:<50}{1:>8}".format("Titulo",column))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    print("-{0:<50}{1:>8}".format(title,count))
                            else:
                                print('Debe ser un numero mayor a 10')         
                        elif criteria=='2':
                            function='greater'
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                res=crear_ranking_de_peliculas(greater, column, lista, numero_de_peliculas)
                                print("-{0:<50}{1:>8}".format("Titulo",column))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    
                                    print("-{0:<50}{1:>8}".format(title,count))
                            else:
                                print('Debe ser un numero mayor a 10')
                        else:
                            print ('Opción invalida')   
                    else:
                        print ('Opción invalida')

            elif int(inputs[0])==3: #opcion 3
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    res=lt.newList()
                    res=conocer_a_un_director(criteria,'director_name',lista)
                    title=lt.lastElement(res)
                    print("El director %s ha filmado %i peliculas y tiene una calificacion promedio de %f " % (criteria,lt.getElement(res,2),lt.getElement(res,1)))
                    print( '-{0:<50} {1:>8} '.format("Titulo","Calificación"))
                    for i in range (1,lt.size(title)+1):
                        print( '-{0:<50} {1:>8} '.format(lt.getElement(title,i)['title'],lt.getElement(title,i)['average']))
                                           
            elif int(inputs[0])==4: #opcion 4
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    res=lt.newList()
                    res=conocer_a_un_actor(criteria,lista)
                    title=lt.lastElement(res)
                    print("El actor %s ha filmado %i peliculas, tiene una calificacion promedio de %f y el director con el que mas trabaja es %s" % (criteria,lt.getElement(res,3),lt.getElement(res,2),lt.getElement(res,1)))
                    print( '-{0:<50} {1:>8} '.format("Titulo","Calificación"))
                    for i in range (1,lt.size(title)+1):
                        print( '-{0:<50} {1:>8} {2:>8} '.format(lt.getElement(title,i)['title'],lt.getElement(title,i)['average'],lt.getElement(title,i)['director']))

            elif int(inputs[0])==5: #opcion 5
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria =input('Ingrese el criterio de búsqueda\n')
                    res=lt.newList()
                    res=entender_un_genero_cine(criteria,lista)
                    title=lt.lastElement(res)
                    print("El genero %s tiene %i peliculas, tiene una calificacion promedio de %f y el director que mas ha contribuido es %s" % (criteria,lt.getElement(res,3),lt.getElement(res,2),lt.getElement(res,1)))
                    print( '-{0:<50} {1:>8} {2:>8}'.format("Titulo","Calificación","Director"))
                    for i in range (1,lt.size(title)+1):
                        print( '-{0:<50} {1:>8} {2:>8} '.format(lt.getElement(title,i)['title'],lt.getElement(title,i)['average'],lt.getElement(title,i)['director']))

            elif int(inputs[0])==6: #opcion 6
                 if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                 else:
                    res=lt.newList()
                    
                    genero =input('Ingrese el genero de busqueda:\n:')
                    print("Criterio de busqueda:  \n 1-Votos \n 2-Promedio")
                    criteria =input('Ingrese el criterio de búsqueda\n:')
                    if criteria=='1':
                        column='vote_count' 
                        criteria='conteo'
                        print("Criterio de busqueda:  \n 1-Peores peliculas segun %s \n 2-Mejores peliculas segun %s" %(criteria,criteria))
                        criteria =input('Ingrese el criterio de búsqueda\n:')
                        if criteria=='1':
                            function='less'
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                lista_genero=entender_un_genero_cine(genero,lista)
                                title=lt.lastElement(lista_genero)
                                res=crear_ranking_del_genero(less, column, title, numero_de_peliculas)
                                print("-{0:<50}{1:^20}{2:>8}".format("Titulo",column,"Genero"))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    gen=lt.getElement(res2,3)
                                    print("-{0:<50}{1:^20}{2:>8}".format(title,count,gen))
                            else:
                                print('Debe ser un numero mayor a 10')
                        elif criteria=='2':
                            function='greater'
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                lista_genero=entender_un_genero_cine(genero,lista)
                                title=lt.lastElement(lista_genero)
                                res=crear_ranking_del_genero(greater, column, title, numero_de_peliculas)
                                print("-{0:<50}{1:^20}{2:>8}".format("Titulo",column,"Genero"))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    gen=lt.getElement(res2,3)
                                    print("-{0:<50}{1:^20}{2:>8}".format(title,count,gen))
                        else:
                            print ('Opción invalida') 
                                      
                    elif criteria=='2':
                        column='vote_average'
                        print("Criterio de busqueda:  \n 1-Peores peliculas segun %s \n 2-Mejores peliculas segun %s"%(column,column))
                        criteria =input('Ingrese el criterio de búsqueda\n:')
                        if criteria=='1':
                            function='less'   
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                lista_genero=entender_un_genero_cine(genero,lista)
                                title=lt.lastElement(lista_genero)
                                res=crear_ranking_del_genero(less, column, title, numero_de_peliculas)
                                print("-{0:<50}{1:^20}{2:>8}".format("Titulo",column,"Genero"))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    gen=lt.getElement(res2,3)
                                    print("-{0:<50}{1:^20}{2:>8}".format(title,count,gen))
                            else:
                                print('Debe ser un numero mayor a 10')         
                        elif criteria=='2':
                            function='greater'
                            criteria =input('Cuantas peliculas desea ver: ')
                            if int(criteria) >=10:
                                numero_de_peliculas=int(criteria)
                                lista_genero=entender_un_genero_cine(genero,lista)
                                title=lt.lastElement(lista_genero)
                                res=crear_ranking_del_genero(greater, column, title, numero_de_peliculas)
                                print("-{0:<50}{1:^20}{2:>8}".format("Titulo",column,"Genero"))
                                for i in range (1,numero_de_peliculas+1): 
                                    res2=lt.getElement(res,i)
                                    title=lt.getElement(res2,2)
                                    count=lt.getElement(res2,1)
                                    gen=lt.getElement(res2,3)
                                    print("-{0:<50}{1:^20}{2:>8}".format(title,count,gen))
                            else:
                                print('Debe ser un numero mayor a 10')
                        else:
                            print ('Opción invalida')   
                    else:
                        print ('Opción invalida')

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()