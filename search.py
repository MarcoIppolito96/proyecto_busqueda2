"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

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
    #Algoritmo de ascension de colinas con reinicio aleatorio.

    def __init__(self)-> None:
        super().__init__()   # traemos los atributos de localsearch
        self.max_iters = 100 # definimos maximo de iteraciones permitidas
        self.max_resets = 100 # definimos maximo de reseteos permitidos

    def solve(self, problem : OptProblem):
        reset_count = 0
        start = time()
        best_value = float('-inf')
        best_solution = []

        while reset_count <= self.max_resets:
            if reset_count == 0:
                actual = problem.init
            else:
                actual = problem.random_reset()
            actual_value = problem.obj_val(actual)

            for _ in range(self.max_iters):
                self.niters += 1

                # buscar el mejor sucesor
                action, next_value = problem.max_action(actual)
                succesor = problem.result(actual, action)

                # revisar si el sucesor es mejor
                if next_value > best_value:
                    actual = succesor
                    actual_value = next_value
                else:
                    break

            if actual_value > best_value:
                best_value = actual_value
                best_solution = actual

            reset_count += 1
        

        end = time()
        self.time = end - start
        self.value = best_value
        self.tour = best_solution
      
        return self.tour


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
            self.tabu_list.append(action)

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

