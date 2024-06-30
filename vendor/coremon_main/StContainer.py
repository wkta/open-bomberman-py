from coremon_main.Singleton import Singleton
from coremon_main.util import underscore_format
import sys
import traceback


@Singleton
class StContainer:
    """
    contient toutes les instances de classes qui dérivent de BaseGameState
    """
    def __init__(self):
        self.__setup_done = False
        self.assoc_id_state_obj = dict()

    def setup(self, enum_game_states):
        self.__setup_done = True

        # -- initialisation d'après ce qu'on recoit comme enumeration...
        for id_choisi, nom_etat in enum_game_states.inv_map.items():
            nom_cl = nom_etat + 'State'

            # charger en mémoire la classe
            nom_module_py = underscore_format(nom_etat)
            chemin = 'app.{}.state'.format(nom_module_py)
                
            try:
                mod = __import__(chemin, fromlist=[nom_cl])
                klass = getattr(mod, nom_cl)

                # instanciation
                obj = klass(id_choisi, nom_etat)
                self.assoc_id_state_obj[id_choisi] = obj
                
            except ImportError as exc:
                sys.stderr.write("Error: failed to import class {} (info= {})\n".format(nom_cl, exc))
                traceback.print_last()
                print('nom_module_py={}'.format(nom_module_py))
                print('chemin={}'.format(chemin))

    def retrieve(self, identifiant):
        """
        :param identifiant: peut-être aussi bien le code (int) que le nom de classe dédiée (e.g. PlayState)
        :return: instance de BaseGameState
        """

        # construction par nom ou identifiant entier
        # TODO rétablir recherche par nom et non par code...

        # if isinstance(identifiant, str):
        #     gamestate_id = None
        #     for num_id, nom in state_listing.items():
        #         if nom == identifiant:
        #             gamestate_id = num_id
        #             break
        #     if gamestate_id is None:
        #         assert 0, "state name not found: " + identifiant
        # else:
        #     gamestate_id = identifiant
        gamestate_id = identifiant
        return self.assoc_id_state_obj[gamestate_id]
