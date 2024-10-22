"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)




class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1



class HillClimbingReset(LocalSearch):
    """Algoritmo de Ascensión de Colinas con Reinicio Aleatorio."""

    def __init__(self) -> None:
        """Inicializa el algoritmo con los parámetros necesarios"""
        super().__init__()
        self.max_iters = 100  # Máximo de iteraciones antes de reiniciar
        self.max_resets = 10  # Número máximo de reinicios permitidos

    def random_reset(self, problem: OptProblem):
        """Genera una nueva solución aleatoria como punto de partida."""
        return problem.random_reset()

    def solve(self, problem: OptProblem):
        """Implementa el proceso de Ascensión de Colinas con Reinicio Aleatorio."""
        # Inicio del reloj
        start = time()
        reset_count = 0  # Contador de reinicios
        best_solution = None
        best_value = float('-inf')  # Inicializamos con el peor valor posible
        
        while reset_count < self.max_resets:
            # Iniciamos desde un estado aleatorio o el inicial
            current_state = problem.init if reset_count == 0 else self.random_reset(problem)
            current_value = problem.obj_val(current_state)
            
            # Iteramos hasta encontrar un máximo local
            for _ in range(self.max_iters):
                self.niters += 1  # Contamos las iteraciones totales

                # Buscar el mejor sucesor del estado actual
                action, next_value = problem.max_action(current_state)
                next_state = problem.result(current_state, action)

                # Si el sucesor es mejor, nos movemos a ese estado
                if next_value > current_value:
                    current_state = next_state
                    current_value = next_value
                else:
                    # Si no hay mejoras, alcanzamos un máximo local
                    break
            
            # Actualizamos la mejor solución si encontramos una mejor
            if current_value > best_value:
                best_solution = current_state
                best_value = current_value

            # Reiniciamos el algoritmo
            reset_count += 1
        
        # Fin del reloj
        end = time()
        self.time = end - start
        self.tour = best_solution  # Guardamos la mejor solución encontrada
        self.value = best_value  # Guardamos el mejor valor objetivo encontrado

        return best_solution











"""
class Tabu(LocalSearch):
    #Algoritmo de busqueda tabu.

    def __init__(self) -> None:
        #Inicializa el algoritmo de búsqueda tabú con los parámetros necesarios.
        super().__init__()
        self.tabu_tenure = 10  # Capacidad de la lista tabú
        self.max_iters = 500  # Número máximo de iteraciones
        self.tabu_list = []  # Lista tabú para almacenar soluciones recientes


    def is_tabu(self, state) -> bool:
        #Verifica si el estado está en la lista tabú.
        return state in self.tabu_list


    def update_tabu_list(self, state):
        #Actualiza la lista tabú, añadiendo un nuevo estado y respetando su capacidad.
        self.tabu_list.append(state)
        if len(self.tabu_list) > self.tabu_tenure:
            self.tabu_list.pop(0)  # Mantener el tamaño de la lista tabú


    def solve(self, problem: OptProblem):
       #Implementa el proceso de búsqueda tabú
       # Inicio del reloj
       start = time()

       # Estado inicial
       actual = problem.init
       best = actual

       while self.niters < self.max_iters:
            self.niters += 1

            # Buscar la mejor acción que no esté en la lista tabú
            action, succ = problem.max_action(actual)
            sucesor = problem.result(actual, action)

            if not self.is_tabu(sucesor):
                # Actualizamos la lista tabú y el estado actual
                self.update_tabu_list(sucesor)
                actual = sucesor

                # Si encontramos una mejor solución, la guardamos
                if problem.obj_val(sucesor) > problem.obj_val(best):
                    best = sucesor
                    self.tour = best
                    self.value = problem.obj_val(best)

            # Si no hay mejores acciones o alcanzamos el límite, terminamos
            if self.niters >= self.max_iters:
                break

       # Fin del reloj
       end = time()
       self.time = end - start
"""




"""
class Tabu(LocalSearch):
   #Algoritmo de busqueda tabu.


   def solve(self, problem: OptProblem):
       # Inicio del reloj
       start = time()


       # Arrancamos del estado inicial
       actual = problem.init
       best = actual
       tabu = []
       while True:
           self.niters += 1
           action, succ = problem.max_action(actual)
           sucesor = problem.result(actual,action)
           if problem.obj_val(best) < problem.obj_val(sucesor):
               best = sucesor
               tabu.append(sucesor)
               self.tour = best
               self.value = succ
           actual = sucesor


           if self.niters == 100:
               break
      
       end = time()
       self.time = end-start
"""











class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""

    def __init__(self) -> None:
        super().__init__()
        self.tabu_tenure = 10  # Capacidad de la lista tabú
        self.max_iters = 100  # Número máximo de iteraciones
        self.max_no_improve = 20  # Máximas iteraciones sin mejorar
        self.tabu_list = []

    def is_tabu(self, action) -> bool:
        """Verifica si la acción está en la lista tabú."""
        return action in self.tabu_list

    def update_tabu_list(self, action):
        """Actualiza la lista tabú, añadiendo una nueva acción y respetando su capacidad."""
        self.tabu_list.append(action)

    def solve(self, problem: OptProblem):
        """Implementa el proceso de búsqueda tabú."""
        # Inicio del reloj
        start = time()

        # Estado inicial
        actual = problem.init
        best = actual
        best_value = problem.obj_val(best)
        no_improve_count = 0

        while self.niters < self.max_iters and no_improve_count < self.max_no_improve:
            self.niters += 1

            # Buscar la mejor acción que no esté en la lista tabú (o que cumpla con el criterio de aspiración)
            action, succ = problem.max_action(actual)
            sucesor = problem.result(actual, action)

            # Evaluamos si es tabú y si debemos permitirlo por el criterio de aspiración
            sucesor_value = problem.obj_val(sucesor)
            if self.is_tabu(action) and sucesor_value <= best_value:
                continue  # Si está en la lista tabú y no mejora, la ignoramos

            # Actualizamos la lista tabú con la nueva acción
            self.update_tabu_list(action)

            # Si encontramos una mejor solución, la actualizamos
            if sucesor_value > best_value:
                best = sucesor
                best_value = sucesor_value
                no_improve_count = 0  # Reiniciamos el contador de iteraciones sin mejora
            else:
                no_improve_count += 1  # Aumentamos el contador si no hay mejora

            actual = sucesor
            self.tour = best
            self.value = best_value

        # Fin del reloj
        end = time()
        self.time = end - start

        return best

