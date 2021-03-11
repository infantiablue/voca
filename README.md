# Vocabulary Keeper

## Development Status

[![CircleCI](https://circleci.com/gh/infantiablue/voca.svg?style=svg)](https://circleci.com/gh/infantiablue/voca) [![Build Status](https://travis-ci.com/infantiablue/voca.svg?branch=main)](https://travis-ci.com/infantiablue/voca) [![codecov.io](https://codecov.io/github/infantiablue/voca/coverage.svg?branch=main)](https://codecov.io/github/infantiablue/voca?branch=main) 

## Video Demo

## Description

As a non-English speaker, I need to learn new vocabulary consecutively. Before CS50, I usually use Apple Notes to save and review new words. However, it's not really an intuitive way to build vocabulary base.
Then, I tried to find some mobile apps for this purpose, yet almost the app I found is focus on flash card base, which means provide users new and random words to memorize. It's not really what I want for my personal pupose.
And with the knowledge (and excitment) from the CS50 class, I decied to build a web app for myself to keep new words I found from daily reading or watching activities.

There are some fundatamental features for user:

- Use API from Oxford dictonary for explanation.
- There is a nice dashboard with random word, quote and Today I learned which is a sub reddit I really prefer.
- The user can browse all the words to review.
- The user can add personal notes for saved words to have better explanation.
- The user can change password.

Some details about technical statck:

- SQLAlchemy with Flask-Migrate.
- Postgres for production and SQLite for testing purpose.
- Deployed on Google Compute Engine, with gUnicorn as WSGI, and nginx as reserved proxy server
- There is a test suite which reach 91% code coverage.
- Tailwind CSS framework for user interface.

[Live site](https://voca.techika.com)