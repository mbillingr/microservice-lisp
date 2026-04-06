Lambda Calculus in Microservices
================================

The probably dumbest way to implement a Lisp. 
You know eval <-> apply from SICP? Here, they are not functions but microservices.
In fact, everything is a microservice: eval, apply, the parser, and the global environment.

The performance is outstanding: compute (fib 5) in close to 2 seconds! (locally on an i7 Laptop, no scaling)

Get Started
-----------

```bash
docker compose build

docker compose up -d

curl -X POST localhost:8000 -d "(define fib (lambda (n) (if (< n 2) 1 (+ (fib (- n 1)) (fib (- n 2))))))"

curl -X POST localhost:8000 -d "(fib 5)"
```

Ok, Why?
--------

Apart from "because I can", it's obviously pointless to implement an interpreter like this. However,
note that we're also deploying Grafana and Tempo. The point of this exercise was not to create a 
good interpreter, but to play with the LGTM stack and see how well it works with out-of-the-box tracing.

Have a look at http://localhost:3000 and marvel at the traces of recursive API calls. In fact, this was
a great help, even while writing the code.
