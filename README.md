# Django-for-beginners-book

## GIT / GIHUB

```git
>>> git init
>>> git add .
>>> git commit -m 'intial commit
>>> git remote add origin https://github.com/wsvincent/hello-world.git
>>> git branch -M main
>>> git push -u origin main

```

## Django Tests

Testing can be divided into two main categories: unit and integration. Unit tests check a piece of functionality in isolation, while Integration tests check multiple pieces linked together. Unit tests run faster and are easier to maintain since they focus on only a small piece of code. Integration tests are slower and harder to maintain since a failure doesn’t point you in the specific direction
of the cause. Most developers focus on writing many unit tests and a small amount of integration tests.
Generally speaking, SimpleTestCase is used when a database is not necessary while TestCase
is used when you do want to test the database. TransactionTestCase is useful if you need to
directly test database transactions while LiveServerTestCase launches a live server thread useful for testing with browser-based tools like Selenium.

## How to learn tests

> > > python manage.py test
