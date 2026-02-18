class Solution:
    def reverseList(self, head):
        previous = None
        current = head

        while current is not None:
            nxt = current.next
            current.next = previous
            previous = current
            current = nxt

        return previous
