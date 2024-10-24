from ..logic.ModelManager import *
from ...model.client import *
from sqlalchemy import or_

class ClientCategoryManager (ModelManager):

    def __init__(self):
        super().__init__(ClientCategory)

    


