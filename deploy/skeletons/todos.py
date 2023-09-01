from viur.core import conf
from viur.core.bones import *
from viur.core.skeleton import Skeleton


class TodosSkel(Skeleton):
    # Defaults
    description = StringBone(
        descr="Todo description",
        required=True
    )

    id = NumericBone(
        descr="Todo ID",
        required=True
    )

    done = BooleanBone(
        descr="Todo state",
        required=True
    )
