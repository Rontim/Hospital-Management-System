from positional_list import PositionalList


class PriorityQueue:
    def __init__(self):
        self._data = PositionalList()

    def is_empty(self):
        return len(self._data) == 0

    def enqueue(self, item, priority):
        new_element = (item, priority)
        if self.is_empty():
            self._data.add_first(new_element)
        else:
            cursor = self._data.first()
            while cursor is not None:
                if priority < cursor.element()[1]:
                    self._data.add_before(cursor, new_element)
                    return
                cursor = self._data.after(cursor)
            self._data.add_last(new_element)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        highest_priority = self._data.first()
        cursor = self._data.first()
        while cursor is not None:
            if cursor.element()[1] < highest_priority.element()[1]:
                highest_priority = cursor
            cursor = self._data.after(cursor)
        return self._data.delete(highest_priority)

    def peek(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._data.first().element()

    def change_priority(self, item, new_priority):

        cursor = self._data.first()
        while cursor is not None:
            if cursor.element()[0] == item:

                old_priority = cursor.element()[1]
                self._data.delete(cursor)

                self.enqueue(item, new_priority)

                return f"Changed priority of {item} from {old_priority} to {new_priority}"

            cursor = self._data.after(cursor)

        return f"Item {item} not found in the priority queue"

    def __len__(self):
        return len(self._data)

    def __str__(self):
        elements = [str(item[0]) for item in self._data]
        return "PriorityQueue: " + ", ".join(elements)

    @property
    def data(self):
        return self._data


def print_menu():
    print("Priority Queue Menu:")
    print("1. Check the queue")
    print("2. Add item")
    print("3. Remove highest priority item")
    print("4. Check top item")
    print("5. Change priority of an item")
    print("6. Exit")


def main():
    pq = PriorityQueue()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            if pq.is_empty():
                print("Priority queue is empty.")
            else:
                print(pq)
        elif choice == "2":
            item = input("Enter the item: ")
            priority = int(input("Enter the priority: "))
            pq.enqueue(item, priority)
            print(f"Added item: {item} with priority {priority}")
        elif choice == "3":
            if pq.is_empty():
                print("Priority queue is empty.")
            else:
                removed_item = pq.dequeue()
                print(
                    f"Removed item: {removed_item[0]} with priority {removed_item[1]}")
        elif choice == "4":
            if pq.is_empty():
                print("Priority queue is empty.")
            else:
                top_item = pq.peek()
                print(f"Top item: {top_item[0]} with priority {top_item[1]}")

        elif choice == "5":
            item = input("Enter the item to change priority: ")
            new_priority = int(input("Enter the new priority: "))
            result = pq.change_priority(item, new_priority)
            print(result)

        elif choice == "6":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option (1-5).")


if __name__ == "__main__":
    main()
