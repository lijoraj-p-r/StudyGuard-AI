"""
Core Logic and Data Management Module
-------------------------------------
Handles the foundational data structures, persistence, and logic of the system.
Contains the subject databases, interview question pool, motivational quotes,
and manager classes for stats and chat logging.
"""

import json
import os
from datetime import datetime, timedelta

# --- Configuration & Databases ---

# Collection of subjects with unique motivational focus messages.
KNOWN_SUBJECTS = {
    "physics": "Focus on the laws of nature. You've got this!",
    "math": "Logic and precision. Solve one problem at a time.",
    "java": "Think in objects. Debugging is part of the process.",
    "python": "Keep it clean and readable. Code is poetry.",
    "mysql": "Queries are just questions. Get the data!",
    "database": "Structure is everything. Understand normalization.",
    "dsa": "Efficiency is key. Optimize your thinking.",
    "aptitude": "Speed and accuracy. Sharpen your mind.",
    "history": "Understand the past to build the future.",
    "biology": "The science of life. Explore the details.",
    "chemistry": "It's all about the reactions. Stay balanced.",
    "english": "Expression matters. Refine your voice.",
    "economics": "Supply, demand, and logic. Analyze the trends."
}

# Questions and comprehensive explanations for various interview topics.
INTERVIEW_DB = {
    "java": [
    {"q": "What is a class in Java?", "a": "A class is a blueprint or template used to create objects. It defines properties (variables) and behaviors (methods)."},
    {"q": "What is an object in Java?", "a": "An object is an instance of a class that contains state (fields) and behavior (methods)."},
    {"q": "What are wrapper classes in Java?", "a": "Wrapper classes convert primitive data types into objects (e.g., int → Integer, double → Double)."},
    {"q": "What is the difference between primitive and non-primitive data types?", "a": "Primitive types store simple values (int, double, char); non-primitive types store references to objects (String, arrays, classes)."},
    {"q": "What is a static variable?", "a": "A static variable belongs to the class rather than instances and is shared among all objects of that class."},
    {"q": "What is a static method?", "a": "A static method belongs to the class and can be called without creating an object."},
    {"q": "What is the super keyword?", "a": "The super keyword refers to the immediate parent class object and is used to access parent methods and constructors."},
    {"q": "What is a default constructor?", "a": "A constructor automatically created by the compiler when no constructor is defined in the class."},
    {"q": "What is a parameterized constructor?", "a": "A constructor that accepts parameters to initialize object properties."},
    {"q": "What is constructor overloading?", "a": "Defining multiple constructors with different parameter lists in the same class."},

    {"q": "What is the difference between this() and super()?", "a": "this() calls another constructor in the same class, while super() calls the constructor of the parent class."},
    {"q": "What is a nested class?", "a": "A class defined within another class. It helps logically group classes used only in one place."},
    {"q": "What is a static nested class?", "a": "A nested class declared static that can be accessed without creating an instance of the outer class."},
    {"q": "What is an inner class?", "a": "A non-static nested class that requires an instance of the outer class to be created."},
    {"q": "What is an anonymous class?", "a": "A class without a name used to instantiate objects with slight modifications, often for interfaces or abstract classes."},
    {"q": "What is an enum in Java?", "a": "An enum is a special class used to represent a fixed set of constants."},
    {"q": "What is type casting?", "a": "Type casting converts one data type into another (e.g., double to int)."},
    {"q": "What is upcasting?", "a": "Upcasting is converting a subclass object into a superclass reference."},
    {"q": "What is downcasting?", "a": "Downcasting converts a superclass reference back into a subclass reference."},
    {"q": "What is the instanceof operator?", "a": "instanceof checks whether an object belongs to a particular class or subclass."},

    {"q": "What is a marker interface?", "a": "An empty interface used to signal to the JVM that a class has special behavior (e.g., Serializable)."},
    {"q": "What is the difference between throw and throws?", "a": "throw is used to explicitly throw an exception; throws declares exceptions that a method may throw."},
    {"q": "What is a custom exception?", "a": "A user-defined exception class created by extending Exception or RuntimeException."},
    {"q": "What is the try-with-resources statement?", "a": "A try block that automatically closes resources like files or streams after execution."},
    {"q": "What is the difference between Error and Exception?", "a": "Error represents serious system issues; Exception represents conditions that a program can catch and handle."},
    {"q": "What is the Optional class?", "a": "Optional is a container object that may or may not contain a non-null value."},
    {"q": "What is the difference between == and equals() for Strings?", "a": "== compares references; equals() compares the actual string values."},
    {"q": "What is the String pool?", "a": "A memory area in the heap where Java stores string literals to optimize memory usage."},
    {"q": "What is immutability in Java?", "a": "An immutable object cannot change its state after creation (e.g., String)."},
    {"q": "What is cloning in Java?", "a": "Cloning creates a copy of an existing object using the clone() method."},

    {"q": "What is shallow copy?", "a": "A shallow copy duplicates the object but not the objects it references."},
    {"q": "What is deep copy?", "a": "A deep copy duplicates both the object and the objects it references."},
    {"q": "What is the difference between ArrayList and LinkedList?", "a": "ArrayList uses dynamic arrays for faster access; LinkedList uses nodes for faster insertion/deletion."},
    {"q": "What is a HashSet?", "a": "A HashSet is a collection that stores unique elements and does not maintain order."},
    {"q": "What is a LinkedHashSet?", "a": "LinkedHashSet stores unique elements and maintains insertion order."},
    {"q": "What is a TreeSet?", "a": "TreeSet stores unique elements in sorted order."},
    {"q": "What is a PriorityQueue?", "a": "A queue that orders elements based on priority rather than insertion order."},
    {"q": "What is the difference between Iterator and ListIterator?", "a": "Iterator traverses forward only; ListIterator can traverse both forward and backward."},
    {"q": "What is a Map in Java?", "a": "A Map stores key-value pairs where each key is unique."},
    {"q": "What is LinkedHashMap?", "a": "LinkedHashMap maintains insertion order of key-value pairs."},

    {"q": "What is TreeMap?", "a": "TreeMap stores keys in sorted order based on natural ordering or a comparator."},
    {"q": "What is ConcurrentHashMap?", "a": "A thread-safe version of HashMap designed for concurrent access."},
    {"q": "What is a thread lifecycle?", "a": "Thread lifecycle includes states such as New, Runnable, Running, Blocked, and Terminated."},
    {"q": "What is thread synchronization?", "a": "A mechanism that ensures only one thread accesses a critical section at a time."},
    {"q": "What is the wait() method?", "a": "wait() pauses the current thread until another thread invokes notify() or notifyAll()."},
    {"q": "What is notify()?", "a": "notify() wakes up a single waiting thread on the object's monitor."},
    {"q": "What is notifyAll()?", "a": "notifyAll() wakes up all threads waiting on the object's monitor."},
    {"q": "What is the Executor framework?", "a": "A framework that simplifies thread management using thread pools."},
    {"q": "What is a Callable interface?", "a": "Callable is similar to Runnable but can return a result and throw exceptions."},
    {"q": "What is a Future object?", "a": "Future represents the result of an asynchronous computation that may not yet be completed."}
],
    "python": [
        {"q": "What is the difference between List and Tuple?", "a": "Lists are mutable (changeable whiteboards); Tuples are immutable (stone tablets). Tuples are faster."},
        {"q": "What is a Decorator in Python?", "a": "A function that wraps another to extend its behavior without modifying the source (like gift wrap)."},
        {"q": "Explain PEP 8.", "a": "The official style guide for Python code formatting, ensuring readability."},
        {"q": "How is memory managed in Python?", "a": "Via a private heap, reference counting, and a cyclic garbage collector."},
        {"q": "What are Python Generators and why use them?", "a": "Lazy iterators that yield items one by one, saving memory for large datasets."},
        {"q": "What is the difference between 'is' and '=='?", "a": "'==' compares value; 'is' compares identity (memory location)."},
        {"q": "Explain List Comprehension in Python.", "a": "An elegant, one-line way to create lists based on existing iterables."}
    ],
    "mysql": [
{"q":"What is the difference between DELETE and TRUNCATE?","a":"DELETE is DML (surgical, rollable-back); TRUNCATE is DDL (resets table, faster, no undo)."},
{"q":"What are Joins and their types?","a":"Methods to link tables. Inner (matches both), Left (all left + matches), Right, Full."},
{"q":"What is an Index and why is it used?","a":"Data structure to speed up data retrieval (like a book index)."},
{"q":"What is a Primary Key vs Unique Key?","a":"Primary Key (unique, no nulls, one per table); Unique Key (unique, allows one null)."},
{"q":"What is the difference between GROUP BY and ORDER BY?","a":"GROUP BY aggregates data; ORDER BY sorts the result."},
{"q":"Explain UNION vs UNION ALL in MySQL.","a":"UNION removes duplicates; UNION ALL keeps duplicates and is faster."},
{"q":"What are Aggregate Functions in MySQL?","a":"Functions performing calculations on sets (COUNT, SUM, AVG, MAX, MIN)."},
{"q":"What is a Foreign Key?","a":"A field that links to the primary key of another table to maintain referential integrity."},
{"q":"What is Normalization?","a":"Process of organizing data to reduce redundancy and improve integrity."},
{"q":"What is Denormalization?","a":"Combining tables to reduce joins and improve read performance."},
{"q":"What is the difference between WHERE and HAVING?","a":"WHERE filters rows before grouping; HAVING filters after GROUP BY."},
{"q":"What is a View in MySQL?","a":"A virtual table created from a query."},
{"q":"What is a Stored Procedure?","a":"Precompiled SQL code stored in the database and executed when called."},
{"q":"What is a Trigger?","a":"A procedure automatically executed when a specific event occurs on a table."},
{"q":"What is a Subquery?","a":"A query nested inside another SQL query."},
{"q":"What is the difference between CHAR and VARCHAR?","a":"CHAR is fixed-length; VARCHAR is variable-length."},
{"q":"What is the LIMIT clause?","a":"Restricts the number of rows returned in a query."},
{"q":"What is the DISTINCT keyword?","a":"Removes duplicate values from query results."},
{"q":"What is AUTO_INCREMENT?","a":"Automatically generates sequential numbers for a column."},
{"q":"What is a Composite Key?","a":"A primary key made from multiple columns."},
{"q":"What is a Candidate Key?","a":"A column that can qualify as a primary key."},
{"q":"What is a Super Key?","a":"A set of attributes that uniquely identifies rows."},
{"q":"What is a Surrogate Key?","a":"Artificial key (often auto-generated) used instead of natural keys."},
{"q":"What is a Self Join?","a":"Joining a table with itself."},
{"q":"What is a Cross Join?","a":"Returns Cartesian product of two tables."},
{"q":"What is the difference between INNER JOIN and OUTER JOIN?","a":"INNER JOIN returns matches only; OUTER JOIN also includes non-matching rows."},
{"q":"What is a Temporary Table?","a":"A table that exists only during the database session."},
{"q":"What is the BETWEEN operator?","a":"Filters values within a specified range."},
{"q":"What is the IN operator?","a":"Checks if a value matches any value in a list."},
{"q":"What is the LIKE operator?","a":"Used for pattern matching in strings."},
{"q":"What are Wildcards in SQL?","a":"Special characters for pattern search like % and _."},
{"q":"What is the EXISTS operator?","a":"Checks if a subquery returns any records."},
{"q":"What is COALESCE()?","a":"Returns the first non-null value from a list."},
{"q":"What is IFNULL()?","a":"Replaces NULL with a specified value."},
{"q":"What is a Transaction?","a":"A sequence of database operations treated as a single unit."},
{"q":"What are ACID properties?","a":"Atomicity, Consistency, Isolation, Durability ensuring reliable transactions."},
{"q":"What is COMMIT?","a":"Saves all changes made in a transaction."},
{"q":"What is ROLLBACK?","a":"Reverts changes made in the current transaction."},
{"q":"What is SAVEPOINT?","a":"Creates a point within a transaction to roll back to."},
{"q":"What is a Cursor?","a":"A pointer used to process query results row by row."},
{"q":"What is a Database Schema?","a":"Logical structure defining tables, relationships, and constraints."},
{"q":"What is a Constraint?","a":"Rules applied to columns (PRIMARY KEY, NOT NULL, UNIQUE)."},
{"q":"What is NOT NULL constraint?","a":"Ensures a column cannot store NULL values."},
{"q":"What is DEFAULT constraint?","a":"Assigns a default value when none is provided."},
{"q":"What is CHECK constraint?","a":"Ensures column values meet a specific condition."},
{"q":"What is a Clustered Index?","a":"Determines the physical order of data in a table."},
{"q":"What is a Non-Clustered Index?","a":"Separate structure pointing to table data."},
{"q":"What is the EXPLAIN statement?","a":"Shows the execution plan of a SQL query."},
{"q":"What is a Data Warehouse?","a":"Central repository for large analytical datasets."},
{"q":"What is OLTP?","a":"Online Transaction Processing systems for day-to-day operations."},
{"q":"What is OLAP?","a":"Online Analytical Processing for complex queries and analysis."},
{"q":"What is Sharding?","a":"Splitting a large database into smaller pieces across servers."},
{"q":"What is Replication?","a":"Copying database data across multiple servers."},
{"q":"What is a Deadlock?","a":"Situation where transactions wait on each other indefinitely."},
{"q":"What is a Materialized View?","a":"A stored view containing query results physically."},
{"q":"What is the difference between DROP and TRUNCATE?","a":"DROP removes the table completely; TRUNCATE removes all rows but keeps structure."},
{"q":"What is a Data Type in SQL?","a":"Defines the type of data a column can store."},
{"q":"What is JSON data type in MySQL?","a":"Used to store JSON formatted data."},
{"q":"What is a Full Text Index?","a":"Index used for fast text searching within large text columns."},
{"q":"What is a Stored Function?","a":"A stored routine that returns a single value."}
],
  "database": [
{"q":"What is Database Normalization?","a":"Organizing data to reduce redundancy and improve integrity."},
{"q":"Explain ACID properties.","a":"Atomicity, Consistency, Isolation, Durability – ensuring reliable database transactions."},
{"q":"What is a Foreign Key?","a":"A column that links to a Primary Key in another table, enforcing referential integrity."},
{"q":"Explain NoSQL vs SQL.","a":"SQL uses relational tables with fixed schema; NoSQL uses flexible schemas like document or key-value."},
{"q":"What is a Database Transaction?","a":"A sequence of operations treated as a single unit (all succeed or all fail)."},
{"q":"Explain Data Integrity and its types.","a":"Ensures accuracy and consistency of data (Entity, Domain, Referential Integrity)."},
{"q":"What is the CAP Theorem?","a":"In distributed systems you can only guarantee two of: Consistency, Availability, Partition Tolerance."},
{"q":"What is a Database Schema?","a":"Logical structure that defines tables, relationships, and constraints."},
{"q":"What is Data Redundancy?","a":"Unnecessary duplication of data in a database."},
{"q":"What is Data Consistency?","a":"Ensuring data remains accurate and uniform across the database."},
{"q":"What is a Relational Database?","a":"A database that stores data in tables with relationships between them."},
{"q":"What is a Distributed Database?","a":"A database spread across multiple physical locations."},
{"q":"What is Data Modeling?","a":"Designing the structure of a database using entities, attributes, and relationships."},
{"q":"What is an Entity?","a":"A real-world object or concept represented in a database."},
{"q":"What is an Attribute?","a":"A property or characteristic of an entity."},
{"q":"What is an ER Diagram?","a":"Entity-Relationship diagram used to visually design database structure."},
{"q":"What is Cardinality?","a":"Defines the number of relationships between entities (1:1, 1:N, N:M)."},
{"q":"What is Data Dictionary?","a":"A centralized repository describing database metadata."},
{"q":"What is Metadata?","a":"Data that describes other data."},
{"q":"What is Database Indexing?","a":"Technique to improve query performance using special data structures."},
{"q":"What is a Clustered Database?","a":"A database system where multiple servers work together as one."},
{"q":"What is Database Replication?","a":"Copying data from one database server to another."},
{"q":"What is Database Sharding?","a":"Splitting a database into smaller pieces distributed across servers."},
{"q":"What is Data Warehousing?","a":"Storing large volumes of historical data for analysis."},
{"q":"What is ETL?","a":"Extract, Transform, Load – process of moving data into a warehouse."},
{"q":"What is OLTP?","a":"Online Transaction Processing for real-time operations."},
{"q":"What is OLAP?","a":"Online Analytical Processing for complex analytical queries."},
{"q":"What is a Data Mart?","a":"A smaller subset of a data warehouse for a specific business unit."},
{"q":"What is Data Mining?","a":"Process of discovering patterns and insights from large datasets."},
{"q":"What is Database Backup?","a":"Copy of database data used for recovery."},
{"q":"What is Database Recovery?","a":"Restoring database after failure or data loss."},
{"q":"What is Checkpoint in DBMS?","a":"Point where database state is saved for recovery."},
{"q":"What is Log File in DBMS?","a":"File recording all database transactions for recovery purposes."},
{"q":"What is Concurrency Control?","a":"Managing simultaneous operations without conflicts."},
{"q":"What is Locking in DBMS?","a":"Mechanism to control access to data during transactions."},
{"q":"What is Deadlock in DBMS?","a":"Situation where transactions wait indefinitely for each other’s locks."},
{"q":"What is Two-Phase Locking?","a":"Protocol ensuring serializability using growing and shrinking lock phases."},
{"q":"What is Isolation Level?","a":"Degree to which transactions are isolated from each other."},
{"q":"What are the Isolation Levels?","a":"Read Uncommitted, Read Committed, Repeatable Read, Serializable."},
{"q":"What is Phantom Read?","a":"When a transaction sees new rows added by another transaction."},
{"q":"What is Dirty Read?","a":"Reading uncommitted data from another transaction."},
{"q":"What is Non-Repeatable Read?","a":"Reading the same row twice but getting different values."},
{"q":"What is Data Partitioning?","a":"Dividing large tables into smaller parts for performance."},
{"q":"What is Horizontal Partitioning?","a":"Splitting rows across multiple tables."},
{"q":"What is Vertical Partitioning?","a":"Splitting columns across multiple tables."},
{"q":"What is Database Security?","a":"Protecting database from unauthorized access."},
{"q":"What is Authentication in DBMS?","a":"Verifying identity of users accessing database."},
{"q":"What is Authorization in DBMS?","a":"Granting permissions to access specific data."},
{"q":"What is Role-Based Access Control?","a":"Assigning permissions based on user roles."},
{"q":"What is Data Encryption?","a":"Converting data into coded form to prevent unauthorized access."},
{"q":"What is Transparent Data Encryption?","a":"Encrypting database files automatically without application changes."},
{"q":"What is a Query Optimizer?","a":"Component that determines the most efficient way to execute a query."},
{"q":"What is Query Execution Plan?","a":"Detailed plan showing how a database executes a query."},
{"q":"What is Database Latency?","a":"Delay between request and database response."},
{"q":"What is Scalability in Databases?","a":"Ability of a database to handle increasing data and users."},
{"q":"What is Vertical Scaling?","a":"Increasing power of a single server (CPU, RAM)."},
{"q":"What is Horizontal Scaling?","a":"Adding more servers to distribute load."},
{"q":"What is Eventual Consistency?","a":"Data will become consistent over time in distributed systems."},
{"q":"What is Strong Consistency?","a":"All users see the same data immediately after a write."}
],
  "aptitude": [
{"q":"A train 150m long crosses a pole in 9s. Speed?","a":"150/9 = 16.67 m/s (≈60 km/h)."},
{"q":"5 workers take 12 days. 10 workers?","a":"Inverse proportion: double workers = half time → 6 days."},
{"q":"Probability of sum of 7 on 2 dice?","a":"6 combinations out of 36 → 1/6."},
{"q":"Item sold for $120 (20% profit). Cost?","a":"SP = 1.2 × Cost → Cost = $100."},
{"q":"A (10d) and B (15d) work together?","a":"Rates: 1/10 + 1/15 = 1/6 → 6 days."},
{"q":"How to calculate 15% of 200 mentally?","a":"10% = 20, 5% = 10 → 30."},

{"q":"If a train travels 360 km in 6 hours, speed?","a":"Speed = 360/6 = 60 km/h."},
{"q":"Average of 10, 20, 30?","a":"(10+20+30)/3 = 20."},
{"q":"Simple interest on $1000 at 5% for 2 years?","a":"SI = PRT/100 → 1000×5×2/100 = $100."},
{"q":"Compound interest formula?","a":"CI = P(1+r/n)^(nt)."},
{"q":"Ratio 2:3, total 50. Find numbers.","a":"Parts=5 → 1 part=10 → numbers=20 and 30."},
{"q":"If 20% of a number is 40, number?","a":"Number = 40 / 0.2 = 200."},

{"q":"Distance = Speed × Time example?","a":"If speed=50 km/h for 4h → distance=200 km."},
{"q":"Probability of head in coin toss?","a":"1 favorable / 2 outcomes → 1/2."},
{"q":"Square of 25?","a":"25 × 25 = 625."},
{"q":"Cube of 4?","a":"4 × 4 × 4 = 64."},
{"q":"LCM of 6 and 8?","a":"24."},
{"q":"HCF of 12 and 18?","a":"6."},

{"q":"If CP=$80 and SP=$100, profit%?","a":"Profit=20 → 20/80 ×100 = 25%."},
{"q":"If SP=$80 and CP=$100, loss%?","a":"Loss=20 → 20/100 ×100 = 20%."},
{"q":"Average speed formula?","a":"Total distance / Total time."},
{"q":"Time = Distance / Speed example?","a":"200 km at 50 km/h → 4 hours."},
{"q":"Area of rectangle?","a":"Length × Breadth."},
{"q":"Area of circle?","a":"πr²."},

{"q":"Perimeter of square?","a":"4 × side."},
{"q":"Sum of first n natural numbers?","a":"n(n+1)/2."},
{"q":"Sum of first n even numbers?","a":"n(n+1)."},
{"q":"Sum of first n odd numbers?","a":"n²."},
{"q":"Probability formula?","a":"Favorable outcomes / Total outcomes."},
{"q":"If 3 pens cost $15, price per pen?","a":"15/3 = $5."},

{"q":"Speed conversion m/s to km/h?","a":"Multiply by 3.6."},
{"q":"Speed conversion km/h to m/s?","a":"Multiply by 5/18."},
{"q":"Discount formula?","a":"Discount% = (Discount / Marked Price) ×100."},
{"q":"Percentage formula?","a":"(Part / Whole) ×100."},
{"q":"Average of 5 numbers with sum 100?","a":"100/5 = 20."},
{"q":"If 8 men finish work in 10 days, 4 men?","a":"Half workers → double time = 20 days."},

{"q":"If 1/4 of a number is 25, number?","a":"25 × 4 = 100."},
{"q":"Simple interest formula?","a":"SI = (P × R × T)/100."},
{"q":"Speed if 120 km in 2 hours?","a":"60 km/h."},
{"q":"Time if 300 km at 75 km/h?","a":"300/75 = 4 hours."},
{"q":"Area of triangle?","a":"(1/2) × base × height."},
{"q":"Volume of cube?","a":"side³."},

{"q":"Volume of cylinder?","a":"πr²h."},
{"q":"If probability of event = 0?","a":"Impossible event."},
{"q":"If probability = 1?","a":"Certain event."},
{"q":"Median of ordered data?","a":"Middle value."},
{"q":"Mode of data?","a":"Most frequent value."},
{"q":"Standard deviation meaning?","a":"Measure of spread of data."},

{"q":"If 40% of salary is $400, salary?","a":"400 / 0.4 = $1000."},
{"q":"If 25% of a number is 50?","a":"Number = 200."},
{"q":"Square root of 144?","a":"12."},
{"q":"Cube root of 27?","a":"3."},
{"q":"If train covers 600 km in 10h?","a":"Speed = 60 km/h."},
{"q":"If average of 4 numbers is 25?","a":"Total sum = 100."}
]
}

# Inspirational quotes that rotate every minute during study sessions.
MOTIVATIONAL_QUOTES = [
"The only way to do great work is to love what you do. — Steve Jobs 🚀",
"Don't stop when you're tired. Stop when you're done. 💪",
"Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill 🔥",
"Believe you can and you're halfway there. — Theodore Roosevelt ⭐",
"It always seems impossible until it's done. — Nelson Mandela 🌍",
"Your focus determines your reality. — Qui-Gon Jinn 🎯",
"The expert in anything was once a beginner. — Helen Hayes 🌱",
"Focus on being productive instead of busy. — Tim Ferriss ⚡",
"Small steps in the right direction can turn out to be the biggest steps of your life. 👣",
"The secret of getting ahead is getting started. — Mark Twain 🚀",
"You don't have to be great to start, but you have to start to be great. — Zig Ziglar 🌟",
"Study while others are sleeping; work while others are loafing; prepare while others are playing; and dream while others are reaching. — William Arthur Ward 📚",

"Dream big. Start small. Act now. 🌟",
"Discipline is choosing between what you want now and what you want most. 🎯",
"Success usually comes to those who are too busy to be looking for it. — Henry David Thoreau 💼",
"Hard work beats talent when talent doesn’t work hard. 💪",
"Push yourself, because no one else is going to do it for you. 🚀",
"Great things never come from comfort zones. 🌄",
"Don’t watch the clock; do what it does. Keep going. — Sam Levenson ⏰",
"The future depends on what you do today. — Mahatma Gandhi 🌱",
"Stay hungry. Stay foolish. — Steve Jobs 🍏",
"Action is the foundational key to all success. — Pablo Picasso 🗝️",
"Believe in yourself and all that you are. 💫",
"Your limitation—it's only your imagination. 🧠",
"Wake up with determination. Go to bed with satisfaction. 🌅",
"Dream it. Wish it. Do it. 🚀",
"Success doesn’t just find you. You have to go out and get it. 🏃",
"Don’t limit your challenges. Challenge your limits. ⚡",
"Do something today that your future self will thank you for. 🙌",
"Sometimes we’re tested not to show our weaknesses, but to discover our strengths. 🛡️",
"Little things make big days. 🌈",
"It’s going to be hard, but hard does not mean impossible. 💯",
"Don’t wait for opportunity. Create it. 🛠️",
"The harder you work for something, the greater you’ll feel when you achieve it. 🏆",
"Dream bigger. Do bigger. 🌍",
"Success is the sum of small efforts repeated day in and day out. 📈",
"If you get tired, learn to rest, not quit. 🧘",
"Stay focused and never give up. 🎯",
"Turn your dreams into plans. 📋",
"The best view comes after the hardest climb. 🧗",
"Consistency is what transforms average into excellence. 🔁",
"You are capable of amazing things. ✨"
]
# --- Data Management ---

class StatsManager:
    """
    Manages the persistence and updates of user statistics.
    
    Attributes:
        stats_file: Path to the JSON file for data storage.
        stats: Dictionary containing points, time, streak, and tasks.
    """
    
    def __init__(self, stats_file="study_stats.json"):
        """Initializes the manager and loads existing stats."""
        self.stats_file = stats_file
        self.stats = {
            "lifetime_seconds": 0,
            "knowledge_points": 0,
            "study_streak": 0,
            "last_study_date": None,
            "subject_breakdown": {},
            "pending_tasks": [],
            "summary_history": []
        }
        self.load_stats()
        self._migrate_tasks()

    def _migrate_tasks(self):
        """Migrates old string-based tasks to the new structured format."""
        updated = False
        new_tasks = []
        for task in self.stats.get("pending_tasks", []):
            if isinstance(task, str):
                new_tasks.append({
                    "id": len(new_tasks) + 1,
                    "text": task,
                    "priority": "Medium",
                    "due_date": None,
                    "status": "pending",
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                })
                updated = True
            else:
                new_tasks.append(task)
        
        if updated:
            self.stats["pending_tasks"] = new_tasks
            self.save_stats()

    def load_stats(self):
        """Loads data from the JSON file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats.update(json.load(f))
            except: pass

    def save_stats(self):
        """Saves current statistics to the JSON file using an atomic swap."""
        try:
            temp_file = self.stats_file + ".tmp"
            with open(temp_file, 'w') as f:
                json.dump(self.stats, f, indent=4)
            os.replace(temp_file, self.stats_file)
        except: pass

    def update_streak(self):
        """Calculates and updates the daily study streak."""
        today = datetime.now().strftime("%Y-%m-%d")
        last = self.stats["last_study_date"]
        if last == today: return
        if last:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            self.stats["study_streak"] = self.stats["study_streak"] + 1 if last == yesterday else 1
        else:
            self.stats["study_streak"] = 1
        self.stats["last_study_date"] = today
        self.save_stats()

    def get_rank(self):
        """Returns the user's rank based on Knowledge Points (KP)."""
        kp = self.stats["knowledge_points"]
        if kp < 100: return "Novice Scholar"
        if kp < 500: return "Dedicated Student"
        if kp < 1500: return "Honor Student"
        return "Master Scholar"

class ChatLogger:
    """
    Maintains a record of interactions between the AI and user.
    """
    
    def __init__(self, log_file="chat_history.json"):
        """Initializes the logger path."""
        self.log_file = log_file

    def log(self, role, message):
        """Appends a new entry to the chat log file."""
        log_entry = {"timestamp": str(datetime.now()), "role": role, "message": message}
        try:
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f: logs = json.load(f)
            logs.append(log_entry)
            with open(self.log_file, 'w') as f: json.dump(logs, f, indent=4)
        except: pass
