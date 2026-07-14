from data_utils import normalize_question


SUBJECT_ANSWERS = {
    "OS": [
        (
            ["fcfs", "first come first serve"],
            "FCFS (First Come First Serve) is a CPU scheduling algorithm. "
            "The process that arrives first gets the CPU first. It is simple, "
            "but long processes can make shorter processes wait for a long time."
        ),
        (
            ["round robin"],
            "Round Robin is a CPU scheduling algorithm used in time-sharing systems. "
            "Each process gets a fixed time quantum. After its time expires, "
            "the process moves to the end of the ready queue."
        ),
        (
            ["deadlock"],
            "Deadlock occurs when processes wait forever for resources held by each other. "
            "Its four conditions are mutual exclusion, hold and wait, no preemption, "
            "and circular wait."
        ),
        (
            ["paging"],
            "Paging is a memory-management technique in which memory is divided into "
            "fixed-size pages and frames. It lets a process be stored in non-contiguous memory."
        ),
        (
            ["virtual memory"],
            "Virtual memory uses disk space as an extension of RAM. It allows larger "
            "programs to run, but excessive swapping can reduce system performance."
        ),
        (
            ["semaphore"],
            "A semaphore is a synchronization tool used to control access to shared resources. "
            "It helps prevent race conditions between processes or threads."
        ),
        (
            ["mutex"],
            "A mutex is a mutual-exclusion lock. Only one thread can hold it at a time, "
            "so it protects shared data from simultaneous modification."
        ),
        (
            ["context switching"],
            "Context switching happens when the CPU saves one process state and loads another. "
            "It enables multitasking but creates some overhead."
        ),
        (
            ["priority scheduling"],
            "Priority scheduling runs the process with the highest priority first. "
            "A disadvantage is starvation, where low-priority processes may wait too long."
        ),
        (
            ["sjf", "shortest job first"],
            "SJF (Shortest Job First) selects the process with the smallest CPU burst time. "
            "It reduces average waiting time, but burst time is difficult to predict."
        ),
        (
            ["thread"],
            "A thread is the smallest unit of execution inside a process. "
            "Threads of the same process share memory and resources."
        ),
        (
            ["process"],
            "A process is a program currently being executed. It has its own memory, "
            "state, resources, and Process Control Block."
        ),
    ],

    "Python": [
        (
            ["python list", "list in python", "list"],
            "A Python list is an ordered and mutable collection. It can store values "
            "of different data types. Example: numbers = [10, 20, 30]. "
            "You can add an item using numbers.append(40)."
        ),
        (
            ["dictionary", "dict"],
            "A Python dictionary stores data as key-value pairs. Keys must be unique. "
            "Example: student = {'name': 'Harish', 'marks': 90}. "
            "Use student['name'] to get a value."
        ),
        (
            ["tuple"],
            "A tuple is an ordered Python collection, but it is immutable. "
            "Example: point = (10, 20). After creation, its values cannot be changed."
        ),
        (
            ["set"],
            "A Python set is an unordered collection of unique values. "
            "Example: {1, 2, 2, 3} becomes {1, 2, 3}. Sets are useful for removing duplicates."
        ),
        (
            ["function"],
            "A Python function is a reusable block of code defined using the def keyword. "
            "Example: def add(a, b): return a + b."
        ),
        (
            ["for loop"],
            "A for loop repeats code for each item in a sequence. "
            "Example: for number in [1, 2, 3]: print(number)."
        ),
        (
            ["while loop"],
            "A while loop runs repeatedly while a condition remains true. "
            "Example: while count < 5: count += 1. Make sure its condition eventually becomes false."
        ),
        (
            ["if else", "if statement"],
            "The if-else statement is used for decision-making in Python. "
            "Example: if marks >= 40: print('Pass') else: print('Fail')."
        ),
        (
            ["lambda"],
            "A lambda function is a short anonymous function in Python. "
            "Example: square = lambda x: x * x. It is useful for simple one-line operations."
        ),
        (
            ["try except", "exception"],
            "Exception handling prevents a Python program from stopping unexpectedly. "
            "Use try for risky code and except to handle possible errors."
        ),
        (
            ["inheritance"],
            "Inheritance in Python allows a child class to reuse properties and methods "
            "of a parent class. It supports code reuse in object-oriented programming."
        ),
        (
            ["class", "object"],
            "A class is a blueprint for creating objects in Python. "
            "An object is an instance of a class containing data and behavior."
        ),
    ],

    "CN": [
        (
            ["tcp ip", "tcp/ip"],
            "The TCP/IP model explains internet communication using four layers: "
            "Application, Transport, Internet, and Network Access. TCP provides reliable delivery, "
            "while IP handles addressing and routing."
        ),
        (
            ["tcp"],
            "TCP (Transmission Control Protocol) is a reliable transport-layer protocol. "
            "It establishes a connection, preserves packet order, checks delivery, "
            "and retransmits lost packets."
        ),
        (
            ["udp"],
            "UDP (User Datagram Protocol) is a fast connectionless transport protocol. "
            "It does not guarantee delivery or packet order, so it is useful for gaming, "
            "live streaming, and voice calls."
        ),
        (
            ["dns"],
            "DNS (Domain Name System) converts domain names such as google.com "
            "into IP addresses that computers use to communicate."
        ),
        (
            ["https"],
            "HTTPS is the secure version of HTTP. It uses TLS encryption to protect data "
            "between a browser and a web server."
        ),
        (
            ["http"],
            "HTTP (HyperText Transfer Protocol) is used for communication between a web browser "
            "and a web server. It is the foundation of data exchange on the web."
        ),
        (
            ["ip address"],
            "An IP address is a unique numerical address assigned to a device on a network. "
            "It identifies the source and destination of network data."
        ),
        (
            ["mac address"],
            "A MAC address is a hardware address assigned to a network interface card. "
            "It is mainly used for communication inside a local network."
        ),
        (
            ["router"],
            "A router connects different networks and forwards packets using IP addresses. "
            "For example, a home router connects local devices to the internet."
        ),
        (
            ["switch"],
            "A switch connects devices in a local area network and forwards data "
            "to the correct device using MAC addresses."
        ),
        (
            ["firewall"],
            "A firewall is a security system that monitors and filters incoming and outgoing "
            "network traffic according to security rules."
        ),
        (
            ["osi"],
            "The OSI model has seven layers: Physical, Data Link, Network, Transport, "
            "Session, Presentation, and Application. It helps explain network communication."
        ),
        (
            ["subnet mask"],
            "A subnet mask separates the network part and host part of an IP address. "
            "It helps divide a large network into smaller subnetworks."
        ),
        (
            ["port"],
            "A port number identifies a specific application or service on a device. "
            "For example, HTTP commonly uses port 80 and HTTPS uses port 443."
        ),
    ],

    "Java": [
        (
            ["method overloading"],
            "Method overloading means defining multiple methods with the same name "
            "but different parameters. It is compile-time polymorphism in Java."
        ),
        (
            ["method overriding"],
            "Method overriding occurs when a child class provides its own version "
            "of a method already defined in the parent class. It is runtime polymorphism."
        ),
        (
            ["inheritance"],
            "Inheritance in Java allows a child class to acquire fields and methods "
            "from a parent class using the extends keyword. It supports code reuse."
        ),
        (
            ["polymorphism"],
            "Polymorphism means one interface or method can have multiple forms. "
            "Java supports compile-time polymorphism through overloading and runtime polymorphism through overriding."
        ),
        (
            ["encapsulation"],
            "Encapsulation means combining data and methods inside a class while hiding internal data. "
            "It is commonly implemented with private variables and public getter/setter methods."
        ),
        (
            ["abstraction"],
            "Abstraction hides implementation details and exposes only essential features. "
            "In Java, it can be achieved using abstract classes and interfaces."
        ),
        (
            ["interface"],
            "An interface defines a contract of methods that implementing classes must provide. "
            "It supports abstraction and allows Java classes to implement multiple interfaces."
        ),
        (
            ["abstract class"],
            "An abstract class cannot be instantiated directly. It can contain both abstract methods "
            "without implementation and normal methods with implementation."
        ),
        (
            ["constructor"],
            "A constructor is a special method used to initialize an object. "
            "It has the same name as its class and runs automatically when an object is created."
        ),
        (
            ["exception"],
            "Exception handling in Java manages runtime errors without crashing the program. "
            "Java uses try, catch, finally, throw, and throws keywords."
        ),
        (
            ["jvm"],
            "JVM means Java Virtual Machine. It runs Java bytecode and enables Java's "
            "Write Once, Run Anywhere feature."
        ),
        (
            ["jdk"],
            "JDK means Java Development Kit. It contains tools needed to develop Java programs, "
            "including the compiler, JVM, and standard libraries."
        ),
        (
            ["jre"],
            "JRE means Java Runtime Environment. It provides the JVM and libraries needed "
            "to run Java applications, but it does not include development tools such as the compiler."
        ),
        (
            ["package"],
            "A package in Java organizes related classes and interfaces. "
            "It helps avoid naming conflicts and improves project structure."
        ),
        (
            ["class", "object"],
            "A class is a blueprint for creating Java objects. An object is an instance "
            "of a class that contains state through fields and behavior through methods."
        ),
    ]
}


FALLBACK_ANSWERS = {
    "OS": (
        "This is an Operating Systems topic. Operating Systems manages processes, "
        "CPU scheduling, memory, files, devices, and system resources."
    ),
    "Python": (
        "This is a Python topic. Python is a high-level programming language used "
        "for automation, web development, data science, and machine learning."
    ),
    "CN": (
        "This is a Computer Networks topic. Networks allow devices to communicate "
        "using protocols, IP addressing, routing, and network services."
    ),
    "Java": (
        "This is a Java topic. Java is an object-oriented programming language used "
        "for backend systems, Android development, and enterprise applications."
    )
}


def generate_answer(question: str, subject: str, confidence: float) -> str:
    clean_question = normalize_question(question)

    subject_topics = SUBJECT_ANSWERS.get(subject, [])

    for keywords, answer in subject_topics:
        if any(keyword in clean_question for keyword in keywords):
            return answer

    if confidence < 0.45:
        return (
            "I am not fully confident about this question. Add more similar examples "
            "to dataset.csv and train the models again for a better prediction."
        )

    return FALLBACK_ANSWERS.get(
        subject,
        "I identified the subject, but a detailed answer for this exact topic is not available yet."
    )