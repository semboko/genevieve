from typing import Optional

class LLItem:
    def __init__(self, value: int) -> None:
        self.value = value
        self.prev: Optional[LLItem] = None
        self.next: Optional[LLItem] = None


class LinkedList:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        
    def insert(self, value: int) -> None:
        item = LLItem(value)
        if self.left is None:
            self.left = item
            self.right = item
            return
        self.right.next = item
        item.prev = self.right
        self.right = item
    
    def search(self, value: int) -> Optional[LLItem]:
        item = self.left
        while item is not None:
            if item.value == value:
                return item
            item = item.next
        return None
            
        
    def delete(self, value: int) -> Optional[LLItem]:
        item = self.search(value)
        if item is None:
            return None
        
        prev_item = item.prev
        next_item = item.next
        
        prev_item.next = next_item
        next_item.prev = prev_item
        
        return item
    

some_list = LinkedList()
some_list.insert(15)
some_list.insert(50)
some_list.insert(10)
el50 = some_list.search(50)
elNone = some_list.search(11)
assert el50.value == 50
assert elNone == None
