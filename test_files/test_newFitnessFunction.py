"""
Created on Friday July 30 15:23:38 2021

@author: vcoopman
"""

def fitnessFunction(population, generation_number):
    ''' rates the the individuals quality using sub-raters.

        Parameters
        -----------
        population : list
        generation_number: int

        Return
        ------
        fitnessArray: np.array

    '''

        """
        Idea: Crear varios subrates (heuristicas) que su resultado en total, sea el valor dado al individuo.
            - Cada uno de los subrates debe retornar un valor entre 0 y 1.
            - Cada subrater debe aspirar a un valor objetivo. Este valor objetivo es generado a partir
            de realizar el rating en individuos de la base de datos (ejemplo de lofi).
            - Para el resultado de cada subrater se utiliza una variable de influencia. Esta influencia del subrater se calcula
            a partir de los ejemplos de la base de datos. Utilizando la ecuacion:
                I = 2 * (0.5 - min(Target rating - Min rating, Max rating - Target rating)

            - El rating final del individuo se calcula:
                VF = SUM (Qk * Ik) / SUM (Ik)
                    k=1 --> n       k=1 --> n

        Como abordar el desarrollo:
            1. Implementar Subraters iniciales
                - Neighboring Pitch Range [DONE]
                - Direction of Melody [DONE]
                - Stability of Melody [DONE]
                - Syncopation of Notes (Not Sure) [DONE]
                - Pitch Range in Melody [DONE]
                - Variety of Silences Density [DONE BUT DIFFERENT]
                - Continuos Silence (Not Sure) [MISSING!]
                - Unique Note Pitches [DONE]
                - Equal Consecutive Notes [DONE]
                - Unique Rhythm Values [DONE]

                Estos subrater los deje afuera, ya que para nuestro caso creo q no aplican.
                - Variety of Note Density


            2. Testear utilizando "Target ratings" inventados y influencia pareja para los subraters.
            3. Idealmente buscar midis ejemplos y convertirlos (?).
        
        Requerimientos extras:
            1. Se quiere ofrecer una interfaz configurable para seleccionar los raters a utilizar --> NO
            2. Se quiere una interfaz facil de usar (idealmente un one-liner) --> YES!

        """
    pass
