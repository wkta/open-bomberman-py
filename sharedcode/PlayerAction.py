import json


class PlayerAction:

    T_SYNCPOS, T_MOVEMENT, T_BOMB = range(1, 1+3)

    def __init__(self, actor_id: int, typeof_action: int, **kwargs):
        self.actor_id = actor_id
        self.action_t = typeof_action
        self._user_defs_attr = list()
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._user_defs_attr.append(k)

    @classmethod
    def deserialize(cls, serial):
        if serial[0] != 'a':
            raise ValueError('invalid PlayerAction serial! serial= {}'.format(serial))

        binf = serial.find('[')
        bsup = serial.find(']')+1
        actor_num, action_num = json.loads(serial[binf:bsup])
        args_str = serial[bsup:]
        args = json.loads(args_str)

        return cls(actor_num, action_num, **args)

    def serialize(self):
        res = 'a['
        res += str(self.actor_id) + ',' +str(self.action_t)
        res += ']'

        dico = dict()
        for attr in self._user_defs_attr:
            dico[attr] = getattr(self, attr)

        res += json.dumps(dico)
        return res


if __name__ == '__main__':
    p = PlayerAction(666, PlayerAction.T_BOMB, x=9, y=5)
    print(p.serialize())

    p = PlayerAction.deserialize('a[88,2]{"destx":5,"desty":99}')
    print('---')
    print(p.actor_id)
    print(p.action_t)
    print(p.destx)
    print(p.desty)
