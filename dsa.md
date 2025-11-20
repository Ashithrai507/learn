# What is a Data Structure?

### A Data Structure is a way to store and organize data in a computer so that it can be used efficiently.

A cupboard is a data structure — it helps you store and organize your clothes.

If your clothes are scattered, finding your favorite t-shirt will take time.

But if your cupboard (data structure) is organized — shirts in one place, pants in another — you can find things fast!

## Why are Data Structures Important?

Because every real-world program — from databases to games to AI models — relies on data.
How efficiently you store, access, and modify that data determines how fast and optimized your program will be.

A list of names can be stored in an array.

If you want to search quickly among millions of names, use a hash table or binary search tree.

If you want to manage tasks (like undo/redo), use a stack.

For handling queues (like print jobs or requests), use a queue.

## linear Data Structures

| Type            | Description                                           | Example Use               |
| --------------- | ----------------------------------------------------- | ------------------------- |
| **Array**       | Stores elements of the same type in contiguous memory | List of marks             |
| **Linked List** | Each element (node) has data + pointer to next        | Dynamic memory usage      |
| **Stack**       | LIFO (Last In, First Out) structure                   | Undo/Redo, Function calls |
| **Queue**       | FIFO (First In, First Out) structure                  | Task scheduling           |

here you can learn:
Array:[https://www.youtube.com/watch?v=G38hQKXa_RU]

## liked list:

Three types 

### **Singly Linked**

The singly linked list is the simplest form of linked list in which the node contains two members data and a next pointer that stores the address of the next node.

### **Doubly Linked List**

The doubly linked list is the modified version of the singly linked list where each node of the doubly linked consists of three data members data, next and prev. The prev is a pointer that stores the address of the previous node in the linked list sequence.

### **Circular Linked List**

Circular linked list can be represented as pointer to the first node where each node contains:

**Data: Actual information is stored.**
**Next: Pointer to the next node and last node Next is pointed to the first node of the linked list.**

### Stack

| Operation           | Description                               | Example                |
| ------------------- | ----------------------------------------- | ---------------------- |
| `push(x)`           | Adds element `x` to the top               | Push 10 → stack = [10] |
| `pop()`             | Removes top element                       | Pop → stack = []       |
| `top()` or `peek()` | Returns top element (without removing it) | Top → 10               |
| `empty()`           | Checks if stack is empty                  | Returns true/false     |
| `size()`            | Returns number of elements                | Size → 1               |


## Non-Linear Data Structures

| Type      | Description                                      | Example Use                        |
| --------- | ------------------------------------------------ | ---------------------------------- |
| **Tree**  | Hierarchical structure with root and child nodes | File systems, XML/HTML parsing     |
| **Graph** | Set of connected nodes (vertices) and edges      | Maps, networks, social connections |

## Hash-based Structures

| Type                      | Description                      | Example Use        |
| ------------------------- | -------------------------------- | ------------------ |
| **Hash Table / Hash Map** | Key-value pairs for quick lookup | Databases, caching |

### What is a Hash Table?

#### A hash table (or hash map) is a data structure that stores key–value pairs and allows extremely fast:

**Insertion**

**Deletion**

**Search**

All in O(1) average time.

#### 1. Key-Value Pair

Like:

Key = "Name"

Value = "Phone Number"

``` m
"apple"  →  100
"banana" →  200

```

#### 2. Hash Function

A function that converts a key into an index of the hash table.

Example:

``` m
hash("apple") → 2
hash("banana") → 5

```

#### 3. Index / Bucket

Position in the table where data is stored.

Example:

``` m
Index: 0  1  2         5 ...
Data : -  -  apple     banana  
```

#### 4. Collision

When two keys get mapped to the same index.

Example:
``` m
hash("cat") → 3
hash("dog") → 3
``` 

