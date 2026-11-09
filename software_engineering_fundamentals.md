## SOLID Principles

+ S: Single Responsibility Principle
+ O: Open/Closed Principle
+ L: Liskov Substitution Principle
+ I: Interface Segregation Principle
+ D: Dependency Inversion Principle

## DRY Principle

+ DRY: Don't Repeat Yourself

## Stack vs Heap

+ Stack
	- Function calls, local references

+ Heap
	- Actual objects

+ Python variables are references on the stack pointing to heap objects

## Python Memory Management

+ Reference counting (primary)
+ Garbage collector (cycles)
+ Generational GC (performance optimization)
+ Internal allocator (pymalloc): for small objects `< 512 bytes`

## Git Merging vs Rebasing

+ Merge
	- "Combine histories"

+ Rebase
	- "Rewrite history to look like it happened in a straight line"

## Virtual Machine vs Docker

+ A VM virtualizes hardware and runs a full OS, while Docker virtualizes the OS and runs isolated processes on the same kernel
