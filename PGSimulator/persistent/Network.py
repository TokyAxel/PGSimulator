from persistent.Branch import Branch
from typing import List, Any, Type, Dict


class Network:

    def __init__(self) -> None:
        self._branches = []
        self._bus = []
    
    def add_branch(self, branches_: List[Branch])->None:
        for branch in branches_:
            self._branches.append(branch)

    def add_branch(self, branch: Branch)->None:
        self._branches.append(branch)

    def remove_branch(self, branches_: List[Branch])->None:
        for branch in branches_:
            self._branches.remove(branch)

    def remove_branch(self, branch: Branch)->None:
        self._branches.remove(branch)

